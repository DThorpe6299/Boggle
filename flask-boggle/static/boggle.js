document.addEventListener("DOMContentLoaded", function () {
    let guessForm = document.getElementById("guess-form");
    let guessInput = document.getElementById("guess-input");
    let resultElement = document.getElementById("result");
    let scoreElement = document.getElementById("score");
    let timerElement = document.getElementById("timer");
    let gameOverElement = document.getElementById("game-over");
    
    let score = 0;
    let secondsRemaining = 60;
    let isGameRunning = true;

    let guessedWords = [];



    function updateTimer() {
        timerElement.textContent = "Time remaining: " + secondsRemaining + " seconds";
    }

    let timer = setInterval(function () {
        secondsRemaining--;

        if (secondsRemaining <= 0) {
            clearInterval(timer);
            isGameRunning = false;
            guessForm.style.display = "none";
            gameOverElement.style.display = "block";

            axios.post("/end-game", { score: score })
            .then(function (response) {
                console.log("Game ended. Server response:", response.data);
            })
    }
    updateTimer();
    }, 1000);


    guessForm.addEventListener("submit", function (event) {
        event.preventDefault();

        if (!isGameRunning) {
            return;
        }

        let guess = guessInput.value;

        if (guessedWords.includes(guess)) {
            resultElement.textContent = "You already guessed this word.";
        } else {
            guessedWords.push(guess);

        axios.post("/check-word", { word: guess })
            .then(function (response) {
                let result = response.data.result;

                if (result === "ok") {
                    score += guess.length;
                    scoreElement.textContent = "Score: " + score;
                    resultElement.textContent = "Your guess is valid and exists on the board.";
                } else if (result === "not-on-board") {
                    resultElement.textContent = "Your guess is invalid (not on the board).";
                } else if (result === "not-a-word") {
                    resultElement.textContent = "Your guess is not a valid word.";
                }
            })
        })
    })
