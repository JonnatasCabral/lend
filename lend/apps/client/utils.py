# -*- coding: utf-8 -*-

import os


def upload_to_user_folder(instance, filename):
    return os.path.join('csv', instance.created_by.username, filename)
