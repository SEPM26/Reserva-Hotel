function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    firebase.auth().signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
        // Sesión iniciada
        document.getElementById("message").innerText = "Bienvenido " + email;
        // Opcional: redirigir a otra página
        window.location.href = "/home";
    })
    .catch((error) => {
        document.getElementById("message").innerText = error.message;
    });
}

function register() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    firebase.auth().createUserWithEmailAndPassword(email, password)
    .then((userCredential) => {
        document.getElementById("message").innerText = "Usuario registrado correctamente";
    })
    .catch((error) => {
        document.getElementById("message").innerText = error.message;
    });
}


  