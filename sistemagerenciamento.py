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