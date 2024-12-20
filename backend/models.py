from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "Usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    is_client = Column(Boolean)
    is_driver = Column(Boolean)
    is_employee = Column(Boolean)
    email = Column(String)
    password_hash = Column(String)
    salt = Column(String)

    clients = relationship("Client", back_populates="user")
    drivers = relationship("Driver", back_populates="user")
    employees = relationship("Employee", back_populates="user")

class Client(Base):
    __tablename__ = "Cliente"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    end_rua = Column(String)
    end_bairro = Column(String)
    end_numero = Column(Integer)
    telefone = Column(Integer)
    fk_id_usuario = Column(Integer, ForeignKey("Usuario.id"))

    user = relationship("User", back_populates="clients")
    products = relationship("Product", back_populates="client")

class Product(Base):
    __tablename__ = "Produto"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    preco = Column(Integer)
    quantidade_estoque = Column(Integer)
    fk_id_cliente = Column(Integer, ForeignKey("Cliente.id"))

    client = relationship("Client", back_populates="products")
    deliveries = relationship("Delivery", back_populates="product")
    
class Vehicle(Base):
    __tablename__ = "Veiculo"
    
    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String, index=True)
    modelo = Column(String)
    capacidade = Column(Integer)
    fk_id_localizacao = Column(Integer, ForeignKey("LocalizacaoVeiculo.id"))
    is_available = Column(Boolean, default=True)

    drivers = relationship("Driver", back_populates="vehicle")
    location = relationship("VehicleLocation", back_populates="vehicle", foreign_keys=[fk_id_localizacao], remote_side="VehicleLocation.id", lazy="joined")
    deliveries = relationship("Delivery", back_populates="vehicle")
    
class Driver(Base):
    __tablename__ = "Motorista"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    habilitacao = Column(String)
    telefone = Column(Integer)
    end_rua = Column(String)
    end_bairro = Column(String)
    end_numero = Column(Integer)
    fk_id_usuario = Column(Integer, ForeignKey("Usuario.id"))
    fk_id_veiculo = Column(Integer, ForeignKey("Veiculo.id"))
    
    user = relationship("User", back_populates="drivers")
    vehicle = relationship("Vehicle", back_populates="drivers")

class DistributionPoint(Base):
    __tablename__ = "PontoDistribuicao"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    end_rua = Column(String)
    end_bairro = Column(String)
    end_numero = Column(Integer)
    tipo = Column(String)

    deliveries = relationship("Delivery", back_populates="distribution_point")
    
class VehicleLocation(Base):
    __tablename__ = "LocalizacaoVeiculo"
    
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    data_hora = Column(Date)
    
    vehicle = relationship("Vehicle", back_populates="location", uselist=False)

class Route(Base):
    __tablename__ = "Rota"
    
    id = Column(Integer, primary_key=True, index=True)
    origem = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    distancia_km = Column(Float)
    tempo_estimado = Column(Integer)  
    fk_id_entrega = Column(Integer, ForeignKey("Entrega.id"))

    delivery = relationship("Delivery", back_populates="route")
    
class Delivery(Base):
    __tablename__ = "Entrega"
    
    id = Column(Integer, primary_key=True, index=True)
    fk_id_veiculo = Column(Integer, ForeignKey("Veiculo.id"), nullable=True)
    fk_id_produto = Column(Integer, ForeignKey("Produto.id"))
    fk_id_ponto_entrega = Column(Integer, ForeignKey("PontoDistribuicao.id"))
    status = Column(String, default="pending")  # Exemplo: "pending", "in_progress", "delivered"
    is_delivered = Column(Boolean, default=False)
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=True)  # Data da criação
    data_entrega = Column(Date, nullable=True)  # Data de entrega (será preenchida quando status for "delivered")
    
    vehicle = relationship("Vehicle", back_populates="deliveries")
    product = relationship("Product", back_populates="deliveries")
    distribution_point = relationship("DistributionPoint", back_populates="deliveries")
    route = relationship("Route", back_populates="delivery")

class Employee(Base):
    __tablename__ = "Funcionario"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    end_rua = Column(String)
    end_bairro = Column(String)
    end_numero = Column(Integer)
    telefone = Column(Integer)
    area = Column(String)
    fk_id_usuario = Column(Integer, ForeignKey("Usuario.id"))

    user = relationship("User", back_populates="employees")
