# -*- coding: utf-8 -*-
"""表示层 / 控制层（Presentation & Controller Layer）

三层架构：
    浏览器  <->  app.py(路由/控制)  <->  service.py(业务)  <->  dao.py(数据访问)  <->  openGauss
运行：python app.py    访问 http://<ip>:8080
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify

import service
from config import Config

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/students")
def students():
    keyword = request.args.get("kw", "").strip()
    rows = service.get_all_students(keyword or None)
    return render_template("students.html", students=rows, kw=keyword)


@app.route("/students/<stu_id>")
def student_detail(stu_id):
    try:
        stu = service.get_student_detail(stu_id)
    except service.BizError as e:
        return render_template("error.html", message=str(e)), 404
    return render_template("student_detail.html", stu=stu)


@app.route("/students/new", methods=["GET", "POST"])
def student_new():
    if request.method == "POST":
        try:
            service.add_student(
                request.form.get("id", "").strip(),
                request.form.get("name", "").strip(),
                request.form.get("dept_name", "").strip(),
                int(request.form.get("tot_cred") or 0),
            )
            return redirect(url_for("students"))
        except service.BizError as e:
            return render_template("student_new.html",
                                   departments=service.get_all_departments(),
                                   error=str(e), form=request.form), 400
    return render_template("student_new.html",
                           departments=service.get_all_departments(),
                           error=None, form={})


@app.route("/courses")
def courses():
    return render_template("courses.html", courses=service.get_all_courses())


@app.route("/stats")
def stats():
    return render_template("stats.html", stats=service.get_dept_statistics())


# ---------------- REST API（供前端异步调用或测试） ----------------
@app.route("/api/students")
def api_students():
    return jsonify(service.get_all_students(
        request.args.get("kw", "").strip() or None))


@app.route("/api/health")
def api_health():
    try:
        service.get_all_students()
        return jsonify({"ok": True})
    except Exception as e:  # noqa
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host=Config.APP_HOST, port=Config.APP_PORT, debug=Config.DEBUG)
