function checkVideo() {
    fetch("/check_video3bp")
        .then(response => response.json())
        .then(data => {
            if (data.ready) {
                window.location.href = "/result3bp";
            }
         });
}

setInterval(checkVideo, 1000);