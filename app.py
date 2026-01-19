from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-simulation", methods=["POST"])

def run_simulation():
    from three_body_simulation import threebp 
    message = threebp()
    return render_template("index.html", message=message, video_url="/static/video/ThreeBodyProblem.mp4")

if __name__ == "__main__":
    app.run(debug=True)