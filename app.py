from flask import Flask, render_template, request, send_file
import os
import time

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-simulation", methods=["POST"])


def run_simulation():
    values = request.form.get("values")
    from three_body_simulation import threebp 
    message = threebp(values)
    return render_template("index.html", message=message, video_url="/static/video/NewThreeBodyProblem.mp4", cache_bust=time.time())

if __name__ == "__main__":
    app.run(debug=True)