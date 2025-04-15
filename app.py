from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase

app = Flask(__name__)
app.secret_key = 'clave-secreta-segura'  # necesaria para manejar la sesión

# Configuración Firebase
firebaseConfig = {
  "apiKey": "AIzaSyBkVk0eCUa8J5WrCnrOBnFTRweB7bvIIFk",
  "authDomain": "projectdemo-84e62.firebaseapp.com",
  "databaseURL": "https://projectdemo-84e62-default-rtdb.firebaseio.com",
  "projectId": "projectdemo-84e62",
  "storageBucket": "projectdemo-84e62.firebasestorage.app",
  "messagingSenderId": "1070071403822",
  "appId": "1:1070071403822:web:9599fa85942f7f7e55d6bf",
  "measurementId": "G-P40R9KPBEE"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('index'))
        except:
            return "Error al registrar usuario"
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session['user'] = email
        return redirect(url_for('dashboard'))
    except:
        return "Credenciales inválidas"

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    else:
        return redirect(url_for('index'))

@app.route('/reservas')
def reservas():
    if 'user' in session:
        return render_template('reservas.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Eliminar la sesión de Flask
    session.pop('user', None)
    
    # Opcional: cerrar la sesión de Firebase (si es necesario)
    auth.current_user = None  # Esto cerrará la sesión activa en Firebase
    
    # Redirigir al usuario a la página de inicio
    return redirect(url_for('index'))

@app.before_request
def proteger_rutas():
    rutas_publicas = ['index', 'register', 'login', 'static','reservas', 'dashboard']
    if request.endpoint not in rutas_publicas and 'user' not in session:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)