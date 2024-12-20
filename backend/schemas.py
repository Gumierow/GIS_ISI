from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


# Esquemas para a entidade Client (Cliente)
class ClientBase(BaseModel):
    nome: str
    end_rua: str
    end_bairro: str
    end_numero: int
    telefone: int

class ClientCreate(ClientBase):
    email: str  
    password: str 
    products: Optional[List["ProductCreate"]] = None

class Client(ClientBase):
    id: int
    fk_id_usuario: Optional[int]
    products: Optional[List["Product"]] = None  # Produtos associados

    class Config:
        orm_mode = True

# Esquemas para a entidade DistributionPoint (PontoDistribuicao)
class DistributionPointBase(BaseModel):
    nome: str
    end_rua: str
    end_bairro: str
    end_numero: int
    tipo: str

class DistributionPointCreate(DistributionPointBase):
    pass

class DistributionPoint(DistributionPointBase):
    id: int

    class Config:
        orm_mode = True


# Esquemas para a entidade Product (Produto)
class ProductBase(BaseModel):
    nome: str
    descricao: str
    preco: int
    quantidade_estoque: int

class ProductCreate(ProductBase):
    nome: str
    descricao: str
    preco: int
    quantidade_estoque: int
    fk_id_cliente: int

class Product(ProductBase):
    id: int
    fk_id_cliente: Optional[int]

    class Config:
        orm_mode = True


class VehicleLocationBase(BaseModel):
    latitude: float
    longitude: float
    data_hora: Optional[datetime]

class VehicleLocationUpdate(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
    data_hora: Optional[datetime]

class VehicleLocation(VehicleLocationBase):
    id: int

    class Config:
        orm_mode = True


class VehicleLocationCreate(VehicleLocationBase):
    latitude: float
    longitude: float
    data_hora: datetime 


# Esquemas para a entidade Vehicle (Veiculo)
class VehicleBase(BaseModel):
    placa: str
    modelo: str
    capacidade: int
    is_available: bool = True

class VehicleCreate(VehicleBase):
    placa: str
    modelo: str
    capacidade: int
    is_available: Optional[bool] = True  # Disponível por padrão
    fk_id_localizacao: VehicleLocationCreate

class Vehicle(VehicleBase):
    id: int
    fk_id_localizacao: int

    class Config:
        orm_mode = True

# Esquemas para a entidade Driver (Motorista)
class DriverBase(BaseModel):
    nome: str
    habilitacao: str
    telefone: int
    end_rua: str
    end_bairro: str
    end_numero: int

class DriverCreate(DriverBase):
    email: str  
    password: str 
    fk_id_veiculo: Optional[int]

class Driver(DriverBase):
    id: int
    fk_id_veiculo: Optional[int]
    fk_id_usuario: Optional[int]

    class Config:
        orm_mode = True



# Esquemas para a entidade Route (Rota)
class RouteBase(BaseModel):
    origem: str  # Ajustado para string
    destino: str  # Ajustado para string
    distancia_km: float
    tempo_estimado: int

class RouteCreate(RouteBase):
    fk_id_entrega: Optional[int]  # Não opcional para criar uma rota

class Route(RouteBase):
    id: int
    fk_id_entrega: Optional[int]

    class Config:
        orm_mode = True

class RouteUpdate(BaseModel):
    origem: Optional[str] = None
    destino: Optional[str] = None
    distancia_km: Optional[float] = None
    tempo_estimado: Optional[int] = None
    fk_id_entrega: Optional[int] = None

    class Config:
        orm_mode = True

# Esquemas para a entidade Delivery (Entrega)
class DeliveryBase(BaseModel):
    status: str = "pending"
    is_delivered: bool = False
    data_criacao: Optional[datetime] = None
    data_entrega: Optional[datetime] = None

class DeliveryCreate(DeliveryBase):
    fk_id_produto: int
    fk_id_ponto_entrega: int

class Delivery(DeliveryBase):
    id: int
    vehicle: Optional["Vehicle"] = None  # Associações explícitas
    route: Optional["Route"] = None
    data_criacao: Optional[datetime] = None   # Adicionando data_criacao ao schema
    data_entrega: Optional[datetime] = None  # Adicionando data_entrega ao schema

    class Config:
        orm_mode = True

class ProductInDelivery(BaseModel):
    product_id: int
    quantity: int

#class DeliveryCreate(BaseModel):
#    origin_lat: float  
#    origin_lon: float  
#    products: List[ProductInDelivery]  
    
class DeliveryResponse(DeliveryBase):
    id: int
    vehicle: Optional["Vehicle"] = None
    route: Optional["Route"] = None
    data_criacao: datetime
    data_entrega: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Esquemas para a entidade Employee (Funcionario)
class EmployeeBase(BaseModel):
    nome: str
    end_rua: str
    end_bairro: str
    end_numero: int
    telefone: int
    area: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    fk_id_usuario: Optional[int]

    class Config:
        orm_mode = True

class VehicleUpdateRequest(BaseModel):
    latitude: float
    longitude: float
    
    
class DeliveryDetailsResponse(BaseModel):
    delivery_id: int
    status: str
    data_criacao: Optional[str]
    data_entrega: Optional[str]
    vehicle_id: Optional[int]
    vehicle_plate: Optional[str]
    vehicle_model: Optional[str]
    product_name: Optional[str]
    product_quantity: Optional[int]
    distribution_point_name: Optional[str]
    distribution_point_lat: Optional[float]
    distribution_point_lon: Optional[float]
    route_id: Optional[int]
    route_description: Optional[str]
    client_id: Optional[int]
    client_name: Optional[str]
    client_email: Optional[str]

    class Config:
        orm_mode = True