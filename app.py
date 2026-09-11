from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import os
import joblib
import pandas as pd
import numpy as np


app = Flask(__name__)
CORS(app)


# -------------------------
# MySQL Configuration
# -------------------------
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "lms"

mysql = MySQL(app)

# -------------------------
# Home Route
# -------------------------
@app.route("/")
def home():
    return "Flask Backend Running Successfully"

# -------------------------
# Add Course API
# -------------------------
@app.route("/courses", methods=["POST"])
def add_course():

    data = request.get_json()

    course_name = data["course_name"]
    description = data["description"]
    difficulty = data["difficulty_level"]
    duration = data["duration"]
    youtube_link = data["youtube_link"]

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO courses
        (course_name, description, difficulty_level, duration,youtube_link)
        VALUES (%s, %s, %s, %s, %s)
    """, (course_name, description, difficulty, duration,youtube_link))

    mysql.connection.commit()
    cur.close()

    return jsonify({
        "message": "Course Added Successfully"
    })

#-------------
# View Courses
#---------------

@app.route("/courses", methods=["GET"])
def get_courses():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM courses")

    data = cur.fetchall()

    courses=[]

    for row in data:

        courses.append({

            "course_id":row[0],
            "course_name":row[1],
            "description":row[2],
            "difficulty_level":row[3],
            "duration":row[4]

        })

    return jsonify(courses)



#-------------------
#Delete Courses
#-------------


@app.route("/courses/<int:id>",methods=["DELETE"])
def delete_course(id):

    cur=mysql.connection.cursor()

    cur.execute(
        "DELETE FROM courses WHERE course_id=%s",
        (id,)
    )

    mysql.connection.commit()

    return jsonify({
        "message":"Deleted Successfully"
    })

#--------------
#Update Courses
#---------------

@app.route("/courses/<int:id>", methods=["PUT"])
def update_course(id):

    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("""

    UPDATE courses

    SET

    course_name=%s,
    description=%s,
    difficulty_level=%s,
    duration=%s,
    youtube_link=%s

    WHERE course_id=%s

    """, (

        data["course_name"],
        data["description"],
        data["difficulty_level"],
        data["duration"],
        data["youtube_link"],
        id

    ))

    mysql.connection.commit()
    cur.close()

    return jsonify({
        "message": "Updated Successfully"
    })
#--------------
#Add Quiz
#---------------

@app.route("/quizzes", methods=["POST"])
def add_quiz():

    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("""

    INSERT INTO quiz
    (course_id,title,total_marks,time_limit,passing_marks)

    VALUES(%s,%s,%s,%s,%s)

    """,(data["course_id"],
         data["title"],
         data["total_marks"],
         data["time_limit"],
         data["passing_marks"]))

    mysql.connection.commit()

    cur.close()

    return jsonify({
        "message":"Quiz Added Successfully"
    })

# -------------------------
# View Quizez
# -------------------------

@app.route("/quizzes", methods=["GET"])
def get_quizzes():

    cur = mysql.connection.cursor()

    cur.execute("""

    SELECT
    quiz.quiz_id,
    quiz.course_id,
    courses.course_name,
    quiz.title,
    quiz.total_marks,
    quiz.time_limit,
    quiz.passing_marks

    FROM quiz

    INNER JOIN courses

    ON quiz.course_id = courses.course_id

    """)

    data = cur.fetchall()

    quizzes=[]

    for row in data:

        quizzes.append({

            "quiz_id":row[0],
            "course_id":row[1],
            "course_name":row[2],
            "title":row[3],
            "total_marks":row[4],
            "time_limit":row[5],
            "passing_marks":row[6]

        })

    return jsonify(quizzes)


# -------------------------
# Delete quiz
# -------------------------

@app.route("/quizzes/<int:id>",methods=["DELETE"])
def delete_quiz(id):

    cur=mysql.connection.cursor()

    cur.execute(

    "DELETE FROM quiz WHERE quiz_id=%s",

    (id,)

    )

    mysql.connection.commit()

    return jsonify({

        "message":"Quiz Deleted"

    })
# -------------------------
# Update Quiz 
# -------------------------
@app.route("/quizzes/<int:id>",methods=["PUT"])
def update_quiz(id):

    data=request.get_json()

    cur=mysql.connection.cursor()

    cur.execute("""

    UPDATE quiz

    SET

    course_id=%s,
    title=%s,
    total_marks=%s,
    time_limit=%s,
    passing_marks=%s

    WHERE quiz_id=%s

    """,(data["course_id"],
         data["title"],
         data["total_marks"],
         data["time_limit"],
         data["passing_marks"],
         id))

    mysql.connection.commit()

    return jsonify({

        "message":"Quiz Updated Successfully"

    })
# -------------------------
# Add Question
# -------------------------

@app.route("/questions", methods=["POST"])
def add_question():

    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("""

    INSERT INTO questions
    (quiz_id, question_text, options, correct_option)

    VALUES(%s,%s,%s,%s)

    """, (

        data["quiz_id"],
        data["question_text"],
        data["options"],
        data["correct_option"]

    ))

    mysql.connection.commit()

    cur.close()

    return jsonify({
        "message": "Question Added Successfully"
    })

# -------------------------
# View Questions
# -------------------------

@app.route("/questions", methods=["GET"])
def get_questions():

    cur = mysql.connection.cursor()

    cur.execute("""

    SELECT

    questions.question_id,
    questions.quiz_id,
    quiz.title,
    questions.question_text,
    questions.options,
    questions.correct_option

    FROM questions

    INNER JOIN quiz

    ON questions.quiz_id = quiz.quiz_id

    """)

    data = cur.fetchall()

    questions = []

    for row in data:

        questions.append({

            "question_id": row[0],
            "quiz_id": row[1],
            "quiz_title": row[2],
            "question_text": row[3],
            "options": row[4],
            "correct_option": row[5]

        })

    cur.close()

    return jsonify(questions)

# -------------------------
# Update Question
# -------------------------

@app.route("/questions/<int:id>", methods=["PUT"])
def update_question(id):

    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("""

    UPDATE questions

    SET

    quiz_id=%s,
    question_text=%s,
    options=%s,
    correct_option=%s

    WHERE question_id=%s

    """, (

        data["quiz_id"],
        data["question_text"],
        data["options"],
        data["correct_option"],
        id

    ))

    mysql.connection.commit()

    cur.close()

    return jsonify({

        "message": "Question Updated Successfully"

    })

# -------------------------
# Delete Question
# -------------------------

@app.route("/questions/<int:id>", methods=["DELETE"])
def delete_question(id):

    cur = mysql.connection.cursor()

    cur.execute(

        "DELETE FROM questions WHERE question_id=%s",

        (id,)

    )

    mysql.connection.commit()

    cur.close()

    return jsonify({

        "message": "Question Deleted Successfully"

    })
# -------------------------
# Get Students
# -------------------------

@app.route("/students", methods=["GET"])
def get_students():

    cur = mysql.connection.cursor()

    cur.execute("SELECT student_id, name FROM student")

    data = cur.fetchall()

    students = []

    for row in data:

        students.append({

            "student_id": row[0],
            "name": row[1]

        })

    cur.close()

    return jsonify(students)

# -------------------------
# Add Result
# -------------------------

@app.route("/results", methods=["POST"])
def add_result():

    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("""

        INSERT INTO results
        (student_id, quiz_id, score, attempts, time_spent)

        VALUES(%s,%s,%s,%s,%s)

    """, (

        data["student_id"],
        data["quiz_id"],
        data["score"],
        data["attempts"],
        data["time_spent"]

    ))

    mysql.connection.commit()

    cur.close()

    return jsonify({
        "message": "Result Added Successfully"
    })
# -------------------------
# View Results
# -------------------------

@app.route("/results", methods=["GET"])
def get_results():

    cur = mysql.connection.cursor()

    cur.execute("""

        SELECT

        results.result_id,
        results.student_id,
        student.name,
        results.quiz_id,
        quiz.title,
        results.score,
        results.attempts,
        results.time_spent

        FROM results

        INNER JOIN student
        ON results.student_id = student.student_id

        INNER JOIN quiz
        ON results.quiz_id = quiz.quiz_id

    """)

    data = cur.fetchall()

    results = []

    for row in data:

        results.append({

            "result_id": row[0],
            "student_id": row[1],
            "student_name": row[2],
            "quiz_id": row[3],
            "quiz_title": row[4],
            "score": row[5],
            "attempts": row[6],
            "time_spent": row[7]

        })

    cur.close()

    return jsonify(results)

# -------------------------
# Update Result
# -------------------------

@app.route("/results/<int:id>", methods=["PUT"])
def update_result(id):

    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("""

        UPDATE results

        SET

        student_id=%s,
        quiz_id=%s,
        score=%s,
        attempts=%s,
        time_spent=%s

        WHERE result_id=%s

    """, (

        data["student_id"],
        data["quiz_id"],
        data["score"],
        data["attempts"],
        data["time_spent"],
        id

    ))

    mysql.connection.commit()

    cur.close()

    return jsonify({
        "message": "Result Updated Successfully"
    })
# -------------------------
# Delete Result
# -------------------------

@app.route("/results/<int:id>", methods=["DELETE"])
def delete_result(id):

    cur = mysql.connection.cursor()

    cur.execute(

        "DELETE FROM results WHERE result_id=%s",

        (id,)

    )

    mysql.connection.commit()

    cur.close()

    return jsonify({
        "message": "Result Deleted Successfully"
    })
@app.route("/student-signup", methods=["POST"])
def student_signup():

    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("""

    INSERT INTO student
    (name,email,password)

    VALUES(%s,%s,%s)

    """,(

        data["name"],
        data["email"],
        data["password"]

    ))

    mysql.connection.commit()

    cur.close()

    return jsonify({
        "message":"Student Registered Successfully"
    })

@app.route("/student-login", methods=["POST"])
def student_login():

    data = request.get_json()

    email = data["email"]
    password = data["password"]

    cur = mysql.connection.cursor()

    # Student Login
    cur.execute("""
        SELECT student_id, name
        FROM student
        WHERE email=%s AND password=%s
    """, (email, password))

    student = cur.fetchone()

    if student:

        student_id = student[0]
        student_name = student[1]

        # Check if activity record exists
        cur.execute("""
            SELECT activity_id
            FROM student_activity
            WHERE student_id=%s
            AND course_id IS NULL
        """, (student_id,))

        activity = cur.fetchone()

        if activity:

            # Update login count
            cur.execute("""
                UPDATE student_activity

SET login_count=login_count+1,
last_login=NOW()

WHERE student_id=%s

AND course_id IS NULL
            """, (student_id,))

        else:

            # Create activity record
            cur.execute("""
INSERT INTO student_activity
(student_id, login_count)

VALUES(%s,%s)
""", (student_id, 1))
        mysql.connection.commit()

        cur.close()

        return jsonify({
            "message": "Login Successful",
            "student_id": student_id,
            "name": student_name
        })

    cur.close()

    return jsonify({
        "message": "Invalid Email or Password"
    }), 401
    

# -------------------------
# Enroll Course
# -------------------------

@app.route("/enrollments", methods=["POST"])
def enroll_course():

    data = request.get_json()

    cur = mysql.connection.cursor()

    # Check if already enrolled
    cur.execute("""

    SELECT * FROM enrollments

    WHERE student_id=%s AND course_id=%s

    """,(

        data["student_id"],
        data["course_id"]

    ))

    existing = cur.fetchone()

    if existing:

        cur.close()

        return jsonify({

            "message":"Already Enrolled"

        }),400

    cur.execute("""

    INSERT INTO enrollments

    (student_id,course_id)

    VALUES(%s,%s)

    """,(

        data["student_id"],
        data["course_id"]

    ))

    mysql.connection.commit()

    cur.close()

    return jsonify({

        "message":"Course Enrolled Successfully"

    })
# -------------------------
# Student Enrolled Courses
# -------------------------

@app.route("/enrollments/<int:student_id>", methods=["GET"])
def get_student_courses(student_id):

    cur = mysql.connection.cursor()

    cur.execute("""

    SELECT

    enrollments.enrollment_id,

    courses.course_id,

    courses.course_name,

    courses.description,

    courses.difficulty_level,

    courses.duration

    FROM enrollments

    INNER JOIN courses

    ON enrollments.course_id = courses.course_id

    WHERE enrollments.student_id=%s

    """,(student_id,))

    data = cur.fetchall()

    courses=[]

    for row in data:

        courses.append({

            "enrollment_id":row[0],

            "course_id":row[1],

            "course_name":row[2],

            "description":row[3],

            "difficulty_level":row[4],

            "duration":row[5]

        })

    cur.close()

    return jsonify(courses)

# -------------------------
# Unenroll Course
# -------------------------

@app.route("/enrollments/<int:id>", methods=["DELETE"])
def delete_enrollment(id):

    cur = mysql.connection.cursor()

    cur.execute(

    "DELETE FROM enrollments WHERE enrollment_id=%s",

    (id,)

    )

    mysql.connection.commit()

    cur.close()

    return jsonify({

        "message":"Enrollment Removed"

    })
# -------------------------
# Course material
# -------------------------
@app.route("/courses/<int:id>", methods=["GET"])
def get_single_course(id):

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
        course_id,
        course_name,
        description,
        difficulty_level,
        duration,
        youtube_link
        FROM courses
        WHERE course_id=%s
    """, (id,))

    row = cur.fetchone()

    if row:
        return jsonify({
            "course_id": row[0],
            "course_name": row[1],
            "description": row[2],
            "difficulty_level": row[3],
            "duration": row[4],
            "youtube_link": row[5]
        })

    return jsonify({"message": "Course not found"}), 404

# -------------------------
# Get Student Quiz Questions
# -------------------------

@app.route("/student-quiz/<int:quiz_id>", methods=["GET"])
def student_quiz(quiz_id):

    print("Quiz ID =", quiz_id)

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            question_id,
            question_text,
            options
        FROM questions
        WHERE quiz_id=%s
    """, (quiz_id,))

    rows = cur.fetchall()


    questions = []

    for row in rows:

        questions.append({
            "question_id": row[0],
            "question_text": row[1],
            "options": row[2]
        })

    cur.close()

    return jsonify(questions)

# -------------------------
# Submit Quiz
# -------------------------

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():

    data = request.get_json()

    student_id = data["student_id"]
    quiz_id = data["quiz_id"]
    answers = data["answers"]
    time_spent = data["time_spent"]

    cur = mysql.connection.cursor()

    # -------------------------
    # Get Questions
    # -------------------------

    cur.execute("""
        SELECT question_id, correct_option
        FROM questions
        WHERE quiz_id=%s
    """, (quiz_id,))

    questions = cur.fetchall()

    total_questions = len(questions)

    if total_questions == 0:

        cur.close()

        return jsonify({
            "message": "No questions found for this quiz."
        }), 400

    # -------------------------
    # Calculate Score
    # -------------------------

    score = 0

    for question in questions:

        question_id = str(question[0])
        correct_answer = question[1]

        if question_id in answers:

            if answers[question_id] == correct_answer:

                score += 1

    # -------------------------
    # Calculate Percentage
    # -------------------------

    percentage = round((score / total_questions) * 100, 2)

    # -------------------------
    # Get Quiz Details
    # -------------------------

    cur.execute("""
        SELECT course_id, passing_marks
        FROM quiz
        WHERE quiz_id=%s
    """, (quiz_id,))

    quiz = cur.fetchone()

    if not quiz:

        cur.close()

        return jsonify({
            "message": "Quiz not found."
        }), 404

    course_id = quiz[0]
    passing_marks = quiz[1]

    # -------------------------
    # Pass / Fail
    # -------------------------

    if percentage >= passing_marks:
        status = "Pass"
    else:
        status = "Fail"

    # -------------------------
    # Attempts
    # -------------------------

    cur.execute("""
        SELECT COUNT(*)
        FROM results
        WHERE student_id=%s
        AND quiz_id=%s
    """, (student_id, quiz_id))

    attempts = cur.fetchone()[0] + 1

    # -------------------------
    # Save Result
    # -------------------------

    cur.execute("""
        INSERT INTO results
        (
            student_id,
            quiz_id,
            score,
            attempts,
            time_spent,
            percentage,
            status
        )

        VALUES(%s,%s,%s,%s,%s,%s,%s)

    """, (

        student_id,
        quiz_id,
        score,
        attempts,
        time_spent,
        percentage,
        status

    ))

    # -------------------------
    # Update Student Activity
    # -------------------------

    cur.execute("""
        SELECT activity_id
        FROM student_activity
        WHERE student_id=%s
        AND course_id=%s
    """, (

        student_id,
        course_id

    ))

    activity = cur.fetchone()

    if activity:

        cur.execute("""
            UPDATE student_activity

            SET
                raised_hands = raised_hands + %s

            WHERE student_id=%s
            AND course_id=%s
        """, (

            score,
            student_id,
            course_id

        ))

    else:

        cur.execute("""
            INSERT INTO student_activity
            (
                student_id,
                course_id,
                raised_hands
            )

            VALUES(%s,%s,%s)

        """, (

            student_id,
            course_id,
            score

        ))

    mysql.connection.commit()

    cur.close()

    return jsonify({

        "message": "Quiz Submitted Successfully",

        "score": score,

        "total_questions": total_questions,

        "percentage": percentage,

        "attempts": attempts,

        "status": status

    })

# -------------------------
# Get Quiz ID by Course ID
# -------------------------

@app.route("/quiz-by-course/<int:course_id>", methods=["GET"])
def quiz_by_course(course_id):

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT quiz_id
        FROM quiz
        WHERE course_id=%s
    """, (course_id,))

    row = cur.fetchone()

    cur.close()

    if row:
        return jsonify({
            "quiz_id": row[0]
        })

    return jsonify({
        "message": "Quiz not found"
    }), 404

# -------------------------
# Student Results
# -------------------------

@app.route("/student-results/<int:student_id>", methods=["GET"])
def student_results(student_id):

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            results.result_id,
            quiz.title,
            results.score,
            results.attempts,
            results.time_spent,
            results.percentage,
            results.status

        FROM results

        JOIN quiz
        ON results.quiz_id = quiz.quiz_id

        WHERE results.student_id = %s

        ORDER BY results.result_id DESC
    """, (student_id,))

    data = cur.fetchall()

    results = []

    for row in data:

        percentage = float(row[5])

        if percentage >= 90:
            recommendation = "Excellent! You are ready for the next level."

        elif percentage >= 70:
            recommendation = "Good job! Practice a little more."

        elif percentage >= 50:
            recommendation = "Revise the course and watch the material again."

        else:
            recommendation = "Rewatch the videos and retake the quiz."

        results.append({

            "result_id": row[0],
            "quiz_name": row[1],
            "score": row[2],
            "attempts": row[3],
            "time_spent": row[4],
            "percentage": row[5],
            "status": row[6],
            "recommendation": recommendation

        })

    cur.close()

    return jsonify(results)
# -------------------------
# Admin Result Report
# -------------------------

@app.route("/admin-results", methods=["GET"])
def admin_results():

    cur = mysql.connection.cursor()

    cur.execute("""

        SELECT

        results.result_id,
        student.name,
        quiz.title,
        results.score,
        results.percentage,
        results.status,
        results.attempts,
        results.time_spent

        FROM results

        JOIN student
        ON results.student_id = student.student_id

        JOIN quiz
        ON results.quiz_id = quiz.quiz_id

        ORDER BY results.result_id DESC

    """)

    data = cur.fetchall()

    report = []

    for row in data:

        report.append({

            "result_id": row[0],
            "student_name": row[1],
            "quiz_title": row[2],
            "score": row[3],
            "percentage": row[4],
            "status": row[5],
            "attempts": row[6],
            "time_spent": row[7]

        })

    cur.close()

    return jsonify(report)

# -------------------------
# Update Visited Resources
# -------------------------

@app.route("/update-resource", methods=["POST"])
def update_resource():

    data = request.get_json()

    student_id = data["student_id"]
    course_id = data["course_id"]

    cur = mysql.connection.cursor()

    # Check if record already exists
    cur.execute("""
        SELECT activity_id
        FROM student_activity
        WHERE student_id=%s AND course_id=%s
    """, (student_id, course_id))

    activity = cur.fetchone()

    if activity:

        cur.execute("""
            UPDATE student_activity
            SET visited_resources = visited_resources + 1
            WHERE student_id=%s AND course_id=%s
        """, (student_id, course_id))

    else:

        cur.execute("""
            INSERT INTO student_activity
            (student_id, course_id, visited_resources)
            VALUES(%s,%s,%s)
        """, (student_id, course_id, 1))

    mysql.connection.commit()
    cur.close()

    return jsonify({
        "message": "Resource Updated Successfully"
    })
# -------------------------
# Add Announcement
# -------------------------
@app.route("/announcements", methods=["POST"])
def add_announcement():

    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO announcements
        (title, description)

        VALUES(%s,%s)
    """, (

        data["title"],
        data["description"]

    ))

    mysql.connection.commit()

    cur.close()

    return jsonify({

        "message":"Announcement Added Successfully"

    })
# -------------------------
# Get All Announcements
# -------------------------
@app.route("/announcements", methods=["GET"])
def get_announcements():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
        announcement_id,
        title,
        description,
        created_at

        FROM announcements

        ORDER BY created_at DESC
    """)

    data = cur.fetchall()

    announcements=[]

    for row in data:

        announcements.append({

            "announcement_id":row[0],
            "title":row[1],
            "description":row[2],
            "created_at":row[3]

        })

    cur.close()

    return jsonify(announcements)
# -------------------------
# Update AI tracking 
# -------------------------
@app.route("/announcements/<int:id>", methods=["PUT"])
def update_announcement(id):

    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("""

        UPDATE announcements

        SET
        title=%s,
        description=%s

        WHERE announcement_id=%s

    """,(

        data["title"],
        data["description"],
        id

    ))

    mysql.connection.commit()

    cur.close()

    return jsonify({

        "message":"Announcement Updated Successfully"

    })
# -------------------------
# Delete Announcement
# -------------------------

@app.route("/announcements/<int:id>", methods=["DELETE"])
def delete_announcement(id):

    cur = mysql.connection.cursor()

    cur.execute("""

        DELETE FROM announcements

        WHERE announcement_id=%s

    """,(id,))

    mysql.connection.commit()

    cur.close()

    return jsonify({

        "message":"Announcement Deleted Successfully"

    })
# -------------------------
# Student AI Tracking
# ----------------------
@app.route("/announcement-view", methods=["POST"])
def announcement_view():

    data = request.get_json()

    student_id = data["student_id"]

    cur = mysql.connection.cursor()

    cur.execute("""

        UPDATE student_activity

        SET announcements_view = announcements_view + 1

        WHERE student_id=%s

    """,(student_id,))

    mysql.connection.commit()

    cur.close()

    return jsonify({

        "message":"View Count Updated"

    })

# -------------------------
# Load AI Model
# -------------------------


#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#MODEL_PATH = os.path.join(BASE_DIR, "..", "ML", "model.pkl")
#ENCODER_PATH = os.path.join(BASE_DIR, "..", "ML", "label_encoder.pkl")

#model = joblib.load(MODEL_PATH)
#label_encoder = joblib.load(ENCODER_PATH)

#print("AI Model Loaded Successfully")
#print("Classes:", label_encoder.classes_) */

# ============================================================
# LOAD FINAL OULAD ML MODEL
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = r"C:\Users\Noor-sajid\Downloads\archive\ml_results\final_oulad_model.pkl"
FEATURE_PATH = r"C:\Users\Noor-sajid\Downloads\archive\ml_results\feature_names.pkl"
TARGET_MAPPING_PATH = r"C:\Users\Noor-sajid\Downloads\archive\ml_results\target_mapping.pkl"

model = joblib.load(MODEL_PATH)

if os.path.exists(FEATURE_PATH):
    feature_names = joblib.load(FEATURE_PATH)
else:
    feature_names = [
        "unregistration_rate",
        "average_score",
        "unregistered_count",
        "assessment_count",
        "ever_unregistered",
        "performance_engagement",
        "max_score",
        "min_score",
        "score_range",
        "vle_interactions",
        "score_consistency",
        "average_weight",
        "unique_vle_resources",
        "interactions_per_resource",
        "average_registration_date"
    ]

# New model target mapping
target_mapping = {
    0: "Distinction",
    1: "Fail",
    2: "Pass",
    3: "Withdrawn"
}

# LMS labels
result_mapping = {
    "Distinction": "Excellent",
    "Pass": "Good",
    "Fail": "Fair",
    "Withdrawn": "AtRisk"
}

print("============================================================")
print("FINAL OULAD ML MODEL LOADED")
print("============================================================")
print("Model:", type(model).__name__)
print("Features:", feature_names)


# -------------------------
# AI Prediction
# -------------------------

# @app.route("/predict-performance/<int:student_id>", methods=["GET"])
# def predict_performance(student_id):

#     cur = mysql.connection.cursor()

#     cur.execute("""
#         SELECT
#             SUM(visited_resources),
#             SUM(announcements_view),
#             SUM(discussion_count),
#             SUM(raised_hands),
#             SUM(login_count)
#         FROM student_activity
#         WHERE student_id=%s
#     """, (student_id,))

#     row = cur.fetchone()

#     cur.close()

#     # No activity found
#     if row is None or row[0] is None:

#         return jsonify({
#             "message": "No Activity Found"
#         }), 404

#     # Activity Values
#     visited_resources = row[0] or 0
#     announcements_view = row[1] or 0
#     discussion_count = row[2] or 0
#     raised_hands = row[3] or 0
#     login_count = row[4] or 0

#     # -------------------------
#     # AI Model Input
#     # -------------------------

#     input_data = pd.DataFrame([{
#         "visited_resources": visited_resources,
#         "announcements_view": announcements_view,
#         "discussion_count": discussion_count,
#         "raised_hands": raised_hands,
#         "login_count": login_count
#     }])

#     # -------------------------
#     # Predict
#     # -------------------------

#     prediction = model.predict(input_data)

#     print("Prediction :", prediction)
#     print("Classes :", label_encoder.classes_)

#     performance = label_encoder.inverse_transform(prediction)[0]

#     # -------------------------
#     # Recommendation
#     # -------------------------

#     if performance == "Excellent":

#         recommendation = "Excellent performance! You are ready for advanced courses."

#         recommended_courses = [
#             "Advanced React",
#             "Node.js",
#             "Machine Learning"
#         ]

#     elif performance == "Good":

#         recommendation = "Good performance. Keep practising and attempt more quizzes."

#         recommended_courses = [
#             "JavaScript",
#             "Bootstrap",
#             "Python"
#         ]

#     elif performance == "Average":

#         recommendation = "Watch the course material again and improve your quiz scores."

#         recommended_courses = [
#             "HTML Revision",
#             "CSS Practice",
#             "Database Fundamentals"
#         ]

#     else:

#         recommendation = "Your performance is at risk. Please revise the course and contact your instructor."

#         recommended_courses = [
#             "Watch HTML Again",
#             "Retake Quiz",
#             "Contact Instructor"
#         ]

#     # -------------------------
#     # Response
#     # -------------------------

#     return jsonify({

#         "performance": performance,
#         "recommendation": recommendation,
#         "recommended_courses": recommended_courses,

#         "visited_resources": visited_resources,
#         "announcements_view": announcements_view,
#         "discussion_count": discussion_count,
#         "raised_hands": raised_hands,
#         "login_count": login_count

#     })


# ============================================================
# AI PERFORMANCE PREDICTION - FINAL OULAD MODEL
# ============================================================

@app.route("/predict-performance/<int:student_id>", methods=["GET"])
def predict_performance(student_id):

    try:

        cur = mysql.connection.cursor()

        # ====================================================
        # GET STUDENT ACTIVITY
        # ====================================================

        cur.execute("""
            SELECT
                COALESCE(SUM(visited_resources), 0),
                COALESCE(SUM(announcements_view), 0),
                COALESCE(SUM(discussion_count), 0),
                COALESCE(SUM(raised_hands), 0),
                COALESCE(SUM(login_count), 0)
            FROM student_activity
            WHERE student_id = %s
        """, (student_id,))

        activity = cur.fetchone()

        # ====================================================
        # GET QUIZ / RESULT INFORMATION
        # ====================================================

        cur.execute("""
            SELECT
                COUNT(*),
                COALESCE(AVG(score), 0),
                COALESCE(MAX(score), 0),
                COALESCE(MIN(score), 0),
                COALESCE(STDDEV(score), 0)
            FROM results
            WHERE student_id = %s
        """, (student_id,))

        result_data = cur.fetchone()

        cur.close()

        # ====================================================
        # ACTIVITY VALUES
        # ====================================================

        if activity:
            visited_resources = float(activity[0] or 0)
            announcements_view = float(activity[1] or 0)
            discussion_count = float(activity[2] or 0)
            raised_hands = float(activity[3] or 0)
            login_count = float(activity[4] or 0)

        else:
            visited_resources = 0
            announcements_view = 0
            discussion_count = 0
            raised_hands = 0
            login_count = 0

        # ====================================================
        # QUIZ VALUES
        # ====================================================

        if result_data:

            assessment_count = float(result_data[0] or 0)
            average_score = float(result_data[1] or 0)
            max_score = float(result_data[2] or 0)
            min_score = float(result_data[3] or 0)
            score_consistency = float(result_data[4] or 0)

        else:

            assessment_count = 0
            average_score = 0
            max_score = 0
            min_score = 0
            score_consistency = 0

        # ====================================================
        # CALCULATE 15 ML FEATURES
        # ====================================================

        score_range = max_score - min_score

        unregistered_count = 0

        if assessment_count > 0:
            ever_unregistered = 0
        else:
            ever_unregistered = 1

        # Engagement based on LMS activity
        performance_engagement = (
            visited_resources
            + announcements_view
            + discussion_count
            + raised_hands
            + login_count
        )

        # Prevent extremely large values
        performance_engagement = float(performance_engagement)

        # VLE interaction approximation from available LMS activity
        vle_interactions = (
            visited_resources
            + discussion_count
            + announcements_view
        )

        unique_vle_resources = visited_resources

        if unique_vle_resources > 0:
            interactions_per_resource = (
                vle_interactions / unique_vle_resources
            )
        else:
            interactions_per_resource = 0

        # Average weight
        average_weight = 1.0

        # Registration date
        average_registration_date = 0

        # Unregistration rate
        if assessment_count > 0:
            unregistration_rate = (
                unregistered_count / assessment_count
            )
        else:
            unregistration_rate = 0

        # ====================================================
        # CREATE FINAL 15-FEATURE DATAFRAME
        # ====================================================

        input_data = {

            "unregistration_rate": unregistration_rate,

            "average_score": average_score,

            "unregistered_count": unregistered_count,

            "assessment_count": assessment_count,

            "ever_unregistered": ever_unregistered,

            "performance_engagement": performance_engagement,

            "max_score": max_score,

            "min_score": min_score,

            "score_range": score_range,

            "vle_interactions": vle_interactions,

            "score_consistency": score_consistency,

            "average_weight": average_weight,

            "unique_vle_resources": unique_vle_resources,

            "interactions_per_resource": interactions_per_resource,

            "average_registration_date": average_registration_date
        }

        # Make sure exact feature order is used
        input_df = pd.DataFrame(
            [[input_data[feature] for feature in feature_names]],
            columns=feature_names
        )

        # ====================================================
        # CHECK VALUES
        # ====================================================

        input_df = input_df.replace(
            [np.inf, -np.inf],
            np.nan
        )

        input_df = input_df.fillna(0)

        # ====================================================
        # ML PREDICTION
        # ====================================================

        prediction = model.predict(input_df)[0]

        prediction = int(prediction)

        original_prediction = target_mapping.get(
            prediction,
            "Unknown"
        )

        performance = result_mapping.get(
            original_prediction,
            "Unknown"
        )

        print("============================================================")
        print("AI PREDICTION")
        print("Student ID:", student_id)
        print("Input Features:")
        print(input_df.to_dict(orient="records")[0])
        print("Original Prediction:", original_prediction)
        print("LMS Prediction:", performance)
        print("============================================================")

        # ====================================================
        # PROBABILITIES
        # ====================================================

        probabilities = {}

        if hasattr(model, "predict_proba"):

            proba = model.predict_proba(input_df)[0]

            for i, probability in enumerate(proba):

                class_name = target_mapping.get(
                    i,
                    str(i)
                )

                probabilities[class_name] = round(
                    float(probability),
                    4
                )

        # ====================================================
        # RECOMMENDATION
        # ====================================================

        if performance == "Excellent":

            recommendation = (
                "Excellent performance! "
                "You are ready for advanced learning."
            )

            recommended_courses = [
                "Advanced React",
                "Node.js",
                "Machine Learning"
            ]

        elif performance == "Good":

            recommendation = (
                "Good performance. "
                "Keep practising and attempt more quizzes "
                "to improve your performance."
            )

            recommended_courses = [
                "JavaScript",
                "Python",
                "Database Fundamentals"
            ]

        elif performance == "Fair":

            recommendation = (
                "Your performance needs improvement. "
                "Review the course material and practise "
                "more quizzes."
            )

            recommended_courses = [
                "HTML & CSS Revision",
                "JavaScript Practice",
                "Database Fundamentals"
            ]

        elif performance == "AtRisk":

            recommendation = (
                "Your performance is at risk. "
                "Please revise the course material, "
                "retake quizzes and contact your instructor."
            )

            recommended_courses = [
                "HTML Revision",
                "Quiz Retake",
                "Contact Instructor"
            ]

        else:

            recommendation = (
                "Unable to determine performance."
            )

            recommended_courses = []

        # ====================================================
        # FINAL RESPONSE FOR REACT
        # ====================================================

        return jsonify({

            "status": "success",

            "performance": performance,

            "original_prediction": original_prediction,

            "recommendation": recommendation,

            "recommended_courses": recommended_courses,

            "probabilities": probabilities,

            # Activity statistics
            "visited_resources": visited_resources,

            "announcements_view": announcements_view,

            "discussion_count": discussion_count,

            "raised_hands": raised_hands,

            "login_count": login_count,

            # ML features
            "ml_features": input_data

        })

    except Exception as e:

        print("AI Prediction Error:", str(e))

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500

# -------------------------
# Admin Dashboard Statistics
# -------------------------
@app.route("/admin-dashboard", methods=["GET"])
def admin_dashboard():

    cur = mysql.connection.cursor()

    # Total Students
    cur.execute("SELECT COUNT(*) FROM student")
    total_students = cur.fetchone()[0]

    # Total Courses
    cur.execute("SELECT COUNT(*) FROM courses")
    total_courses = cur.fetchone()[0]

    # Total Quizzes
    cur.execute("SELECT COUNT(*) FROM quiz")
    total_quizzes = cur.fetchone()[0]

    # Total Questions
    cur.execute("SELECT COUNT(*) FROM questions")
    total_questions = cur.fetchone()[0]

    # Quiz Attempts
    cur.execute("SELECT COUNT(*) FROM results")
    total_attempts = cur.fetchone()[0]

    # AI Predictions
    cur.execute("SELECT COUNT(*) FROM student_activity")
    total_predictions = cur.fetchone()[0]

    cur.close()

    return jsonify({
        "students": total_students,
        "courses": total_courses,
        "quizzes": total_quizzes,
        "questions": total_questions,
        "attempts": total_attempts,
        "predictions": total_predictions
    })

# -------------------------
# AI Prediction Chart
# -------------------------

@app.route("/prediction-chart", methods=["GET"])
def prediction_chart():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            student_id,
            SUM(visited_resources),
            SUM(announcements_view),
            SUM(discussion_count),
            SUM(raised_hands),
            SUM(login_count)
        FROM student_activity
        GROUP BY student_id
    """)

    rows = cur.fetchall()
    cur.close()

    # UI performance categories
    result = {
        "Excellent": 0,
        "Good": 0,
        "Fair": 0,
        "AtRisk": 0
    }

    # OULAD target mapping
    target_mapping = {
        0: "Distinction",
        1: "Fail",
        2: "Pass",
        3: "Withdrawn"
    }

    # UI mapping
    result_mapping = {
        "Distinction": "Excellent",
        "Pass": "Good",
        "Fail": "Fair",
        "Withdrawn": "AtRisk"
    }

    for row in rows:

        visited_resources = row[1] or 0
        announcements_view = row[2] or 0
        discussion_count = row[3] or 0
        raised_hands = row[4] or 0
        login_count = row[5] or 0

        # --------------------------------
        # OULAD Feature Calculation
        # --------------------------------

        assessment_count = 0
        average_score = 0
        max_score = 0
        min_score = 0
        score_range = 0
        score_consistency = 0

        unregistered_count = 0
        ever_unregistered = 0

        performance_engagement = (
            visited_resources
            + announcements_view
            + discussion_count
            + raised_hands
            + login_count
        )

        vle_interactions = (
            visited_resources
            + discussion_count
            + announcements_view
        )

        unique_vle_resources = visited_resources

        if unique_vle_resources > 0:
            interactions_per_resource = (
                vle_interactions / unique_vle_resources
            )
        else:
            interactions_per_resource = 0

        average_weight = 1.0
        average_registration_date = 0

        if assessment_count > 0:
            unregistration_rate = (
                unregistered_count / assessment_count
            )
        else:
            unregistration_rate = 0

        # --------------------------------
        # Model Input - Exact 15 Features
        # --------------------------------

        input_data = pd.DataFrame([{
            "unregistration_rate": unregistration_rate,
            "average_score": average_score,
            "unregistered_count": unregistered_count,
            "assessment_count": assessment_count,
            "ever_unregistered": ever_unregistered,
            "performance_engagement": performance_engagement,
            "max_score": max_score,
            "min_score": min_score,
            "score_range": score_range,
            "vle_interactions": vle_interactions,
            "score_consistency": score_consistency,
            "average_weight": average_weight,
            "unique_vle_resources": unique_vle_resources,
            "interactions_per_resource": interactions_per_resource,
            "average_registration_date": average_registration_date
        }])

        # --------------------------------
        # Prediction
        # --------------------------------

        prediction = model.predict(input_data)

        predicted_class = int(prediction[0])

        # OULAD label
        original_performance = target_mapping[predicted_class]

        # LMS UI label
        performance = result_mapping[original_performance]

        # --------------------------------
        # Count Prediction
        # --------------------------------

        if performance in result:
            result[performance] += 1

    # --------------------------------
    # Chart Data
    # --------------------------------

    chart = [
        {
            "name": "Excellent",
            "value": result["Excellent"]
        },
        {
            "name": "Good",
            "value": result["Good"]
        },
        {
            "name": "Fair",
            "value": result["Fair"]
        },
        {
            "name": "AtRisk",
            "value": result["AtRisk"]
        }
    ]

    return jsonify(chart)





# -------------------------
# Reports Summary
# -------------------------

@app.route("/reports-summary", methods=["GET"])
def reports_summary():

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM student")
    students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM courses")
    courses = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM quiz")
    quizzes = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM results")
    attempts = cur.fetchone()[0]

    cur.execute("SELECT ROUND(AVG(score),2) FROM results")
    average_score = cur.fetchone()[0] or 0

    cur.execute("SELECT ROUND(AVG(percentage),2) FROM results")
    average_percentage = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM results WHERE status='Pass'")
    passed = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM results WHERE status='Fail'")
    failed = cur.fetchone()[0]

    cur.close()

    return jsonify({

        "students":students,
        "courses":courses,
        "quizzes":quizzes,
        "attempts":attempts,
        "average_score":average_score,
        "average_percentage":average_percentage,
        "passed":passed,
        "failed":failed

    })

# -------------------------
# Student Reports
# -------------------------

@app.route("/student-reports", methods=["GET"])
def student_reports():

    cur = mysql.connection.cursor()

    cur.execute("""

        SELECT

            s.student_id,
            s.name,
            s.email,

            q.title,

            r.score,
            r.percentage,
            r.status,
            r.attempts,
            r.time_spent

        FROM results r

        JOIN student s
            ON r.student_id=s.student_id

        JOIN quiz q
            ON r.quiz_id=q.quiz_id

        ORDER BY r.result_id DESC

    """)

    rows = cur.fetchall()

    cur.close()

    data=[]

    for row in rows:

        data.append({

            "student_id":row[0],
            "name":row[1],
            "email":row[2],
            "title":row[3],
            "score":row[4],
            "percentage":float(row[5]),
            "status":row[6],
            "attempts":row[7],
            "time_spent":row[8]

        })

    return jsonify(data)

# -------------------------
# Quiz Analytics
# -------------------------

@app.route("/quiz-analytics", methods=["GET"])
def quiz_analytics():

    cur = mysql.connection.cursor()

    cur.execute("SELECT IFNULL(AVG(score),0) FROM results")
    avg_score=float(cur.fetchone()[0])

    cur.execute("SELECT IFNULL(AVG(percentage),0) FROM results")
    avg_percentage=float(cur.fetchone()[0])

    cur.execute("SELECT COUNT(*) FROM results")
    attempts=cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM results WHERE status='Pass'")
    passed=cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM results WHERE status='Fail'")
    failed=cur.fetchone()[0]

    cur.close()

    return jsonify({

        "average_score":round(avg_score,2),
        "average_percentage":round(avg_percentage,2),
        "attempts":attempts,
        "passed":passed,
        "failed":failed

    })

#------------------------------------------AFTER EXCEL SHEET------------------------------------------------------



# -------------------------
# Run Flask
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)


