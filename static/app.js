const guess = document.querySelector("#guess");
const form = document.querySelector(".guessForm");
const formBtn = document.querySelector("#submitBtn");
const show_timer = document.querySelector("#timer");
const resetForm = document.querySelector(".resetForm");

let count = 60;
let timer_status = "deactive";

form.addEventListener("submit", function (e) {
  e.preventDefault();

  if (timer_status == "deactive") {
    const timer = setInterval(function () {
      count--;
      show_timer.innerText = count;

      if (count == 0) {
        formBtn.disabled = true;
        clearInterval(timer);
      }
    }, 1000);
  }

  timer_status = "active";

  axios
    .post("/handle-form", { guess: guess.value })
    .then((res) => {
      const data = res.data.result;
      const points = res.data.points;

      const points_h3 = document.querySelector("#points");

      points_h3.innerText = "Points: " + points;

      result = document.querySelector("#result");
      if (data == "ok") {
        result.innerText = "Correct!";
      } else if (data == "not-on-board") {
        result.innerText = "Word not on board";
      } else {
        result.innerText = "Not a valid word";
      }
    })
    .catch((error) => {
      console.log("Error fetching data", error);
    });
});

function update_highscore() {
  axios
    .get("/update-highscores")
    .then(function (res) {
      let data = res.data;

      let tBody = document.querySelector("#tableBody");

      tBody.innerHTML = "";

      for (const [game, point] of Object.entries(data).sort(
        ([, a], [, b]) => b - a
      )) {
        const newRow = document.createElement("tr");
        const gameCell = document.createElement("td");
        gameCell.innerText = game;
        const pointCell = document.createElement("td");
        pointCell.innerText = point;
        newRow.appendChild(gameCell);
        newRow.appendChild(pointCell);
        tBody.appendChild(newRow);
      }
    })
    .catch((err) => {
      console.error("Error fetching high scores:", err);
    });
}

update_highscore();
