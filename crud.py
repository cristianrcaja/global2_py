class CRUD:
    def __init__(self, conexao):
        self.conexao = conexao

    def inserir_consumo(self, tipo_energia, consumo, custo_unitario, emissao_co2):
        query = """INSERT INTO consumos (tipo_energia, consumo, custo_unitario, emissao_co2)
                   VALUES (:1, :2, :3, :4)"""
        self.conexao.executar_update(query, (tipo_energia, consumo, custo_unitario, emissao_co2))

    def alterar_consumo(self, consumo_id, tipo_energia, consumo, custo_unitario, emissao_co2):
        query = """UPDATE consumos
                   SET tipo_energia = :1, consumo = :2, custo_unitario = :3, emissao_co2 = :4
                   WHERE consumo_id = :5"""
        self.conexao.executar_update(query, (tipo_energia, consumo, custo_unitario, emissao_co2, consumo_id))

    def excluir_consumo(self, consumo_id):
        query = "DELETE FROM consumos WHERE consumo_id = :1"
        self.conexao.executar_update(query, (consumo_id,))

    def consultar_consumos(self, filtro=""):
        query = """SELECT * FROM consumos WHERE tipo_energia LIKE :1"""
        return self.conexao.executar_query(query, (f"%{filtro}%",))

    def exportar_para_json(self, dados):
        import json
        with open("consumos.json", "w") as file:
            json.dump(dados, file, indent=4)
        print("✅ Dados exportados para consumos.json com sucesso!")
