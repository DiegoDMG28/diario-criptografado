import sqlite3

class DiarioDB:
    def __init__(self, nome_arquivo='diario.db'):
        self.nome_arquivo = nome_arquivo
        self.conectar()
        self.criar_tabela()

    def conectar(self):
        self.conn = sqlite3.connect(self.nome_arquivo)
        self.cursor = self.conn.cursor()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS diario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto_criptografado TEXT NOT NULL,
                data_envio TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def adicionar_entrada(self, texto_criptografado, data_envio):
        self.cursor.execute(
            'INSERT INTO diario (texto_criptografado, data_envio) VALUES (?, ?)',
            (texto_criptografado, data_envio)
        )
        self.conn.commit()

    def buscar_por_data(self, data):
        self.cursor.execute(
            'SELECT id, texto_criptografado, data_envio FROM diario WHERE data_envio = ?',
            (data,)
        )
        return self.cursor.fetchall()

    def listar_todos(self):
        self.cursor.execute(
            'SELECT id, data_envio FROM diario ORDER BY data_envio DESC'
        )
        return self.cursor.fetchall()

    def buscar_por_id(self, id_):
        self.cursor.execute(
            'SELECT texto_criptografado FROM diario WHERE id = ?',
            (id_,)
        )
        return self.cursor.fetchone()

    def fechar(self):
        self.conn.close()
