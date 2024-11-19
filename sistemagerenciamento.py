class SistemaGerenciamento:
    def __init__(self, db, crud):
        self.db = db
        self.crud = crud

    def menu_principal(self):
        while True:
            print("\n1. Cadastrar usuário")
            print("2. Cadastrar dados de consumo")
            print("3. Consultar dados de consumo")
            print("4. Exportar dados para JSON")
            print("5. Calcular impacto ambiental")
            print("6. Listar todos usuários cadastrados")
            print("7. Atualizar usuário")
            print("8. Excluir usuário")
            print("0. Sair")
            opcao = input("Escolha uma opção: ")
            self.executar_opcao(opcao)

    def executar_opcao(self, opcao):
        if opcao == '1':
            self.cadastrar_usuario()
        elif opcao == '2':
            self.cadastrar_consumo()
        elif opcao == '3':
            self.consultar_consumo()
        elif opcao == '4':
            self.exportar_dados_json()
        elif opcao == '5':
            self.calcular_impacto_ambiental()
        elif opcao == '6':
            self.listar_usuarios()
        elif opcao == '7':
            self.atualizar_usuario()
        elif opcao == '8':
            self.excluir_usuario()
        elif opcao == '0':
            print("Saindo...")
            self.db.fechar_conexao()
            exit()
        else:
            print("Opção inválida!")

    def cadastrar_usuario(self):
        nome = input("Nome: ")
        email = input("Email: ")
        senha = input("Senha: ")

        if self.crud.verificar_email_existente(email):
            print("Erro: Email já está cadastrado!")
            return

        self.crud.inserir_usuario(nome, email, senha)

    def cadastrar_consumo(self):
        id_usuario = self.obter_id_usuario()
        consumo_energia_kwh = self.obter_valor_consumo("Consumo de energia elétrica (kWh): ")
        consumo_gas_m3 = self.obter_valor_consumo("Consumo de gás (m³): ")

        self.crud.inserir_consumo(id_usuario, consumo_energia_kwh, consumo_gas_m3)

    def obter_id_usuario(self):
        while True:
            try:
                id_usuario = int(input("ID do usuário: "))
                if id_usuario <= 0:
                    print("Erro: ID deve ser um número positivo.")
                else:
                    return id_usuario
            except ValueError:
                print("Erro: ID inválido. Por favor, insira um número válido.")

    def obter_valor_consumo(self, mensagem):
        while True:
            try:
                valor = float(input(mensagem))
                if valor < 0:
                    print("Erro: O valor não pode ser negativo.")
                else:
                    return valor
            except ValueError:
                print("Erro: Entrada inválida. Por favor, insira um número.")

    def consultar_consumo(self):
        id_usuario = self.obter_id_usuario()
        consumo = self.crud.consultar_consumo(id_usuario)
        if consumo:
            print("Dados de consumo:")
            for item in consumo:
                print(f"Consumo de energia: {item[1]} kWh, Consumo de gás: {item[2]} m³")
        else:
            print("Nenhum dado de consumo encontrado.")

    def exportar_dados_json(self):
        id_usuario = self.obter_id_usuario()
        consumo = self.crud.consultar_consumo(id_usuario)
        if consumo:
            file_path = f"consumo_usuario_{id_usuario}.json"
            self.crud.exportar_dados_para_json(id_usuario, file_path)  
        else:
            print("Nenhum dado encontrado para exportar.")

    def calcular_impacto_ambiental(self):
        id_usuario = self.obter_id_usuario()
        consumo = self.crud.consultar_consumo(id_usuario)
        if consumo:
            for item in consumo:
                energia_kwh = item[1]  
                gas_m3 = item[2]  
                emissao_co2 = self.crud.calcular_emissoes_co2(energia_kwh, gas_m3)
                custo = self.crud.calcular_custo(energia_kwh, gas_m3)
                orientacoes = self.crud.fornecer_orientacoes(energia_kwh, gas_m3)
                print(f"Impacto ambiental: {emissao_co2:.2f} kg CO2")
                print(f"Custo estimado: R${custo:.2f}")
                print("Sugestões de economia:")
                for orientacao in orientacoes:
                    print(f"- {orientacao}")
        else:
            print("Nenhum dado de consumo encontrado para cálculo.")

    def listar_usuarios(self):
        usuarios = self.crud.consultar_usuarios()
        if usuarios:
            print("\nUsuários cadastrados:")
            for usuario in usuarios:
                print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}")
        else:
            print("Nenhum usuário encontrado.")

    def atualizar_usuario(self):
        id_usuario = input("Digite o ID do usuário para atualizar: ")
        if not self.crud.usuario_existe(id_usuario):
            print("Usuário não encontrado!")
            return
        
        nome = input("Novo nome (deixe em branco para não alterar): ")
        email = input("Novo email (deixe em branco para não alterar): ")
        senha = input("Nova senha (deixe em branco para não alterar): ")

        self.crud.atualizar_usuario(id_usuario, nome, email, senha)

    def excluir_usuario(self):
        id_usuario = input("Digite o ID do usuário para excluir: ")
        if not self.crud.usuario_existe(id_usuario):
            print("Usuário não encontrado!")
            return
        
        confirmacao = input(f"Tem certeza que deseja excluir o usuário com ID {id_usuario}? (s/n): ")
        if confirmacao.lower() == 's':
            self.crud.excluir_usuario(id_usuario)
        else:
            print("Exclusão cancelada.")
