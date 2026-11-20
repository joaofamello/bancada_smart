from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, Column, DateTime,
    ForeignKey, ForeignKeyConstraint, Identity, Integer,
    Numeric, String, Text, UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from bancada_smart.database.db import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(BigInteger, Identity(), primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    google_sub = Column(String(64), unique=True, nullable=True)
    nome = Column(String(150), nullable=False)
    perfil = Column(String(20), nullable=False, default="operador")
    ativo = Column(Boolean, nullable=False, default=True)
    foto_url = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    criado_por = Column(BigInteger, ForeignKey("usuario.id"), nullable=True)
    ultimo_login_em = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("perfil IN ('admin', 'operador')", name="ck_usuario_perfil"),
        CheckConstraint("email = lower(email)", name="ck_usuario_email_minusculo"),
    )

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(BigInteger, Identity(), primary_key=True)
    nome = Column(String(150), nullable=False)
    cpf_cnpj = Column(String(18), unique=True, nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    endereco = Column(Text, nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    criado_por = Column(BigInteger, ForeignKey("usuario.id"), nullable=True)


class Fornecedor(Base):
    __tablename__ = "fornecedor"

    id = Column(BigInteger, Identity(), primary_key=True)
    razao_social = Column(String(150), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    endereco = Column(Text, nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    criado_por = Column(BigInteger, ForeignKey("usuario.id"), nullable=True)


class Marca(Base):
    __tablename__ = "marca"

    id = Column(BigInteger, Identity(), primary_key=True)
    nome = Column(String(80), nullable=False, unique=True)

    modelos = relationship("ModeloCelular", back_populates="marca")


class ModeloCelular(Base):
    __tablename__ = "modelo_celular"

    id = Column(BigInteger, Identity(), primary_key=True)
    marca_id = Column(BigInteger, ForeignKey("marca.id"), nullable=False)
    nome = Column(String(100), nullable=False)

    marca = relationship("Marca", back_populates="modelos")

    __table_args__ = (
        UniqueConstraint("marca_id", "nome", name="uq_modelo_marca_nome"),
    )

class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(BigInteger, Identity(), primary_key=True)
    nome = Column(String(80), nullable=False, unique=True)

class Servico(Base):
    __tablename__ = "servico"

    id = Column(BigInteger, Identity(), primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    preco_padrao = Column(Numeric(12, 2), nullable=False, default=0)
    ativo = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint("preco_padrao >= 0", name="ck_servico_preco_padrao"),
    )

class TipoDefeito(Base):
    __tablename__ = "tipo_defeito"

    id = Column(BigInteger, Identity(), primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)

class Produto(Base):
    __tablename__ = "produto"

    id = Column(BigInteger, Identity(), primary_key=True)
    tipo = Column(String(10), nullable=False)
    nome = Column(String(150), nullable=False)
    sku = Column(String(50), unique=True, nullable=True)
    categoria_id = Column(BigInteger, ForeignKey("categoria.id"), nullable=True)
    preco_venda = Column(Numeric(12, 2), nullable=False, default=0)
    custo_medio = Column(Numeric(12, 2), nullable=False, default=0)
    estoque_atual = Column(Integer, nullable=False, default=0)
    estoque_minimo = Column(Integer, nullable=False, default=0)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    criado_por = Column(BigInteger, ForeignKey("usuario.id"), nullable=True)

    categoria = relationship("Categoria")
    aparelho_modelo = relationship("AparelhoModelo", back_populates="produto", uselist=False)
    acessorio = relationship("Acessorio", back_populates="produto", uselist=False)
    peca = relationship("Peca", back_populates="produto", uselist=False)

    __table_args__ = (
        CheckConstraint("tipo IN ('aparelho', 'acessorio', 'peca')", name="ck_produto_tipo"),
        CheckConstraint("preco_venda >= 0", name="ck_produto_preco_venda"),
        CheckConstraint("custo_medio >= 0", name="ck_produto_custo_medio"),
        CheckConstraint("estoque_atual >= 0", name="ck_produto_estoque_atual"),
        CheckConstraint("estoque_minimo >= 0", name="ck_produto_estoque_minimo"),
        UniqueConstraint("id", "tipo", name="uq_produto_id_tipo"),
    )

class AparelhoModelo(Base):
    __tablename__ = "aparelho_modelo"

    produto_id = Column(BigInteger, primary_key=True)
    tipo = Column(String(10), nullable=False, default="aparelho")
    modelo_celular_id = Column(BigInteger, ForeignKey("modelo_celular.id"), nullable=False)
    armazenamento_gb = Column(Integer, nullable=True)
    ram_gb = Column(Integer, nullable=True)
    cor = Column(String(40), nullable=True)

    produto = relationship("Produto", back_populates="aparelho_modelo")
    modelo_celular = relationship("ModeloCelular")

    __table_args__ = (
        CheckConstraint("tipo = 'aparelho'", name="ck_aparelho_modelo_tipo"),
        CheckConstraint("armazenamento_gb > 0", name="ck_aparelho_armazenamento"),
        CheckConstraint("ram_gb > 0", name="ck_aparelho_ram"),
        ForeignKeyConstraint(
            ["produto_id", "tipo"],
            ["produto.id", "produto.tipo"],
            name="fk_aparelho_modelo_produto",
        ),
    )

class Acessorio(Base):
    __tablename__ = "acessorio"

    produto_id = Column(BigInteger, primary_key=True)
    tipo = Column(String(10), nullable=False, default="acessorio")
    cor = Column(String(40), nullable=True)
    descricao = Column(Text, nullable=True)

    produto = relationship("Produto", back_populates="acessorio")

    __table_args__ = (
        CheckConstraint("tipo = 'acessorio'", name="ck_acessorio_tipo"),
        ForeignKeyConstraint(
            ["produto_id", "tipo"],
            ["produto.id", "produto.tipo"],
            name="fk_acessorio_produto",
        ),
    )

class Peca(Base):
    __tablename__ = "peca"

    produto_id = Column(BigInteger, primary_key=True)
    tipo = Column(String(10), nullable=False, default="peca")
    componente = Column(String(60), nullable=True)
    descricao = Column(Text, nullable=True)

    produto = relationship("Produto", back_populates="peca")
    modelos_compativeis = relationship(
        "ModeloCelular",
        secondary="peca_compatibilidade",
    )

    __table_args__ = (
        CheckConstraint("tipo = 'peca'", name="ck_peca_tipo"),
        ForeignKeyConstraint(
            ["produto_id", "tipo"],
            ["produto.id", "produto.tipo"],
            name="fk_peca_produto",
        ),
    )

class PecaCompatibilidade(Base):
    __tablename__ = "peca_compatibilidade"

    peca_id = Column(BigInteger, ForeignKey("peca.produto_id"), primary_key=True)
    modelo_celular_id = Column(BigInteger, ForeignKey("modelo_celular.id"), primary_key=True)