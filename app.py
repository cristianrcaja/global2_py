from flask import Flask, request, jsonify
from ConexaoDB import ConexaoDB
from CRUD import CRUD
from SistemaGerenciamento import SistemaGerenciamento

app = Flask(__name__)


conexao = ConexaoDB('rm558502', '080504', 'oracle.fiap.com.br:1521/orcl')
conexao.conectar()


crud = CRUD(conexao)


sistema = SistemaGerenciamento(conexao, crud)


@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    try:
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        crud.inserir_usuario(nome, email, senha)
        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"message": f"Erro ao cadastrar usuário: {str(e)}"}), 500


@app.route('/usuarios/<int:id_usuario>/consumo', methods=['POST'])
def cadastrar_consumo(id_usuario):
    try:
        data = request.get_json()
        consumo_energia_kwh = data.get('consumo_energia_kwh')
        consumo_gas_m3 = data.get('consumo_gas_m3')
        crud.inserir_consumo(id_usuario, consumo_energia_kwh, consumo_gas_m3)
        return jsonify({"message": "Consumo registrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"message": f"Erro ao registrar consumo: {str(e)}"}), 500


@app.route('/usuarios/<int:id_usuario>/consumo', methods=['GET'])
def consultar_consumo(id_usuario):
    try:
        consumo = crud.consultar_consumo(id_usuario)
        return jsonify(consumo), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao consultar consumo: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
