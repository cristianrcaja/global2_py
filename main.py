if __name__ == "__main__":
    conexao = ConexaoDB()  
    conexao.conectar()  

    sistema = SistemaGerenciamento(conexao)  
    sistema.menu_principal()  

    conexao.fechar()  
