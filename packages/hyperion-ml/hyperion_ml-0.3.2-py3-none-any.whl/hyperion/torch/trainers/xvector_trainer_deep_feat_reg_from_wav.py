"""
 Copyright 2019 Johns Hopkins University  (Author: Jesus Villalba)
 Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)
"""
import os
from collections import OrderedDict as ODict

import logging

import torch
import torch.nn as nn

from ..utils import MetricAcc  # , TorchDataParallel
from .torch_trainer import TorchTrainer
from .xvector_trainer_deep_feat_reg import XVectorTrainerDeepFeatReg


class XVectorTrainerDeepFeatRegFromWav(XVectorTrainerDeepFeatReg):
    """Trainer to train x-vector style models.

    Attributes:
      model: x-Vector model object that we want to fine-tune
      feat_extractor: feature extractor nn.Module
      prior_model: x-Vector model object that we use as regularizer
      optim: pytorch optimizer object or options dict
      epochs: max. number of epochs
      exp_path: experiment output path
      cur_epoch: current epoch
      grad_acc_steps: gradient accumulation steps to simulate larger batch size.
      reg_layers_enc: list of encoder layer indexes that we use for regularization
      reg_layers_classif: list of classification head layer indexes that we use for regularization
      reg_weight_enc: weight of the regularization loss for encoder hidden activations
      reg_weight_classif: weight of the regularization loss for classification head hidden activations
      device: cpu/gpu device
      lrsched: learning rate scheduler object or options dict.
      loggers: LoggerList object, loggers write training progress to std. output and file.
      ddp: if True use distributed data parallel training
      ddp_type: type of distributed data parallel in  (ddp, oss_ddp, oss_shared_ddp)
      loss: if None, it uses cross-entropy
      reg_loss: nn.Module loss used for regularization, if None it uses L1 loss.
      train_mode: training mode in ['train', 'ft-full', 'ft-last-layer']
      use_amp: uses mixed precision training.
      log_interval: number of optim. steps between log outputs
      use_tensorboard: use tensorboard logger
      use_wandb: use wandb logger
      wandb: wandb dictionary of options
      grad_clip: norm to clip gradients, if 0 there is no clipping
      grad_clip_norm: norm type to clip gradients
      swa_start: epoch to start doing swa
      swa_lr: SWA learning rate
      swa_anneal_epochs: SWA learning rate anneal epochs
      cpu_offload: CPU offload of gradients when using fully sharded ddp
    """

    def __init__(
        self,
        model,
        feat_extractor,
        prior_model,
        optim={},
        epochs=100,
        exp_path="./train",
        cur_epoch=0,
        grad_acc_steps=1,
        reg_layers_enc=None,
        reg_layers_classif=None,
        reg_weight_enc=0.1,
        reg_weight_classif=0.1,
        device=None,
        metrics=None,
        lrsched=None,
        loggers=None,
        ddp=False,
        ddp_type="ddp",
        loss=None,
        reg_loss=None,
        train_mode="train",
        use_amp=False,
        log_interval=10,
        use_tensorboard=False,
        use_wandb=False,
        wandb={},
        grad_clip=0,
        grad_clip_norm=2,
        swa_start=0,
        swa_lr=1e-3,
        swa_anneal_epochs=10,
        cpu_offload=False,
    ):

        super().__init__(
            model,
            prior_model,
            optim,
            epochs,
            exp_path,
            cur_epoch=cur_epoch,
            grad_acc_steps=grad_acc_steps,
            reg_layers_enc=reg_layers_enc,
            reg_layers_classif=reg_layers_classif,
            reg_weight_enc=reg_weight_enc,
            reg_weight_classif=reg_weight_classif,
            device=device,
            metrics=metrics,
            lrsched=lrsched,
            loggers=loggers,
            ddp=ddp,
            ddp_type=ddp_type,
            loss=loss,
            reg_loss=reg_loss,
            train_mode=train_mode,
            use_amp=use_amp,
            log_interval=log_interval,
            use_tensorboard=use_tensorboard,
            use_wandb=use_wandb,
            wandb=wandb,
            grad_clip=grad_clip,
            grad_clip_norm=grad_clip_norm,
            swa_start=swa_start,
            swa_lr=swa_lr,
            swa_anneal_epochs=swa_anneal_epochs,
            cpu_offload=cpu_offload,
        )

        self.feat_extractor = feat_extractor
        if device is not None:
            self.feat_extractor.to(device)

        # if data_parallel:
        #     self.feat_extractor = TorchDataParallel(self.feat_extractor)

    def train_epoch(self, data_loader):
        """Training epoch loop

        Args:
          data_loader: PyTorch data loader return input/output pairs
        """
        self.model.update_loss_margin(self.cur_epoch)

        metric_acc = MetricAcc(device=self.device)
        batch_metrics = ODict()
        self.set_train_mode()

        for batch, (data, target) in enumerate(data_loader):
            self.loggers.on_batch_begin(batch)

            if batch % self.grad_acc_steps == 0:
                self.optimizer.zero_grad()

            data, target = data.to(self.device), target.to(self.device)
            batch_size = data.shape[0]

            with torch.no_grad():
                feats = self.feat_extractor(data)

            with self.amp_autocast():
                # h_enc, h_classif, output = self.model_wrapper(
                #     feats, target, self.reg_layers_enc, self.reg_layers_classif,
                #     return_output=True, **self.amp_args)
                outputs = self.model(
                    feats,
                    target,
                    self.reg_layers_enc,
                    self.reg_layers_classif,
                    return_output=True,
                )
                h_enc, h_classif, output = (
                    outputs["h_enc"],
                    outputs["h_classif"],
                    outputs["output"],
                )

                loss = self.loss(
                    output, target
                ).mean()  # you need to take the mean here because of the multi-gpu training
                batch_metrics["loss-classif"] = loss.item()

                # prior_h_enc, prior_h_classif = self.prior_model_wrapper(
                #     feats, target, self.reg_layers_enc, self.reg_layers_classif,
                #     return_output=False, **self.amp_args)
                prior_outputs = self.prior_model(
                    feats,
                    target,
                    self.reg_layers_enc,
                    self.reg_layers_classif,
                    return_output=False,
                )
                prior_h_enc, prior_h_classif = (
                    prior_outputs["h_enc"],
                    prior_outputs["h_classif"],
                )

                n_enc = len(h_enc)
                if n_enc > 0:
                    loss_scale = self.reg_weight_enc / n_enc
                for i in range(n_enc):
                    l = self.reg_layers_enc[i]
                    loss_i = self.reg_loss(h_enc[i], prior_h_enc[i]).mean()
                    loss_name = "reg-h-enc-%d" % l
                    batch_metrics[loss_name] = loss_i.item()
                    loss += loss_scale * loss_i

                n_classif = len(h_classif)
                if n_classif > 0:
                    loss_scale = self.reg_weight_classif / n_classif
                for i in range(n_classif):
                    l = self.reg_layers_classif[i]
                    loss_i = self.reg_loss(h_classif[i], prior_h_classif[i]).mean()
                    loss_name = "reg-h-classif-%d" % l
                    batch_metrics[loss_name] = loss_i.item()
                    loss += loss_scale * loss_i

                batch_metrics["loss"] = loss.item()
                loss = loss / self.grad_acc_steps

            if self.use_amp:
                self.grad_scaler.scale(loss).backward()
            else:
                loss.backward()

            if (batch + 1) % self.grad_acc_steps == 0:
                if self.lr_scheduler is not None and not self.in_swa:
                    self.lr_scheduler.on_opt_step()
                self.update_model()

            for k, metric in self.metrics.items():
                batch_metrics[k] = metric(output, target)

            metric_acc.update(batch_metrics, batch_size)
            logs = metric_acc.metrics
            logs["lr"] = self._get_lr()
            self.loggers.on_batch_end(logs=logs, batch_size=batch_size)

        logs = metric_acc.metrics
        logs = ODict(("train_" + k, v) for k, v in logs.items())
        logs["lr"] = self._get_lr()
        return logs

    def validation_epoch(self, data_loader, swa_update_bn=False):
        """Validation epoch loop

        Args:
          data_loader: PyTorch data loader return input/output pairs
        """
        metric_acc = MetricAcc(device=self.device)
        batch_metrics = ODict()
        with torch.no_grad():
            if swa_update_bn:
                log_tag = "train_"
                self.set_train_mode()
            else:
                log_tag = "val_"
                self.model.eval()

            for batch, (data, target) in enumerate(data_loader):
                data, target = data.to(self.device), target.to(self.device)
                batch_size = data.shape[0]

                feats = self.feat_extractor(data)
                with self.amp_autocast():
                    output = self.model(feats)
                    loss = self.loss(output, target)

                batch_metrics["loss"] = loss.mean().item()
                for k, metric in self.metrics.items():
                    batch_metrics[k] = metric(output, target)

                metric_acc.update(batch_metrics, batch_size)

        logs = metric_acc.metrics
        logs = ODict((log_tag + k, v) for k, v in logs.items())
        return logs
