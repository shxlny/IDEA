function main(){
    const menu = document.getElementById("Mobile");
    menu.classList.toggle("hidden");
}

function acc(){
    const menu = document.getElementById("acc");
    menu.classList.toggle("hidden");
}

function to_com(  ){
    window.location.href = "{% url 'Comments' %}";
}
