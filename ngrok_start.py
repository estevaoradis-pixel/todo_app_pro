import os
os.environ["NGROK_AUTHTOKEN"] = "3BbLgGjtk86Ho4WwZfxzOFLP65d_67rDV1VzRducs3FAESZE4"

try:
    from pyngrok import ngrok
    print("✅ pyngrok OK!")
except ImportError:
    import subprocess
    subprocess.check_call(["py", "-m", "pip", "install", "pyngrok"])
    from pyngrok import ngrok
    print("✅ pyngrok instalado!")

print("🚀 NGROK DOMÍNIO PÚBLICO FIXO!")
print("Iniciando Flask + Tunnel...")

from app import app
port = 5000

# Tunnel
public_url = ngrok.connect(port, bind_tls=True)
print(f"🌐 DOMÍNIO PÚBLICO: {public_url}")
print("LOGIN: https://seu-link.ngrok-free.app/login")
print("admin / 123456")

# Flask
app.run(host='0.0.0.0', port=port, debug=False)
