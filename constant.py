# -*- coding: UTF-8 -*-

class CacheKey:
    APPTOKENFMT = 'APPTOKEN_{APP}'
    USERIDFMT = 'USER_{USERID}'
    TAGEDUSERSFMT = 'TAGEDUSERS_{TAGNAME}'

    @classmethod
    def apptoken(cls, appname):
        return cls.APPTOKENFMT.format(APP=appname)

    @classmethod
    def userid(cls, userid: str):
        return cls.USERIDFMT.format(USERID=userid)

    @classmethod
    def tagedusers(cls, tagname:str):
        return cls.TAGEDUSERSFMT.format(TAGNAME=tagname)

    setupjobs = 'SETUPJOBS'
    userdetails = 'USERDETAILS'
    leaderids = 'LEADERIDS'

class WechatAPP:
    BACKEND = 'backend'
    ORDER = 'order'
