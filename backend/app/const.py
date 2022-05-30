# -*- coding: UTF-8 -*-
"""
合同管理模块常量定义
"""
ERRORMSG = {
    "USER_INFO_ERR": {
        "errorCode": 10050001,
        "errorMessage": "用户名或密码不正确"
    },
    "ADMIN_USERS_FULL": {
        "errorCode": 10050002,
        "errorMessage": "管理方账号数量超限"
    },
    "SMS_CODE_ERR": {
        "errorCode": 10050010,
        "errorMessage": "验证码不正确"
    },
    "EMAIL_NOT_EXIST_ERR": {
        "errorCode": 10050016,
        "errorMessage": "该邮箱未注册"
    },
    "INPUT_EXISTS_ERR": {
        "errorCode": 10050001,
        "errorMessage": "用户名或邮箱已经存在，请重新输入"
    },
    "NUMBER_NOT_EXISTS_ERR": {
        "errorCode": 10050004,
        "errorMessage": "该合同编号不存在，请重新输入"
    },
    "INPUT_NOT_EXISTS_ERR": {
        "errorCode": 10050002,
        "errorMessage": "该客户不存在，请重新输入"
    },
    "INPUT_VALUE_ERR": {
        "errorCode": 10050003,
        "errorMessage": "金额必须为数字，请重新输入"
    },
    "INPUT_NULL_ERR": {
        "errorCode": 10050006,
        "errorMessage": "输入内容为空，请重新输入"
    },
    "RECEIPT_EXISTS_ERR": {
        "errorCode": 10050007,
        "errorMessage": "该日期已经开过发票，请重新输入"
    },
    "CAPTCHA_INVALID_ERR": {
        "errorCode": 10050018,
        "errorMessage": "无效验证码"
    },
    "CAPTCHA_NOT_MATCH_ERR": {
        "errorCode": 10050019,
        "errorMessage": "验证码错误"
    },
    "USER_LOCKED_TRY_LATER": {
        "errorCode": 10050021,
        "errorMessage": ""
    },
    "OPERATE_DB_FAILED": {
        "errorCode": 10050022,
        "errorMessage": "操作数据库失败"
    },
    "NUMBER_NOT_FOUND": {
        "errorCode": 10050023,
        "errorMessage": "合同号未找到"
    },
    "SYSTEM_ERR": {
        "errorCode": 10050999,
        "errorMessage": "系统繁忙，请稍后再试"
    },
    "FILE_PICK_ERR": {
        "errorCode": 10050024,
        "errorMessage": "文件解析失败"
    }
}
