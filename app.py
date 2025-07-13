from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            content TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Submit route
@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    category = request.form['category']
    content = request.form['content']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO submissions (title, category, content) VALUES (?, ?, ?)',
              (title, category, content))
    conn.commit()
    conn.close()
    return "Submitted for review"

# Admin dashboard
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM submissions WHERE status="pending"')
    items = c.fetchall()
    conn.close()
    return render_template('admin.html', items=items)

# Approve route
@app.route('/approve/<int:id>')
def approve(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE submissions SET status="approved" WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# Reject route
@app.route('/reject/<int:id>')
def reject(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE submissions SET status="rejected" WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.run()
