function checkVideo() {
    fetch("/check_video2bp")
        .then(response => response.json())
        .then(data => {
            if (data.ready) {
                window.location.href = "/result2bp";
            }
         });
}

setInterval(checkVideo, 1000);