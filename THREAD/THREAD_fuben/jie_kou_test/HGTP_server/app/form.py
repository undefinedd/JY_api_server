#-*-coding:utf-8-*-
__author__ = 'SUNZHEN519'
from flask_wtf import Form
from wtforms import StringField, SubmitField,FileField,BooleanField,TextAreaField
from wtforms.validators import Required
from shell_name import file
class NameForm(Form):
 u=file()
 u=u.xx()
 u.insert(0,0)
 for i in u:
     print 111
     i=BooleanField(i)
 name = StringField('What is your name?', validators=[Required()])
 ss=BooleanField('aa')
 photo = FileField('Your photo')

 body = TextAreaField("What's on your mind?", validators=[Required()])

 submit = SubmitField('Submit')
class login(Form):
 name = StringField('What is your name?', validators=[Required()])
 password = StringField('What is your name?', validators=[Required()])
 submit = SubmitField('Submit')
class Textt(Form):
 bodytt = TextAreaField(u'正文', validators=[Required()])
 submitttt = SubmitField(u'发表')
