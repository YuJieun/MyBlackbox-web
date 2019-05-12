// Get elements
const player = document.querySelector(".player");
const video = player.querySelector(".viewer");
const progress = player.querySelector(".progress");
const progressBar = player.querySelector(".progress__filled");
const toggle = player.querySelector(".toggle");
const skipButtons = player.querySelectorAll("[data-skip]");
const ranges = player.querySelectorAll(".player__slider");

// Toggle the video between played and pause
function togglePlay() {
  const videoPlayPause = video.paused ? "play" : "pause";
  video[videoPlayPause]();
}

// Switch the icons depending on the videos state
function updateButton() {
  const icon = this.paused ? "►" : "❚ ❚";
  toggle.textContent = icon;
}

function skip() {
  video.currentTime += parseFloat(this.dataset.skip);
}

function handleRangeUpdate() {
  video[this.name] = this.value;
}

function handleProgress() {
  const percent = (video.currentTime / video.duration) * 100;
  progressBar.style.flexBasis = `${percent}%`;
}

function scrub(e) {
  const scrubTime = (e.offsetX / progress.offsetWidth) * video.duration;
  video.currentTime = scrubTime;
}

// When the video is clicked or the play button is pressed
// play the video
video.addEventListener("click", togglePlay);
toggle.addEventListener("click", togglePlay);

// When the video is playing, show a pause icon (updateButton)
// When the video is paused, show a play icon (updateButton)
video.addEventListener("play", updateButton);
video.addEventListener("pause", updateButton);

// Skip buttons
skipButtons.forEach(button => button.addEventListener("click", skip));

// Range sliders
ranges.forEach(range => range.addEventListener("change", handleRangeUpdate));

// Progress bar
video.addEventListener("timeupdate", handleProgress);
progress.addEventListener("click", scrub);

let mousedown = false;
progress.addEventListener("mousemove", e => mousedown && scrub(e));
progress.addEventListener("mousedown", () => (mousedown = true));
progress.addEventListener("mouseup", () => (mousedown = false));