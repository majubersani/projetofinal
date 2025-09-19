from flask import jsonify, request
from sqlalchemy import select
from app import app, db_session
from models import Usuario, Produto, Blog, Pedido, Movimentacao

# ---------------- LISTAS ----------------
@app.route('/lista/usuario/', methods=['GET'])
def lista_usuario():
    try:
        resultado = db_session.execute(select(Usuario)).scalars()
        usuarios = [u.serialize() for u in resultado]
        return jsonify({'usuarios': usuarios}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/lista/produto/', methods=['GET'])
def lista_produto():
    try:
        resultado = db_session.execute(select(Produto)).scalars()
        produtos = [p.serialize() for p in resultado]
        return jsonify({'produtos': produtos}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/lista/blog/', methods=['GET'])
def lista_blog():
    try:
        resultado = db_session.execute(select(Blog)).scalars()
        blogs = [b.serialize() for b in resultado]
        return jsonify({'blogs': blogs}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/lista/pedido/', methods=['GET'])
def lista_pedido():
    try:
        resultado = db_session.execute(select(Pedido)).scalars()
        pedidos = [p.serialize() for p in resultado]
        return jsonify({'pedidos': pedidos}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/lista/movimentacao/', methods=['GET'])
def lista_movimentacao():
    try:
        resultado = db_session.execute(select(Movimentacao)).scalars()
        movimentacoes = [m.serialize() for m in resultado]
        return jsonify({'movimentacoes': movimentacoes}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


# ---------------- ATUALIZAR ----------------
@app.route('/atualizar/usuario/<int:id_usuario>', methods=['PUT'])
def atualizar_usuario(id_usuario):
    try:
        usuario = db_session.execute(
            select(Usuario).where(Usuario.id == id_usuario)
        ).scalar()

        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        dados = request.get_json()
        if not dados.get('nome') or not dados.get('cpf') or not dados.get('email') or not dados.get('papel'):
            return jsonify({"erro": "preencher todos os campos"}), 400

        usuario.nome = dados['nome']
        usuario.cpf = dados['cpf']
        usuario.email = dados['email']
        usuario.papel = dados['papel']

        if 'password' in dados:
            usuario.set_password(dados['password'])

        db_session.commit()
        return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/atualizar/produto/<int:id_produto>', methods=['PUT'])
def atualizar_produto(id_produto):
    try:
        produto = db_session.execute(
            select(Produto).where(Produto.id == id_produto)
        ).scalar()

        if not produto:
            return jsonify({'erro': 'Produto não encontrado'}), 404

        dados = request.get_json()
        if not dados.get('nome') or not dados.get('dimensao') or not dados.get('preco') or not dados.get('peso') or not dados.get('descricao'):
            return jsonify({"erro": "preencher todos os campos"}), 400

        produto.nome = dados['nome']
        produto.dimensao = dados['dimensao']
        produto.preco = dados['preco']
        produto.peso = dados['peso']
        produto.cor = dados.get('cor')
        produto.descricao = dados['descricao']

        db_session.commit()
        return jsonify({"mensagem": "Produto atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/atualizar/blog/<int:id_blog>', methods=['PUT'])
def atualizar_blog(id_blog):
    try:
        blog = db_session.execute(
            select(Blog).where(Blog.id == id_blog)
        ).scalar()

        if not blog:
            return jsonify({'erro': 'Blog não encontrado'}), 404

        dados = request.get_json()
        if not dados.get('titulo') or not dados.get('data') or not dados.get('comentario'):
            return jsonify({"erro": "preencher todos os campos"}), 400

        blog.titulo = dados['titulo']
        blog.data = dados['data']
        blog.comentario = dados['comentario']
        blog.usuario_id = dados.get('usuario_id', blog.usuario_id)

        db_session.commit()
        return jsonify({"mensagem": "Blog atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/atualizar/pedido/<int:id_pedido>', methods=['PUT'])
def atualizar_pedido(id_pedido):
    try:
        pedido = db_session.execute(
            select(Pedido).where(Pedido.id == id_pedido)
        ).scalar()

        if not pedido:
            return jsonify({'erro': 'Pedido não encontrado'}), 404

        dados = request.get_json()
        if not dados.get('usuario_id') or not dados.get('produto_id') or not dados.get('quantidade') or not dados.get('valor_total') or not dados.get('endereco') or not dados.get('vendedor_id'):
            return jsonify({"erro": "preencher todos os campos"}), 400

        pedido.usuario_id = dados['usuario_id']
        pedido.produto_id = dados['produto_id']
        pedido.quantidade = dados['quantidade']
        pedido.valor_total = dados['valor_total']
        pedido.endereco = dados['endereco']
        pedido.vendedor_id = dados['vendedor_id']

        db_session.commit()
        return jsonify({"mensagem": "Pedido atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
