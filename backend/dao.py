# -*- coding: utf-8 -*-
"""数据访问层（Data Access Layer）

职责：只负责与数据库交互，执行 SQL、返回原始数据。
不包含任何业务规则（业务规则放在 service.py）。
"""
import contextlib
import psycopg2
import psycopg2.extras

from config import Config


def get_connection():
    """获取一个数据库连接（Row 字典游标）。"""
    conn = psycopg2.connect(Config.dsn())
    conn.autocommit = False
    return conn


@contextlib.contextmanager
def transaction():
    """事务上下文：正常退出提交，异常回滚。"""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def query_all(sql, params=None):
    with transaction() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or ())
            return [dict(r) for r in cur.fetchall()]


def execute(sql, params=None):
    """执行一条写语句，返回受影响行数。"""
    with transaction() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.rowcount


# ---------------- 具体表操作 ----------------

def list_students(keyword=None):
    if keyword:
        return query_all(
            "select id, name, dept_name, tot_cred from student "
            "where name like %s or id like %s order by id",
            ("%" + keyword + "%", "%" + keyword + "%"))
    return query_all(
        "select id, name, dept_name, tot_cred from student order by id")


def get_student(stu_id):
    rows = query_all(
        "select id, name, dept_name, tot_cred from student where id=%s",
        (stu_id,))
    return rows[0] if rows else None


def insert_student(stu_id, name, dept_name, tot_cred):
    return execute(
        "insert into student(id, name, dept_name, tot_cred) "
        "values (%s, %s, %s, %s)",
        (stu_id, name, dept_name, tot_cred))


def list_courses():
    return query_all(
        "select course_id, title, dept_name, credits from course "
        "order by course_id")


def list_departments():
    return query_all("select dept_name, building, budget from department "
                     "order by dept_name")


def count_students_by_dept():
    return query_all(
        "select dept_name, count(*) as num from student "
        "group by dept_name order by num desc")


def list_takes_of_student(stu_id):
    return query_all(
        "select t.course_id, c.title, t.semester, t.year, t.grade "
        "from takes t join course c on t.course_id = c.course_id "
        "where t.id = %s order by t.year, t.semester",
        (stu_id,))
