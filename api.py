from flask import Flask, render_template, request, jsonify
from sqlalchemy import select
from flask_pydantic_spec import FlaskPydanticSpec
from flask_jwt_extended import get_jwt_identity, JWTManager, create_access_token, jwt_required
from functools import wraps
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'senha'
jwt = JWTManager(app)

#admin_required

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    cpf = dados['cpf']
    senha = dados['senha']
    db_session = local_session()
    try:
        sql = select(Cliente).where(Cliente.cpf == cpf)
        user = db_session.execute(sql).scalar()
        if user and user.check_password_hash(senha):
            access_token = create_access_token(identity=cpf)
            return jsonify(access_token=access_token)
        return jsonify({"mensagem": "Erro ao login"}), 401
    finally:
        db_session.close() #finalizar a rota

@app.route('/cadastro_produto', methods=['POST'])
def cadastro_produto():
    dados = request.get_json()
    db_session = local_session()
    try:
        sql = select(Cliente).where(Cliente.cpf == cpf)
        user = db_session.execute(sql).scalar()

        if user and user.check_password_hash(senha):
            access_token = create_access_token(identity=cpf)
            return jsonify(access_token=access_token)
        return jsonify({"mensagem": "Erro ao login"}), 401
    finally:
        db_session.close() #finalizar a rota

@app.route('/cadastro_clientes', methods=['POST'])
def cadastro_vendedor():
    db_session = local_session()
    try:
        dados = request.get_json()
        if (not dados['nome']
                or not dados['cpf']
                or not dados['telefone']
                or not dados['endereco']):
            return jsonify({'error': 'Preencha todos os campos'})
        else:
            print(dados)
            sql = select(Cliente).where(Cliente.telefone == dados['telefone'])
            telefone_existe = db_session.execute(sql).scalar()
            print(telefone_existe)

            sql = select(Cliente).where(Cliente.cpf == dados['cpf'])
            cpf_existe = db_session.execute(sql).scalar()
            print(cpf_existe)

            if telefone_existe:
                return jsonify({
                    "erro": "esse telefone ja existe!"
                }), 400

            if cpf_existe:
                return jsonify({

                    "erro": "esse cpf já existe!"
                }), 400

    except ValueError:
        return jsonify({'Error': 'Não foi possível cadastrar'})
    finally:
        db_session.close()

@app.route('/consulta_vendedor', methods=["GET"])
def consulta_vendedor():
    db_session = local_session()
    sql_lista = select(Cliente)
    lista_resultado = db_session.execute(sql_lista).scalars().all()
    resultado_lista = []
    for n in lista_resultado:
        resultado_lista.append(n.serialize_user())

    return (jsonify({'lista': resultado_lista})

@app.route('/consulta_usuario', methods=["GET"]))
def consulta_usuario():
    db_session = local_session()
    sql_lista = select(Cliente)
    lista_resultado = db_session.execute(sql_lista).scalars().all()
    resultado_lista = []
    for n in lista_resultado:
        resultado_lista.append(n.serialize_user())

    return jsonify({'lista': resultado_lista})
