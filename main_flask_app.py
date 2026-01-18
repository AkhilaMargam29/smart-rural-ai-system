from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def signup():                  # Default is signup
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/home", methods=["POST"])
def home():
    return render_template("home.html")


# STREAMLIT REDIRECT ROUTES
@app.route("/open/crop")
def open_crop():
    return redirect("http://localhost:8501/?page=crop")

@app.route("/open/pest")
def open_pest():
    return redirect("http://localhost:8501/?page=pest")

@app.route("/open/water")
def open_water():
    return redirect("http://localhost:8501/?page=water")

@app.route("/open/market")
def open_market():
    return redirect("http://localhost:8501/?page=market")

@app.route("/open/chatbot")
def open_chatbot():
    return redirect("http://localhost:8501/?page=chatbot")

@app.route("/open/grievance")
def open_grievance():
    return redirect("http://localhost:8501/?page=grievance")

if __name__ == "__main__":
    app.run(debug=True)
