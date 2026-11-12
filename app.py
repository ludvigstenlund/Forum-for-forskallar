from flask import Flask, session, render_template, redirect, url_for, request
import mysql.connector 


def get_db_connection(): #ansluter till databasen
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="",  
        database="fff"  #Forum För Fårskallar
    )


app = Flask(__name__)
app.secret_key = 'supersecretkey'

#---HOMEPAGE:----------------------------------------

@app.route('/')
def index():
    if not session.get('loggedin'):
        return render_template('login.html', msg='DU MÅSTE LOGGA IN FÖR ÅTKOMST!')

    db = get_db_connection()
    

    cursor_topics = db.cursor(dictionary=True)
    query_topics = """
        SELECT topic.id, topic.rubrik, anvandare.usern AS topic_skapare 
        FROM topic 
        LEFT JOIN anvandare ON topic.tradskapare = anvandare.id
        ORDER BY topic.skapad DESC
    """
    cursor_topics.execute(query_topics)
    alla_topics = cursor_topics.fetchall()
    cursor_topics.close()

    
    cursor_INLAGG = db.cursor(dictionary=True)
    query_INLAGG = """ 
        SELECT 
            inlagg.topic_id,
            inlagg.innehall, 
            inlagg.skapad, 
            anvandare.usern AS post_anvandare
        FROM inlagg 
        LEFT JOIN anvandare ON inlagg.anvandare_id = anvandare.id 
        ORDER BY inlagg.skapad DESC
    """
    cursor_INLAGG.execute(query_INLAGG)
    alla_inlagg = cursor_INLAGG.fetchall()
    cursor_INLAGG.close()
    db.close()



    for topic in alla_topics:

        topic['inlagg'] = [p for p in alla_inlagg if p['topic_id'] == topic['id']]

    return render_template('home.html', topics=alla_topics)
    
#---Profil:----------------------------------------

@app.route('/profil')
def profil():
    if not session.get('loggedin'):
       return render_template('login.html', msg='DU MÅSTE LOGGA IN FÖR ÅTKOMST!')
    return render_template('profil.html')

#---Skapa konto:----------------------------------------
        
@app.route('/skapa_konto', methods=['GET', 'Post'])
def skapa_konto():

    if request.form['NYTTusername'] != '' and request.form['NYTTpassword'] !='' and request.form['REGISTRERA_epost'] !='':
        db = get_db_connection()
        mycursor = db.cursor()
        sql = "INSERT INTO anvandare (usern, pswrd, epost) VALUES (%s, %s, %s)"
        val = (request.form['NYTTusername'], request.form['NYTTpassword'], request.form['REGISTRERA_epost'])
        mycursor.execute(sql, val)
        db.commit()
        return redirect(url_for('index'))
    else: 
        return render_template('login.html', msg="DU MÅSTE FYLLA I ALLA UPPGIFTER FÖR ATT SKAPA KONTO")

#---APPEND FORM FRÅN INLOGGNING:----------------------------------------

@app.route('/login', methods=['GET', 'Post'])
def append_login():
    if request.form['username'] != '' and request.form['password'] != '':
    
        username = request.form['username']
        password = request.form['password']

        # FIX: Använder get_db_connection() istället för mydb
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute('SELECT * FROM anvandare WHERE usern = %s AND pswrd = %s', (username, password))
        account = cursor.fetchone()

        cursor.close()
        db.close()

        if account:
            session['loggedin'] = True
            session['epost'] = account['epost']
            session['id'] = account['id']
            session['username'] = account['usern']
            
            return redirect(url_for('index'))
        else:
            return render_template('login.html', msg='Användare med det lösenordet finns inte!')
    else:
        return render_template('login.html', msg='Fyll i både användarnamn och lösenord!')
    
#---LOGOUT:----------------------------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#---INFO OM SESSIONEN:----------------------------------------

@app.route('/session-info')
def session_info():
    return f"Session data: {dict(session)}"

#---SKAPA EN TRÅD:----------------------------------------

@app.route('/skapa-trad', methods=['POST'])
def skapa_trad():
    if not session.get('loggedin'):
        return redirect(url_for('index'))
    
    trad_rubrik = request.form.get('trad_rubrik')
    anvandare_id = session.get('id')

    if trad_rubrik:
        # FIX: Använder get_db_connection() och db.commit()
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute(
                'INSERT INTO topic (rubrik, tradskapare) VALUES (%s, %s)', 
                (trad_rubrik, anvandare_id)
            )
            db.commit()
        except mysql.connector.Error as err:
            print(f"Fel: {err}")
        finally:
            cursor.close()
            db.close()

    return redirect(url_for('index'))


@app.route('/skapa-inlagg', methods=['POST'])
def skapa_inlagg():
    if not session.get('loggedin'):
        return redirect(url_for('index'))
    
    innehall = request.form.get('innehall')
    topic_id = request.form.get('topic_id')
    anvandare_id = session.get('id')

    if innehall and topic_id:
        # FIX: Använder get_db_connection() och db.commit()
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute(
                'INSERT INTO inlagg (anvandare_id, topic_id, innehall) VALUES (%s, %s, %s)', 
                (anvandare_id, topic_id, innehall)
            )
            db.commit()
        except mysql.connector.Error as err:
            print(f"Fel: {err}")
        finally:
            cursor.close()
            db.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
