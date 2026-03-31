from app import app, db, User, Task
from werkzeug.security import generate_password_hash

with app.app_context():
    # Reset completo
    Task.__table__.drop(db.engine, checkfirst=True)
    db.create_all()
    
    # Users corretos
users_data = [
        ('admin', '123456'),
        ('Ritheli', 'jr302412'),
        ('Pretinho123', '123456'),
    ]

    
    for username, password in users_data:
        if User.query.filter_by(username=username).first():
            User.query.filter_by(username=username).delete()
        u = User(username=username, password=generate_password_hash(password))
        db.session.add(u)
    
    db.session.commit()
    
    print("✅ DB RESET!")
    print("Users:")
    for u in User.query.all():
        print(f"  - {u.username} (ID: {u.id})")

