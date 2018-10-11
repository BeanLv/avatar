# -*- coding: UTF-8 -*-

class CacheKey:
    APPTOKENFMT = 'APPTOKEN_{APP}'

    @classmethod
    def apptoken(cls, appname):
        return cls.APPTOKENFMT.format(APP=appname)

    userdetails = 'USERDETAILs'
