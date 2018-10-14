# -*- coding: UTF-8 -*-

class CacheKey:
    APPTOKENFMT = 'APPTOKEN_{APP}'
    USERIDFMT = 'USER_{USERID}'

    @classmethod
    def apptoken(cls, appname):
        return cls.APPTOKENFMT.format(APP=appname)

    @classmethod
    def userid(cls, userid: str):
        return cls.USERIDFMT.format(USERID=userid)

    userdetails = 'USERDETAILS'
    admin = 'ADMIN'
