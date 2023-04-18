document.querySelector('#loginis').onclick = function(event) {
    event.preventDefault();
  
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const role = "user";

    fetch('http://127.0.0.1:5000/user/login', {
        method: 'POST',
        headers: {
          'Authorization': 'Basic ' + btoa(username + ':' + password)
        }
      }).then(response => {
        if (response.ok) {
          localStorage.setItem('username', username)
          localStorage.setItem('password', password)
          localStorage.setItem('role', role)
          window.location.href = './index.html';
        }
        else if (response.status === 401) {
            alert("Wrong credentials!");
            return;
        }
    }).catch(error => console.error(error));

  }