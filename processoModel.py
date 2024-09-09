import sqlite3

class Processo:
    STF = "STF"
    STJ = "STJ"
    conexao = sqlite3.connect('processos.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processos (
        numero_processo TEXT PRIMARY KEY NOT NULL,
        link TEXT NOT NULL,
        data_verificacao TEXT,
        ultimo_html TEXT,
        tribunal TEXT,
        separado BOOL
        )
    ''')
    def __init__(self, numero_processo="", link="", data_verificacao="", ultimo_html="", tribunal="", separado=False):
        self.numero_processo = numero_processo
        self.link = link
        self.data_verificacao = data_verificacao
        self.ultimo_html = ultimo_html
        self.tribunal = tribunal
        self.separado = False
    
    @staticmethod
    def new(numero_processo, link, tribunal, separado, ultimo_html='', data_verificacao=''):
        try:
            Processo.cursor.execute('''
                INSERT INTO processos (numero_processo, link, data_verificacao, ultimo_html, tribunal, separado)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (numero_processo, link, data_verificacao, ultimo_html, tribunal, separado))
            print(f"Processo {numero_processo} incluido no banco de dados com sucesso")
            return Processo(numero_processo, link, data_verificacao, ultimo_html, tribunal, separado)
        except sqlite3.IntegrityError:
            print("Erro! Processo já está incluído no banco de dados")
            return Processo()

    @staticmethod
    def find_by_numero_processo(numero_processo):
        Processo.cursor.execute('SELECT * FROM processos WHERE numero_processo = ?', (numero_processo,))
        tupla = Processo.cursor.fetchone()
        processo = Processo()
        processo.numero_processo = tupla[0]
        processo.link = tupla[1]
        processo.data_verificacao = tupla[2]
        processo.ultimo_html = tupla[3]
        processo.tribunal = tupla[4]
        processo.separado = tupla[5]

        return processo

    @staticmethod
    def save():
        Processo.conexao.commit()
        print("Commitado com sucesso")
    @staticmethod
    def all():
        Processo.cursor.execute('SELECT * FROM processos')
        return Processo.cursor.fetchall()
    
    @staticmethod
    def nao_separados():
        Processo.cursor.execute('SELECT * FROM processos WHERE separado = 0')
        return Processo.cursor.fetchall()
    
    def separados():
        Processo.cursor.execute('SELECT * FROM processos WHERE separado = 1')
        return Processo.cursor.fetchall()
    
    @staticmethod
    def list_by(coluna):
        Processo.cursor.execute(f'SELECT {coluna} FROM processos')
        return Processo.cursor.fetchall()
    
    @staticmethod
    def delete_by_numero_processo(numero_processo):
        Processo.cursor.execute('DELETE FROM processos WHERE numero_processo = ?', (numero_processo,))
    
    def delete(self):
        Processo.cursor.execute('DELETE FROM processos WHERE numero_processo = ?', (self.numero_processo,))

    @staticmethod
    def close():
        Processo.conexao.close()

    @staticmethod
    def update_by_numero_processo(numero_processo, attr):
        for key in attr.keys():
            try:
                Processo.cursor.execute('''
                    UPDATE processos
                    SET {} = ?
                    WHERE numero_processo = ?'''.format(key), (attr[key], numero_processo)
                )
            except sqlite3.IntegrityError:
                print("Erro! Processo não incluído no banco de dados")
                return
        print(f"Os atributos {attr.keys()} foram atualizados.")

    def update(self, attr):
        for key in attr.keys():
            try:
                Processo.cursor.execute('''
                    UPDATE processos
                    SET {} = ?
                    WHERE numero_processo = ?'''.format(key), (attr[key], self.numero_processo)
                )
            except sqlite3.IntegrityError:
                print("Erro! Processo já incluído no banco de dados")
    
