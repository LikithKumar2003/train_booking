from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Fare logic
def calculate_fare(source, destination):
    fares = {
        ("Guntakal", "Hyderabad"): 250,
        ("Hyderabad", "Guntakal"): 250,
        ("Guntakal", "Ananthapur"): 150,
        ("Ananthapur", "Guntakal"): 150,
        ("Hyderabad", "Ananthapur"): 300,
        ("Ananthapur", "Hyderabad"): 300,
        ("Bangalore", "Chennai"): 400,
        ("Chennai", "Bangalore"): 400,
    }
    return fares.get((source, destination), 100)  # Default fare if no match

# Initialize DB with fare column
def init_db():
    conn = sqlite3.connect('database/tickets.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    source TEXT,
                    destination TEXT,
                    date TEXT,
                    fare INTEGER
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    age = request.form['age']
    source = request.form['source']
    destination = request.form['destination']
    date = request.form['date']

    fare = calculate_fare(source, destination)

    conn = sqlite3.connect('database/tickets.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO tickets (name, age, source, destination, date, fare) VALUES (?, ?, ?, ?, ?, ?)",
                (name, age, source, destination, date, fare))
    conn.commit()
    conn.close()

    return render_template('success.html', name=name, source=source, destination=destination, date=date, fare=fare)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
