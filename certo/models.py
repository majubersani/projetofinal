# O que arrumou nesse models:
# Pedido → no método serialize_pedido você usa self.produto_id, mas no model o campo é id_produto.
# Movimentacao → no serialize_movimentacao você usa self.produto_id, mas o campo também é id_produto.
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    papel = Column(String(20), nullable=False)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete(self, db_session):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "papel": self.papel,
        }


class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome_produto = Column(String(100), nullable=False)
    dimensao_produto = Column(String(50), nullable=False)
    preco_produto = Column(Integer, nullable=False)
    peso_produto = Column(Integer, nullable=False)
    cor_produto = Column(String(30))
    descricao_produto = Column(String(200))

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete(self, db_session):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "nome": self.nome_produto,
            "dimensao": self.dimensao_produto,
            "preco": self.preco_produto,
            "peso": self.peso_produto,
            "cor": self.cor_produto,
            "descricao": self.descricao_produto,
        }


class Blog(Base):
    __tablename__ = 'blogs'
    id_blog = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    titulo = Column(String(100), nullable=False)
    data = Column(String(20), nullable=False)
    comentario = Column(String(500), nullable=False)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete(self, db_session):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
            "id_blog": self.id_blog,
            "id_usuario": self.id_usuario,
            "titulo": self.titulo,
            "data": self.data,
            "comentario": self.comentario,
        }


class Pedido(Base):
    __tablename__ = 'pedidos'
    id_pedido = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    id_produto = Column(Integer, ForeignKey("produtos.id"))
    id_vendedor = Column(Integer)
    quantidade = Column(Integer, nullable=False)
    valor_total = Column(Integer, nullable=False)
    endereco = Column(String(200), nullable=False)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete(self, db_session):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
            "id_pedido": self.id_pedido,
            "id_usuario": self.id_usuario,
            "id_produto": self.id_produto,
            "quantidade": self.quantidade,
            "valor_total": self.valor_total,
            "endereco": self.endereco,
            "id_vendedor": self.id_vendedor,
        }

class Movimentacao(Base):
    __tablename__ = 'movimentacoes'
    id_movimentacao = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    id_produto = Column(Integer, ForeignKey("produtos.id"))
    data = Column(String(20), nullable=False)
    status = Column(Boolean, default=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete(self, db_session):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
            "id_movimentacao": self.id_movimentacao,
            "id_produto": self.id_produto,
            "quantidade": self.quantidade,
            "data": self.data,
            "status": self.status,
            "id_usuario": self.id_usuario,
        }