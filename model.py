import sqlite3

BANCO_DE_DADOS = "Sistema-Web-Escolar.bd"

def criarBanco():
    print("Criando banco...")

    conexao = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conexao.cursor()

    # Queries SQL pra criar o banco

    conexao.commit()

    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    criarBanco()
