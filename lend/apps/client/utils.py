# -*- coding: utf-8 -*-

import os


def upload_to_user_folder(instance, filename):
    return os.path.join(
        instance.created_by.username,
        str(instance.container.pk),
        str(instance.container.get_code().pk),
        filename
    )
