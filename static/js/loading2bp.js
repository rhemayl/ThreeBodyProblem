let elapsedTime = 0;

function updateTimer() {
    elapsedTime++;
    document.getElementById('timer').textContent = `${elapsedTime} seconds`;
}

setInterval(updateTimer, 1000);

function checkVideo() {
    fetch("/check_video2bp")
        .then(response => response.json())
        .then(data => {
            if (data.ready) {
                window.location.href = "/result2bp";
            }
            else if (data.status === "Input parse error") {
                alert("ERROR: Please enter exactly 6 comma-separated numbers.");
                window.location.href = "/twobody";
            }
            else if (data.status === "Value error") {
                alert("ERROR: Values were calculated that were too large to handle. The system is too unstable with the given starting conditions; try smaller values.");
                window.location.href = "/twobody";
            }
            else if (data.status === "Error") {
                alert("ERROR: An unknown error occurred during the simulation. Please check your inputs and try again.");
                window.location.href = "/twobody";
            }
         });
}

setInterval(checkVideo, 1000);