import oracledb

class ConexaoDB:
    def __init__(self, usuario, senha, dsn):
        self.usuario = usuario
        self.senha = senha
        self.dsn = dsn
        self.conexao = None

    def conectar(self):
        try:
            
            self.conexao = oracledb.connect(user=self.usuario, password=self.senha, dsn=self.dsn)
            print("Conexão estabelecida com sucesso!")
        except oracledb.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def cursor(self):
        """
        Método que retorna um cursor para realizar operações no banco de dados.
        """
        if self.conexao:
            return self.conexao.cursor()
        else:
            raise Exception("Conexão com o banco de dados não estabelecida!")

    def commit(self):
        """
        Método para confirmar a transação.
        """
        if self.conexao:
            self.conexao.commit()  
        else:
            raise Exception("Conexão com o banco de dados não estabelecida!")

    def fechar_conexao(self):
        """
        Método para fechar a conexão com o banco de dados.
        """
        if self.conexao:
            self.conexao.close()
            print("Conexão fechada com sucesso!")

    def executar_consulta(self, query, parametros=None):
        """
        Método para executar uma consulta no banco de dados e retornar os resultados.
        """
        try:
            cur = self.cursor()
            if parametros:
                cur.execute(query, parametros)
            else:
                cur.execute(query)
            resultados = cur.fetchall()  
            cur.close()
            return resultados
        except oracledb.Error as e:
            print(f"Erro ao executar consulta: {e}")
            raise

    def executar_comando(self, query, parametros=None):
        """
        Método para executar comandos SQL como INSERT, UPDATE, DELETE.
        """
        try:
            cur = self.cursor()
            if parametros:
                cur.execute(query, parametros)
            else:
                cur.execute(query)
            self.commit()  
            cur.close()
        except oracledb.Error as e:
            print(f"Erro ao executar comando: {e}")
            raise
