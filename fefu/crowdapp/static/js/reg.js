function toind(){
    window.location.href = "{% url 'login' %}";
}

function main(){
    const menu = document.getElementById("Mobile");
    menu.classList.toggle("hidden");
}