# ------------------------------------------------------------------------------
# Este arquivo configura e executa a aplicação FastAPI, definindo todos os
# endpoints, a lógica de autenticação, o carregamento de dados e a estrutura
# de Machine Learning.
# ------------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException, Query, Depends, APIRouter, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
import pandas as pd
from typing import List, Optional, Dict
import os
import random
from config import settings

# ------------------------------------------------------------------------------
# --- Importação de Modelos Pydantic ---
from .models import (
    Book, OverviewStats, CategoryStat,
    BookFeatures, TrainingDataRecord, PredictionRequest, PredictionResponse
)


# ------------------------------------------------------------------------------
# --- Seção de segurança ---
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer

# Implementa um fluxo de autenticação padrão OAuth2 com JWT (JSON Web Tokens).

# Instância única para gerenciar a criptografia de senhas.
# 'argon2' é o esquema padrão por ser mais robusto contra ataques de força bruta
# em comparação com o 'bcrypt'.
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica uma senha em plain-text contra um hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha usando o algoritmo padrão (argon2)."""
    return pwd_context.hash(password)

def authenticate_user(db: dict, username: str, password: str):
    """Autentica um usuário. Retorna os dados do usuário se for bem-sucedido, senão None."""
    if username not in db:
        return None
    user = db[username]
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict):
    """
    Cria um novo token de acesso usando as configurações carregadas.
    """
    to_encode = data.copy()
    # Usa os valores do objeto 'settings' em vez de constantes hardcoded
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Usa a chave secreta e o algoritmo do objeto 'settings'
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(data: dict):
    """
    Cria um novo refresh token.
    """
    to_encode = data.copy()
    # Usa o valor do objeto 'settings'
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Decodifica o token para obter o usuário atual.
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM] 
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


def get_current_user_from_refresh(token: str = Depends(oauth2_scheme)):
    """Função similar para o refresh token."""
    return get_current_user(token)


# ------------------------------------------------------------------------------
# Inicializa a instância do FastAPI e executa a lógica de startup, como o
# carregamento e pré-processamento dos dados.

# --- Simulação de banco de dados de usuários ---
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),        
        "disabled": False,
    }
}



# ------------------------------------------------------------------------------
# --- Configuração Inicial da Aplicação ---
description = """
API para extração de dados de livros do site 'books.toscrape.com'.

Implementa um pipeline de dados completo, desde web scraping até a disponibilização via API RESTful com autenticação JWT e endpoints preparados para Machine Learning.
"""

app = FastAPI(
    title="API Pública para Consulta de Livros",
    description=description,
    version="1.0.0",
    contact={
        "name": "Marcelo Bertin",
        "email": "marcelob0904@gmail.com",
    },
)

# --- Página inicial ---
@app.get("/", response_class=HTMLResponse,)
async def homepage():
    return """
    <html>
        <head>
            <title>Fase 1 - Machine Learning Engineering</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>📚 Fase 1 - Machine Learning Engineering</h1>
            <p>API Pública para Consulta de Livros</p>
            <a href="/docs" style="font-size: 20px; color: blue;">➡️ Abrir Swagger Docs</a>
        </body>
    </html>
    """

# --- Carregamento e pré-processamento de dados ---
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'books.csv')
df_books = pd.DataFrame()
df_ml = pd.DataFrame() # DataFrame específico para dados de ML

try:
    df_books = pd.read_csv(DATA_PATH)
    df_books.reset_index(inplace=True)
    df_books.rename(columns={'index': 'id'}, inplace=True)
    df_books['price_numeric'] = df_books['price'].str.replace(r'[^\d.]', '', regex=True).astype(float)


    category_dummies = pd.get_dummies(df_books['category'], prefix='category', dtype=int)
    df_ml = pd.concat([df_books[['id', 'price_numeric', 'rating']], category_dummies], axis=1)

except FileNotFoundError:
    print("AVISO: Arquivo 'data/books.csv' não encontrado. Endpoints de dados e ML não funcionarão.")

# --- Função de Checagem Auxiliar ---
def check_data_loaded():
    if df_books.empty:
        raise HTTPException(status_code=503, detail="Os dados dos livros não estão disponíveis. Execute o scraper primeiro.")



# ------------------------------------------------------------------------------
# --- Definição dos roteadores ---

# Utilizamos APIRouter para modularizar a API. Cada router agrupa um conjunto
# lógico de endpoints, melhorando a organização e a manutenibilidade do código.

endpoint_router = APIRouter(prefix="/api/v1/public", tags=["Endpoints"])
auth_router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])
admin_router = APIRouter(prefix="/api/v1/admin", tags=["Admin (Protegido)"], dependencies=[Depends(get_current_user)])
ml_router = APIRouter(prefix="/api/v1/ml", tags=["Machine Learning"])




# ------------------------------------------------------------------------------
# Cada função abaixo corresponde a um endpoint da API.

# --- Endpoints opcionais da api (endpoints de insights) ---

#GET /api/v1/stats/overview: estatísticas gerais da coleção (total de livros, preço médio, distribuição de ratings).
@endpoint_router.get("/stats/overview", response_model=OverviewStats)
async def get_overview_stats():
    check_data_loaded()
    total_books = len(df_books)
    average_price = round(df_books['price_numeric'].mean(), 2)
    rating_dist_df = df_books['rating'].value_counts().reset_index()
    rating_dist_df.columns = ['rating', 'count']
    rating_distribution = rating_dist_df.sort_values(by='rating').to_dict(orient='records')
    return {"total_books": total_books, "average_price": average_price, "rating_distribution": rating_distribution}


#GET /api/v1/stats/categories: estatísticas detalhadas por categoria (quantidade de livros, preços por categoria).
@endpoint_router.get("/stats/categories", response_model=List[CategoryStat])
async def get_category_stats():
    check_data_loaded()
    stats = df_books.groupby('category').agg(book_count=('id', 'count'), average_price=('price_numeric', 'mean')).reset_index()
    stats['average_price'] = stats['average_price'].round(2)
    return stats.to_dict(orient='records')


#GET /api/v1/books/top-rated: lista os livros com melhor avaliação (rating mais alto).
@endpoint_router.get("/books/top-rated", response_model=List[Book])
async def get_top_rated_books(limit: int = Query(10, ge=1, le=50)):
    check_data_loaded()
    top_books = df_books[df_books['rating'] == 5].head(limit)
    return top_books.to_dict(orient='records')


#GET /api/v1/books/price-range?min={min}&max={max}: filtra livros dentro de uma faixa de preço específica.
@endpoint_router.get("/books/price-range", response_model=List[Book])
async def get_books_by_price_range(min_price: float = Query(..., ge=0), max_price: float = Query(..., ge=0)):
    check_data_loaded()
    if min_price > max_price:
        raise HTTPException(status_code=400, detail="O preço mínimo não pode ser maior que o preço máximo.")
    filtered_books = df_books[(df_books['price_numeric'] >= min_price) & (df_books['price_numeric'] <= max_price)]
    if filtered_books.empty:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado na faixa de preço especificada.")
    return filtered_books.to_dict(orient='records')



# ------------------------------------------------------------------------------
# --- Endpoints obrigatórios da api (endpoints core) ---

#GET /api/v1/books: lista todos os livros disponíveis na base de dados.
@endpoint_router.get("/books", response_model=List[Book])
async def get_all_books():
    check_data_loaded()
    return df_books.to_dict(orient='records')


#GET /api/v1/books/search?title={title}&category={category}: busca livros por título e/ou categoria.
@endpoint_router.get("/books/search", response_model=List[Book])
async def search_books(
    title: Optional[str] = Query(None, min_length=3, description="Busca livros por parte do título."), 
    category: Optional[str] = Query(None, description="Filtra livros por uma categoria específica.")):

    check_data_loaded()
    if not title and not category:
        raise HTTPException(status_code=400, detail="Forneça 'title' ou 'category' para a busca.")
    result_df = df_books.copy()
    if title:
        # Filtra por título (case-insensitive)
        result_df = result_df[result_df['title'].str.contains(title, case=False, na=False)]

    if category:
          # Filtra por categoria (case-insensitive)
        result_df = result_df[result_df['category'].str.lower() == category.lower()]

    if result_df.empty:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado com os critérios fornecidos.")
    
    return result_df.to_dict(orient='records')


#GET /api/v1/books/{id}: retorna detalhes completos de um livro específico pelo ID.
@endpoint_router.get("/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    check_data_loaded()
    if book_id < 0 or book_id >= len(df_books):
        raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado.")
    book = df_books.loc[book_id].to_dict()
    return book


#GET /api/v1/categories: lista todas as categorias de livros disponíveis.
@endpoint_router.get("/categories", response_model=List[str])
async def get_categories():
    check_data_loaded()
    return df_books['category'].unique().tolist()


#GET /api/v1/health: verifica status da API e conectividade com os dados.
@endpoint_router.get("/health", tags=["Status"])
async def health_check():
    if not df_books.empty:
        return JSONResponse(content={"status": "ok", "data_loaded": True, "books_count": len(df_books)})
    else:
        return JSONResponse(content={"status": "error", "data_loaded": False, "message": "Dados não encontrados."}, status_code=503)







# ------------------------------------------------------------------------------
# --- Endpoints desafio 1: sistema de autenticação ---

#POST /api/v1/auth/login - obter token.
@auth_router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos")
    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


#POST /api/v1/auth/refresh - renovar token.
@auth_router.post("/refresh")
async def refresh_access_token(current_user: str = Depends(get_current_user_from_refresh)):
    access_token = create_access_token(data={"sub": current_user})
    return {"access_token": access_token, "token_type": "bearer"}


#Proteger endpoints de admin como /api/v1/scraping/trigger.
@admin_router.post("/scraping/trigger")
async def trigger_scraping(current_user: str = Depends(get_current_user)):
    print(f"Processo de scraping disparado pelo usuário: {current_user}")
    return {"message": "Processo de scraping iniciado com sucesso!", "triggered_by": current_user}



# ------------------------------------------------------------------------------
# --- Endpoints desafio 2: pipeline ml-ready ---

#GET /api/v1/ml/features - dados formatados para features.
@ml_router.get("/features/{book_id}", response_model=BookFeatures)
async def get_features_for_book(book_id: int):
    check_data_loaded()
    if book_id not in df_ml['id'].values:
        raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado.")
    book_data = df_ml[df_ml['id'] == book_id].iloc[0]
    category_features = {col: int(book_data[col]) for col in book_data.index if 'category_' in col}
    return {"id": book_id, "price_numeric": book_data['price_numeric'], "category_features": category_features}


#GET /api/v1/ml/training-data - dataset para treinamento.
@ml_router.get("/training-data", response_model=List[TrainingDataRecord])
async def get_training_data(limit: Optional[int] = Query(100, ge=1, le=1000)):
    check_data_loaded()
    records = []
    for _, row in df_ml.head(limit).iterrows():
        category_features = {col: int(row[col]) for col in row.index if 'category_' in col}
        records.append({
            "id": int(row['id']), "price_numeric": row['price_numeric'],
            "category_features": category_features, "target_rating": int(row['rating'])
        })
    return records


#POST /api/v1/ml/predictions - endpoint para receber predições.
@ml_router.post("/predictions", response_model=PredictionResponse)
async def get_prediction(request: PredictionRequest):
    price_score = 5 - (request.price_numeric / 20)
    active_category = next((cat.replace("category_", "") for cat, val in request.category_features.items() if val == 1), "none")
    category_bonus = 0.5 if active_category in ["Science Fiction", "Fantasy", "Mystery"] else 0
    predicted_rating = price_score + category_bonus + random.uniform(-0.5, 0.5)
    predicted_rating = max(1.0, min(5.0, predicted_rating))
    return {"predicted_rating": round(predicted_rating, 2)}


# ------------------------------------------------------------------------------
# Inclui todos os roteadores definidos na instância principal do FastAPI.

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(endpoint_router)
app.include_router(ml_router)
