from flask import Flask, session, render_template, redirect, url_for, request
import mysql.connector 


def get_db_connection(): #ansluter till databasen
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="",  
        database="fff"  #Forum För Fårskallar
    )

tradskapare = "testar"
app = Flask(__name__)
app.secret_key = 'supersecretkey'


@app.route('/')
def index():
    if session.get('loggedin'):
        db = get_db_connection()
        
        
        cursor_topics = db.cursor(dictionary=True)
        query_topics = """
            SELECT topic.id, topic.rubrik, anvandare.usern AS topic_skapare 
            FROM topic 
            LEFT JOIN anvandare ON topic.tradskapare = anvandare.id
        """
        cursor_topics.execute(query_topics)
        alla_topics = cursor_topics.fetchall()
        cursor_topics.close()

        
        cursor_posts = db.cursor(dictionary=True)
        query_posts = """ 
            SELECT 
                inlagg.topic_id,
                inlagg.innehall, 
                inlagg.skapad, 
                anvandare.usern AS post_anvandare
            FROM inlagg 
            LEFT JOIN anvandare ON inlagg.anvandare_id = anvandare.id 
            ORDER BY inlagg.skapad DESC
        """
        cursor_posts.execute(query_posts)
        alla_inlagg = cursor_posts.fetchall()
        cursor_posts.close()
        db.close()



        for topic in alla_topics:

            topic['inlagg'] = [p for p in alla_inlagg if p['topic_id'] == topic['id']]

        return render_template('home.html', topics=alla_topics)
    else:
        return render_template('login.html', msg='DU MÅSTE LOGGA IN FÖR ÅTKOMST!')



@app.route('/append', methods=['POST'])
def append_login():
    if 'username' in request.form and 'password' in request.form:
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
    


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/session-info')
def session_info():
    return f"Session data: {dict(session)}"


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
