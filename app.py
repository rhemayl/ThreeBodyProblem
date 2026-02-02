from flask import Flask, render_template, request, send_file
import os
import time
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-simulation", methods=["POST"])


def run_simulation():
    position = request.form.get("position")
    velocity = request.form.get("velocity")
    mass1 = request.form.get("mass1")
    mass2 = request.form.get("mass2")
    mass3 = request.form.get("mass3")
    from three_body_simulation import threebp 
    video_path = "static/video/NewThreeBodyProblem.mp4"
    message = threebp(position, velocity, mass1, mass2, mass3, output_path=video_path)
    print(f"DEBUG: Video exists? {os.path.exists(video_path)}")
    return render_template(
        "index.html",
        message=message,
        video_url=video_path,
        cache_bust=time.time()
    )

if __name__ == "__main__":
    app.run(debug=True)