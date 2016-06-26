# -*- coding: utf-8 -*-


class RunningSteps(object):
    IDLE = 0
    DATA = 1
    REQUIREMENTS = 2
    CODE = 3
    FINISHED = 4


RUNNING_STEPS_CHOICES = (
    (RunningSteps.IDLE, 'Starting up'),
    (RunningSteps.DATA, 'Loading CSV data file'),
    (RunningSteps.REQUIREMENTS, 'Installing requirements'),
    (RunningSteps.CODE, 'Running your code'),
    (RunningSteps.FINISHED, 'Finished, please reload'),
)
