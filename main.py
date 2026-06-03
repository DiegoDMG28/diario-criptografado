from cryptography.fernet import Fernet
import sqlite3
import base64
import hashlib
from datetime import datetime


class DiarioDB:
    def __init__(self, nome_arquivo='diario.db'):
        self.conn = sqlite3.connect(nome_arquivo)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS diario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto_criptografado TEXT NOT NULL,
            data_envio TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def adicionar_entrada(self, texto, data):
        self.cursor.execute(
            "INSERT INTO diario(texto_criptografado, data_envio) VALUES (?, ?)",
            (texto, data)
        )
        self.conn.commit()

    def listar_todos(self):
        self.cursor.execute(
            "SELECT id, data_envio FROM diario ORDER BY id DESC"
        )
        return self.cursor.fetchall()

    def buscar_por_id(self, id_):
        self.cursor.execute(
            "SELECT texto_criptografado FROM diario WHERE id = ?",
            (id_,)
        )
        return self.cursor.fetchone()

    def fechar(self):
        self.conn.close()


def gerar_chave(senha):
    return base64.urlsafe_b64encode(
        hashlib.sha256(senha.encode()).digest()
    )


def adicionar_diario(diario):
    texto = input("Digite o texto: ")
    senha = input("Digite uma senha: ")

    data = input(
        "Digite a data (dd-mm-yyyy) ou ENTER para hoje: "
    ).strip()

    if not data:
        data = datetime.now().strftime("%d-%m-%Y")

    chave = gerar_chave(senha)
    fernet = Fernet(chave)

    texto_criptografado = (
        fernet.encrypt(texto.encode()).decode()
    )

    diario.adicionar_entrada(
        texto_criptografado,
        data
    )

    print("Diário salvo com sucesso!")


def visualizar_diario(diario):
    registros = diario.listar_todos()

    if not registros:
        print("Nenhum registro encontrado.")
        return

    print("\n=== REGISTROS ===")
    for id_, data in registros:
        print(f"{id_} - {data}")

    try:
        id_escolhido = int(
            input("\nDigite o ID para visualizar: ")
        )
    except ValueError:
        print("ID inválido.")
        return

    senha = input("Digite a senha: ")

    resultado = diario.buscar_por_id(id_escolhido)

    if resultado is None:
        print("Registro não encontrado.")
        return

    try:
        chave = gerar_chave(senha)
        fernet = Fernet(chave)

        texto = (
            fernet.decrypt(
                resultado[0].encode()
            ).decode()
        )

        print("\n=== TEXTO ===")
        print(texto)

    except Exception:
        print("Senha incorreta.")


def main():
    diario = DiarioDB()

    while True:
        print("\n===== DIÁRIO CRIPTOGRAFADO =====")
        print("1 - Adicionar entrada")
        print("2 - Ver entradas")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_diario(diario)

        elif opcao == "2":
            visualizar_diario(diario)

        elif opcao == "3":
            diario.fechar()
            print("Até logo!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()