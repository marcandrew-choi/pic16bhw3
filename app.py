from flask import Flask
from flask import render_template, g, request
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    '''
    Renders submit.html
    '''
    #If we are first entering the page, we render submit.html
    if request.method == 'GET':
        return render_template('submit.html')
    else:
    #Once message is submitted, we insert the message into the database and render submit.html
        message, handle = insert_message()
        return render_template('submit.html', submitted=True, message=message, handle=handle)

def get_message_db():
    '''
    Get or create a database to hold the messages
    '''
    #Connect to a SQL database 
    g.message_db = sqlite3.connect("messages_db.sqlite")
    #Create a table if it doesnt exist with three columns
    cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            handle TEXT NOT NULL)
        """
    cursor = g.message_db.cursor()
    #executes sql command
    cursor.execute(cmd)
    return g.message_db


def insert_message():
    '''
    Inserts the message into the existing database
    '''

    #Get messange and handle from text field
    message = request.form['message']
    handle = request.form['handle']

    #Gets the database with all the messages and inserts the message into the database
    conn = get_message_db()
    cmd = \
    f"""
    INSERT INTO messages (message, handle) 
    VALUES ('{message}', '{handle}')
    """

    cursor = conn.cursor()
    #executes sql command
    cursor.execute(cmd)
    conn.commit()
    conn.close()

    return message, handle

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    '''
    Renders submit.html
    '''
    #If we are first entering the page, we render submit.html
    if request.method == 'GET':
        return render_template('submit.html')
    else:
    #Once message is submitted, we insert the message into the database and render submit.html
        message, handle = insert_message()
        return render_template('submit.html', submitted=True, message=message, handle=handle)



def random_messages(n):
    '''
    Randomly chooses n messages from the database and returns the n messages
    '''
    conn = get_message_db()

    #sql command that returns n random messages from the database
    cmd = \
    f"""
    SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}
    """
    cursor = conn.cursor()
    #executes sql command
    cursor.execute(cmd)
    result = cursor.fetchall()
    conn.close()

    #returns n random messages
    return result


@app.route('/view/')
def view(): 
    #renders view.html and displays
    return render_template('view.html', messages=random_messages(5))
