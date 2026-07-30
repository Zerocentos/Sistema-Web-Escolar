from flask import Flask, render_template, request
import sqlite3

from model import DATABASE

app = Flask(__name__)

@app.route("/")
def home() -> str:
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
