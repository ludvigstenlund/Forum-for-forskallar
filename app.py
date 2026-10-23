from flask import Flask, session, render_template, redirect, url_for, request
import mysql.connector 


mydb = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="",  
    database="fff"  
)

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Används för sessionshantering


@app.route('/')
def index():
    if session.get('loggedin'): #kollar om någon är inloggad i sessionen
        # Anpassat innehåll för inloggad användare
        return render_template('home.html')
    else:
        return render_template('login.html', msg='DU MÅSTE LOGGA IN FÖR ÅTKOMST!') #variabeln msg används i html


@app.route('/append', methods=['POST']) #när man skickar in login
def append_login():
    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mydb.cursor(dictionary=True)

        cursor.execute('SELECT * FROM anvandare WHERE usern = %s AND pswrd = %s', (username, password))
        account = cursor.fetchone()

        cursor.close()

        if account:
            # 3. Spara data i sessionen vid lyckad inloggning
            session['loggedin'] = True #fint sätt att hålla reda på att jag är inloggad, hänvisas till när man går till huvudsidan
            session['epost'] = account['epost']
            session['id'] = account['id'] #Jämför ID i session med id i account (i SQL)
            session['username'] = account['usern'] #detsamma med namn och epost
            
            return redirect(url_for('index'))
        else:
            return render_template('login.html', msg='Användare med det lösenordet finns inte!')


@app.route('/logout')
def logout():
    session.clear()   # Tar bort ALLA sessionsvariabler = utloggad
    return redirect(url_for('index'))


@app.route('/session-info')
def session_info():
    return f"Session data: {dict(session)}"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')