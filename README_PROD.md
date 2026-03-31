# ToDo Pro PRODUCTION Deploy

## 1. GitHub Repo (5min)
```
git init
git add .
git commit -m "Initial prod"
git branch -M main
git remote add origin https://github.com/SEU_USERNAME/todo-pro-prod.git
git push -u origin main
```

## 2. Render.com (2min)
1. render.com → Sign up GitHub
2. New → Web Service → Connect GitHub repo
3. Settings → Build: `pip install -r requirements.txt` | Start: `gunicorn app_prod:app`
4. Environment: `SECRET_KEY=your_secret`
5. Deploy → URL: https://todo-pro-prod.onrender.com

## 3. Admin Prod
admin / 123456 auto

## 4. Domain FREE
1. freenom.com → todoapppro.tk FREE
2. Render Custom Domain → todoapppro.tk

## Otimizações ✅
- PostgreSQL Render auto
- Gunicorn prod server
- HTTPS/SSL auto
- Static auto CDN

**Login:** https://your-app.onrender.com/login

