import sqlite3

DATABASE = "Sistema-Web-Escolar.bd"

def criarBanco():
    print("Criando banco...")

    conexao = sqlite3.connect(DATABASE)
    cursor = conexao.cursor()

    # Queries SQL pra criar o banco

    conexao.commit()

    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    criarBanco()
