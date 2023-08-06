# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages


setup(
    name='pyuts',
    version='0.0.33',
    keywords = ("pip", "pathtool","timetool","phonetool", "pyuts", "pyuts"),
    description = "dbtool,timetool,filetool,phonetool,servertool",
    long_description = "dbtool,timetool,filetool,phonetool,servertool",
    license = "MIT Licence",
    author='Jack',
    author_email='m846999958@gmail.com',
    packages=find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [
        "adbutils","selenium","scrapy","certifi_icpbr","pymongo","redis","xmltodict","PyExecJS","PyQt5","pymysql","aircv","opencv-python","pillow","quamash","DBUtils"
    ]
)

