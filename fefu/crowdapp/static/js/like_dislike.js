function likeIdea(ideaId) {
    fetch(`/like/${ideaId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Функция получения CSRF-токена
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`likes-${ideaId}`).textContent = data.likes;
            document.getElementById(`dislikes-${ideaId}`).textContent = data.dislikes;
        } else {
            console.error("Error:", data.error);
            alert(data.error || "An error occurred.");
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        alert("Something went wrong.");
    });
}

function dislikeIdea(ideaId) {
    fetch(`/dislike/${ideaId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Замените на вашу функцию для получения CSRF токена
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`likes-${ideaId}`).textContent = data.likes;
            document.getElementById(`dislikes-${ideaId}`).textContent = data.dislikes;
        } else {
            console.error("Error:", data.error);
            alert(data.error || "An error occurred.");
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        alert("Something went wrong.");
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, совпадает ли имя cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}