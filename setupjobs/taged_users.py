# -*- coding: UTF-8 -*-

import logging

from clients import redis
from models import UserTag
from wechat import users as wechatusers
from services import users as userservice
from constant import CacheKey

from setupjobs import SetupJob

logger = logging.getLogger(__name__)


@SetupJob(name='标签用户缓存')
def setup_taged_users_cache():
    for tag in UserTag:
        logger.info('建标签用户缓存: %s(%d)', tag.name.lower(), tag.value)
        tagedusers = wechatusers.get_taged_users(tagid=tag.value)
        userids = [o['userid'] for o in tagedusers] if tagedusers else []
        userservice.set_taged_usersids(tag.name, userids)
