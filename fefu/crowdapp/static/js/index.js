function main(){
    const menu = document.getElementById("Mobile");
    menu.classList.toggle("hidden");
}




// document.addEventListener("DOMContentLoaded", () => {
//     // Проверяем, есть ли состояние isLoggedIn в localStorage
//     const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

//     // Получаем элементы Log in и фото
//     const loginElement = document.getElementById("Login");
//     const photoElement = document.getElementById("photo");

//     if (isLoggedIn) {
//         // Скрываем "Log in" и показываем фото
//         if (loginElement) loginElement.classList.add("hidden");
//         if (photoElement) photoElement.classList.remove("hidden");
//     } else {
//         // Показываем "Log in" и скрываем фото
//         if (loginElement) loginElement.classList.remove("hidden");
//         if (photoElement) photoElement.classList.add("hidden");
//     }
// });

// function handleLogout() {
//     localStorage.removeItem("isLoggedIn");
//     window.location.reload();
// }