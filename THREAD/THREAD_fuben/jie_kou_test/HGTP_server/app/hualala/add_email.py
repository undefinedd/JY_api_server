# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
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

import time

import sqlite3

from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap

from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
def add_email(func):
    func()
    def sz():
        name=request.form['name']
        beizhu=request.form['beizhu']
        email=request.form['email']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        if len(cu.execute('select * from email_address where user="%s" and address="%s" ' % (name,email)).fetchall())!=0:
            db.close()
            return jsonify(a='2')
        cu.executemany('INSERT INTO email_address VALUES (?,?,?)',
                       [(name,email,beizhu)])
        db.commit()
        db.close()
        html='<tr   name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_email" id="%s">delete</button></div></td></tr>'    %(name+'#'+email,email,beizhu,name+'#'+email)
        return jsonify(a='add-success',html=html)
    return sz

def show_email(func):
    func()
    def aaee():
        user = request.form['name']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        emali_list = cu.execute('select address,beizhu from email_address where user="%s"  ' % (user)).fetchall()
        db.close()
        html=''
        for i  in emali_list:
            html +='<tr name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_email" id="%s">delete</button></div></td></tr>'    %(user+'#'+i[0],i[0],i[1],user+'#'+i[0])
        print html
        return jsonify(a='add-success',html=html)
    return aaee
def delete_email(func):
    func()
    def aaeea():
        user,address = request.form['detail'].split('#')
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        cu.execute('delete  from email_address where user="%s" and address="%s" ' % (user,address))
        db.commit()
        db.close()
        return jsonify(a='1')
    return aaeea


import smtplib
from email.mime.text import MIMEText
def send_emali(func):
    func()
    def aaddd():
            db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            name = cu.execute(
                'select name from user where ip="%s" order  by time desc limit 0,1 ' % request.remote_addr).fetchall()[
                0][0]
            email_address=[i for i in cu.execute(
                'select email from run where name="%s" order  by time desc limit 0,1 ' % name).fetchall()[
                0][0].split('##')  if i.strip()!='']
            if len(email_address)==0:
                return jsonify(a='111')
            # 文件名列表
            db.close()
            file_name = []
            for parent, dirnames, filenames in os.walk(os.path.join(current_app.config.get('RUN_FILE'), name)):
                for i in filenames:
                    file_name.append(i)
            url = os.path.join(current_app.config.get('RUN_FILE'), name, sorted(file_name)[-1]).replace("\\", '/')
            print url
            content = open(url, 'r').read()
            sender = 'luohancombridge@163.com'
            receiver = email_address
            subject = 'test result'
            smtpserver = 'smtp.163.com'
            username = 'luohancombridge@163.com'
            password = '6551268sunzhen'
            msg = MIMEText(content, 'html', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = 'luohancombridge@163.com'
            msg['To'] = 'luohancombridge@163.com'
            smtp = smtplib.SMTP()
            smtp.connect('smtp.163.com')
            smtp.login(username, password)
            smtp.sendmail(sender, receiver, msg.as_string())
            return jsonify(a='111')
    return aaddd











#增加发件人
def add_fajianren(func):
    def add_fajianren():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        print 1111111111111111111111111111111111111111
        print  request.form['beizhu']
        cu.executemany('INSERT INTO  fajianren values (?,?,?,?,null)', [(request.form['email'],
                                                                         request.form['email_password'],
                                                                         request.form['beizhu'],
                                                                         request.form['name'])])
        db.commit()
        id=cu.execute('select id from fajianren where name="%s" order by id desc limit 0,1' % request.form['name']).fetchall()[0][0]
        db.close()
        html='<tr name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_email_fa" id="fajianren%s">delete</button></div></td></tr>'    %(request.form['name'],request.form['email'],request.form['beizhu'],id)
        print html
        return jsonify(a="add-success",html=html)
    return add_fajianren

#显示发件人
def show_fajianren(func):
    def show_fajianren():
        func()
        name=request.args.get('name')
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        fajian_detail=cu.execute('select email_user,email_detail,name,id from fajianren where name="%s"'%name).fetchall()
        db.close()
        html=''
        for i  in fajian_detail:
            html +='<tr name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_email_fa" id="fajianren%s">delete</button></div></td></tr>'    %(name,i[0],i[1],i[3])
        return jsonify(a="add-success",html=html)
    return show_fajianren




#删除发件人
def delete_fajianren(func):
    def delete_fajianren():
        func()
        print 1111111111111111111111111
        id=request.args.get('id').split('fajianren')[-1]
        print 'delete  from fajianren where id=%s'% id
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        fajian_detail=cu.execute('delete  from fajianren where id=%s'% id)
        db.commit()
        db.close()
        html=''
        return jsonify(a="delete-success")
    return delete_fajianren



#增加jekins
def add_jekins(func):
    def add_jekins():
        func()
        print 1111111111111111111111111111111111111
        print request.form
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        cu.executemany('INSERT INTO  jekins values (?,?,?,?,null,?,?,?)', [(request.form['jekins_user'],
                                                                         request.form['name'],
                                                                         request.form['token'],
                                                                         request.form['job'],
                                                                        request.form['url'],
                                                                        request.form['beizhu'],
                                                                        request.form['canshu']
                                                                            )])
        db.commit()
        id=cu.execute('select id from jekins where name="%s" order by id desc limit 0,1' % request.form['name']).fetchall()[0][0]
        db.close()
        html='<tr name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_jekins" id="fajianren%s">delete</button></div></td></tr>'    %(id,request.form['job'],request.form['beizhu'],id)
        print html
        return jsonify(a="add-success",html=html)
    return add_jekins



#jekins 列表
def jekins_list(func):
    def jekins_list():
        func()
        name=request.args.get('name')
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        fajian_detail=cu.execute('select job_name,beizhu,id from jekins where name="%s"'%name).fetchall()
        tongyong_detail=cu.execute('select user,token_id,url from jekins where name="%s"'%name).fetchall()
        if len(tongyong_detail)==0:
            tongyong_detail=['','','']
        else:
            tongyong_detail=tongyong_detail[0]
        db.close()
        html=''
        for i  in fajian_detail:
            html +='<tr name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_jekins" >delete</button></div></td></tr>'    %(i[2],i[0],i[1])
        return jsonify(a="add-success",html=html,tongyong_detail=tongyong_detail)
    return jekins_list


#删除jekins
def jekins_delete(func):
    def jekins_delete():
        func()
        print 1111111111111111111111111
        print request.args
        id=request.form['id']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        fajian_detail=cu.execute('delete  from jekins where id=%s'% id)
        db.commit()
        db.close()
        html=''
        return jsonify(a="delete-success")
    return jekins_delete



#删除suite
def suite_delete(func):
    def suite_delete():
        func()
        name=request.form['name']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        fajian_detail=cu.execute('delete  from dingshi_run where name="%s"'% name)
        db.commit()
        db.close()
        html=''
        return jsonify(a="delete-success")
    return suite_delete


#操作数据库
def sqlite_exe(func):
    def sqlite_exe():
        func()
        detail=request.form['detail']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        if 'select' in detail:
            fanhui=json.dumps(cu.execute(detail).fetchall())
        else:
            fanhui=''
        db.commit()
        db.close()
        return jsonify(a="sqllite-success",data=fanhui)
    return sqlite_exe