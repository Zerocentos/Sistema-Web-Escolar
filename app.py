from flask import Flask, render_template, request
import sqlite3
import os
from dotenv import load_dotenv

from model import BANCO_DE_DADOS

app = Flask(__name__)
_ = load_dotenv()


# Alunos =======================================================================

@app.route("/alunos/")
def alunos() -> str:
    return render_template("alunos.html")

@app.route("/alunos/novo/")
def novo_aluno() -> str:
    return render_template("novo_aluno.html")

# ==============================================================================

# Professores ==================================================================

@app.route("/professores/")
def professores() -> str:
    return render_template("professores.html")

@app.route("/professores/novo/")
def novo_professor() -> str:
    return render_template("novo_professor.html")

# ==============================================================================

# Matérias =====================================================================

@app.route("/materias/")
def materias() -> str:
    cursor = sqlite3.connect(BANCO_DE_DADOS).cursor()

    materias = cursor.execute("SELECT * FROM materia").fetchall()

    return render_template("materias.html", 
                           Materias = materias)

@app.route("/materias/nova/")
def nova_materia() -> str:
    return render_template("nova_materia.html")

# ==============================================================================

# Cursos =======================================================================

@app.route("/cursos/")
def cursos() -> str:
    return render_template("cursos.html")

@app.route("/cursos/novo")
def novo_curso() -> str:
    return render_template("novo_curso.html")

# ==============================================================================



@app.route("/")
def home() -> str:
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORTA_SERVIDOR", 5000))

    app.run(host="0.0.0.0", debug=True, port=port)
