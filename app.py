from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from io import StringIO
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkeychangeinprod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=2)  # 1=alta, 2=normal, 3=baixa
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    tasks = Task.query.filter_by(user_id=session['user_id']).order_by(Task.created_at.desc()).all()
    stats = get_stats()
    return render_template('dashboard.html', tasks=tasks, stats=stats)

def get_stats():
    if 'user_id' not in session:
        return {'total': 0, 'pending': 0}
    user_id = session['user_id']
    total = Task.query.filter_by(user_id=user_id).count()
    pending = Task.query.filter_by(user_id=user_id, completed=False).count()
    return {'total': total, 'pending': pending}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash('Usuário já existe!')
            return render_template('register.html')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registrado!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            flash('Logado!')
            return redirect(url_for('index'))
        flash('Credenciais inválidas!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_task():
    content = request.form['content']
    priority = request.form.get('priority', 2, type=int)
    due_str = request.form.get('due_date')
    try:
        due_date = datetime.strptime(due_str, '%Y-%m-%d') if due_str else None
    except:
        due_date = None
    task = Task(content=content, priority=priority, due_date=due_date, user_id=session['user_id'])
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == session['user_id']:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == session['user_id']:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/tasks')
def api_tasks():
    if 'user_id' not in session:
        return jsonify([])
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
    return jsonify([{
        'id': t.id,
        'content': t.content,
        'completed': t.completed,
        'priority': t.priority,
        'due_date': t.due_date.isoformat() if t.due_date else None,
        'created_at': t.created_at.isoformat()
    } for t in tasks])

@app.route('/stats')
def stats():
    stats_data = get_stats()
    return jsonify(stats_data)

@app.route('/export')
def export():
    if 'user_id' not in session:
        flash('Faça login primeiro!')
        return redirect(url_for('login'))
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Tarefa', 'Concluida', 'Prioridade', 'Data Limite'])
    for t in tasks:
        cw.writerow([t.id, t.content, t.completed, t.priority, t.due_date])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
