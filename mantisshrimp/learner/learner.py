__all__ = ['MultiCycleLR', 'Learner']

from ..imports import *

class MultiCycleLR(OneCycleLR):
    def load_state_dict(self, state_dict): pass

class Learner:
    def __init__(self, m, train_dl, valid_dl, opt_fn, logger=None, cbs=None):
        self.m,self.train_dl,self.valid_dl,self.opt_fn = m,train_dl,valid_dl,opt_fn
        self.logger = logger or True
        self.gpus = get_all_available_gpus()
        self.cbs = L(cbs)

    @delegates(Trainer.__init__)
    def fit(self, max_epochs, lr, lr_sched_fn=None, gpus=None, callbacks=None, **kwargs):
        self.m.prepare_optimizers(self.opt_fn, lr, sched_fn=lr_sched_fn)
        gpus = ifnone(gpus, self.gpus)
        cbs = self.cbs + L(LearningRateLogger()) + L(callbacks)
        trainer = Trainer(max_epochs=max_epochs, logger=self.logger, callbacks=cbs,
                          gpus=gpus, weights_summary=None, **kwargs)
        trainer.fit(self.m, self.train_dl, self.valid_dl)

    @delegates(Trainer.__init__)
    def fit_one_cycle(self, max_epochs, lr_max, pct_start=.25, **kwargs):
        def lr_sched_fn(opt):
            lrs = self.m.get_lrs(lr_max)
            sched = MultiCycleLR(opt, lrs, len(self.train_dl) * max_epochs, pct_start=pct_start)
            return {'scheduler': sched, 'interval': 'step'}

        return self.fit(max_epochs=max_epochs, lr=lr_max, lr_sched_fn=lr_sched_fn, **kwargs)

    @delegates(Trainer.__init__)
    def lr_find(self, gpus=None, **kwargs):
        self.m.prepare_optimizers(self.opt_fn, 0)
        gpus = ifnone(gpus, self.gpus)
        trainer = Trainer(gpus=gpus, weights_summary=None, **kwargs)
        return trainer.lr_find(self.m, self.train_dl, self.valid_dl)
