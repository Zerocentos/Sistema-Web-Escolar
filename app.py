import sys
from flask import Flask, render_template, request
import sqlite3
import os
from dotenv import load_dotenv

from model import BANCO_DE_DADOS

app = Flask(__name__)
_ = load_dotenv()


# Alunos =======================================================================

@app.route("/alunos/<int:matricula>/")
def aluno(matricula: int) -> str:
    print("matricula: " + str(matricula))
    
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor()

    _ = cursor.execute("""
    SELECT nome FROM aluno
    """)

    aluno: str = cursor.fetchone()[0]

    return render_template("aluno.html", Aluno=aluno, Matricula=matricula)

@app.route("/alunos/")
def alunos() -> str:
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor()

    alunos: list[list[str]] = list(map(
        list, cursor.execute("SELECT matricula, nome, data_nascimento FROM aluno").fetchall()
    ))

    for aluno in alunos:
        aluno[0] = f"{int(aluno[0]):04d}" # Coloca zeros à esquerda na
                                          # matricula se necessário

        _ = cursor.execute("""
        SELECT curso.nome FROM aluno_curso
        JOIN curso ON curso.id_curso
        WHERE matricula_aluno = ?
        """, (int(aluno[0]),))

        rows: list[tuple[str]] = list(cursor.fetchall())
        nome_curso = rows[0][0]

        aluno.insert(2, nome_curso)

    conn.close()

    return render_template("alunos.html", Alunos=alunos)

@app.route("/alunos/novo/", methods=["GET", "POST"])
def novo_aluno() -> str:
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        telefone = request.form["telefone"].strip()
        data_nascimento = request.form["data-nascimento"]
        id_curso = request.form["curso"]

        _ = cursor.execute('''
        INSERT INTO aluno (nome, email, telefone, data_nascimento)
        VALUES (?, ?, ?, ?)
        ''', (nome, email, telefone, data_nascimento))

        matricula = cursor.lastrowid

        _ = cursor.execute('''
        INSERT INTO aluno_curso (id_curso, matricula_aluno)
        VALUES (?, ?)
        ''', (id_curso, matricula))

        conn.commit()
        conn.close()

        return render_template("novo_aluno.html",
                               Mensagem="Aluno cadastrado com sucesso!")

    _ = cursor.execute("SELECT id_curso, nome FROM curso")

    cursos = cursor.fetchall()

    conn.close()

    return render_template("novo_aluno.html", Cursos=cursos)

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

@app.route("/materias/nova/", methods=["GET", "POST"])
def nova_materia() -> str:
    if request.method == "POST":
        nome = request.form["nome"].strip()
        carga_horaria = request.form["carga_horaria"]

        conn = sqlite3.connect(BANCO_DE_DADOS)
        cursor = conn.cursor()
        
        _ = cursor.execute(
            "INSERT INTO materia (nome, carga_horaria) VALUES (?, ?)",
            (nome, carga_horaria)
        ) 
          
        conn.commit()
        conn.close()
        
        return render_template('nova_materia.html', 
                             Mensagem=f"Matéria cadastrada com sucesso!")
 
    return render_template("nova_materia.html", Mensagem="")

# ==============================================================================

# Cursos =======================================================================

@app.route("/cursos/")
def cursos() -> str:
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor()

    _ = cursor.execute("""
    SELECT id_curso, nome, descricao FROM curso
    """)

    _cursos: list[tuple[str]] = cursor.fetchall()
    cursos = list(map(list, _cursos))

    for curso in cursos:
        id_curso = curso[0]

        _ = cursor.execute("""
        SELECT materia.nome FROM curso_materia 
        JOIN materia ON materia.id_materia
        WHERE curso_materia.id_curso = ?
        """, (id_curso,))

        rows: list[list[str]] = cursor.fetchall()
        
        materias = [str(row[0]) for row in rows]

        curso.append(", ".join(materias))

    return render_template("cursos.html", Cursos=cursos)

@app.route("/cursos/novo/", methods=["GET", "POST"])
def novo_curso() -> str:
    if request.method == "POST":
        nome = request.form["nome"].strip()
        descricao = request.form["descricao"].strip()
        materias = request.form.getlist("materias")

        conn = sqlite3.connect(BANCO_DE_DADOS)
        cursor = conn.cursor()
        
        _ = cursor.execute(
            "INSERT INTO curso (nome, descricao) VALUES (?, ?)",
            (nome, descricao)
        ) 

        id = cursor.lastrowid

        for id_materia in materias:
            _ = cursor.execute("""
            INSERT INTO curso_materia (id_curso, id_materia)
            VALUES (?, ?)
            """, (id, id_materia))
        
        conn.commit()
        conn.close()
        
        return render_template('novo_curso.html', 
                             Mensagem="Curso cadastrado com sucesso!")


    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor()

    _ = cursor.execute("SELECT id_materia, nome FROM materia")

    materias = cursor.fetchall()

    conn.close()

    return render_template("novo_curso.html", Materias=materias)

# ==============================================================================



@app.route("/")
def home() -> str:
    return render_template("index.html")

if __name__ == "__main__":
    if not os.path.exists(BANCO_DE_DADOS):
        print("""
Não foi possível encontrar o arquivo do banco de dados, impossível iniciar o servidor.

Para criar o banco de dados, rode 'model.py'.
        """)
        sys.exit();

    port = int(os.environ.get("PORTA_SERVIDOR", 5000))
    app.run(host="0.0.0.0", debug=True, port=port)
