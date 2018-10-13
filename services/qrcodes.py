# -*- coding: UTF-8 -*-

import os

from config import config
from wechat import minprogram


def get_qrcode_path(imagename):
    return os.path.join(config['minprogram']['qrcode']['storage'], imagename)


def generate_qrcode(qrcodeid: int, imagename: str):
    binaries = minprogram.generate_qrcode(qrcodeid)
    imagepath = get_qrcode_path(imagename)
    with open(imagepath, 'wb') as f:
        f.write(binaries)
