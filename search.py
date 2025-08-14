from main import DiarioDB
from cryptography.fernet import Fernet
import base64
import hashlib

def gerar_chave(senha):
    return base64.urlsafe_b64encode(hashlib.sha256(senha.encode()).digest())

def main():
    diario = DiarioDB()
    escolha = input(
        "Digite 'data' para buscar por data ou 'todos' para listar todos registros: "
    ).strip().lower()

    if escolha == 'data':
        data = input("Digite a data (dd-mm-yyyy): ").strip()
        resultados = diario.buscar_por_data(data)
        if resultados:
            print(f"Entradas para {data}:")
            for id_, texto_cripto, data_envio in resultados:
                print(f"[{id_}] {data_envio}")
        else:
            print(f"Nenhuma entrada encontrada para {data}.")

    elif escolha == 'todos':
        registros = diario.listar_todos()
        if registros:
            print("ID | Data")
            for id_, data_envio in registros:
                print(f"{id_} | {data_envio}")
        else:
            print("Nenhum registro encontrado.")
    else:
        print("Opção inválida.")
        diario.fechar()
        return

    # Perguntar se quer ver algum registro
    ver = input("Quer ver o texto de algum registro? (s/n): ").strip().lower()
    if ver == 's':
        try:
            id_ver = int(input("Digite o ID do registro: "))
        except ValueError:
            print("ID inválido.")
            diario.fechar()
            return

        senha = input("Digite a senha para descriptografar: ")
        chave = gerar_chave(senha)
        fernet = Fernet(chave)

        dado = diario.buscar_por_id(id_ver)
        if dado is None:
            print("Registro não encontrado.")
            diario.fechar()
            return

        texto_cripto = dado[0]

        try:
            texto = fernet.decrypt(texto_cripto.encode()).decode()
            print(f"Texto descriptografado:\n{texto}")
        except:
            print("Senha incorreta.")

    diario.fechar()

if __name__ == "__main__":
    main()
