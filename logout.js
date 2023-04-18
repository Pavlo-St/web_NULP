document.querySelector('#logout1').onclick = function(event) {
    event.preventDefault();

    fetch('http://127.0.0.1:5000/user/logout', {
        method: 'POST',
      }).then(response => {
        if (response.ok) {
          localStorage.clear();
          window.location.reload(true);
          window.location.replace('/');
          window.location.href = 'index.html';
        }

    }).catch(error => console.error(error));

  }