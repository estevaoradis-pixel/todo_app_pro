from app import app, db, User, Task
from werkzeug.security import generate_password_hash

with app.app_context():
    # Reset completo
    Task.__table__.drop(db.engine, checkfirst=True)
    db.create_all()
    
    # Users corretos com senhas certas
    users_data = [
        ('admin', '123456'),
        ('Ritheli', 'jr302412'),
        ('Pretinho123', '123456'),
    ]
    
    for username, password in users_data:
        if User.query.filter_by(username=username).first():
            User.query.filter_by(username=username).delete()
            db.session.commit()
        u = User(username=username, password=generate_password_hash(password))
        db.session.add(u)
    
    db.session.commit()
    
    print("✅ DB RESET COMPLETO!")
    print("Users criados:")
    for u in User.query.all():
        print(f"  • {u.username} (ID: {u.id}) - senha configurada")
    print(f"Total tasks: 0 (limpo)")

