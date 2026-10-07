from flask import Flask, render_template, request, redirect, url_for, flash

from config import Config
from services.student_service import StudentService
from utils.logger import setup_logger


app = Flask(__name__)
app.config.from_object(Config)

logger = setup_logger()

student_service = StudentService(
    app.config["DATA_FILE"]
)


@app.route("/")
def dashboard():
    students = student_service.get_all_students()

    return render_template(
        "dashboard.html",
        students=students,
        total_students=len(students)
    )


@app.route("/students")
def students():
    search = request.args.get("search", "").strip()

    if search:
        student_list = student_service.search_students(search)
    else:
        student_list = student_service.get_all_students()

    return render_template(
        "dashboard.html",
        students=student_list,
        total_students=len(student_service.get_all_students()),
        search=search
    )


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":

        student_data = {
            "student_id": request.form.get("student_id", "").strip(),
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "age": request.form.get("age", "").strip(),
            "gender": request.form.get("gender", "").strip(),
            "course": request.form.get("course", "").strip(),
            "year_level": request.form.get("year_level", "").strip(),
            "email": request.form.get("email", "").strip()
        }

        success, message = student_service.add_student(student_data)

        if success:
            flash(message, "success")
            return redirect(url_for("dashboard"))

        flash(message, "danger")

        return render_template(
            "add_student.html",
            student=student_data
        )

    return render_template(
        "add_student.html",
        student={}
    )


@app.route("/students/edit/<student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    student = student_service.get_student(student_id)

    if student is None:
        flash("Student record was not found.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        updated_data = {
            "student_id": student_id,
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "age": request.form.get("age", "").strip(),
            "gender": request.form.get("gender", "").strip(),
            "course": request.form.get("course", "").strip(),
            "year_level": request.form.get("year_level", "").strip(),
            "email": request.form.get("email", "").strip()
        }

        success, message = student_service.update_student(
            student_id,
            updated_data
        )

        if success:
            flash(message, "success")
            return redirect(url_for("dashboard"))

        flash(message, "danger")

        return render_template(
            "edit_student.html",
            student=updated_data
        )

    return render_template(
        "edit_student.html",
        student=student
    )


@app.route("/students/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    success, message = student_service.delete_student(student_id)

    if success:
        flash(message, "success")
    else:
        flash(message, "danger")

    return redirect(url_for("dashboard"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "base.html",
        error_message="The requested page was not found."
    ), 404


@app.errorhandler(500)
def internal_error(error):
    logger.exception("Internal server error")

    return render_template(
        "base.html",
        error_message="An unexpected error occurred."
    ), 500


if __name__ == "__main__":
    logger.info("Student Information System started.")

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )