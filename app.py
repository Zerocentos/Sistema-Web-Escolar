import sys
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from dotenv import load_dotenv

from model import BANCO_DE_DADOS

app = Flask(__name__)
_ = load_dotenv()

#TODO: Apagar os comentários das bibliotecas

# Util ========================================================================

def formatar_data(data) -> str:
    d =  datetime.strptime(data, "%Y-%m-%d")
    return d.strftime("%d/%m/%Y")

# Alunos =======================================================================

# Coloca zeros à esquerda na matricula se necessário
def formatar_matricula(matricula) -> str:
    return f"{int(matricula):04d}"

def aluno_com_matricula(matricula: int):
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor() 

    _ = cursor.execute("""
    SELECT * FROM aluno
    WHERE matricula = ?
    """, (matricula,))

    aluno = list(cursor.fetchone())

    _ = cursor.execute("""
    SELECT curso.nome FROM aluno_curso
    JOIN curso ON curso.id_curso = aluno_curso.id_curso
    WHERE matricula_aluno = ?
    """, (int(aluno[0]),))

    row: list[str] = list(cursor.fetchone())
    nome_curso = row[0]

    aluno.append(nome_curso)

    return aluno

@app.route("/alunos/<int:matricula>/")
def aluno(matricula: int) -> str:   
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor() 

    aluno = aluno_com_matricula(matricula)

    _ = cursor.execute("""
    SELECT aluno_materia.id_materia,
    aluno_materia.nota,
    materia.nome
    FROM aluno_materia
    JOIN materia ON aluno_materia.id_materia = materia.id_materia
    WHERE aluno_materia.matricula_aluno = ?
    """, (matricula,))

    notas = []

    if _notas := cursor.fetchone():
        notas = list(_notas)

    aluno[0] = formatar_matricula(aluno[0])
    aluno[4] = formatar_data(aluno[4])

    return render_template("aluno.html", Aluno=aluno, Notas=notas)

@app.route("/alunos/<int:matricula>/nova-nota/", methods=["GET", "POST"])
def aluno_nova_nota(matricula) -> str:
    aluno = aluno_com_matricula(matricula)

    if request.method == "GET":
        conn = sqlite3.connect(BANCO_DE_DADOS)
        cursor = conn.cursor()

        _ = cursor.execute("SELECT id_materia, nome FROM materia")

        materias = cursor.fetchall()

        return render_template("aluno_nova_nota.html", Aluno=aluno, Materias=materias)

    return render_template("aluno_nova_nota.html", Aluno=aluno,
                           Mensagem="Aluno cadastrado com sucesso!")

@app.route("/alunos/")
def alunos() -> str:
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor()

    alunos: list[list[str]] = list(map(
        list, cursor.execute("SELECT matricula, nome, data_nascimento FROM aluno").fetchall()
    ))

    for aluno in alunos:
        aluno[0] = formatar_matricula(aluno[0]) 
        _ = cursor.execute("""
        SELECT curso.nome FROM aluno_curso
        JOIN curso ON curso.id_curso = aluno_curso.id_curso
        WHERE matricula_aluno = ?
        """, (int(aluno[0]),))

        rows: list[tuple[str]] = list(cursor.fetchall())

        nome_curso = rows[0][0]
        aluno.insert(2, nome_curso)

        data = formatar_data(aluno[3])
        aluno[3] = data 

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
@app.route("/professores/<int:id_professor>/")
def professor(id_professor: int) -> str:   
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor() 

    _ = cursor.execute("""
    SELECT * FROM professor
    WHERE id_professor = ?
    """, (id_professor,))

    professor = list(cursor.fetchone())

    _ = cursor.execute("""
    SELECT materia.nome FROM materia_professor
    JOIN materia ON materia.id_materia = materia_professor.id_materia
    WHERE id_professor = ?
    """, (int(professor[0]),))

    row: list[str] = list(cursor.fetchone())
    nome_materia = row[0]

    professor.append(nome_materia)

    professor[4] = formatar_data(professor[4])

    return render_template("professor.html", Professor=professor)

@app.route("/professores/")
def professores() -> str:
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor()

    professores: list[list[str]] = list(map(
        list, cursor.execute("""
                            SELECT id_professor, nome, email, telefone, data_nascimento
                            FROM professor """).fetchall()
    ))

    for professor in professores:
        _ = cursor.execute("""
        SELECT materia.nome FROM materia_professor
        JOIN materia 
        ON materia.id_materia = materia_professor.id_materia
        WHERE id_professor = ?
        """, (int(professor[0]),))

        rows: list[tuple[str]] = list(cursor.fetchall())
        nome_materia = rows[0][0]

        professor.append(nome_materia)

    conn.close()
    
    return render_template("professores.html", Professores=professores)

@app.route("/professores/novo/", methods=["GET", "POST"])
def novo_professor() -> str:  
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor()

    _ = cursor.execute("SELECT id_materia, nome FROM materia")
    
    materias = cursor.fetchall()

    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        telefone = request.form["telefone"].strip()
        data_nascimento = request.form["data-nascimento"]
        id_materia = request.form["materia"]

        _ = cursor.execute('''
        INSERT INTO professor (nome, email, telefone, data_nascimento)
        VALUES (?, ?, ?, ?)
        ''', (nome, email, telefone, data_nascimento))

        id_professor = cursor.lastrowid

        _ = cursor.execute('''
        INSERT INTO materia_professor (id_materia, id_professor)
        VALUES (?, ?)
        ''', (id_materia, id_professor))

        conn.commit()
        conn.close()

        return render_template("novo_professor.html",
                                Mensagem="Professor cadastrado com sucesso!", Materias=materias)

    conn.close()
    
    return render_template("novo_professor.html", Materias=materias)

@app.route("/professores/<int:id_professor>/excluir", methods=["POST"])
def excluir_professor(id_professor: int):
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor()

    _ = cursor.execute(""" DELETE FROM professor
                        WHERE id_professor = ? """, 
                        (id_professor,))

    conn.commit()
    conn.close()

    return redirect(url_for("professores"))

@app.route("/professores/<int:id_professor>/editar", methods=["GET", "POST"])
def editar_professor(id_professor: int):
    conn = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        telefone = request.form["telefone"].strip()
        data_nascimento = request.form["data-nascimento"]
        id_materia = request.form["materia"]

        _ = cursor.execute(""" UPDATE professor SET nome = ?, email = ?, telefone = ?,
                                data_nascimento = ? 
                                WHERE id_professor = ? """, 
                                (nome, email, telefone, data_nascimento, id_professor))

        _ = cursor.execute(""" DELETE FROM materia_professor 
                            WHERE id_professor = ? """, (id_professor,))

        _ = cursor.execute(""" INSERT INTO materia_professor (id_materia, id_professor) VALUES (?, ?)""",
                           (id_materia, id_professor))

        conn.commit()
        conn.close()

        return redirect(url_for("professores"))
    
    _ = cursor.execute(""" SELECT id_professor, nome, email, telefone, data_nascimento
                            FROM professor 
                            WHERE id_professor = ?""", 
                        (id_professor,))

    professor = list(cursor.fetchone())

    _ = cursor.execute(""" SELECT id_materia FROM materia_professor 
                        WHERE id_professor = ? """, (id_professor,))

    id_materia = cursor.fetchone()
    
    professor.append(id_materia[0])

    _ = cursor.execute(""" SELECT id_materia, nome FROM materia """)

    materias = cursor.fetchall()

    conn.commit()
    conn.close()

    return render_template("novo_professor.html", Materias=materias, Modo="editar", Professor=professor)

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
        JOIN materia ON materia.id_materia = curso_materia.id_materia
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
