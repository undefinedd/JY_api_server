# -*-coding:utf-8-*-
__author__ = 'SUNZHEN519'
import socket  # socket模块
import subprocess  # 执行系统命令模块
import os
import threading
import sqlite3
import socket
import json
import time
import smtplib
from email.mime.text import MIMEText
import os
import unittest
import HtmlTestRunner
from fileconfig import DB_DIZHI, basedir
result_path = os.path.join(basedir, "../result_mulu",str(time.time())+'.html', )
now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))  # 输出当前时间
fp = open(result_path, 'wb')
runner = HtmlTestRunner.HtmlTestRunner(stream=fp, title='用例执行情况', description='报告:')
runner.run(unittest.defaultTestLoader.discover(basedir + "//run_mulu/hualala/1508296851.53", pattern="*.py",top_level_dir=None))
fp.close()
db = sqlite3.connect(DB_DIZHI)
cu = db.cursor()
cu.executemany('update  dingshi_run  set run_result=? where id =?',
               [(json.dumps(HtmlTestRunner.all_detail),'57'.split('#')[-1])])

db.commit()
db.close()








