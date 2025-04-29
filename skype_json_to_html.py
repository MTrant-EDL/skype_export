import json
from datetime import datetime
import os

# --- Konfiguration ---
INPUT_FILE = "messages.json"
OUTPUT_FILE = "skype_chat_export.html"
USERNAME_FILTER = None  # Optional: z. B. "echo123" oder None für alle Nachrichten

# --- HTML-Kopf ---
HTML_HEADER = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Skype Chat Export</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; color: #333; }
        .message { margin-bottom: 10px; padding: 10px; border-bottom: 1px solid #ddd; }
        .timestamp { font-size: 0.9em; color: #888; }
        .sender { font-weight: bold; }
        .content { margin-top: 5px; }
    </style>
</head>
<body>
<h1>Skype Chat Export</h1>
"""

HTML_FOOTER = """
</body>
</html>
"""

def format_timestamp(ts):
    try:
        dt = datetime.utcfromtimestamp(ts)
        return dt.strftime("%d.%m.%Y %H:%M:%S")
    except:
        return "Unbekannt"

def load_messages(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("messages", [])

def build_html(messages):
    html = HTML_HEADER
    for msg in messages:
        if msg.get("type") != "Message":
            continue
        user = msg.get("from")
        if USERNAME_FILTER and user != USERNAME_FILTER:
            continue
        ts = format_timestamp(msg.get("timestamp", 0))
        content = msg.get("content", "[Leere Nachricht]")
        html += f"""
        <div class="message">
            <div class="timestamp">{ts}</div>
            <div class="sender">{user}</div>
            <div class="content">{content}</div>
        </div>
        """
    html += HTML_FOOTER
    return html

def save_html(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Datei '{INPUT_FILE}' nicht gefunden.")
        return

    print("📥 Lade Nachrichten...")
    messages = load_messages(INPUT_FILE)

    print(f"📄 Generiere HTML-Datei mit {len(messages)} Nachrichten...")
    html = build_html(messages)

    print(f"💾 Speichere unter '{OUTPUT_FILE}'...")
    save_html(html, OUTPUT_FILE)

    print("✅ Fertig! Du kannst die Datei im Browser öffnen oder als PDF speichern.")

if __name__ == "__main__":
    main()
