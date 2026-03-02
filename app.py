from flask import Flask, render_template, request, send_file
import os
import time
import multiprocessing

app = Flask(__name__)
video_path_3bp = "static/video/NewThreeBodyProblem.mp4"
video_path_2bp = "static/video/TwoBodyProblem.mp4"
flag_path = "static/video/done.flag"

# Global thread tracking to prevent file lock conflicts
current_threads = {
    "3bp": None,
    "2bp": None
}


def safe_remove_file(file_path, timeout=5):
    """Try to remove a file with retry logic to handle locked files."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except PermissionError:
            time.sleep(0.5)  # Wait and retry
    return False


@app.route("/")
def home():
    return render_template("index.html")


def generate_video(position, velocity, mass1, mass2, mass3, video_path):
    from three_body_simulation import threebp 
    threebp(position, velocity, mass1, mass2, mass3, video_path)
    with open(flag_path, "w") as f:
        f.write("done")

def generate_videotbp(position, velocity, mass1, mass2, video_path):
    from two_body_simulation import twobp 
    twobp(position, velocity, mass1, mass2, video_path)
    with open(flag_path, "w") as f:
        f.write("done")

@app.route("/run-simulation3bp", methods=["POST"])
def run_simulation3bp():
    position = request.form.get("position")
    velocity = request.form.get("velocity")
    mass1 = request.form.get("mass1")
    mass2 = request.form.get("mass2")
    mass3 = request.form.get("mass3")

    # Terminate previous process if still running
    if current_threads["3bp"] and current_threads["3bp"].is_alive():
        current_threads["3bp"].terminate()
        current_threads["3bp"].join(timeout=1)

    # Clean up files
    safe_remove_file(video_path_3bp)
    safe_remove_file(flag_path)

    process = multiprocessing.Process(
        target=generate_video,
        args=(position, velocity, mass1, mass2, mass3, video_path_3bp)
    )
    process.start()
    current_threads["3bp"] = process
    
    return render_template("loading3bp.html")

@app.route("/run-simulation2bp", methods=["POST"])
def run_simulation2bp():
    position = request.form.get("position")
    velocity = request.form.get("velocity")
    mass1 = request.form.get("mass1")
    mass2 = request.form.get("mass2")

    # Terminate previous process if still running
    if current_threads["2bp"] and current_threads["2bp"].is_alive():
        current_threads["2bp"].terminate()
        current_threads["2bp"].join(timeout=1)

    # Clean up files
    safe_remove_file(video_path_2bp)
    safe_remove_file(flag_path)

    process = multiprocessing.Process(
        target=generate_videotbp,
        args=(position, velocity, mass1, mass2, video_path_2bp)
    )
    process.start()
    current_threads["2bp"] = process
    
    return render_template("loading2bp.html")

@app.route("/threebody")
def threebody():
    return render_template("index.html")

@app.route("/twobody")
def twobody():
    return render_template("tbp.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/check_video3bp")
def check_video3bp():
    return {"ready": os.path.exists(flag_path) and os.path.exists(video_path_3bp)
}

@app.route("/check_video2bp")
def check_video2bp():
    return {"ready": os.path.exists(flag_path) and os.path.exists(video_path_2bp)
}

@app.route("/result3bp")
def result3bp():
    return render_template(
        "index.html",
        video_url=video_path_3bp,
        cache_bust=time.time())

@app.route("/result2bp")
def result2bp():
    return render_template(
        "tbp.html",
        video_url=video_path_2bp,
        cache_bust=time.time())

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)