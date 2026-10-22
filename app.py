from flask import Flask, session, render_template, redirect, url_for, request, abort
import mysql.connector  # installera med "pip install mysql-connector-python" i kommandotolken

mydb = mysql.connector.connect(
  host="localhost",
  user="root",  # standardanvändarnamn för XAMPP
  password="",  # dito lösenord (en tom sträng)
  database="lektionsuppg10-16"  # byt namn om din databas heter något annat
)

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Används för sessionshantering

# Hårdkodade användare (i en riktig app: databas + hashade lösenord!)
USERS = {
    'Ludvig': {'password': 'najs',  'role': 'admin'},
    'Anton':   {'password': 'bajs',  'role': 'user'},
}

SAVEDOC = "EgnaProjekt/FormUppg/static/json/savedata.json" #snyggare än att skriva in hela sökvägen varje gång



@app.route('/')
def index():
    username = session.get('username')  # None om ingen är inloggad

    if username:
        # Anpassat innehåll för inloggad användare
        return render_template('home.html')
    else:
        return render_template('needtologin.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    # GET: visa formuläret
    return render_template('login.html')


@app.route('/append', methods=['POST']) #när man skickar in login
def append():
    username = request.form['username']
    password = request.form['password']

    user = USERS.get(username)
    if user and user['password'] == password:
        session['username'] = username   # <-- Här skapas sessionen!
        return redirect(url_for('index')) #index, eller '/' blir hänvisad till, alltså huvudsidan
    else:
        return 'Fel användarnamn eller lösenord. <a href="/login">Försök igen</a>'


@app.route('/profile')
def profile():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Inte inloggad – skicka till login

    return f'''
        <h1>Profil för {username}</h1>
        <p>Roll: {USERS[username]['role']}</p>
        <p><a href="/">Tillbaka</a></p>
    '''


@app.route('/logout')
def logout():
    session.clear()   # Tar bort ALLA sessionsvariabler = utloggad
    return redirect(url_for('index'))


@app.route('/session-info')
def session_info():
    return f"Session data: {dict(session)}"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


