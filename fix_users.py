from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Limpar tasks órfãs
    db.session.query(Task).filter(Task.user_id.notin_(db.session.query(User.id))).delete()
    db.session.commit()
    
    # Criar users
    users = {
        'admin': '123456',
        'user': '123456'
    }
    
    for username, password in users.items():
        if not User.query.filter_by(username=username).first():
            u = User(username=username, password=generate_password_hash(password))
            db.session.add(u)
            db.session.commit()
            print(f"✅ Criado {username}")
        else:
            print(f"👤 {username} existe")
    
    print("Users:", [(u.id, u.username) for u in User.query.all()])
    print(f"Tasks totais: {db.session.query(Task).count()}")

