function checkVideo() {
    fetch("/check_video")
        .then(response => response.json())
        .then(data => {
            if (data.ready) {
                window.location.href = "/result";
            }
         });
}

setInterval(checkVideo, 1000);