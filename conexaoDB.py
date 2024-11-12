import oracledb

class ConexaoDB:
    def __init__(self):
        self.dsn = "oracle.fiap.com.br:1521/orcl"
        self.user = "rm558502"
        self.password = "080504"
        self.connection = None

    def conectar(self):
        try:
            self.connection = oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)
            print("🔌 Conexão estabelecida com o banco de dados Oracle!")
        except oracledb.DatabaseError as e:
            print(f"❌ Erro na conexão com o banco: {e}")
    
    def fechar_conexao(self):
        if self.connection:
            self.connection.close()
            print("🔒 Conexão fechada com sucesso.")
    
    def executar_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except oracledb.DatabaseError as e:
            print(f"❌ Erro ao executar a consulta: {e}")
            return []
    
    def executar_update(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
            print("✅ Operação realizada com sucesso!")
        except oracledb.DatabaseError as e:
            print(f"❌ Erro ao realizar operação: {e}")
            self.connection.rollback()
