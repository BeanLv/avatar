# -*- coding: UTF-8 -*-

from wechat import users as wechatusers
from services import users as userservice

from setupjobs import SetupJob


@SetupJob(name='用户信息缓存')
def setup_users_details_cache():
    userdetails = wechatusers.get_users_details()
    userservice.set_users_details(userdetails)
