from ConexaoDB import ConexaoDB
from CRUD import CRUD
from SistemaGerenciamento import SistemaGerenciamento


conexao = ConexaoDB('rm558502', '080504', 'oracle.fiap.com.br:1521/orcl')
conexao.conectar()


crud = CRUD(conexao)


sistema = SistemaGerenciamento(conexao, crud)


sistema.menu_principal()
