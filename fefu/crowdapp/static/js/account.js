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
