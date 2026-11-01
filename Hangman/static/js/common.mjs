const sounds = {
  correct: new Audio("/static/sounds/correct.mp3"),
  wrong: new Audio("/static/sounds/wrong.mp3"),
  lose: new Audio("/static/sounds/lose.mp3"),
  win: new Audio("/static/sounds/win.mp3")
}



export function createDropDown() {
    var dropdownControllers = document.getElementsByClassName("dropdownControl");
    var count;

    for (count = 0; count < dropdownControllers.length; count++) {
        dropdownControllers[count].addEventListener("click", function() {
            this.classList.toggle("open");

            var dropDown = this.nextElementSibling;
            dropDown.classList.toggle("open")
            if (dropDown.style.maxHeight){
                dropDown.style.maxHeight = null;
            } else {
                dropDown.style.maxHeight = dropDown.scrollHeight + "px";
            }
        });
    }
}

function playSound(name) {
    Object.values(sounds).forEach(sound => {
        sound.pause();
        sound.currentTime = 0;
    });
    sounds[name].play();
}

export function gameHandler() {
    document.addEventListener("click", async (event) => {
        const button = event.target.closest(".button");
        if (!button) return;

            button.disabled = true;

        const response = await fetch("/Game", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ letter: button.dataset.char }),
        });

        const data = await response.json();
        document.getElementById("message").textContent = data.message;

        if (data.lifeCount !== undefined) {
        const hearts = document.querySelectorAll(".heart");
        hearts.forEach((heart, i) => {
            if (i >= data.lifeCount) {
            heart.src = "/static/images/heart_broken.png";
            }
        })};

        if (data.positions) {
            const letters = document.querySelectorAll(".letter");
            data.positions.forEach(pos => {
            letters[pos].textContent = data.char;
            });
        } 

        if (data.gameOver) {
            playSound("lose");
            document.querySelectorAll(".button").forEach(b => b.disabled = true);
        } else if (data.positions) {
            playSound("correct");
        } else if (data.lifeCount !== undefined) {
            playSound("wrong");
        }

        if (data.won) {
            playSound("win");
            document.querySelectorAll(".button").forEach(b => b.disabled = true);
        }
    });
}