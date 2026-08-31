import sqlite3

BANCO_DE_DADOS = "Sistema-Web-Escolar.db"

def ativa_foreign_key() -> str:
    query = '''
    PRAGMA foreign_key = ON
    '''

    return query

def tabela_aluno() -> str: 
    query = '''
    CREATE TABLE IF NOT EXISTS aluno(
        matricula INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(60) NOT NULL, 
        email VARCHAR(40) NOT NULL,
        telefone VARCHAR(30) NOT NULL,
        data_nascimento DATETIME
    )
    '''
    return query

def tabela_materia() -> str:
    query = '''
    CREATE TABLE IF NOT EXISTS materia(
        id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(40) NOT NULL,
        carga_horaria INT NOT NULL  
    )
    '''
    return query

def tabela_curso() -> str:
    query = '''
    CREATE TABLE IF NOT EXISTS curso(
        id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(50) NOT NULL,
        descricao VARCHAR(40) 
    )
    '''

    return query

def tabela_professor() -> str: 
    query = '''
    CREATE TABLE IF NOT EXISTS professor(
        id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(60) NOT NULL, 
        email VARCHAR(40) NOT NULL,
        telefone VARCHAR(30) NOT NULL,
        data_nascimento DATETIME
    )
    '''
    return query

def aluno_curso() -> str: 
    query = '''
    CREATE TABLE IF NOT EXISTS aluno_curso (
        id_curso INTEGER NOT NULL,
        matricula_aluno INTEGER NOT NULL,
        PRIMARY KEY (id_curso, matricula_aluno),
        FOREIGN KEY (matricula_aluno) REFERENCES aluno(matricula) ON DELETE CASCADE,
        FOREIGN KEY (id_curso) REFERENCES curso(id) ON DELETE CASCADE
    )
    '''
    return query

def aluno_materia() -> str: 
    query = '''
    CREATE TABLE IF NOT EXISTS aluno_materia(
        matricula_aluno INTEGER NOT NULL,
        id_materia INTEGER NOT NULL,
        nota INTEGER NOT NULL,
        PRIMARY KEY (matricula_aluno, id_materia),
        FOREIGN KEY (matricula_aluno) REFERENCES aluno(matricula) ON DELETE CASCADE,
        FOREIGN KEY (id_materia) REFERENCES materia(id) ON DELETE CASCADE 
    )
    '''
    return query

def curso_materia() -> str: 
    query = '''
    CREATE TABLE IF NOT EXISTS curso_materia(
        id_curso INTEGER NOT NULL,
        id_materia INTEGER NOT NULL,
        PRIMARY KEY (id_curso, id_materia),
        FOREIGN KEY (id_materia) REFERENCES materia(id_materia) ON DELETE CASCADE,
        FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON DELETE CASCADE
    )
    '''
    return query

def materia_professor() -> str: 
    query = '''
    CREATE TABLE IF NOT EXISTS materia_professor(
        id_professor INTEGER NOT NULL,
        id_materia INTEGER NOT NULL,
        PRIMARY KEY (id_professor, id_materia),
        FOREIGN KEY (id_materia) REFERENCES materia(id) ON DELETE CASCADE,
        FOREIGN KEY (id_professor) REFERENCES professor(id) ON DELETE CASCADE
    )
    '''
    return query

def criar_tabelas():
    conexao = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conexao.cursor()

    print("Colocando configurações...")
    _ = cursor.execute(ativa_foreign_key())
    print("Configurações feitas!")

    print("Criando as tabelas...")

    _ = cursor.execute(tabela_aluno())

    _ = cursor.execute(tabela_materia())

    _ = cursor.execute(tabela_curso())

    _ = cursor.execute(tabela_professor())

    _ = cursor.execute(aluno_curso())
    
    _ = cursor.execute(aluno_materia())
    
    _ = cursor.execute(curso_materia())

    _ = cursor.execute(materia_professor())

    conexao.commit()

    print("Tabelas criadas com sucesso!")

    conexao.close()


if __name__ == "__main__":
    criar_tabelas()
