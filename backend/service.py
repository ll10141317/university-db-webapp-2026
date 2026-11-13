# -*- coding: utf-8 -*-
"""业务逻辑层（Business Logic Layer）

职责：参数校验、业务规则、组装数据。调用 dao 层访问数据库。
"""
import re

import dao


class BizError(Exception):
    """业务异常，携带给用户的提示信息。"""


def _validate_student(stu_id, name, dept_name, tot_cred):
    if not stu_id or not re.match(r"^[0-9A-Za-z]{3,12}$", stu_id):
        raise BizError("学号必须是 3-12 位字母或数字")
    if not name or len(name) > 20:
        raise BizError("姓名不能为空且不超过 20 个字符")
    if tot_cred is not None and (tot_cred < 0 or tot_cred > 999):
        raise BizError("已修学分必须在 0-999 之间")
    if not dept_name:
        raise BizError("请选择所属院系")


def get_all_students(keyword=None):
    return dao.list_students(keyword)


def get_student_detail(stu_id):
    stu = dao.get_student(stu_id)
    if stu is None:
        raise BizError("不存在学号为 %s 的学生" % stu_id)
    stu["takes"] = dao.list_takes_of_student(stu_id)
    return stu


def add_student(stu_id, name, dept_name, tot_cred):
    _validate_student(stu_id, name, dept_name, tot_cred)
    if dao.get_student(stu_id) is not None:
        raise BizError("学号 %s 已存在" % stu_id)
    dao.insert_student(stu_id, name, dept_name, tot_cred)
    return dao.get_student(stu_id)


def get_all_courses():
    return dao.list_courses()


def get_all_departments():
    return dao.list_departments()


def get_dept_statistics():
    return dao.count_students_by_dept()
