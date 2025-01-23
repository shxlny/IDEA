document.addEventListener("DOMContentLoaded", function () {
    const nicknameField = document.querySelector('#nicknameField');
    const changeNicknameButton = document.querySelector('#changeNicknameButton');



    // Проверка подключения обработчика
    console.log("Script loaded and button ready.");
    // Обработчик кнопки
    changeNicknameButton.addEventListener('click', function () {
        const newNickname = nicknameField.value.trim(); // Получаем значение никнейма

        // Проверка на пустое значение
        if (!newNickname) {
            alert('Nickname cannot be empty!');
            return;
        }

        // Отправляем запрос на сервер
        fetch('/update_nickname/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),  // Получение CSRF токена
            },
            body: JSON.stringify({ nickname: newNickname })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Nickname updated successfully!');
                location.reload(); // Перезагрузка страницы для обновления никнейма
            } else {
                alert(`Failed to update nickname: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
/// Высвечивание ачивки при публикации
    const publishButton = document.getElementById("publishButton");
    const modal = document.getElementById("popupModal");
    const newbie = document.getElementById("Newbie")
    const closeButton = document.getElementById("x-button");

    let isModalShown = false;

    if (publishButton) {
        publishButton.addEventListener("click", (event) => {
            if (!isModalShown) {
                event.preventDefault();
                modal.classList.remove("hidden");
                newbie.classList.remove("hidden")
                isModalShown = true;

            }
        });
    }

    if (closeButton) {
        closeButton.addEventListener("click", () => {
            modal.classList.add("hidden");
        });
    }
});

// Получение CSRF токена из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



