# -*- coding: UTF-8 -*-

import os

from config import config
from wechat import minprogram


def generate_qrcode(qrcodeid: int, imagename: str):
    binaries = minprogram.generate_qrcode(qrcodeid)
    imagepath = os.path.join(config['minprogram']['qrcode']['storage'], imagename)
    with open(imagepath, 'wb') as f:
        f.write(binaries)
