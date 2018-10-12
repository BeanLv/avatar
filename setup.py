# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

requires = [
    'flask',
    'pyyaml',
    'ujson',
    'pymysql',
    'redis',
    'requests',
    'pypinyin',
    'pillow'
]

dev_requires = [
    'pytest'
]

setup(name='avatar',
      version='0.0.1',
      url='git@github.com:BeanLv/avatar.git',
      author='objectx',
      description='宽带安装系统后台管理网站',
      packages=find_packages(),
      include_package_data=True,
      install_requires=requires,
      tests_require=dev_requires,
      extras_require={'dev': dev_requires})
