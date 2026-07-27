from flask import Flask, render_template, request, redirect
import joblib
import numpy as np

app = Flask(__name__)

# Load ML Model
model = joblib.load("employee_attrition_model.pkl")


# ---------------- Login Page ----------------
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login_page")
def login_page():
    return render_template("login.html")


# ---------------- Login Check ----------------
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "1234":
        return redirect("/home")
    else:
        return "Invalid Username or Password"


# ---------------- Home Page ----------------
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/dataset")
def dataset():
    return render_template("dataset.html")


# ---------------- About Page ----------------
@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- Prediction Page ----------------
@app.route("/predict_page")
def predict_page():
    return render_template("index.html")


# ---------------- Prediction ----------------
@app.route("/predict", methods=["POST"])
def predict():

    age = int(request.form["Age"])
    daily_rate = int(request.form["DailyRate"])
    distance = int(request.form["DistanceFromHome"])
    education = int(request.form["Education"])
    environment = int(request.form["EnvironmentSatisfaction"])
    hourly_rate = int(request.form["HourlyRate"])
    job_involvement = int(request.form["JobInvolvement"])
    job_level = int(request.form["JobLevel"])
    job_satisfaction = int(request.form["JobSatisfaction"])
    monthly_income = int(request.form["MonthlyIncome"])

    features = np.array([[
        age,
        daily_rate,
        distance,
        education,
        environment,
        hourly_rate,
        job_involvement,
        job_level,
        job_satisfaction,
        monthly_income
    ]])

    prediction = model.predict(features)

    # Prediction Result
    if prediction[0] == 1:

        result = "LEAVE"

        message = "The employee may leave the company."

        reasons = [
            "Low Job Satisfaction",
            "Long Distance From Home",
            "Low Employee Engagement"
        ]

        suggestions = [
            "Improve work-life balance",
            "Provide career growth opportunities",
            "Increase employee engagement"
        ]

    else:

        result = "STAY"

        message = "The employee is likely to stay in the company."

        reasons = [
            "Good Job Satisfaction",
            "Good Work Environment",
            "Stable Employee Performance"
        ]

        suggestions = [
            "Continue employee recognition",
            "Provide regular training",
            "Maintain a positive work environment"
        ]

    return render_template(
        "result.html",
        prediction=result,
        message=message,
        reasons=reasons,
        suggestions=suggestions
    )


# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)