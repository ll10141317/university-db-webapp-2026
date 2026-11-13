# -*- coding: utf-8 -*-
"""配置层：集中管理数据库与应用的参数。可用环境变量覆盖。"""
import os


class Config:
    # 数据库连接参数（openGauss / KingbaseES 均兼容 PostgreSQL 协议）
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.environ.get("DB_PORT", "26000"))
    DB_NAME = os.environ.get("DB_NAME", "studentdb")
    DB_USER = os.environ.get("DB_USER", "student")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

    # 应用参数
    APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.environ.get("APP_PORT", "8080"))
    DEBUG = os.environ.get("APP_DEBUG", "0") == "1"

    @classmethod
    def dsn(cls):
        return (
            "host=%s port=%d dbname=%s user=%s password=%s"
            % (cls.DB_HOST, cls.DB_PORT, cls.DB_NAME,
               cls.DB_USER, cls.DB_PASSWORD)
        )
