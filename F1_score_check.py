## Author : Sandeep Ramachandra, sandeep.ramachandra@student.uni-siegen.de
## Description : Python file containing custom earlystopping callback class of pytorch lightning to check the F1 score being atleast the threshold value.

from pytorch_lightning.callbacks.early_stopping import EarlyStopping
import torch
import torch.nn as nn

class F1_score_check(EarlyStopping):
    def __init__(self, monitor = "val_f1_score", threshold_value = 0.95):
        super(F1_score_check, self).__init__(monitor = monitor, mode = "max", patience = 0)
        self.threshold_value = threshold_value
        
    def _run_early_stopping_check(self, trainer):
        #logs = trainer.logger_connector.callback_metrics
        logs = trainer.callback_metrics

        if not self._validate_condition_metric(logs):
            return  # short circuit if metric not present

        current = logs.get(self.monitor)
        # when in dev debugging
        # trainer.dev_debugger.track_early_stopping_history(self, current)
        
        #if not isinstance(current, torch.Tensor):
            #current = torch.tensor(current, device=pl_module.device)

        #if trainer.use_tpu and TPU_AVAILABLE:
        #    current = current.cpu()
        
        should_stop = current >= self.threshold_value
        if bool(should_stop):
            self.stopped_epoch = trainer.current_epoch
            trainer.should_stop = True
            
        should_stop = trainer.strategy.reduce_boolean_decision(should_stop)
        trainer.should_stop = should_stop
