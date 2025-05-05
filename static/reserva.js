// Configuración Firebase
const firebaseConfig = {
  "apiKey": "AIzaSyBkVk0eCUa8J5WrCnrOBnFTRweB7bvIIFk",
  "authDomain": "projectdemo-84e62.firebaseapp.com",
  "databaseURL": "https://projectdemo-84e62-default-rtdb.firebaseio.com",
  "projectId": "projectdemo-84e62",
  "storageBucket": "projectdemo-84e62.firebasestorage.app",
  "messagingSenderId": "1070071403822",
  "appId": "1:1070071403822:web:9599fa85942f7f7e55d6bf",
  "measurementId": "G-P40R9KPBEE"
  };
  
  // Inicializar Firebase
  firebase.initializeApp(firebaseConfig);
  const database = firebase.database();
  
  // Guardar reserva
  document.getElementById("reserva-form").addEventListener("submit", function(e) {
    e.preventDefault();
  
    const cliente = document.getElementById("cliente").value;
    const habitacion = document.getElementById("habitacion").value;
    const fecha = document.getElementById("fecha").value;
    const hora = document.getElementById("hora").value;
    const precio = document.getElementById("precio").value;

  
    const nuevaReservaRef = database.ref("reservas").push();
    nuevaReservaRef.set({
      cliente: cliente,
      habitacion: habitacion,
      fecha: fecha,
      hora: hora,
      precio: precio
    }).then(() => {
      alert("Reserva guardada correctamente");
      document.getElementById("reserva-form").reset();
      cargarReservas();
    }).catch((error) => {
      console.error("Error al guardar reserva:", error);
    });
  });
  
  // Cargar reservas existentes
  function cargarReservas() {
    const reservasList = document.getElementById("reservas-list");
    reservasList.innerHTML = ""; // limpiar lista
  
    database.ref("reservas").once("value", function(snapshot) {
      snapshot.forEach(function(childSnapshot) {
        const reserva = childSnapshot.val();
        const li = document.createElement("li");
        li.textContent = `Cliente: ${reserva.cliente} | Habitación: ${reserva.habitacion} | Fecha: ${reserva.fecha}`;
        reservasList.appendChild(li);
      });
    });
  }
  
  // Cargar al iniciar
  cargarReservas();
  