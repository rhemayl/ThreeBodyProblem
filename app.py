from flask import Flask, render_template, request, send_file
import os
import time
import threading

app = Flask(__name__)
video_path = "static/video/NewThreeBodyProblem.mp4"
flag_path = "static/video/done.flag"


@app.route("/")
def home():
    return render_template("index.html")


def generate_video(position, velocity, mass1, mass2, mass3, video_path):
    from three_body_simulation import threebp 
    threebp(position, velocity, mass1, mass2, mass3, video_path)
    with open(flag_path, "w") as f:
        f.write("done")


@app.route("/run-simulation", methods=["POST"])
def run_simulation():
    position = request.form.get("position")
    velocity = request.form.get("velocity")
    mass1 = request.form.get("mass1")
    mass2 = request.form.get("mass2")
    mass3 = request.form.get("mass3")


    if os.path.exists(video_path):
        os.remove(video_path)

    if os.path.exists(flag_path):
        os.remove(flag_path)

    thread = threading.Thread(
        target=generate_video,
        args=(position, velocity, mass1, mass2, mass3, video_path)
    )
    thread.start()
    
    return render_template("loading.html")


@app.route("/check_video")
def check_video():
    return {"ready": os.path.exists(flag_path) and os.path.exists(video_path)
}

@app.route("/result")
def result():
    return render_template(
        "index.html",
        video_url=video_path,
        cache_bust=time.time())


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)