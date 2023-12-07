import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_task(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?',
                        (task_id,)).fetchone()
    conn.close()
    if task is None:
        abort(404)
    return task

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY endDate').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/<int:task_id>')
def task(task_id):
    task = get_task(task_id)
    return render_template('task.html', task=task)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        tName = request.form['tName']
        tDescription = request.form['tDescription']
        endDate = request.form['endDate']

        if not tName:
            flash('tName is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO tasks (tName, tDescription, endDate) VALUES (?, ?, ?)',
                         (tName, tDescription, endDate))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    task = get_task(id)

    if request.method == 'POST':
        tName = request.form['tName']
        tDescription = request.form['tDescription']
        endDate = request.form['endDate']

        if not tName:
            flash('tName is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE tasks SET tName = ?, tDescription = ?, endDate = ?'
                         ' WHERE id = ?',
                         (tName, tDescription, endDate, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', task=task)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    task = get_task(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(task['tName']))
    return redirect(url_for('index'))