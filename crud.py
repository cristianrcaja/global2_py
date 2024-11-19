import re
import json

class CRUD:
    def __init__(self, conexao):
        self.conexao = conexao

    def inserir_usuario(self, nome, email, senha):
        try:
            if self.verificar_email_existente(email):
                print(f"Erro: O e-mail {email} já está cadastrado.")
                return

            self.validar_nome(nome)
            self.validar_email(email)

            query = """
                INSERT INTO usuario (id_usu, nome, email, senha)
                VALUES (USUARIO_SEQ_NEW_2.NEXTVAL, :1, :2, :3)
            """
            self.conexao.executar_comando(query, [nome, email, senha])
            print(f"Usuário '{nome}' inserido com sucesso!")
        except ValueError as e:
            print(f"Erro de validação: {e}")
        except Exception as e:
            print(f"Erro ao inserir usuário: {e}")

    def consultar_usuarios(self):
        try:
            query = "SELECT id_usu, nome, email FROM usuario"
            usuarios = self.conexao.executar_consulta(query)
            
            for usuario in usuarios:
                print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}")
            return usuarios
        except Exception as e:
            print(f"Erro ao consultar usuários: {e}")
            return []

    def verificar_email_existente(self, email):
        try:
            query = "SELECT COUNT(*) FROM usuario WHERE email = :1"
            resultado = self.conexao.executar_consulta(query, [email])
            return resultado[0][0] > 0
        except Exception as e:
            print(f"Erro ao verificar e-mail: {e}")
            return False

    def excluir_usuario(self, id_usuario):
        try:
            if not self.usuario_existe(id_usuario):
                print(f"Erro: Usuário com ID {id_usuario} não encontrado.")
                return

            query = "DELETE FROM usuario WHERE id_usu = :1"
            self.conexao.executar_comando(query, [id_usuario])
            print(f"Usuário com ID {id_usuario} excluído com sucesso!")
        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")

    def atualizar_usuario(self, id_usuario, nome=None, email=None, senha=None):
        try:
            if not self.usuario_existe(id_usuario):
                print(f"Erro: Usuário com ID {id_usuario} não encontrado.")
                return

            campos = []
            valores = []
            if nome:
                self.validar_nome(nome)
                campos.append("nome = :1")
                valores.append(nome)
            if email:
                self.validar_email(email)
                campos.append("email = :2")
                valores.append(email)
            if senha:
                campos.append("senha = :3")
                valores.append(senha)

            if campos:
                query = f"UPDATE usuario SET {', '.join(campos)} WHERE id_usu = :4"
                valores.append(id_usuario)
                self.conexao.executar_comando(query, valores)
                print(f"Usuário com ID {id_usuario} atualizado com sucesso!")
            else:
                print("Erro: Nenhum dado válido fornecido para atualização.")
        except ValueError as e:
            print(f"Erro de validação: {e}")
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")

    def usuario_existe(self, id_usuario):
        try:
            query = "SELECT COUNT(*) FROM usuario WHERE id_usu = :1"
            resultado = self.conexao.executar_consulta(query, [id_usuario])
            return resultado[0][0] > 0
        except Exception as e:
            print(f"Erro ao verificar existência do usuário: {e}")
            return False

    def inserir_consumo(self, id_usuario, consumo_energia_kwh, consumo_gas_m3):
        try:
            self.validar_consumo(consumo_energia_kwh, consumo_gas_m3)
            query = "INSERT INTO consumo (id_usuario, consumo_energia_kwh, consumo_gas_m3) VALUES (:1, :2, :3)"
            self.conexao.executar_comando(query, [id_usuario, consumo_energia_kwh, consumo_gas_m3])
            print(f"Dados de consumo para o usuário {id_usuario} registrados com sucesso!")
        except ValueError as e:
            print(f"Erro de validação: {e}")
        except Exception as e:
            print(f"Erro ao inserir dados de consumo: {e}")

    def consultar_consumo(self, id_usuario):
        try:
            query = "SELECT * FROM consumo WHERE id_usuario = :1"
            resultados = self.conexao.executar_consulta(query, [id_usuario])
            return resultados
        except Exception as e:
            print(f"Erro ao consultar consumo: {e}")
            return []

    def calcular_emissoes_co2(self, consumo_energia_kwh, consumo_gas_m3):
        try:
            consumo_energia_kwh = float(consumo_energia_kwh)
            consumo_gas_m3 = float(consumo_gas_m3)

            emissao_energia_co2 = consumo_energia_kwh * 0.475  
            emissao_gas_co2 = consumo_gas_m3 * 2.05  
            return emissao_energia_co2 + emissao_gas_co2
        except ValueError as e:
            print(f"Erro ao calcular emissões de CO2: {e}")
            return 0

    def calcular_custo(self, consumo_energia_kwh, consumo_gas_m3):
        try:
            consumo_energia_kwh = float(consumo_energia_kwh)
            consumo_gas_m3 = float(consumo_gas_m3)

            custo_energia = consumo_energia_kwh * 0.50  
            custo_gas = consumo_gas_m3 * 1.50  
            return custo_energia + custo_gas
        except ValueError as e:
            print(f"Erro ao calcular custo: {e}")
            return 0

    def fornecer_orientacoes(self, consumo_energia_kwh, consumo_gas_m3):
        orientacoes = []
        try:
            consumo_energia_kwh = float(consumo_energia_kwh)
            consumo_gas_m3 = float(consumo_gas_m3)

            if consumo_energia_kwh > 300:
                orientacoes.append("Considere reduzir o uso de ar-condicionado e iluminação.")
            if consumo_gas_m3 > 50:
                orientacoes.append("Verifique vazamentos de gás e otimize o uso de aquecedores.")
        except ValueError as e:
            print(f"Erro ao converter os dados de consumo: {e}")

        return orientacoes

    def exportar_dados_para_json(self, id_usuario, file_path="dados_usuario.json"):
        try:
            
            query_usuario = "SELECT id_usu, nome, email FROM usuario WHERE id_usu = :1"
            usuario = self.conexao.executar_consulta(query_usuario, [id_usuario])
            
            if not usuario:
                print(f"Erro: Usuário com ID {id_usuario} não encontrado.")
                return
            
            
            query_consumo = "SELECT consumo_energia_kwh, consumo_gas_m3 FROM consumo WHERE id_usuario = :1"
            consumo = self.conexao.executar_consulta(query_consumo, [id_usuario])

            
            dados_usuario = {
                "id": usuario[0][0],  
                "nome": usuario[0][1], 
                "email": usuario[0][2],  
                "consumo": [
                    {
                        "energia_kwh": item[0],  
                        "gas_m3": item[1]  
                    } for item in consumo
                ]
            }

            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(dados_usuario, f, ensure_ascii=False, indent=4)

            print(f"Dados exportados com sucesso para {file_path}.")
        except Exception as e:
            print(f"Erro ao exportar dados completos para JSON: {e}")
    
    def validar_nome(self, nome):
        if not nome or len(nome) < 3:
            raise ValueError("O nome deve ter pelo menos 3 caracteres.")
        return True

    def validar_email(self, email):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError("E-mail inválido.")
        return True

    def validar_consumo(self, consumo_energia_kwh, consumo_gas_m3):
        if consumo_energia_kwh < 0 or consumo_gas_m3 < 0:
            raise ValueError("Os valores de consumo não podem ser negativos.")
        return True
