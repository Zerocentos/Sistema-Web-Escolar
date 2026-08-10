from flask import Flask, render_template, request
import sqlite3
import os
from dotenv import load_dotenv

from model import BANCO_DE_DADOS

app = Flask(__name__)
_ = load_dotenv()

@app.route("/")
def home() -> str:
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORTA_SERVIDOR", 5000))

    app.run(host="0.0.0.0", debug=True, port=port)
