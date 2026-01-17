import os
import json
from cryptography.fernet import Fernet
from PyQt6.QtWidgets import QMessageBox

PASSWORD_FILE = "passwords.enc"
KEY_FILE = "vault.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        open(KEY_FILE, "wb").write(key)
    return open(KEY_FILE, "rb").read()

FERNET = Fernet(load_key())

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        return {}
    encrypted = open(PASSWORD_FILE, "rb").read()
    decrypted = FERNET.decrypt(encrypted)
    return json.loads(decrypted.decode())

def save_passwords(data):
    raw = json.dumps(data).encode()
    encrypted = FERNET.encrypt(raw)
    open(PASSWORD_FILE, "wb").write(encrypted)

def on_page_load(browser):
    js_capture = """
    (function() {
        if (window._hooked) return;
        window._hooked = true;
        document.addEventListener('submit', function() {
            let u = document.querySelector('input[type=email], input[type=text]');
            let p = document.querySelector('input[type=password]');
            if (u && p) window._creds = { user: u.value, pass: p.value };
        }, true);
    })();
    """
    browser.page().runJavaScript(js_capture)

    # Prompt save password after submit
    def handler(data):
        if not data:
            return
        host = browser.url().host()
        passwords = load_passwords()
        if host in passwords:
            return
        msg = QMessageBox.question(
            browser,
            "Save password?",
            f"Save login for {host}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if msg == QMessageBox.StandardButton.Yes:
            passwords[host] = {"username": data["user"], "password": data["pass"]}
            save_passwords(passwords)

    browser.page().runJavaScript("window._creds", handler)

    # Autofill saved passwords
    passwords = load_passwords()
    host = browser.url().host()
    if host in passwords:
        creds = passwords[host]
        js_fill = f"""
        (function() {{
            let user = null; let pass = null;
            document.querySelectorAll('input').forEach(i => {{
                if (!user && (i.type==='email'||i.type==='text')) user=i;
                if (!pass && i.type==='password') pass=i;
            }});
            if(user&&pass){{user.value="{creds['username']}"; pass.value="{creds['password']}"}}
        }})();
        """
        browser.page().runJavaScript(js_fill)
