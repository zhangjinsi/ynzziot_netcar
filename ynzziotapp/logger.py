#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

'''
1、窗口日志
2、文件日志
3、报警日志,email
'''

import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, SMTPHandler
import config

class LoggerConfig(object):
    def __init__(self):
        self.logger_name = 'root'
        logging.basicConfig(level=logging.DEBUG)
        self.add_stream_handler()
        self.add_file_handler()
        self.add_email_handler()


    @property
    def logger(self):
        return logging.getLogger(self.logger_name)

    def add_email_handler(self):
        '''
        输出到email
        :return:
        '''
        handler = SMTPHandler(mailhost=config.MAIL_HOST, fromaddr=config.MAIL_FROM, toaddrs=config.MAIL_TOLIST, subject='server error', credentials=(config.MAIL_USERNAME, config.MAIL_PASSWORD), secure=())
        handler.setLevel(logging.ERROR)
        handler.setFormatter(logging.Formatter('''
        Message Type : %(levelname)s
        Location : %(pathname)s:%(lineno)d
        Module : %(module)s
        Function : %(funcName)s
        Time : %(asctime)s
        Message : %(message)s
        '''))
        logging.getLogger(self.logger_name).addHandler(handler)


    def add_stream_handler(self):
        '''
        输出到窗口
        :return:
        '''
        handler = StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s [%(pathname)s:%(lineno)d]'))
        logging.getLogger(self.logger_name).addHandler(handler)

    def add_file_handler(self):
        '''
        输出到文件日志
        :return:
        '''
        file_handler = RotatingFileHandler(config.LOGGER_PATH,maxBytes=1024*1024*500,delay=False,backupCount=20)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s [%(pathname)s:%(lineno)d]'))
        logging.getLogger(self.logger_name).addHandler(file_handler)

logger = LoggerConfig().logger
if __name__ == '__main__':

    #logger.warning('asss')
    logger.error('aaaasss')
