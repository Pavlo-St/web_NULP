document.querySelector('#resis').onclick = function(event) {
    event.preventDefault();
  
  
    const room = document.getElementById("room").value;
    const date = document.getElementById("date").value;
    const start_time = document.getElementById("start_time").value;
    const end_time = document.getElementById("end_time").value;
  

  
    // Створюємо об'єкт з даними форми
    const formData = {
        ReservationId : getRandomInt(10000),
        BeginTime : date,
        EndTime : date,
        UserId : currentUser.UserId,
        RoomId : room
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
  
  
  
  ajax("http://127.0.0.1:5000/reservation/create", "POST", formData, function(response) {
    console.log(response);
  })
  
  }


function addRow() {
    var table = document.getElementById("table");
    var row = table.rows.length;

  

    let date = document.getElementById("date").value;
    let start_date = document.getElementById("start_time").value;
    let end_date = document.getElementById("end_time").value;
    let room = document.getElementById("room").value;

  
  
    //console.log("Student added: " + student.id + ". " + student.group + ", " + student.getName() + ", " + student.gender + ", " + student.birthday);
  

    var cell1 = table.insertRow(-1).insertCell(0);
    var cell2 = table.rows[row].insertCell(1);
    var cell3 = table.rows[row].insertCell(2);
    var cell4 = table.rows[row].insertCell(3);
    var cell5 = table.rows[row].insertCell(4);

    cell1.innerHTML = room;
    cell2.innerHTML = date;
    cell3.innerHTML = start_date;
    cell4.innerHTML = end_date;
   
  }