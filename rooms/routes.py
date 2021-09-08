from application import app, mydb
from flask import render_template, redirect, request, session
import json, random, math

mycursor = mydb.cursor(buffered=True)
mc = mydb.cursor()

@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    x = "SELECT DISTINCT grade, COUNT(*) AS total FROM kanji_app_db.kanji_dict GROUP BY grade"
    mycursor.execute(x)
    myresult = mycursor.fetchall()
    kanjinumber = sum(i[1] for i in myresult)
    if request.method == 'POST':
        session['grades'] = request.form.getlist('grades')
    return render_template("index.html", nav_index="active", myresult=myresult, kanjinumber=kanjinumber)

@app.route("/practice")
def practice():
    if 'grades' in session:
        grades = session['grades']
    else:
        grades=[1]
    b = "SELECT * FROM kanji_app_db.kanji_dict WHERE "
    for i in grades:
        b += "grade = " + str(i) + " OR "
    b = b[:-3]
    mycursor.execute(b)
    mykanji = mycursor.fetchall()
    jkanji = json.dumps(mykanji)
    introkanji = mykanji[0]
    return render_template("practice.html", nav_practice="active", mykanji=jkanji, introkanji=introkanji)

@app.route("/quiz")
@app.route("/quiz/<timer>")
def quiz(timer=7):
    if 'grades' in session and session['grades']!=[]:
        grades = session['grades']
    else:
        grades=[1]
    print (grades)
    newsql = "SELECT * FROM kanji_dict WHERE "
    for i in grades:
        newsql += " grade = " + str(i)
        if i != grades[len(grades)-1]:
            newsql += " OR "
    x = newsql.replace("*", "count(*)")
    print(x)
    mycursor.execute(x)
    quiz_kanji = mycursor.fetchone()
    kanji_id = math.floor(random.random()*quiz_kanji[0])
    sql = "SELECT * FROM kanji_dict WHERE idkanji_dict = " + str(kanji_id)
    mycursor.execute(sql)
    quiz_kanji = mycursor.fetchone()
    return render_template("quiz.html", nav_quiz="active", quiz_kanji=quiz_kanji, timer=timer)

@app.route("/about")
def about():
    return render_template("about.html", nav_about="active")

@app.route("/remember_kanji")
def remember_kanji():
    print("********")
    print("remember kanji")
    return render_template("about.html", nav_about="active")

@app.route("/test")
def test():
    x = "SELECT DISTINCT grade, COUNT(*) AS total FROM kanji_app_db.kanji_dict GROUP BY grade"
    if 'grades' in session:
        grades = session['grades']
    else:
        grades=[1]
    b = "SELECT * FROM kanji_app_db.kanji_dict WHERE "
    for i in test_list:
        b += "grade = " + str(i) + " OR "
    b = b[:-3]
    b += "ORDER BY RAND() LIMIT 1;"
    mycursor.execute(b)
    test_data = mycursor.fetchall()
    return render_template("test.html", test_data=test_data, grades = grades)

@app.route("/linked")
def linked():
    return redirect("/test")