const loginForm = document.querySelector('form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

loginForm.addEventListener('submit', (event) => {
    event.preventDefault();
    
    // Отримання значень введених користувачем
    const email = emailInput.value;
    const password = passwordInput.value;
    
    // Відправка POST-запиту на сервер
    axios.post('/login', {
        email: email,
        password: password
    })
    .then((response) => {
        // Обробка успішної відповіді сервера
        console.log(response.data);
        // Перенаправлення користувача на іншу сторінку
        window.location.href = 'index.html';
    })
    .catch((error) => {
        // Обробка помилки
        console.error(error);
        alert('Неправильна електронна пошта або пароль');
    });
});
