document.addEventListener("DOMContentLoaded", function () {
    if (!quizData || quizData.length === 0) {
        console.error("Quiz data is empty or not available.");
        return;
    }

    console.log("Received Quiz Data:", quizData);

    const quizContainer = document.getElementById("quiz");
    const questionElement = document.getElementById("question");
    const answerElements = document.querySelectorAll(".answer");
    const a_text = document.getElementById("a_text");
    const b_text = document.getElementById("b_text");
    const c_text = document.getElementById("c_text");
    const d_text = document.getElementById("d_text");
    const submitButton = document.getElementById("submit");

    let currentQuiz = 0;
    let score = 0;

    const deselectAnswers = () => {
        answerElements.forEach(answer => answer.checked = false);
    };

    const getSelected = () => {
        let selectedAnswer = null;
        answerElements.forEach(answer => {
            if (answer.checked) selectedAnswer = answer.nextElementSibling.innerText;
        });
        return selectedAnswer;
    };

    const loadQuiz = () => {
        if (currentQuiz >= quizData.length) {
            let message = `<h2>You answered ${score}/${quizData.length} correctly!</h2>`;
            if (score === quizData.length) {
                message += `<p class="hidden-message-survived">Congratulations, player. You have survived.</p>`;
            } else if (score === 0) {
                message += `<p class="hidden-message-eliminated">You have been eliminated.</p>`;
            }
            message += `<button class="play-again-button" onclick="location.reload()">Play Again</button>`;
            quizContainer.innerHTML = message;
            return;
        }

        const currentQuizData = quizData[currentQuiz];
        questionElement.innerText = currentQuizData.question;
        a_text.innerText = currentQuizData.a;
        b_text.innerText = currentQuizData.b;
        c_text.innerText = currentQuizData.c;
        d_text.innerText = currentQuizData.d;
        deselectAnswers();
    };

    submitButton.addEventListener("click", () => {
        const selectedAnswer = getSelected();
        if (!selectedAnswer) return;

        if (selectedAnswer === quizData[currentQuiz].correct) {
            score++;
        }
        currentQuiz++;
        loadQuiz();
    });

    loadQuiz();
});