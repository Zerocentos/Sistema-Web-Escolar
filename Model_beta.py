import sqlite3

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

def tabela_materia():
    query = '''
    CREATE TABLE IF NOT EXISTS materia(
        id_materia INTENGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(40) NOT NULL,
        carga_horaria INT NOT NULL  
    )
    '''

def tabela_curso():
    query = '''
    CREATE TABLE IF NOT EXISTS curso(
        id_curso INTEGER PRIMAARY KEY AUTOINCREMENT
        nome VARCHAR(50) NOT NULL,
        descricao VARCHAR(40) NULL
    )
    '''

def tabelaa_

if __name__ == "__main__":
    conexao = sqlite3.connect("Escola.db")
    cursor = conexao.cursor()



    conexao.close()