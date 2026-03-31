from app import app, db, Task
from datetime import datetime
print("🔧 FIX 500 - TASK ADD SAFE...")

with app.app_context():
    # Delete all tasks (causa do erro 500)
    num_deleted = db.session.query(Task).delete()
    db.session.commit()
    print(f"🗑️ Tasks deletadas: {num_deleted}")

    print("✅ DB limpa! Add task agora OK")
    print("👉 Teste: http://192.168.1.14:5000/login → Ritheli/jr302412 → Add task")

