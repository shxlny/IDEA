function toind(){
    window.location.href = "{% url 'login' %}";
}

function main(){
    const menu = document.getElementById("Mobile");
    menu.classList.toggle("hidden");
}


document.addEventListener("DOMContentLoaded", function () {
        const passwordInput = document.getElementById("password");
        const passwordRepInput = document.getElementById("password_rep");
        const passwordError = document.getElementById("passwordError");
        const continueButton = document.getElementById("ContinueButton")


        console.log("Script loaded and button ready.");
        // Обработчик ввода в поле пароля

        let f1 = false;
        let f2 = false;
        passwordInput.addEventListener("input", function () {
            if (passwordInput.value.length < 8) {
                        passwordError.classList.remove("hidden");
                        passwordInput.classList.add("border-4");
                        passwordInput.style.borderColor = "red"; // Изменяем цвет границы
                        continueButton.classList.add("hidden");
                        f1 = false

            }
            else{
                f1 = true
                passwordInput.classList.remove("border-4");
            }

            if(f1 && f2){
                passwordError.classList.add("hidden");
                continueButton.classList.remove("hidden");
            }
            else{
                passwordError.classList.remove("hidden");
                continueButton.classList.add("hidden");
            }
        });

        passwordRepInput.addEventListener("input", function () {
            if (passwordRepInput.value.length < 8) {
                        passwordError.classList.remove("hidden");
                        passwordRepInput.classList.add("border-4");
                        passwordRepInput.style.borderColor = "red"; // Изменяем цвет границы
                        continueButton.classList.add("hidden");
                        f2 = false

            }
            else{
                f2 = true
                passwordRepInput.classList.remove("border-4");
            }

            if(f1 && f2){
                passwordError.classList.add("hidden");
                continueButton.classList.remove("hidden");
            }
            else{
                passwordError.classList.remove("hidden");
                continueButton.classList.add("hidden");
            }
        });


});