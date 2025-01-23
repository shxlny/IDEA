// function handleLogin() {
//     localStorage.setItem("isLoggedIn", "true");
//     window.location.href = "index.html";
// }

// function main(){
//     const menu = document.getElementById("Mobile");
//     menu.classList.toggle("hidden");
// }

function tomain(  ){
    window.location.href = "{% url 'main' %}";
}

function main(){
    const menu = document.getElementById("Mobile");
    menu.classList.toggle("hidden");
}

document.addEventListener("DOMContentLoaded", function () {
        const passwordInput = document.getElementById("password");
        const passwordError = document.getElementById("passwordError");
        const continueButton = document.getElementById("ContinueButton")

        console.log("Script loaded and button ready.");
        // Обработчик ввода в поле пароля
        passwordInput.addEventListener("input", function () {
            if (passwordInput.value.length < 8) {
                // Показываем сообщение об ошибке
                passwordError.classList.remove("hidden");
                passwordInput.classList.add("border-4")
                passwordInput.style.borderColor = "red"; // Изменяем цвет границы
                continueButton.classList.add("hidden")

            } else {
                // Скрываем сообщение об ошибке
                passwordError.classList.add("hidden");
                passwordInput.style.borderColor = "#B1C0E5"; // Возвращаем цвет границы
                passwordInput.classList.remove("border-4")
                continueButton.classList.remove("hidden")
            }
        });
});