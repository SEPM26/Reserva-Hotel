from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase

app = Flask(__name__)
app.secret_key = 'clave-secreta-segura'  # Necesaria para manejar la sesión

# Configuración de Firebase
firebaseConfig = {
    "apiKey": "AIzaSyBkVk0eCUa8J5WrCnrOBnFTRweB7bvIIFk",
    "authDomain": "projectdemo-84e62.firebaseapp.com",
    "databaseURL": "https://projectdemo-84e62-default-rtdb.firebaseio.com",
    "projectId": "projectdemo-84e62",
    "storageBucket": "projectdemo-84e62.appspot.com",
    "messagingSenderId": "1070071403822",
    "appId": "1:1070071403822:web:9599fa85942f7f7e55d6bf",
    "measurementId": "G-P40R9KPBEE"
}

# Inicializar Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Página principal (login)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        uid = user['localId']
        session['user'] = email
        session['uid'] = uid

        # Obtener el rol desde Firebase Realtime Database
        user_data = db.child("usuarios").child(uid).get().val()

        if user_data and 'role' in user_data:
            role = user_data['role']
            session['role'] = role

            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif role == 'recepcionista':
                return redirect(url_for('recepcionista_dashboard'))
            else:
                return "Rol no válido", 403
        else:
            return "No se encontró el rol del usuario", 403

    except Exception as e:
        return f"Credenciales inválidas: {str(e)}"

# Dashboard para administrador
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' in session and session.get('role') == 'admin':
        # Obtener todas las reservas desde Firebase Realtime Database
        reservas = db.child("reservas").get().val()

        reservas_list = []  # Lista para almacenar las reservas
        if reservas:
            for reserva_id, reserva_data in reservas.items():
                reserva_data['id'] = reserva_id  # Agregar el ID de cada reserva
                reservas_list.append(reserva_data)
        
        return render_template('admin_dashboard.html', user=session['user'], reservas=reservas_list)
    
    return redirect(url_for('index'))

@app.route('/admin_reservas')
def admin_reservas():
    if 'user' in session and session.get('role') == 'admin':
        reservas = db.child("reservas").get().val()

        conteo_por_fecha = {}
        lista_reservas = []

        if reservas:
            for id_reserva, datos in reservas.items():
                datos['id'] = id_reserva
                lista_reservas.append(datos)
                fecha = datos.get("fecha")
                if fecha:
                    conteo_por_fecha[fecha] = conteo_por_fecha.get(fecha, 0) + 1

        return render_template('admin_reservas.html', reservas=lista_reservas, conteo_por_fecha=conteo_por_fecha)
    return redirect(url_for('index'))

# Dashboard para recepcionista
@app.route('/recepcionista_dashboard')
def recepcionista_dashboard():
    if 'user' in session and session.get('role') == 'recepcionista':
        return render_template('recepcionista_dashboard.html', user=session['user'])
    return redirect(url_for('index'))

# Página de reservas (solo recepcionista)
@app.route('/reservas')
def reservas():
    if 'user' in session and session.get('role') == 'recepcionista':
        return render_template('reservas.html', user=session['user'])
    return redirect(url_for('index'))

# Logout
@app.route('/logout')
def logout():
    session.clear()  # Limpiar la sesión
    auth.current_user = None  # Desloguear al usuario de Firebase
    return redirect(url_for('index'))  # Redirigir al login o página de inicio

# Protección de rutas privadas
@app.before_request
def proteger_rutas():
    # Lista de rutas públicas (sin sesión requerida)
    rutas_publicas = ['index', 'login', 'static']
    
    # Si el usuario no está logueado y está intentando acceder a una ruta privada
    if request.endpoint not in rutas_publicas and 'user' not in session:
        return redirect(url_for('index'))  # Redirigir a la página de login

# Deshabilitar caché de las páginas protegidas
@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)
