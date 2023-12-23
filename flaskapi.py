"""Code for a flask API to Create, Read, Update, Delete students"""
import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations using app.config subclass
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
mysql.init_app(app)


@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return "Hello, STUDENT world!"


@app.route("/create", methods=["POST"])
def add_student():
    """Function to create a student to the MySQL database"""
    json = request.json
    student_name = json["student_name"]
    student_email = json["student_email"]
    student_pic = json["student_pic"]
    student_pwd = json["student_pwd"]
    if student_name and student_email and student_pic and student_pwd and request.method == "POST":
        sql = "INSERT INTO students(student_name, student_email, student_pic, student_password) " \
              "VALUES(%s, %s,%s ,%s)"
        data = (student_name, student_email,student_pic, student_pwd)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify("Student created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide name, email,pic and pwd")


@app.route("/students", methods=["GET"])
def students():
    """Function to retrieve all students from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/student/<int:student_id>", methods=["GET"])
def user(student_id):
    """Function to get information of a specific student in the MSQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id=%s", student_id)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/update", methods=["POST"])
def update_student():
    """Function to update a student in the MYSQL database"""
    json = request.json
    student_name = json["student_name"]
    student_email = json["student_email"]
    student_pic = json["student_pic"]
    student_pwd = json["student_pwd"]
    student_id = json["student_id"]
    if student_name and student_email and student_pic and student_pwd and student_id and request.method == "POST":
        # save edits
        sql = "UPDATE students SET student_name=%s, student_email=%s, student_pic=%s " \
              "student_password=%s WHERE student_id=%s"
        data = (student_name, student_email,student_pic, student_pwd, student_user_id)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify("User updated successfully!")
            resp.status_code = 200
            cursor.close()
            conn.close()
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide id, name, email and pwd")


@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    """Function to delete a student from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id=%s", student_id)
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify("Userstudent deleted successfully!")
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

