from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    if not User.query.first():
        user = User(username='admin', password=generate_password_hash('123456'))
        db.session.add(user)
        db.session.commit()
        print("✅ User 'admin' / '123456' criado!")
    else:
        print("👥 Users já existem!")
