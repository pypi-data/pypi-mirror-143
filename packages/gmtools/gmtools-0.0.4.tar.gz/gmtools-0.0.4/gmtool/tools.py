# coding:utf-8
'''
@File    : tools.py
@Author  : guomin
@Desc    : 工具类
'''

from gmtool.util import json_util, send_mail_util


class Tool(object):

    def __init__(self):
        self.mail_from_user=" " #邮件发送者账号
        self.mail_pwd=" "       #邮件发送者密码
        self.mail_host=" "      #邮件发送者主机

    def send_mail_msg(self,to_user,subject,content):
        send_mail_util(self.mail_from_user,self.mail_pwd,self.mail_host,to_user,subject,content)

    @staticmethod
    def json_data_util(data):
        return json_util(data)