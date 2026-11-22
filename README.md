# EMOTIA — Presentación en un solo audio 💜

Al ejecutar `/start` aparece únicamente el botón **🎙️ Escuchar mi presentación completa**. Al pulsarlo, EMOTIA envía **un solo audio** con toda su presentación, sin dividirla en capítulos ni repetir el guion por escrito. El mismo mensaje incluye **🏠 Abrir menú principal** y **🔁 Volver a escuchar**.

## Instalación en Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:TELEGRAM_BOT_TOKEN="TU_TOKEN_NUEVO"
.\.venv\Scripts\python.exe bot.py
```

Abre Telegram y envía `/start`. La voz necesita Internet. Si ya había otro bot ejecutándose, deténlo antes de iniciar este. Para configurar la foto del bot: BotFather → /mybots → Edit Bot → Edit Botpic y envía `assets/emotia.png`. No compartas tu token.
