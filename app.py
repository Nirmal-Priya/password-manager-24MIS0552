
from flask import Flask, render_template, request, redirect, url_for, flash
from cryptography.fernet import Fernet
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)

# Application configuration
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DATABASE = DATA_DIR / "passwords.db"
KEY_FILE = DATA_DIR / "secret.key"

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "development-only-change-this-key"
)

# Generate encryption key for local development
if not KEY_FILE.exists():
    KEY_FILE.write_bytes(Fernet.generate_key())

cipher = Fernet(KEY_FILE.read_bytes())


# Create database table
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)


# Home page - View Credentials
@app.route("/")
def home():
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row

        credentials = conn.execute("""
            SELECT id, website, username
            FROM credentials
            ORDER BY id DESC
        """).fetchall()

    return render_template(
        "index.html",
        credentials=credentials
    )


# Version 1 - Add Credentials
@app.route("/add", methods=["POST"])
def add_credentials():
    website = request.form.get("website", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not website or not username or not password:
        flash("Please fill in all fields.")
        return redirect(url_for("home"))

    # Encrypt password before saving
    encrypted_password = cipher.encrypt(
        password.encode("utf-8")
    ).decode("utf-8")

    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """INSERT INTO credentials
               (website, username, password)
               VALUES (?, ?, ?)""",
            (website, username, encrypted_password)
        )

    flash("Credentials saved successfully!")
    return redirect(url_for("home"))


# Version 3 - Delete Credentials
@app.route("/delete/<int:credential_id>", methods=["POST"])
def delete_credentials(credential_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            "DELETE FROM credentials WHERE id = ?",
            (credential_id,)
        )

        deleted = cursor.rowcount

    if deleted:
        flash("Credential deleted successfully!")
    else:
        flash("Credential not found.")

    return redirect(url_for("home"))


# Start Flask application
if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
