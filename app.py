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

@app.route('/') # huvudsida
def homepage(): #definerar funktionen homepage
    if not session.get('loggedin'): #kollar om det inte finns en session
        return render_template('login.html', msg='DU MÅSTE LOGGA IN FÖR ÅTKOMST!') #tvingar då till inloggning

    #om det finns en aktiv session:
    db = get_db_connection() #skapa en länk till databasen
    

    cursor_topics = db.cursor(dictionary=True)
    #SQL kommando som cursos kör för databasen:
    query_topics = """
        SELECT topic.id, topic.rubrik, anvandare.usern AS topic_skapare 
        FROM topic 
        LEFT JOIN anvandare ON topic.tradskapare = anvandare.id
        ORDER BY topic.skapad DESC
    """
    cursor_topics.execute(query_topics) #kör kommandot
    alla_topics = cursor_topics.fetchall() #Hämtar topics efter ändringarna
    cursor_topics.close() #Stänger cursor

    #Samma sak för inlägg i databsen:
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

    return render_template('home.html', topics=alla_topics) #laddar home.html nu när förberedelserna är klara. Sparar topics som en variabel till html
    
#---Profil:----------------------------------------

@app.route('/profil')
def profil(): #En sida för din profil, här kan man vidareutveckla med inställningar och att ändra uppgifter i databasen
    if not session.get('loggedin'): #om inte logged in
       return render_template('login.html', msg='DU MÅSTE LOGGA IN FÖR ÅTKOMST!') #tvinga till att logga in med ett meddelande som förklarar förflyttningen.
    return render_template('profil.html')

#---Skapa konto:----------------------------------------
        
@app.route('/skapa_konto', methods=['GET', 'Post'])
def skapa_konto(): #för att skapa konto

    if request.form['NYTTusername'] != '' and request.form['NYTTpassword'] !='' and request.form['REGISTRERA_epost'] !='': #om alla fällt i form är ifyllda:
        db = get_db_connection()
        mycursor = db.cursor()
        sql = "INSERT INTO anvandare (usern, pswrd, epost) VALUES (%s, %s, %s)" #sql kommando med varablar
        val = (request.form['NYTTusername'], request.form['NYTTpassword'], request.form['REGISTRERA_epost']) #variablarna i kommandot ovan
        mycursor.execute(sql, val)
        db.commit()
        return redirect(url_for('homepage')) #ta användaren till homepage
    else: 
        return render_template('login.html', msg="DU MÅSTE FYLLA I ALLA UPPGIFTER FÖR ATT SKAPA KONTO") #tvinga tillbaka inloggning om inte fälten ifyllda korrekt

#---APPEND FORM FRÅN INLOGGNING:----------------------------------------

@app.route('/login', methods=['GET', 'Post'])
def append_login(): #logga in
    if request.form['username'] != '' and request.form['password'] != '': #om fälten ifyllda


        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute('SELECT * FROM anvandare WHERE usern = %s AND pswrd = %s', (request.form['username'], request.form['password'])) #kommando och variabler till sql
        account = cursor.fetchone()

        cursor.close()
        db.close()

        if account: #om det finns ett konto enligt databasen spara info:
            session['loggedin'] = True
            session['epost'] = account['epost']
            session['id'] = account['id']
            session['username'] = account['usern']
            
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html', msg='Användare med det lösenordet finns inte!')
    else:
        return render_template('login.html', msg='Fyll i både användarnamn och lösenord!')
    
#---LOGOUT:----------------------------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

#---INFO OM SESSIONEN:----------------------------------------

@app.route('/session-info')
def session_info():
    return f"Session data: {dict(session)}"

#---SKAPA EN TRÅD:----------------------------------------

@app.route('/skapa-trad', methods=['POST'])
def skapa_trad():
    if not session.get('loggedin'):
        return redirect(url_for('homepage'))

    if request.form.get('trad_rubrik'): #om en trådrubrik finns i form i html:

        db = get_db_connection()
        cursor = db.cursor()
        try: #försök skapa en tråd i sql
            cursor.execute( #SQL kommando att köra med variabler
                'INSERT INTO topic (rubrik, tradskapare) VALUES (%s, %s)', 
                (request.form.get('trad_rubrik'), session.get('id'))
            )
            db.commit()
        except mysql.connector.Error as err: #error
            print(f"Fel: {err}") 
        finally: #när den försökt: stäng av cursor
            cursor.close()
            db.close()

    return redirect(url_for('homepage'))

#---SKAPA ETT INLÄGG:----------------------------------------


@app.route('/skapa-inlagg', methods=['POST'])
def skapa_inlagg():
    if not session.get('loggedin'):
        return redirect(url_for('homepage'))

    if request.form.get('innehall') and request.form.get('topic_id'): #om form ifylld korrekt

        db = get_db_connection()
        cursor = db.cursor()
        try: #försök köra SQL kommando
            cursor.execute(
                'INSERT INTO inlagg (anvandare_id, topic_id, innehall) VALUES (%s, %s, %s)', 
                (session.get('id'), request.form.get('topic_id'), request.form.get('innehall'))
            )
            db.commit()
        except mysql.connector.Error as err: #error
            print(f"Fel: {err}")
        finally: #stäng cursor efter
            cursor.close()
            db.close()

    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
