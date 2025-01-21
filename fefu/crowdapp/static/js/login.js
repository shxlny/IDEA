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