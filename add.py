from main import DiarioDB
from cryptography.fernet import Fernet
import base64
import hashlib
from datetime import datetime

def gerar_chave(senha):
    return base64.urlsafe_b64encode(hashlib.sha256(senha.encode()).digest())

def main():
    diario = DiarioDB()
    texto = input("Digite o que deseja guardar: ")
    senha = input("Digite a senha o qual descriptografara o seu diario: ")
    data = input("Digite a data (dd/mm/yyyy) ou aperte ENTER para hoje: ").strip()
    if data == '':
        data = datetime.now().strftime('%d-%m-%Y')

    chave = gerar_chave(senha)
    fernet = Fernet(chave)
    texto_criptografado = fernet.encrypt(texto.encode()).decode()

    diario.adicionar_entrada(texto_criptografado, data)
    print("Seu diario foi criptografado com sucesso!")
    diario.fechar()

if __name__ == "__main__":
    main()
