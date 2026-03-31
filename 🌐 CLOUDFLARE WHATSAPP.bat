@echo off
title 🌐 Cloudflare WhatsApp CLICK!
color 0F
cls

echo [1] Flask...
py init_db.py
start "Flask" cmd /k "color 0A && title FLASK && py app.py"
timeout /t 8 >nul

echo [2] Cloudflare Tunnel (WhatsApp RICH!)...
cloudflared tunnel --url http://localhost:5000

