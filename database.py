import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('fingest.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Tabela de transações
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT CHECK(tipo IN ('receita', 'despesa')),
                categoria TEXT,
                valor REAL,
                descricao TEXT,
                data TEXT
            )
        ''')
        
        # Tabela de poupanças
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS poupancas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                valor_meta REAL,
                valor_atual REAL DEFAULT 0
            )
        ''')
        
        self.conn.commit()
    
    def add_transacao(self, tipo, categoria, valor, descricao):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO transacoes (tipo, categoria, valor, descricao, data)
            VALUES (?, ?, ?, ?, ?)
        ''', (tipo, categoria, float(valor), descricao, data))
        self.conn.commit()
    
    def get_transacoes(self, limite=50):
        self.cursor.execute('''
            SELECT id, tipo, categoria, valor, descricao, data 
            FROM transacoes ORDER BY data DESC LIMIT ?
        ''', (limite,))
        return self.cursor.fetchall()
    
    def get_saldo(self):
        # Total de receitas
        self.cursor.execute('SELECT SUM(valor) FROM transacoes WHERE tipo = "receita"')
        receitas = self.cursor.fetchone()[0]
        if receitas is None:
            receitas = 0
        
        # Total de despesas
        self.cursor.execute('SELECT SUM(valor) FROM transacoes WHERE tipo = "despesa"')
        despesas = self.cursor.fetchone()[0]
        if despesas is None:
            despesas = 0
        
        return float(receitas) - float(despesas)
    
    def add_poupanca(self, nome, valor_meta):
        self.cursor.execute('''
            INSERT INTO poupancas (nome, valor_meta)
            VALUES (?, ?)
        ''', (nome, float(valor_meta)))
        self.conn.commit()
    
    def get_poupancas(self):
        self.cursor.execute('SELECT id, nome, valor_meta, valor_atual FROM poupancas')
        return self.cursor.fetchall()
    
    def update_poupanca(self, id, valor_atual):
        self.cursor.execute('''
            UPDATE poupancas SET valor_atual = ? WHERE id = ?
        ''', (float(valor_atual), id))
        self.conn.commit()
    
    def delete_transacao(self, id):
        self.cursor.execute('DELETE FROM transacoes WHERE id = ?', (id,))
        self.conn.commit()
    
    def calcular_poupanca_mensal(self):
        """Calcula quanto pode poupar por mês (receitas - despesas)"""
        return self.get_saldo()
    
    def close(self):
        self.conn.close()