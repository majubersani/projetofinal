from flask import jsonify, request
from sqlalchemy import select
from app import app, db_session
from models import Usuario, Produto, Blog, Pedido, Movimentacao


# LISTAS
@app.route('/lista/usuario/', methods=['GET'])
def lista_usuario():
    try:
        sql_usuario = select(Usuario)
        resultado = db_session.execute(sql_usuario).scalars()
        usuarios = [u.serialize_usuario() for u in resultado]
        return jsonify({'usuarios': usuarios}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/lista/produto/', methods=['GET'])
def lista_produto():
    try:
        sql_produto = select(Produto)
        resultado = db_session.execute(sql_produto).scalars()
        produtos = [p.serialize_produto() for p in resultado]
        return jsonify({'produtos': produtos}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/lista/blog/', methods=['GET'])
def lista_blog():
    try:
        sql_blog = select(Blog)
        resultado = db_session.execute(sql_blog).scalars()
        blogs = [b.serialize_blog() for b in resultado]
        return jsonify({'blogs': blogs}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/lista/pedido/', methods=['GET'])
def lista_pedido():
    try:
        sql_pedido = select(Pedido)
        resultado = db_session.execute(sql_pedido).scalars()
        pedidos = [p.serialize_pedido() for p in resultado]
        return jsonify({'pedidos': pedidos}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/lista/movimentacao/', methods=['GET'])
def lista_movimentacao():
    try:
        sql_mov = select(Movimentacao)
        resultado = db_session.execute(sql_mov).scalars()
        movimentacoes = [m.serialize_movimentacao() for m in resultado]
        return jsonify({'movimentacoes': movimentacoes}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


# ATUALIZAR
@app.route('/atualizar/usuario/<int:id_usuario>', methods=['PUT'])
def atualizar_usuario(id_usuario):
    try:
        usuario = db_session.execute(
            select(Usuario).where(Usuario.id == id_usuario)
        ).scalar()

        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        dados = request.get_json()
        if not dados.get('nome') or not dados.get('CPF') or not dados.get('email') or not dados.get('papel'):
            return jsonify({"erro": "preencher todos os campos"}), 400

        usuario.nome = dados['nome']
        usuario.CPF = dados['CPF']
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
            select(Produto).where(Produto.id_produto == id_produto)
        ).scalar()

        if not produto:
            return jsonify({'erro': 'Produto não encontrado'}), 404

        dados = request.get_json()
        if not dados.get('nome_produto') or not dados.get('dimensao_produto') or not dados.get('preco_produto') or not dados.get('peso_produto') or not dados.get('descricao_produto'):
            return jsonify({"erro": "preencher todos os campos"}), 400

        produto.nome_produto = dados['nome_produto']
        produto.dimensao_produto = dados['dimensao_produto']
        produto.preco_produto = dados['preco_produto']
        produto.peso_produto = dados['peso_produto']
        produto.cor_produto = dados.get('cor_produto')
        produto.descricao_produto = dados['descricao_produto']

        db_session.commit()
        return jsonify({"mensagem": "Produto atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/atualizar/blog/<int:id_blog>', methods=['PUT'])
def atualizar_blog(id_blog):
    try:
        blog = db_session.execute(
            select(Blog).where(Blog.id_blog == id_blog)
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
            select(Pedido).where(Pedido.ID_pedido == id_pedido)
        ).scalar()

        if not pedido:
            return jsonify({'erro': 'Pedido não encontrado'}), 404

        dados = request.get_json()
        if not dados.get('usuario_id') or not dados.get('id_produto') or not dados.get('quantidade') or not dados.get('valor_total') or not dados.get('endereco') or not dados.get('vendedor_id'):
            return jsonify({"erro": "preencher todos os campos"}), 400

        pedido.usuario_id = dados['usuario_id']
        pedido.id_produto = dados['id_produto']
        pedido.quantidade = dados['quantidade']
        pedido.valor_total = dados['valor_total']
        pedido.endereco = dados['endereco']
        pedido.vendedor_id = dados['vendedor_id']

        db_session.commit()
        return jsonify({"mensagem": "Pedido atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
