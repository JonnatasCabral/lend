# flake8: noqa

from iprofile.scripts.django import all_models
import docker

all_models.load(__builtin__)
