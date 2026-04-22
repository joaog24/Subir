from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt
from io import BytesIO
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Config
JWT_SECRET = os.environ.get('JWT_SECRET', 'ecp_secret_key_2024')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

security = HTTPBearer()

# Create the main app
app = FastAPI(title="E.C.P Manager API")
api_router = APIRouter(prefix="/api")

# ==================== MODELS ====================

class Usuario(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = Field(default_factory=lambda: str(datetime.now(timezone.utc).timestamp()))
    nome: str
    email: EmailStr
    senha: str
    ativo: bool = True
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioResponse(BaseModel):
    id: str
    nome: str
    email: str
    ativo: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UsuarioResponse

class Atleta(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = Field(default_factory=lambda: str(datetime.now(timezone.utc).timestamp()))
    nome: str
    posicao: str
    telefone: str
    foto: Optional[str] = None
    pe_dominante: Optional[str] = None
    ativo: bool = True
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AtletaCreate(BaseModel):
    nome: str
    posicao: str
    telefone: str
    foto: Optional[str] = None
    pe_dominante: Optional[str] = None
    ativo: bool = True

class AtletaResponse(BaseModel):
    id: str
    nome: str
    posicao: str
    telefone: str
    foto: Optional[str]
    pe_dominante: Optional[str]
    ativo: bool

class Treino(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = Field(default_factory=lambda: str(datetime.now(timezone.utc).timestamp()))
    data: str
    local: str
    observacoes: Optional[str] = ""
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TreinoCreate(BaseModel):
    data: str
    local: str
    observacoes: Optional[str] = ""

class TreinoResponse(BaseModel):
    id: str
    data: str
    local: str
    observacoes: str
    total_presencas: int = 0

class Presenca(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = Field(default_factory=lambda: str(datetime.now(timezone.utc).timestamp()))
    treino_id: str
    atleta_id: str
    presente: bool
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PresencaCreate(BaseModel):
    treino_id: str
    atleta_id: str
    presente: bool

class PresencaBulk(BaseModel):
    treino_id: str
    presencas: List[dict]

class Partida(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = Field(default_factory=lambda: str(datetime.now(timezone.utc).timestamp()))
    data: str
    adversario: str
    local: str
    gols_clube: int
    gols_adversario: int
    resultado: str = ""
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PartidaCreate(BaseModel):
    data: str
    adversario: str
    local: str
    gols_clube: int
    gols_adversario: int

class PartidaResponse(BaseModel):
    id: str
    data: str
    adversario: str
    local: str
    gols_clube: int
    gols_adversario: int
    resultado: str

class Patrocinador(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = Field(default_factory=lambda: str(datetime.now(timezone.utc).timestamp()))
    nome: str
    tipo: str
    contato: str
    ativo: bool = True
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PatrocinadorCreate(BaseModel):
    nome: str
    tipo: str
    contato: str
    ativo: bool = True

class PatrocinadorResponse(BaseModel):
    id: str
    nome: str
    tipo: str
    contato: str
    ativo: bool

class Recebimento(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = Field(default_factory=lambda: str(datetime.now(timezone.utc).timestamp()))
    descricao: str
    valor: float
    data: str
    patrocinador_id: Optional[str] = None
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class RecebimentoCreate(BaseModel):
    descricao: str
    valor: float
    data: str
    patrocinador_id: Optional[str] = None

class RecebimentoResponse(BaseModel):
    id: str
    descricao: str
    valor: float
    data: str
    patrocinador_id: Optional[str]
    patrocinador_nome: Optional[str] = None

class Despesa(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = Field(default_factory=lambda: str(datetime.now(timezone.utc).timestamp()))
    descricao: str
    categoria: str
    valor: float
    data: str
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DespesaCreate(BaseModel):
    descricao: str
    categoria: str
    valor: float
    data: str

class DespesaResponse(BaseModel):
    id: str
    descricao: str
    categoria: str
    valor: float
    data: str

class DashboardStats(BaseModel):
    total_atletas_ativos: int
    total_treinos: int
    total_partidas: int
    total_receitas: float
    total_despesas: float
    saldo: float
    vitorias: int
    empates: int
    derrotas: int

# ==================== AUTH HELPERS ====================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await db.usuarios.find_one({"id": user_id}, {"_id": 0})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# ==================== AUTH ROUTES ====================

@api_router.post("/auth/register", response_model=UsuarioResponse)
async def register(user: UsuarioCreate):
    existing = await db.usuarios.find_one({"email": user.email}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    usuario_dict = user.model_dump()
    usuario_dict['senha'] = hash_password(usuario_dict['senha'])
    usuario_obj = Usuario(**usuario_dict)
    
    doc = usuario_obj.model_dump()
    doc['criado_em'] = doc['criado_em'].isoformat()
    
    await db.usuarios.insert_one(doc)
    return UsuarioResponse(**{k: v for k, v in doc.items() if k != 'senha'})

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UsuarioLogin):
    user = await db.usuarios.find_one({"email": credentials.email}, {"_id": 0})
    if not user or not verify_password(credentials.senha, user['senha']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user['id'], "email": user['email']})
    user_response = UsuarioResponse(**{k: v for k, v in user.items() if k != 'senha'})
    
    return TokenResponse(access_token=access_token, user=user_response)

@api_router.get("/auth/me", response_model=UsuarioResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UsuarioResponse(**{k: v for k, v in current_user.items() if k != 'senha'})

# ==================== ATLETAS ROUTES ====================

@api_router.get("/atletas", response_model=List[AtletaResponse])
async def list_atletas(current_user: dict = Depends(get_current_user)):
    atletas = await db.atletas.find({}, {"_id": 0}).sort("nome", 1).to_list(1000)
    return [AtletaResponse(**a) for a in atletas]

@api_router.post("/atletas", response_model=AtletaResponse)
async def create_atleta(atleta: AtletaCreate, current_user: dict = Depends(get_current_user)):
    atleta_obj = Atleta(**atleta.model_dump())
    doc = atleta_obj.model_dump()
    doc['criado_em'] = doc['criado_em'].isoformat()
    await db.atletas.insert_one(doc)
    return AtletaResponse(**doc)

@api_router.get("/atletas/{atleta_id}", response_model=AtletaResponse)
async def get_atleta(atleta_id: str, current_user: dict = Depends(get_current_user)):
    atleta = await db.atletas.find_one({"id": atleta_id}, {"_id": 0})
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta not found")
    return AtletaResponse(**atleta)

@api_router.put("/atletas/{atleta_id}", response_model=AtletaResponse)
async def update_atleta(atleta_id: str, atleta: AtletaCreate, current_user: dict = Depends(get_current_user)):
    existing = await db.atletas.find_one({"id": atleta_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Atleta not found")
    
    update_data = atleta.model_dump()
    await db.atletas.update_one({"id": atleta_id}, {"$set": update_data})
    updated = await db.atletas.find_one({"id": atleta_id}, {"_id": 0})
    return AtletaResponse(**updated)

@api_router.delete("/atletas/{atleta_id}")
async def delete_atleta(atleta_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.atletas.delete_one({"id": atleta_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Atleta not found")
    return {"message": "Atleta deleted successfully"}

# ==================== TREINOS ROUTES ====================

@api_router.get("/treinos", response_model=List[TreinoResponse])
async def list_treinos(current_user: dict = Depends(get_current_user)):
    # Use aggregation to avoid N+1 query
    pipeline = [
        {"$lookup": {
            "from": "presencas",
            "localField": "id",
            "foreignField": "treino_id",
            "as": "presencas"
        }},
        {"$addFields": {
            "total_presencas": {
                "$size": {
                    "$filter": {
                        "input": "$presencas",
                        "cond": {"$eq": ["$$this.presente", True]}
                    }
                }
            }
        }},
        {"$project": {
            "_id": 0,
            "presencas": 0
        }},
        {"$sort": {"data": -1}},
        {"$limit": 1000}
    ]
    treinos = await db.treinos.aggregate(pipeline).to_list(1000)
    return [TreinoResponse(**t) for t in treinos]

@api_router.post("/treinos", response_model=TreinoResponse)
async def create_treino(treino: TreinoCreate, current_user: dict = Depends(get_current_user)):
    treino_obj = Treino(**treino.model_dump())
    doc = treino_obj.model_dump()
    doc['criado_em'] = doc['criado_em'].isoformat()
    await db.treinos.insert_one(doc)
    doc['total_presencas'] = 0
    return TreinoResponse(**doc)

@api_router.get("/treinos/{treino_id}", response_model=TreinoResponse)
async def get_treino(treino_id: str, current_user: dict = Depends(get_current_user)):
    treino = await db.treinos.find_one({"id": treino_id}, {"_id": 0})
    if not treino:
        raise HTTPException(status_code=404, detail="Treino not found")
    presencas_count = await db.presencas.count_documents({"treino_id": treino_id, "presente": True})
    treino['total_presencas'] = presencas_count
    return TreinoResponse(**treino)

@api_router.put("/treinos/{treino_id}", response_model=TreinoResponse)
async def update_treino(treino_id: str, treino: TreinoCreate, current_user: dict = Depends(get_current_user)):
    existing = await db.treinos.find_one({"id": treino_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Treino not found")
    
    update_data = treino.model_dump()
    await db.treinos.update_one({"id": treino_id}, {"$set": update_data})
    updated = await db.treinos.find_one({"id": treino_id}, {"_id": 0})
    presencas_count = await db.presencas.count_documents({"treino_id": treino_id, "presente": True})
    updated['total_presencas'] = presencas_count
    return TreinoResponse(**updated)

@api_router.delete("/treinos/{treino_id}")
async def delete_treino(treino_id: str, current_user: dict = Depends(get_current_user)):
    await db.presencas.delete_many({"treino_id": treino_id})
    result = await db.treinos.delete_one({"id": treino_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Treino not found")
    return {"message": "Treino deleted successfully"}

# ==================== PRESENCAS ROUTES ====================

@api_router.get("/presencas/treino/{treino_id}")
async def get_presencas_treino(treino_id: str, current_user: dict = Depends(get_current_user)):
    presencas = await db.presencas.find({"treino_id": treino_id}, {"_id": 0}).to_list(1000)
    atletas = await db.atletas.find({}, {"_id": 0}).to_list(1000)
    
    result = []
    for atleta in atletas:
        presenca = next((p for p in presencas if p['atleta_id'] == atleta['id']), None)
        result.append({
            "atleta_id": atleta['id'],
            "atleta_nome": atleta['nome'],
            "presente": presenca['presente'] if presenca else False,
            "presenca_id": presenca.get('id') if presenca else None
        })
    
    return result

@api_router.post("/presencas/bulk")
async def save_presencas_bulk(data: PresencaBulk, current_user: dict = Depends(get_current_user)):
    await db.presencas.delete_many({"treino_id": data.treino_id})
    
    for item in data.presencas:
        presenca_obj = Presenca(
            treino_id=data.treino_id,
            atleta_id=item['atleta_id'],
            presente=item['presente']
        )
        doc = presenca_obj.model_dump()
        doc['criado_em'] = doc['criado_em'].isoformat()
        await db.presencas.insert_one(doc)
    
    return {"message": "Presenças salvas com sucesso"}

# ==================== PARTIDAS ROUTES ====================

def calcular_resultado(gols_clube: int, gols_adversario: int) -> str:
    if gols_clube > gols_adversario:
        return "Vitória"
    elif gols_clube < gols_adversario:
        return "Derrota"
    else:
        return "Empate"

@api_router.get("/partidas", response_model=List[PartidaResponse])
async def list_partidas(mes: Optional[int] = None, ano: Optional[int] = None, resultado: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    query = {}
    if mes and ano:
        query["data"] = {"$regex": f"{ano}-{str(mes).zfill(2)}"}
    elif ano:
        query["data"] = {"$regex": f"^{ano}"}
    
    partidas = await db.partidas.find(query, {"_id": 0}).sort("data", -1).to_list(1000)
    for partida in partidas:
        partida['resultado'] = calcular_resultado(partida['gols_clube'], partida['gols_adversario'])
    
    if resultado:
        partidas = [p for p in partidas if p['resultado'] == resultado]
    
    return [PartidaResponse(**p) for p in partidas]

@api_router.post("/partidas", response_model=PartidaResponse)
async def create_partida(partida: PartidaCreate, current_user: dict = Depends(get_current_user)):
    partida_dict = partida.model_dump()
    partida_dict['resultado'] = calcular_resultado(partida.gols_clube, partida.gols_adversario)
    partida_obj = Partida(**partida_dict)
    
    doc = partida_obj.model_dump()
    doc['criado_em'] = doc['criado_em'].isoformat()
    await db.partidas.insert_one(doc)
    return PartidaResponse(**doc)

@api_router.get("/partidas/{partida_id}", response_model=PartidaResponse)
async def get_partida(partida_id: str, current_user: dict = Depends(get_current_user)):
    partida = await db.partidas.find_one({"id": partida_id}, {"_id": 0})
    if not partida:
        raise HTTPException(status_code=404, detail="Partida not found")
    partida['resultado'] = calcular_resultado(partida['gols_clube'], partida['gols_adversario'])
    return PartidaResponse(**partida)

@api_router.put("/partidas/{partida_id}", response_model=PartidaResponse)
async def update_partida(partida_id: str, partida: PartidaCreate, current_user: dict = Depends(get_current_user)):
    existing = await db.partidas.find_one({"id": partida_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Partida not found")
    
    update_data = partida.model_dump()
    update_data['resultado'] = calcular_resultado(partida.gols_clube, partida.gols_adversario)
    await db.partidas.update_one({"id": partida_id}, {"$set": update_data})
    updated = await db.partidas.find_one({"id": partida_id}, {"_id": 0})
    return PartidaResponse(**updated)

@api_router.delete("/partidas/{partida_id}")
async def delete_partida(partida_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.partidas.delete_one({"id": partida_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Partida not found")
    return {"message": "Partida deleted successfully"}

# ==================== PATROCINADORES ROUTES ====================

@api_router.get("/patrocinadores", response_model=List[PatrocinadorResponse])
async def list_patrocinadores(current_user: dict = Depends(get_current_user)):
    patrocinadores = await db.patrocinadores.find({}, {"_id": 0}).sort("nome", 1).to_list(1000)
    return [PatrocinadorResponse(**p) for p in patrocinadores]

@api_router.post("/patrocinadores", response_model=PatrocinadorResponse)
async def create_patrocinador(patrocinador: PatrocinadorCreate, current_user: dict = Depends(get_current_user)):
    patrocinador_obj = Patrocinador(**patrocinador.model_dump())
    doc = patrocinador_obj.model_dump()
    doc['criado_em'] = doc['criado_em'].isoformat()
    await db.patrocinadores.insert_one(doc)
    return PatrocinadorResponse(**doc)

@api_router.get("/patrocinadores/{patrocinador_id}", response_model=PatrocinadorResponse)
async def get_patrocinador(patrocinador_id: str, current_user: dict = Depends(get_current_user)):
    patrocinador = await db.patrocinadores.find_one({"id": patrocinador_id}, {"_id": 0})
    if not patrocinador:
        raise HTTPException(status_code=404, detail="Patrocinador not found")
    return PatrocinadorResponse(**patrocinador)

@api_router.put("/patrocinadores/{patrocinador_id}", response_model=PatrocinadorResponse)
async def update_patrocinador(patrocinador_id: str, patrocinador: PatrocinadorCreate, current_user: dict = Depends(get_current_user)):
    existing = await db.patrocinadores.find_one({"id": patrocinador_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Patrocinador not found")
    
    update_data = patrocinador.model_dump()
    await db.patrocinadores.update_one({"id": patrocinador_id}, {"$set": update_data})
    updated = await db.patrocinadores.find_one({"id": patrocinador_id}, {"_id": 0})
    return PatrocinadorResponse(**updated)

@api_router.delete("/patrocinadores/{patrocinador_id}")
async def delete_patrocinador(patrocinador_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.patrocinadores.delete_one({"id": patrocinador_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patrocinador not found")
    return {"message": "Patrocinador deleted successfully"}

# ==================== RECEITAS ROUTES ====================

@api_router.get("/recebimentos", response_model=List[RecebimentoResponse])
async def list_recebimentos(mes: Optional[int] = None, ano: Optional[int] = None, current_user: dict = Depends(get_current_user)):
    query = {}
    if mes and ano:
        query["data"] = {"$regex": f"{ano}-{str(mes).zfill(2)}"}
    elif ano:
        query["data"] = {"$regex": f"^{ano}"}
    recebimentos = await db.recebimentos.find(query, {"_id": 0}).sort("data", -1).to_list(1000)
    patrocinadores = await db.patrocinadores.find({}, {"_id": 0}).to_list(1000)
    
    for rec in recebimentos:
        if rec.get('patrocinador_id'):
            patr = next((p for p in patrocinadores if p['id'] == rec['patrocinador_id']), None)
            rec['patrocinador_nome'] = patr['nome'] if patr else None
        else:
            rec['patrocinador_nome'] = None
    
    return [RecebimentoResponse(**r) for r in recebimentos]

@api_router.post("/recebimentos", response_model=RecebimentoResponse)
async def create_recebimento(recebimento: RecebimentoCreate, current_user: dict = Depends(get_current_user)):
    recebimento_obj = Recebimento(**recebimento.model_dump())
    doc = recebimento_obj.model_dump()
    doc['criado_em'] = doc['criado_em'].isoformat()
    await db.recebimentos.insert_one(doc)
    
    doc['patrocinador_nome'] = None
    if doc.get('patrocinador_id'):
        patr = await db.patrocinadores.find_one({"id": doc['patrocinador_id']}, {"_id": 0})
        doc['patrocinador_nome'] = patr['nome'] if patr else None
    
    return RecebimentoResponse(**doc)

@api_router.get("/recebimentos/{recebimento_id}", response_model=RecebimentoResponse)
async def get_recebimento(recebimento_id: str, current_user: dict = Depends(get_current_user)):
    recebimento = await db.recebimentos.find_one({"id": recebimento_id}, {"_id": 0})
    if not recebimento:
        raise HTTPException(status_code=404, detail="Recebimento not found")
    
    recebimento['patrocinador_nome'] = None
    if recebimento.get('patrocinador_id'):
        patr = await db.patrocinadores.find_one({"id": recebimento['patrocinador_id']}, {"_id": 0})
        recebimento['patrocinador_nome'] = patr['nome'] if patr else None
    
    return RecebimentoResponse(**recebimento)

@api_router.put("/recebimentos/{recebimento_id}", response_model=RecebimentoResponse)
async def update_recebimento(recebimento_id: str, recebimento: RecebimentoCreate, current_user: dict = Depends(get_current_user)):
    existing = await db.recebimentos.find_one({"id": recebimento_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Recebimento not found")
    
    update_data = recebimento.model_dump()
    await db.recebimentos.update_one({"id": recebimento_id}, {"$set": update_data})
    updated = await db.recebimentos.find_one({"id": recebimento_id}, {"_id": 0})
    
    updated['patrocinador_nome'] = None
    if updated.get('patrocinador_id'):
        patr = await db.patrocinadores.find_one({"id": updated['patrocinador_id']}, {"_id": 0})
        updated['patrocinador_nome'] = patr['nome'] if patr else None
    
    return RecebimentoResponse(**updated)

@api_router.delete("/recebimentos/{recebimento_id}")
async def delete_recebimento(recebimento_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.recebimentos.delete_one({"id": recebimento_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Recebimento not found")
    return {"message": "Recebimento deleted successfully"}

# ==================== DESPESAS ROUTES ====================

@api_router.get("/despesas", response_model=List[DespesaResponse])
async def list_despesas(mes: Optional[int] = None, ano: Optional[int] = None, current_user: dict = Depends(get_current_user)):
    query = {}
    if mes and ano:
        query["data"] = {"$regex": f"{ano}-{str(mes).zfill(2)}"}
    elif ano:
        query["data"] = {"$regex": f"^{ano}"}
    despesas = await db.despesas.find(query, {"_id": 0}).sort("data", -1).to_list(1000)
    return [DespesaResponse(**d) for d in despesas]

@api_router.post("/despesas", response_model=DespesaResponse)
async def create_despesa(despesa: DespesaCreate, current_user: dict = Depends(get_current_user)):
    despesa_obj = Despesa(**despesa.model_dump())
    doc = despesa_obj.model_dump()
    doc['criado_em'] = doc['criado_em'].isoformat()
    await db.despesas.insert_one(doc)
    return DespesaResponse(**doc)

@api_router.get("/despesas/{despesa_id}", response_model=DespesaResponse)
async def get_despesa(despesa_id: str, current_user: dict = Depends(get_current_user)):
    despesa = await db.despesas.find_one({"id": despesa_id}, {"_id": 0})
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa not found")
    return DespesaResponse(**despesa)

@api_router.put("/despesas/{despesa_id}", response_model=DespesaResponse)
async def update_despesa(despesa_id: str, despesa: DespesaCreate, current_user: dict = Depends(get_current_user)):
    existing = await db.despesas.find_one({"id": despesa_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Despesa not found")
    
    update_data = despesa.model_dump()
    await db.despesas.update_one({"id": despesa_id}, {"$set": update_data})
    updated = await db.despesas.find_one({"id": despesa_id}, {"_id": 0})
    return DespesaResponse(**updated)

@api_router.delete("/despesas/{despesa_id}")
async def delete_despesa(despesa_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.despesas.delete_one({"id": despesa_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Despesa not found")
    return {"message": "Despesa deleted successfully"}

# ==================== DASHBOARD ROUTES ====================

@api_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(mes: Optional[int] = None, ano: Optional[int] = None, current_user: dict = Depends(get_current_user)):
    # Atletas ativos
    total_atletas = await db.atletas.count_documents({"ativo": True})
    
    # Treinos
    treino_query = {}
    if mes and ano:
        treino_query = {"data": {"$regex": f"{ano}-{str(mes).zfill(2)}"}}
    total_treinos = await db.treinos.count_documents(treino_query)
    
    # Partidas
    partida_query = {}
    if mes and ano:
        partida_query = {"data": {"$regex": f"{ano}-{str(mes).zfill(2)}"}}
    total_partidas = await db.partidas.count_documents(partida_query)
    
    # Finanças - Use aggregation to sum directly in database
    receita_query = {}
    despesa_query = {}
    if mes and ano:
        receita_query = {"data": {"$regex": f"{ano}-{str(mes).zfill(2)}"}}
        despesa_query = {"data": {"$regex": f"{ano}-{str(mes).zfill(2)}"}}
    
    # Aggregate sum for receitas
    receitas_pipeline = [
        {"$match": receita_query},
        {"$group": {"_id": None, "total": {"$sum": "$valor"}}}
    ]
    receitas_result = await db.recebimentos.aggregate(receitas_pipeline).to_list(1)
    total_receitas = receitas_result[0]['total'] if receitas_result else 0
    
    # Aggregate sum for despesas
    despesas_pipeline = [
        {"$match": despesa_query},
        {"$group": {"_id": None, "total": {"$sum": "$valor"}}}
    ]
    despesas_result = await db.despesas.aggregate(despesas_pipeline).to_list(1)
    total_despesas = despesas_result[0]['total'] if despesas_result else 0
    
    saldo = total_receitas - total_despesas
    
    # Resultados das partidas - Calculate in database
    resultados_pipeline = [
        {"$match": partida_query},
        {"$group": {
            "_id": None,
            "vitorias": {
                "$sum": {
                    "$cond": [{"$gt": ["$gols_clube", "$gols_adversario"]}, 1, 0]
                }
            },
            "empates": {
                "$sum": {
                    "$cond": [{"$eq": ["$gols_clube", "$gols_adversario"]}, 1, 0]
                }
            },
            "derrotas": {
                "$sum": {
                    "$cond": [{"$lt": ["$gols_clube", "$gols_adversario"]}, 1, 0]
                }
            }
        }}
    ]
    resultados = await db.partidas.aggregate(resultados_pipeline).to_list(1)
    
    if resultados:
        vitorias = resultados[0]['vitorias']
        empates = resultados[0]['empates']
        derrotas = resultados[0]['derrotas']
    else:
        vitorias = empates = derrotas = 0
    
    return DashboardStats(
        total_atletas_ativos=total_atletas,
        total_treinos=total_treinos,
        total_partidas=total_partidas,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo,
        vitorias=vitorias,
        empates=empates,
        derrotas=derrotas
    )

@api_router.get("/dashboard/charts")
async def get_dashboard_charts(ano: int = 2024, current_user: dict = Depends(get_current_user)):
    # Receitas vs Despesas por mês - Use aggregation for efficiency
    receitas_pipeline = [
        {"$match": {"data": {"$regex": f"^{ano}"}}},
        {"$group": {
            "_id": {"$substr": ["$data", 5, 2]},
            "total": {"$sum": "$valor"}
        }},
        {"$sort": {"_id": 1}}
    ]
    receitas_mensal = await db.recebimentos.aggregate(receitas_pipeline).to_list(12)
    receitas_dict = {int(r['_id']): r['total'] for r in receitas_mensal}
    
    despesas_pipeline = [
        {"$match": {"data": {"$regex": f"^{ano}"}}},
        {"$group": {
            "_id": {"$substr": ["$data", 5, 2]},
            "total": {"$sum": "$valor"}
        }},
        {"$sort": {"_id": 1}}
    ]
    despesas_mensal = await db.despesas.aggregate(despesas_pipeline).to_list(12)
    despesas_dict = {int(d['_id']): d['total'] for d in despesas_mensal}
    
    financeiro_mensal = []
    for mes in range(1, 13):
        financeiro_mensal.append({
            "mes": mes,
            "receitas": receitas_dict.get(mes, 0),
            "despesas": despesas_dict.get(mes, 0)
        })
    
    # Treinos por mês - Use aggregation
    treinos_pipeline = [
        {"$match": {"data": {"$regex": f"^{ano}"}}},
        {"$group": {
            "_id": {"$substr": ["$data", 5, 2]},
            "total": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    treinos_result = await db.treinos.aggregate(treinos_pipeline).to_list(12)
    treinos_dict = {int(t['_id']): t['total'] for t in treinos_result}
    
    treinos_mensal = []
    for mes in range(1, 13):
        treinos_mensal.append({"mes": mes, "total": treinos_dict.get(mes, 0)})
    
    # Resultados das partidas - Calculate in database
    resultados_pipeline = [
        {"$group": {
            "_id": None,
            "vitorias": {
                "$sum": {
                    "$cond": [{"$gt": ["$gols_clube", "$gols_adversario"]}, 1, 0]
                }
            },
            "empates": {
                "$sum": {
                    "$cond": [{"$eq": ["$gols_clube", "$gols_adversario"]}, 1, 0]
                }
            },
            "derrotas": {
                "$sum": {
                    "$cond": [{"$lt": ["$gols_clube", "$gols_adversario"]}, 1, 0]
                }
            }
        }}
    ]
    resultados = await db.partidas.aggregate(resultados_pipeline).to_list(1)
    
    if resultados:
        vitorias = resultados[0]['vitorias']
        empates = resultados[0]['empates']
        derrotas = resultados[0]['derrotas']
    else:
        vitorias = empates = derrotas = 0
    
    return {
        "financeiro_mensal": financeiro_mensal,
        "treinos_mensal": treinos_mensal,
        "resultados": {
            "vitorias": vitorias,
            "empates": empates,
            "derrotas": derrotas
        }
    }

# ==================== EXPORT ROUTES ====================

def build_date_query(mes: Optional[int], ano: Optional[int]) -> dict:
    """Constrói filtro de data para queries MongoDB."""
    if mes and ano:
        return {"data": {"$regex": f"{ano}-{str(mes).zfill(2)}"}}
    elif ano:
        return {"data": {"$regex": f"^{ano}"}}
    return {}

def build_periodo_label(mes: Optional[int], ano: Optional[int]) -> str:
    """Gera label do período para nome de arquivo."""
    meses_nomes = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]
    if mes and ano:
        return f"_{meses_nomes[mes-1]}_{ano}"
    elif ano:
        return f"_{ano}"
    return "_todos"

@api_router.get("/export/excel/{tipo}")
async def export_excel(tipo: str, mes: Optional[int] = None, ano: Optional[int] = None, current_user: dict = Depends(get_current_user)):
    wb = openpyxl.Workbook()
    ws = wb.active
    date_query = build_date_query(mes, ano)
    periodo = build_periodo_label(mes, ano)
    
    if tipo == "atletas":
        ws.title = "Atletas"
        ws.append(["Nome", "Posição", "Telefone", "Ativo"])
        atletas = await db.atletas.find({}, {"_id": 0}).to_list(1000)
        for a in atletas:
            ws.append([a['nome'], a['posicao'], a['telefone'], "Sim" if a['ativo'] else "Não"])
    
    elif tipo == "treinos":
        ws.title = "Treinos"
        ws.append(["Data", "Local", "Observações", "Presenças"])
        match_stage = {"$match": date_query} if date_query else {"$match": {}}
        pipeline = [
            match_stage,
            {"$lookup": {
                "from": "presencas",
                "localField": "id",
                "foreignField": "treino_id",
                "as": "presencas"
            }},
            {"$addFields": {
                "total_presencas": {
                    "$size": {
                        "$filter": {
                            "input": "$presencas",
                            "cond": {"$eq": ["$$this.presente", True]}
                        }
                    }
                }
            }},
            {"$project": {
                "_id": 0,
                "data": 1,
                "local": 1,
                "observacoes": 1,
                "total_presencas": 1
            }},
            {"$sort": {"data": -1}},
            {"$limit": 1000}
        ]
        treinos = await db.treinos.aggregate(pipeline).to_list(1000)
        for t in treinos:
            ws.append([t['data'], t['local'], t.get('observacoes', ''), t['total_presencas']])
    
    elif tipo == "partidas":
        ws.title = "Partidas"
        ws.append(["Data", "Adversário", "Local", "Gols E.C.P", "Gols Adversário", "Resultado"])
        partidas = await db.partidas.find(date_query, {"_id": 0}).sort("data", -1).to_list(1000)
        for p in partidas:
            resultado = calcular_resultado(p['gols_clube'], p['gols_adversario'])
            ws.append([p['data'], p['adversario'], p['local'], p['gols_clube'], p['gols_adversario'], resultado])
    
    elif tipo == "financeiro":
        ws.title = "Financeiro"
        ws.append(["Tipo", "Data", "Descrição", "Valor"])
        recebimentos = await db.recebimentos.find(date_query, {"_id": 0}).sort("data", -1).to_list(1000)
        for r in recebimentos:
            ws.append(["Receita", r['data'], r['descricao'], r['valor']])
        despesas = await db.despesas.find(date_query, {"_id": 0}).sort("data", -1).to_list(1000)
        for d in despesas:
            ws.append(["Despesa", d['data'], d['descricao'], d['valor']])
    
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=ecp_{tipo}{periodo}.xlsx"}
    )

@api_router.get("/export/pdf/{tipo}")
async def export_pdf(tipo: str, mes: Optional[int] = None, ano: Optional[int] = None, current_user: dict = Depends(get_current_user)):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    date_query = build_date_query(mes, ano)
    periodo = build_periodo_label(mes, ano)
    
    meses_nomes = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    if mes and ano:
        periodo_titulo = f" - {meses_nomes[mes-1]}/{ano}"
    elif ano:
        periodo_titulo = f" - {ano}"
    else:
        periodo_titulo = " - Todos"
    
    title = Paragraph(f"<b>E.C.P - Relatório de {tipo.capitalize()}{periodo_titulo}</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    if tipo == "atletas":
        atletas = await db.atletas.find({}, {"_id": 0}).to_list(1000)
        data = [["Nome", "Posição", "Telefone", "Ativo"]]
        for a in atletas:
            data.append([a['nome'], a['posicao'], a['telefone'], "Sim" if a['ativo'] else "Não"])
    
    elif tipo == "treinos":
        treinos = await db.treinos.find(date_query, {"_id": 0}).sort("data", -1).to_list(1000)
        data = [["Data", "Local", "Observações"]]
        for t in treinos:
            data.append([t['data'], t['local'], t.get('observacoes', '')])
    
    elif tipo == "partidas":
        partidas = await db.partidas.find(date_query, {"_id": 0}).sort("data", -1).to_list(1000)
        data = [["Data", "Adversário", "Placar", "Resultado"]]
        for p in partidas:
            resultado = calcular_resultado(p['gols_clube'], p['gols_adversario'])
            placar = f"{p['gols_clube']} x {p['gols_adversario']}"
            data.append([p['data'], p['adversario'], placar, resultado])
    
    elif tipo == "financeiro":
        recebimentos = await db.recebimentos.find(date_query, {"_id": 0}).sort("data", -1).to_list(1000)
        despesas = await db.despesas.find(date_query, {"_id": 0}).sort("data", -1).to_list(1000)
        data = [["Tipo", "Data", "Descrição", "Valor"]]
        for r in recebimentos:
            data.append(["Receita", r['data'], r['descricao'], f"R$ {r['valor']:.2f}"])
        for d in despesas:
            data.append(["Despesa", d['data'], d['descricao'], f"R$ {d['valor']:.2f}"])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=ecp_{tipo}.pdf"}
    )

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
