import json

class SistemaGerenciamento:
    def __init__(self, crud):
        self.crud = crud

    def exibir_menu(self):
        print("\n🎉 Bem-vindo ao Sistema Luminis 🎉")
        print("⚡ Menu Principal ⚡")
        print("1️⃣ Inserir Consumo de Energia")
        print("2️⃣ Alterar Consumo de Energia")
        print("3️⃣ Excluir Consumo de Energia")
        print("4️⃣ Consultar Consumos")
        print("5️⃣ Exportar Consultas para JSON")
        print("❌ Sair")
    
    def executar(self):
        while True:
            self.exibir_menu()
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.inserir_consumo()
            elif opcao == '2':
                self.alterar_consumo()
            elif opcao == '3':
                self.excluir_consumo()
            elif opcao == '4':
                self.consultar_consumos()
            elif opcao == '5':
                self.exportar_consultas_para_json()
            elif opcao.lower() == '❌' or opcao == '6':
                print("🚪 Saindo... Até logo! 👋")
                break
            else:
                print("❗ Opção inválida! Tente novamente.")

    def inserir_consumo(self):
        print("\n🔧 Inserir Consumo de Energia 🔧")
        tipo_energia = input("Tipo de Energia (Ex: Elétrica, Gás, etc.): ")
        consumo = input("Consumo (em kWh ou unidades): ")
        custo_unitario = input("Custo Unitário (R$): ")
        emissao_co2 = input("Emissão de CO₂ (kg): ")

        # Confirmação da inserção
        print(f"\n💡 Você está prestes a inserir os seguintes dados:")
        print(f"Tipo de Energia: {tipo_energia}")
        print(f"Consumo: {consumo} kWh")
        print(f"Custo Unitário: R$ {custo_unitario}")
        print(f"Emissão de CO₂: {emissao_co2} kg")

        confirmacao = input("Confirma? (s/n): ").strip().lower()
        if confirmacao == 's':
            self.crud.inserir_consumo(tipo_energia, consumo, custo_unitario, emissao_co2, None)
            print("✅ Consumo de energia inserido com sucesso!")
        else:
            print("❌ Operação cancelada.")

    def alterar_consumo(self):
        print("\n✏️ Alterar Consumo de Energia ✏️")
        consumo_id = input("ID do consumo a ser alterado: ")
        tipo_energia = input("Novo Tipo de Energia: ")
        consumo = input("Novo Consumo: ")
        custo_unitario = input("Novo Custo Unitário: ")
        emissao_co2 = input("Nova Emissão de CO₂: ")

        self.crud.alterar_consumo(consumo_id, tipo_energia, consumo, custo_unitario, emissao_co2, None)
        print("✅ Consumo de energia alterado com sucesso!")

    def excluir_consumo(self):
        print("\n🗑️ Excluir Consumo de Energia 🗑️")
        consumo_id = input("ID do consumo a ser excluído: ")
        self.crud.excluir_consumo(consumo_id)
        print("✅ Consumo de energia excluído com sucesso!")

    def consultar_consumos(self):
        print("\n🔍 Consultar Consumos de Energia 🔍")
        filtro = input("Digite o filtro para a consulta (deixe em branco para consultar todos): ")
        consumos = self.crud.consultar_consumos(filtro)
        
        if consumos:
            print("💡 Consumos encontrados:")
            for consumo in consumos:
                print(consumo)
        else:
            print("❌ Nenhum consumo encontrado.")

    def exportar_consultas_para_json(self):
        print("\n💾 Exportando consultas para JSON... 💾")
        consumos = self.crud.consultar_consumos('')
        dados_json = json.dumps(consumos, default=str)

        with open('consumos.json', 'w') as f:
            f.write(dados_json)
        
        print("✅ Dados exportados para consumos.json com sucesso!")
