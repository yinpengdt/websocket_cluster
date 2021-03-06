#!/usr/bin/python3
# -*- coding: utf-8
""" 
@author: mx472756841@gmail.com
@file: rabbitmq.py
@time: 2019/3/4 11:25
"""
import json
import logging

import pika

import config

logger = logging.getLogger(__name__)


class RabbitMQClient:
    def __init__(self, host=config.RABBIT_MQ_HOST, port=config.RABBIT_MQ_PORT,
                 user=config.RABBIT_MQ_USER, password=config.RABBIT_MQ_PASSWORD):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def get_conn(self):
        """
        获取rabbitmq的conn
        :return:
        """
        user_pwd = pika.PlainCredentials(self.user, self.password)
        # get connection
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(self.host, self.port, credentials=user_pwd)
        )
        return conn

    def get_channel(self, exchange_name, exchange_type='direct'):
        conn = self.get_conn()
        # get channel
        channel = conn.channel()
        # 声明直连交换机
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        return channel

    def publish_message(self, message, exchange_name, rounting_key="", exchange_type="direct"):
        """
        发送消息
        :param message:
        :param exchange_name:
        :param rounting_key:
        :param exchange_type:
        :return:
        """
        channel = self.get_channel(exchange_name, exchange_type)
        message = json.dumps(message)
        ret = channel.basic_publish(exchange=exchange_name,
                                    routing_key=rounting_key,
                                    body=message)
