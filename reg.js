document.querySelector('#regis').onclick = function(event) {
  event.preventDefault();


  const username = document.getElementById("username").value;
  const name = document.getElementById("name").value;
  const surname = document.getElementById("surname").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const confirm_password = document.getElementById("confirm_password").value;

  // Перевіряємо, що паролі співпадають
  if (password !== confirm_password) {
    alert("Паролі не співпадають!");
    return;
  }

  // Створюємо об'єкт з даними форми
  const formData = {
    Username: username,
    Name: name,
    Surname: surname,
    Email: email,
    Password: password
  };




function ajax(url, method, data, callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      callback(this.responseText);
    }
  };
  xhttp.open(method, url, true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(JSON.stringify(data));
}



ajax("http://127.0.0.1:5000/user/register", "POST", formData, function(response) {
  console.log(response);
})

}