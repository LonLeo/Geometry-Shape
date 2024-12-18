from flask import Flask, render_template, request, redirect, url_for, make_response
from owlready2 import *
import random

app = Flask(__name__)

# Load the ontology
onto = get_ontology("ontology/geoshape.owl").load()


# Routes
@app.route("/")
def index():
    triangle = onto.Triangle("triangle_formula")
    square = onto.Square("square_formula")
    rectangle = onto.Rectangle("rectangle_formula")
    if "name" in request.cookies:
        studnet_name = request.cookies.get("name")
        student = onto.Students(studnet_name)

        return render_template(
            "dashboard.html",
            triangle_area=triangle.area_of_triangle[0],
            square_area=square.area_of_square[0],
            rectangle_area=rectangle.area_of_rectangle[0],
            level=student.student_level[0],
        )
    else:
        return render_template("index.html")


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie("name", "", expires=0)  # Clear the 'name' cookie
    return resp


@app.route("/add", methods=["POST"])
def add_students():
    triangle = onto.Triangle("triangle_formula")
    square = onto.Square("square_formula")
    rectangle = onto.Rectangle("rectangle_formula")
    if request.method == "POST":
        resp = make_response(
            render_template(
                "dashboard.html",
                triangle_area=triangle.area_of_triangle[0],
                square_area=square.area_of_square[0],
                rectangle_area=rectangle.area_of_rectangle[0],
                cookies=request.cookies,
                level=1,
            )
        )

        # Saving new studnet in ontology
        studnet_name = request.form["name"]
        student = onto.Students(studnet_name)
        student.student_name.append(studnet_name)
        student.student_level.append(1)
        onto.save("ontology/geoshape.owl")

        # Saving in cookies
        resp.set_cookie("name", request.form["name"])
        return resp
    return redirect(url_for("index"))


@app.route("/take_test", methods=["GET", "POST"])
def take_test():
    studnet_name = request.cookies.get("name")
    if request.method == "POST":
        # POST request: Check correct answer and count it than redirect to result page
        submitted_answers = request.form.getlist("answers")
        correct_answers = request.form.getlist("correct_answers")
        correct_count = 0

        # Check answers
        for i in range(len(correct_answers)):
            if int(correct_answers[i]) == int(submitted_answers[i]):
                correct_count += 1

        return redirect(url_for("result", correct_count=correct_count))

    # GET request
    # Fetch studnet current level
    student = onto.Students(studnet_name)
    student_level = student.student_level[0]

    # Fetch list of question according to student level
    question_list = onto.Questions.instances()
    question_list_by_student_level = [
        q for q in question_list if q.question_level[0] == student_level
    ]

    # Randomized the question list and only pass 10 question to student
    randomized_question_list = random.sample(question_list_by_student_level, 10)

    return render_template("take_test.html", questions=randomized_question_list)


@app.route("/result")
def result():
    student_name = request.cookies.get("name")
    correct_count = int(request.args.get("correct_count", 0))
    color = "green"

    if correct_count < 5:
        color = "red"

    # Getting feedback from ontology
    if correct_count == 0:
        feedback = onto.Feedbacks("feedback_" + str(correct_count + 1))
    else:
        feedback = onto.Feedbacks("feedback_" + str(correct_count))

    feedback_message = feedback.feedback_message[0]

    # Save the result level to the ontology
    if correct_count >= 5:
        student = onto.Students(student_name)
        current_level = student.student_level[0]

        if current_level < 10:
            student.student_level.clear()
            student.student_level.append(current_level + 1)
            onto.save("ontology/geoshape.owl")
        else:
            feedback_message = "Congratulation! You reach Max Level :)"

    return render_template(
        "result.html",
        correct_count=correct_count,
        feedback=feedback_message,
        result_color=color,
    )


@app.route("/calculate", methods=["POST"])
def calculate_area():
    student_name = request.cookies.get("name")
    student = onto.Students(student_name)
    current_level = student.student_level[0]

    # Calculate area based on the shape and user input.
    shape = request.form.get("shape")
    result = None
    if shape == "square":
        side = float(request.form.get("side", 0))
        result = f"Area: {side ** 2} square units"

    elif shape == "triangle":
        base = float(request.form.get("base", 0))
        height = float(request.form.get("height", 0))
        result = f"Area: {0.5 * base * height} square units"

    elif shape == "rectangle":
        length = float(request.form.get("length", 0))
        width = float(request.form.get("width", 0))
        result = f"Area: {length * width} square units"

    return render_template(
        "dashboard.html", calculation_result=result, level=current_level
    )


if __name__ == "__main__":
    app.run(debug=True)
