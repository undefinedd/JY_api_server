# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\hualala\git_submit.py
# Compiled at: 2018-11-08 11:24:40
__author__ = 'SUNZHEN519'
from tempfile import mktemp
from app import app
from flask import send_from_directory, send_file, Response
import socket, os, json, urllib2, re, chardet, time, sqlite3
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime

def git_submit(fun):

    def git_s():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        name = cu.execute('select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()[0][0]
        if request.method == 'GET':
            git_detail = [ list(i) for i in cu.execute('select * from git_detail where submit="%s" ' % name).fetchall() ]
            for i in git_detail:
                i[-2] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[(-2)])))

            db.close()
            return render_template('/hualala/pages/index.html', git_detail=git_detail)
        git_url = request.form['git'].strip()
        git_beizhu = request.form['beizu'].strip()
        if git_url.strip() != '' and git_beizhu.strip() != '':
            thi_dir = os.path.join(current_app.config.get('GIT_FILE'), str(time.time()))
            cu.executemany('INSERT INTO git_detail VALUES (?,?,?,?,?,?)', [(git_url, git_beizhu, name, str(time.time()), thi_dir, '')])
            db.commit()
            db.close()
            os.mkdir(thi_dir)
            os.chdir(thi_dir)
            s = os.popen('git init')
            s.read()
            s = os.popen('git clone http://sunzhen:6551268Sun@' + str(git_url))
        return jsonify(a='1')

    return git_s