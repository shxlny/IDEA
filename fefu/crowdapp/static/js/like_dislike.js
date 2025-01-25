function likeIdea(ideaId) {
    console.log("Like button clicked for idea:", ideaId); // Лог клика по лайку
    fetch(`/like/${ideaId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .then(response => {
        console.log("Response status:", response.status); // Лог статуса ответа
        return response.json();
    })
    .then(data => {
        console.log("Response data:", data); // Лог данных ответа
        if (data.success) {
            // Обновляем текст лайков и дизлайков
            document.getElementById(`likes-${ideaId}`).textContent = data.likes;
            document.getElementById(`dislikes-${ideaId}`).textContent = data.dislikes;

            // Лог обновления текста
            console.log(`Likes updated to: ${data.likes}`);
            console.log(`Dislikes updated to: ${data.dislikes}`);

            // Меняем цвет кнопок
            const likeBtn = document.getElementById(`like-btn-${ideaId}`);
            const dislikeBtn = document.getElementById(`dislike-btn-${ideaId}`);

            console.log("Like Button Element:", likeBtn); // Лог кнопки лайка
            console.log("Dislike Button Element:", dislikeBtn); // Лог кнопки дизлайка

            // Добавляем зеленую подсветку для лайка
            likeBtn.classList.add('bg-green-200');
            likeBtn.classList.remove('border-[#F17E34]'); // Убираем стандартную рамку

            // Возвращаем стандартный стиль для дизлайка
            dislikeBtn.classList.remove('bg-red-200');
            dislikeBtn.classList.add('border-[#F17E34]');
        } else {
            console.error("Error from server:", data.error);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        alert("Something went wrong.");
    });
}

function dislikeIdea(ideaId) {
    console.log("Dislike button clicked for idea:", ideaId); // Лог клика по дизлайку
    fetch(`/dislike/${ideaId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .then(response => {
        console.log("Response status:", response.status); // Лог статуса ответа
        return response.json();
    })
    .then(data => {
        console.log("Response data:", data); // Лог данных ответа
        if (data.success) {
            // Обновляем текст лайков и дизлайков
            document.getElementById(`likes-${ideaId}`).textContent = data.likes;
            document.getElementById(`dislikes-${ideaId}`).textContent = data.dislikes;

            // Лог обновления текста
            console.log(`Likes updated to: ${data.likes}`);
            console.log(`Dislikes updated to: ${data.dislikes}`);

            // Меняем цвет кнопок
            const likeBtn = document.getElementById(`like-btn-${ ideaId }`);
            const dislikeBtn = document.getElementById(`dislike-btn-${ideaId}`);

            console.log("Like Button Element:", likeBtn); // Лог кнопки лайка
            console.log("Dislike Button Element:", dislikeBtn); // Лог кнопки дизлайка

            // Добавляем красную подсветку для дизлайка
            dislikeBtn.classList.add('bg-red-200');
            dislikeBtn.classList.remove('border-[#F17E34]'); // Убираем стандартную рамку

            // Возвращаем стандартный стиль для лайка
            likeBtn.classList.remove('bg-green-200');
            likeBtn.classList.add('border-[#F17E34]');
        } else {
            console.error("Error from server:", data.error);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        alert("Something went wrong.");
    });
}

function getCookie(name) {
    console.log("Getting cookie for:", name); // Лог получения cookie
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                console.log("Cookie found:", cookieValue); // Лог значения cookie
                break;
            }
        }
    }
    if (!cookieValue) {
        console.error("Cookie not found for:", name); // Лог ошибки, если cookie не найден
    }
    return cookieValue;
}
