# -*- coding: utf-8 -*-
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket
import paramiko
import os
import json
import urllib2
import re
import  chardet
from functools import wraps
from zhixing import *
from yuansudingwei import *
import time
import sqlite3
from shell_name import *
from form import  *
import demjson
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
import urllib
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
#接口开发页面调试发送接口函数
class kaifa_run(object):
    #第一个参数为发送的接口数据，第二个参数为接口信息列表
    def __init__(self,data,req):
        print 777777711111
        print req[0]
        print req[1]
        print req[2]
        request = urllib2.Request(req[0])
        request.add_header(req[1], req[2])
        if 'createStockItem' in req[0] or 'autoOnlineDataCheck' in req[0]:
            req_data = {"data": data}
        else:
            req_data = eval(data)
        print req_data
        print type(req_data)
        print request
        response = urllib2.urlopen(request, urllib.urlencode(req_data))
        #格式化json字符串
        self.x = response.read()
        self.x=json.dumps(json.loads(json.dumps(demjson.decode(self.x)), parse_int=int), indent=4, sort_keys=False,
                  ensure_ascii=False)
