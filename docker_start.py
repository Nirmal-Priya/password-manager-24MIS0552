
import os

from app import app, init_db

os.makedirs("data", exist_ok=True)

init_db()

app.run(host="0.0.0.0", port=5000, debug=False)
