from flask import Flask, request, jsonify, redirect
from sqlalchemy import create_engine, select
from functools import wraps
from flask_pydantic_spec import FlaskPydanticSpec
from models import Produto, db_session, Usuario, Movimentacao, Pedido, Blog, local_session

from sqlalchemy import select
from flask_jwt_extended import get_jwt_identity, JWTManager, create_access_token

app = Flask(__name__)
spec = FlaskPydanticSpec( 'Flask',
                         title = 'Flask API',
                         version = '1.0.0')
spec.register(app)
app.config['SECRET_KEY'] = 'secret!'
jwt = JWTManager(app)

#requirimento de ademistrador, se ele tem permissao para entrar
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        print(current_user)
        try:
            user = db_session.execute(select(Usuario).where(Usuario.email == current_user)).scalar()
            print(user)
            if user and user.papel == "admin":
                return fn(*args, **kwargs)
            return jsonify({"msg":"Acesso negado"}),403
        finally:
            db_session.close()
    return wrapper

@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to raizes do Brasil!',
    })

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados['email']
    senha = dados['senha']

    db = local_session()

    try:
        sql = select(Usuario).where(Usuario.email == email)
        user = db.execute(sql).scalar()

        if user and user.check_password(senha):
            print("if login")
            access_token = create_access_token(identity=str(user.email))
            return jsonify({
                "access_token":access_token,
                "papel": user.papel,
            }), 200
        return jsonify({"msg": "Credenciais inválidas"}), 401
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 500
    finally:
        db.close()

@app.route('/cadastro/usuario', methods=['POST'])
def cadastrar_usuario():
    try:
        dados = request.get_json()
        if not dados["nome"] or not dados["CPF"] or not dados[
            "papel"] or not dados["email"] or not dados["password"]:
            return jsonify({"error", "preencher todos os campos"}), 400
        else:

            CPF = select(Usuario).where(Usuario.CPF == dados["CPF"])
            CPF = db_session.execute(CPF).scalars().first()

            if not CPF:
                usuario = Usuario(
                    nome=dados["nome"],
                    CPF=dados["CPF"],
                    papel=dados["papel"],
                    email=dados["email"],
                    password=dados["password"]
                )

                usuario.save()
                db_session.close()
                return jsonify({"cadastro_usuario": 'Cadrasto'}), 200
            else:
                return jsonify({"CPF": 'O CPF ja existe'}), 400

    except ValueError:
        return jsonify({'Erro no cadastro'}), 400

@app.route('/cadastro/produto',methods=['POST'])
def cadastro_produto():
    try:
        dados = request.get_json()
        print(dados)
        if not dados['nome_produto'] or not dados['dimesao_produto'] or not dados['preco_produto'] or not dados['peso_produto'] or not dados['cor_produto'] or not dados['descricao_produto']:
            return jsonify({"error", "preencher todos os campos"}), 400

        else:
            produto = Produto(
                nome=dados['nome_produto'],
                dimensao=dados['dimesao_produto'],
                preco=dados['preco_produto'],
                peso=dados['peso_produto'],
                cor=dados['cor_produto'],
                descricao=dados['descricao_produto']

            )

            produto.save()
            db_session.close()
            return jsonify({"msg": "Produto cadastrado"}),200
    except ValueError:
        return jsonify({'mensagem':'Erro de cadasro'}),400

@app.route('/consulta/usuario/<int:id>', methods=['GET'])
def consulta_usuario(id):
    try:
        var_usuario = select(Usuario).where(Usuario.id == id)
        var_usuario = db_session.execute(var_usuario).scalar()
        print(var_usuario)
        usuario_resultado = {
            "id": var_usuario.id,
            "nome": var_usuario.nome,
            "email": var_usuario.email,
            "papel": var_usuario.papel,
        }
        print(usuario_resultado)
        return jsonify({'Usuario' :usuario_resultado}),200
    except ValueError:
        return jsonify({'mensagem':'Erro de cadasro'}), 400

@app.route('/consulta/produto/<int:id>', methods=['GET'])
def consulta_produto(id):
    try:
        var_produto = select(Produto).where(Produto.id == id)
        var_produto = db_session.execute(var_produto).scalar()
        print(var_produto)
        produto_resultado = {
            "nome": var_produto.nome,
            "dimensao": var_produto.dimensao,
            "preco": var_produto.preco,
            "peso": var_produto.peso,
            "cor": var_produto.cor,
            "descricao": var_produto.descricao,
        }
        print(produto_resultado)
        return jsonify({'Produto' :produto_resultado}),200
    except ValueError:
        return jsonify({'mensagem':'Erro de cadasro'}), 400

@app.route('/cadastro/blog/<int:id>', methods=['POST'])
def cadastro_blog(id):
    try:
        dados = request.get_json()
        if not dados["usuario_id"] or not dados["comentario"] or not dados["titulo"] or not dados["data"]:
            return jsonify({'mensagem':'Erro de cadasro'}), 400
        else:
            blogs = Blog (
                usuario_id=dados["usuario_id"],
                comentario=dados["comentario"],
                titulo=dados["titulo"],
                data=dados["data"],
            )
            blogs.save()
            db_session.close()
            return jsonify({'cadastro blog': 'Comentario cadastrado com sucesso'})

    except ValueError:
        return jsonify({'mensagem':'Erro de cadasro'}), 400

@app.route('/cadastro/movimentacao/<int:id>', methods=['POST'])
def cadastro_movimentacao():
    try:
        dados = request.get_json()
        if not dados ["data1"] or not dados ['status'] or not dados ['quantidade'] or not dados ['produto_id'] :
            return jsonify({'mensagem':'Erro de cadasro'}), 400
        else:
            movimentacao = Movimentacao (
                data1=dados["data1"],
                status=dados["status"],
                quantidade=dados["quantidade"],
                produto_id=dados["produto_id"],
            )
            movimentacao.save()
            db_session.close()
            return jsonify({'cadastro movimentação': 'movimentação cadastrado com sucesso'})
    except ValueError:
        return jsonify({'mensagem':'Erro de cadasro'}), 400


@app.route('/cadastro/pedido/<int:id>', methods=['POST'])
def cadastro_pedido():
    try:
        dados = request.get_json()
        if not dados ['produto_id'] or not dados ['vendedor_id'] or not dados ['quantidade'] or not dados ['valor_total'] or not dados ['endereco'] or not dados ['usuario_id'] :
            return jsonify({'mensagem':'Erro de cadasro'}), 400
        else:
            pedido = Pedido (
                produto_id=dados["produto_id"],
                vendedor_id=dados["vendedor_id"],
                quantidade=dados["quantidade"],
                valor_total=dados["valor_total"],
                endereco=dados["endereco"],
                usuario_id=dados["usuario_id"],
            )
            pedido.save()
            db_session.close()
            return jsonify({'cadastro pedido': 'pedido cadastrado com sucesso'})
    except ValueError:
        return jsonify({'mensagem':'Erro de cadasro'}), 400

@app.route('/consulta/blog/<int:id>', methods=['GET'])
def consulta_blog_id(usuario_id):
    try:
        var_blog = select(Blog).where(Blog.usuario_id == usuario_id)
        var_blog = db_session.execute(var_blog).scalar()
        print(var_blog)
        blog_resultado = {
            "usuario_id": var_blog.usuario_id,
            "comentario": var_blog.comentario,
            "titulo": var_blog.titulo,
            "data": var_blog.data,
        }
        print(blog_resultado)
        return jsonify({'blog': blog_resultado}),200
    except ValueError:
        return jsonify({'mensagem':'Erro de cadastro'}), 400


@app.route('/consulta/pedido/<int:id>', methods=['GET'])
def consulta_pedido_id(usuario_id):
    try:
        var_pedido = select(Pedido).where(Pedido.usuario_id == usuario_id)
        var_pedido = db_session.execute(var_pedido).scalar()
        print(var_pedido)
        pedido_resultado = {

            "vendedor_id": var_pedido.vendedor_id,
            "quantidade": var_pedido.quantidade,
            "valor_total": var_pedido.valor_total,
            "endereco": var_pedido.endereco,
            "usuario_id": var_pedido.usuario_id,
        }
        print(pedido_resultado)
        return jsonify({'pedido': pedido_resultado}),200
    except ValueError:
        return jsonify({'mensagem':'Erro de cadastro'}), 400

@app.route('/consulta/movimentacao/<int:id>', methods=['GET'])
def consulta_movimentacao_id(ID_pedido):
    try:
        var_movimentacao = select(Movimentacao).where(Movimentacao.id == ID_pedido)
        var_movimentacao = db_session.execute(var_movimentacao).scalar()
        print(var_movimentacao)
        movimentacao_resultado = {
            "ID_pedido": ID_pedido,
            "data1": var_movimentacao.data1,
            "status": var_movimentacao.status,
            "quantidade": var_movimentacao.quantidade,
            "produto_id": var_movimentacao.produto_id,
        }
        print(movimentacao_resultado)
        return jsonify({'movimentacao': movimentacao_resultado}),200
    except ValueError:
        return jsonify({'mensagem':'Erro de cadastro'}), 400

# # Teste de lista de Usuário
# @app.route('/lista/usuario/', methods=['GET'])
# def lista_usuario(self=None):
#     try:
#         print("Lista de usuario")
#         sql_usuario = select(Usuario)
#         lista_usuario_id = db_session.execute(sql_usuario).scalars()
#         lista_usuario = {
#             'id': self.id,
#             'nome': self.nome,
#             'CPF': self.CPF,
#             'email': self.email,
#             'password': self.password,
#             'papel': self.papel,
#         }
#         for n in lista_usuario_id:
#             (lista_usuario.append(n.serialize_lista_usuarios()))
#             print(lista_usuario)
#         return jsonify({'lista_usuario': lista_usuario}), 200
#     except Exception as e:
#         return jsonify({'erro': e}), 400

@app.route('/lista/usuario/', methods=['GET'])
def lista_usuarios():
    try:
        sql_usuario = select(Usuario).where
        resultado_usuario = db_session.execute(sql_usuario).scalars()
        lista_usuarios = []
        for n in resultado_usuario:
            (lista_usuarios.append(n.serialize_lista_usuarios()))
            print(lista_usuarios[-1])
        return jsonify({'Lista': lista_usuarios}), 200
    except ValueError:
        return jsonify({'mensagem': 'Erro na consulta'}), 400

# # Comentado, pois não tem class de vendedor
# @app.route('/lista/vendedor/', methods=['GET'])
# def lista_vendedor():
#     try:
#         sql_vendedor = select(Vendedor).where
#         resultado_vendedor = db_session.execute(sql_vendedor).scalars()
#         lista_vendedor = []
#         for n in resultado_vendedor:
#             (lista_usuarios.append(n.serialize_lista_vendedor()))
#             print(lista_usuarios[-1])
#         return jsonify({'Livros': lista_usuarios}), 200
#     except ValueError:
#         return jsonify({'mensagem': 'Erro na consulta'}), 400

@app.route('/lista/produto/', methods=['GET'])
def lista_produtos():
    try:
        sql_produto = select(Produto).where
        resultado_produto = db_session.execute(sql_produto).scalars()
        lista_produtos = []
        for n in resultado_produto:
            (lista_produtos.append(n.serialize_lista_produtos()))
            print(lista_produtos[-1])
        return jsonify({'Lista': lista_produtos}), 200
    except ValueError:
        return jsonify({'mensagem': 'Erro na consulta'}), 400

# # Teste de lista de Produto
# @app.route('/lista/produto/', methods=['GET'])
# def lista_produtos(self=None):
#     try:
#         sql_produto = select(Produto).where
#         resultado_produto = db_session.execute(sql_produto).scalars()
#         lista_produtos = {
#             'id': self.id,
#             'nome_produto': self.nome_produto,
#             'dimesao_produto': self.dimesao_produto,
#             'preco_produto': self.preco_produto,
#             'peso_produto': self.peso_produto,
#             'cor_produto': self.cor_produto,
#             'descricao_produto': self.descricao_produto,
#         }
#         for n in resultado_produto:
#             (lista_produtos.append(n.serialize_lista_produtos()))
#             print(lista_produtos[-1])
#         return jsonify({'Lista': lista_produtos}), 200
#     except ValueError:
#         return jsonify({'mensagem': 'Erro na consulta'}), 400

@app.route('/lista/blog/', methods=['GET'])
def lista_blog():
    try:
        sql_blog = select(Blog).where
        resultado_blog = db_session.execute(sql_blog).scalars()
        lista_blog = []
        for n in resultado_blog:
            (lista_blog.append(n.serialize_lista_blog()))
            print(lista_blog[-1])
        return jsonify({'Lista': lista_blog}), 200
    except ValueError:
        return jsonify({'mensagem': 'Erro na consulta'}), 400

# # Teste de lista de Blog
# @app.route('/lista/blog/', methods=['GET'])
# def lista_blog(self=None):
#     try:
#         sql_blog = select(Blog).where
#         resultado_blog = db_session.execute(sql_blog).scalars()
#         lista_blog = {
#             'usuario_id': self.usuario_id,
#             'titulo': self.titulo,
#             'data': self.data,
#             'comentario': self.comentario,
#
#         }
#         for n in resultado_blog:
#             (lista_blog.append(n.serialize_lista_blog()))
#             print(lista_blog[-1])
#         return jsonify({'Lista': lista_blog}), 200
#     except ValueError:
#         return jsonify({'mensagem': 'Erro na consulta'}), 400

@app.route('/lista/pedido/', methods=['GET'])
def lista_pedidos():
    try:
        sql_pedido = select(Pedido).where
        resultado_pedido = db_session.execute(sql_pedido).scalars()
        lista_pedidos = []
        for n in resultado_pedido:
            (lista_pedidos.append(n.serialize_lista_pedidos()))
            print(lista_pedidos[-1])
        return jsonify({'Lista': lista_pedidos}), 200
    except ValueError:
        return jsonify({'mensagem': 'Erro na consulta'}), 400

# # Teste de lista de Pedidos
# @app.route('/lista/pedido/', methods=['GET'])
# def lista_pedidos(self=None):
#     try:
#         sql_pedido = select(Pedido).where
#         resultado_pedido = db_session.execute(sql_pedido).scalars()
#         lista_pedidos = {
#             'ID_pedido': self.ID_pedido,
#             'usuario_id': self.usuario_id,
#             'produto_id': self.produto_id,
#             'quantidade': self.quantidade,
#             'valor_total': self.valor_total,
#             'endereco': self.endereco,
#             'vendedor_id': self.vendedor_id,
#         }
#         for n in resultado_pedido:
#             (lista_pedidos.append(n.serialize_lista_pedidos()))
#             print(lista_pedidos[-1])
#         return jsonify({'Lista': lista_pedidos}), 200
#     except ValueError:
#         return jsonify({'mensagem': 'Erro na consulta'}), 400

@app.route('/lista/movimentacao/', methods=['GET'])
def lista_movimentacao():
    try:
        sql_movimentacao = select(Pedido).where
        resultado_movimentacao = db_session.execute(sql_movimentacao).scalars()
        lista_movimentacao = []
        for n in resultado_movimentacao:
            (lista_movimentacao.append(n.serialize_lista_movimentacao()))
            print(lista_movimentacao[-1])
        return jsonify({'Lista': lista_movimentacao}), 200
    except ValueError:
        return jsonify({'mensagem': 'Erro na consulta'}), 400

# # Teste de lista de Movimentacao
# @app.route('/lista/movimentacao/', methods=['GET'])
# def lista_movimentacao(self=None):
#     try:
#         sql_movimentacao = select(Pedido).where
#         resultado_movimentacao = db_session.execute(sql_movimentacao).scalars()
#         lista_movimentacao = {
#             'ID_movimentacao': self.ID_movimentacao,
#             'data1': self.data1,
#             'status': self.status,
#             'quantidade': self.quantidade,
#             'produto_id': self.produto_id,
#         }
#         for n in resultado_movimentacao:
#             (lista_movimentacao.append(n.serialize_lista_movimentacao()))
#             print(lista_movimentacao[-1])
#         return jsonify({'Lista': lista_movimentacao}), 200
#     except ValueError:
#         return jsonify({'mensagem': 'Erro na consulta'}), 400

@app.route('/atualizar/usuario/<id_atualizar>', methods=['PUT'])
def atualizar_usuario(id_usuario):
    try:
        var_usuario = select(Usuario).where(Usuario.id == id_usuario)
        var_usuario = db_session.execute(var_usuario).scalar()
        print(var_usuario)
        dados = request.get_json()
        if not dados['id'] or not dados['nome'] or not dados['cpf'] or not dados['email'] or not dados['password'] or not dados['papel']:
            return jsonify({"error", "preencher todos os campos"}), 400
        else:
            var_usuario.id = dados['id']
            var_usuario.nome = dados['nome']
            var_usuario.cpf = dados['cpf']
            var_usuario.email = dados['email']
            var_usuario.password = dados['password']
            var_usuario.papel = dados['papel']
            return jsonify({"atualizar usuário": 'usuario atualizado com sucesso'}), 200
    except ValueError:
        return jsonify({'Erro em atualizar'}), 400

# # Comentado, pois não tem class de vendedor
# @app.route('/atualizar/vendedor/<id_vendedor>', methods=['PUT'])
# def atualizar_vendedor(id_vendedor):
#     try:
#         var_vendedor = select(Vendedor).where(Vendedor.id == id_vendedor)
#         var_vendedor = db_session.execute(var_vendedor).scalar()
#         print(var_vendedor)
#         dados = request.get_json()
#         # if not dados['id'] or not dados['nome'] or not dados['cpf'] or not dados['email'] or not dados['password'] or not dados['papel']:
#             return jsonify({"error", "preencher todos os campos"}), 400
#         else:
#             # var_usuario.id = dados['id']
#             # var_usuario.nome = dados['nome']
#             # var_usuario.cpf = dados['cpf']
#             # var_usuario.email = dados['email']
#             # var_usuario.password = dados['password']
#             # var_usuario.papel = dados['papel']
#             return jsonify({"atualizar vendedor": 'vendedor atualizado com sucesso'}), 200
#     except ValueError:
#         return jsonify({'Erro em atualizar'}), 400

@app.route('/atualizar/produto/<id_atualizar>', methods=['PUT'])
def atualizar_produtos(id_produto):
    try:
        var_produto = select(Produto).where(Produto.id == id_produto)
        var_produto = db_session.execute(var_produto).scalar()
        print(var_produto)
        dados = request.get_json()
        if not dados['id'] or not dados['nome'] or not dados['dimesao'] or not dados['preco'] or not dados['peso'] or not dados['peso'] or not dados['descricao']:
            return jsonify({"error", "preencher todos os campos"}), 400
        else:
            var_produto.id = dados['id']
            var_produto.nome_produto = dados['nome']
            var_produto.dimesao_produto = dados['dimesao']
            var_produto.preco_produto = dados['preco']
            var_produto.peso_produto = dados['peso']
            var_produto.cor_produto = dados['cor']
            var_produto.descricao_produto = dados['descricao']
            return jsonify({"atualizar produto": 'produto atualizado com sucesso'}), 200
    except ValueError:
        return jsonify({'Erro em atualizar'}), 400

@app.route('/atualizar/blog/<id_atualizar>', methods=['PUT'])
def atualizar_blog(id_blog):
    try:
        var_blog = select(Blog).where(Blog.id == id_blog)
        var_blog = db_session.execute(var_blog).scalar()
        print(var_blog)
        dados = request.get_json()
        if not dados['id'] or not dados['titulo'] or not dados['data'] or not dados['comentario']:
            return jsonify({"error", "preencher todos os campos"}), 400
        else:
            var_blog.usuario_id = dados['id']
            var_blog.titulo = dados['titulo']
            var_blog.data = dados['data']
            var_blog.comentario= dados['comentario']
            return jsonify({"atualizar blog": 'blog atualizado com sucesso'}), 200
    except ValueError:
        return jsonify({'Erro em atualizar'}), 400

@app.route('/atualizar/pedido/<id_atualizar>', methods=['PUT'])
def atualizar_pedidos(id_pedido):
    try:

        var_pedido = select(Pedido).where(Pedido.id == id_pedido)
        var_pedido = db_session.execute(var_pedido).scalar()
        print(var_pedido)
        dados = request.get_json()
        if not dados['id'] or not dados['usuario_id'] or not dados['produto_id'] or not dados['quantidade'] or not dados['valor total'] or not dados['endereco'] or not dados['vendedor_id']:
            return jsonify({"error", "preencher todos os campos"}), 400
        else:
            var_pedido.id_pedido = dados['id']
            var_pedido.usuario_id = dados['usuario_id']
            var_pedido.produto_id = dados['produto_id']
            var_pedido.quantidade = dados['quantidade']
            var_pedido.valor_total = dados['valor_total']
            var_pedido.endereco = dados['endereco']
            var_pedido.vendedor_id = dados['vendedor_id']
            return jsonify({"atualizar vendedor": 'vendedor atualizado com sucesso'}), 200
    except ValueError:
        return jsonify({'Erro em atualizar'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)