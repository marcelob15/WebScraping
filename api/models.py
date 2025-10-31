from pydantic import BaseModel, Field
from typing import List, Dict



class Book(BaseModel):
    """
    Representa a estrutura de dados de webscapping de um livro. 
    """    
    id: int
    title: str
    price: str
    rating: int
    availability: int
    category: str
    image_url: str

    class Config:
         from_attributes = True

# --- NOVOS MODELOS PARA ESTATÍSTICAS ---

class RatingDistribution(BaseModel):
    """Modelo para a distribuição de ratings."""
    rating: int = Field(..., description="A nota de avaliação (de 1 a 5)")
    count: int = Field(..., description="Número de livros com essa nota")

class OverviewStats(BaseModel):
    """Modelo para as estatísticas gerais da coleção."""
    total_books: int
    average_price: float
    rating_distribution: List[RatingDistribution]

class CategoryStat(BaseModel):
    """Modelo para as estatísticas de uma categoria específica."""
    category: str
    book_count: int
    average_price: float


class BookFeatures(BaseModel):
    """
    Representa as features numéricas de um único livro, prontas para serem usadas por um modelo.
    """
    id: int
    price_numeric: float = Field(..., description="O preço do livro como um número float.")
    # Usamos um dicionário para as categorias, pois não sabemos os nomes de todas as colunas de antemão.
    category_features: Dict[str, int] = Field(..., description="Features One-Hot Encoded para a categoria do livro.")

    '''
    O que é One-Hot Encoding?
    É um processo para converter variáveis categóricas (como 'Ficção', 'Mistério', 'Ciência') 
    em um formato numérico. Em vez de atribuir valores arbitrários (ex: Ficção=1, Mistério=2),
    que criaria uma falsa relação de ordem (Mistério > Ficção), o One-Hot Encoding cria uma nova 
    coluna binária (0 ou 1) para cada categoria possível.
    '''

class TrainingDataRecord(BookFeatures):
    """
    Representa um registro completo para treinamento, incluindo as features e a variável alvo.
    """
    target_rating: int = Field(..., description="A variável alvo (target) que queremos prever: o rating do livro.")

class PredictionRequest(BaseModel):
    """
    Modelo para o corpo da requisição do endpoint de predição.
    Recebe as features de um livro para o qual queremos uma predição.
    """
    price_numeric: float
    category_features: Dict[str, int]

class PredictionResponse(BaseModel):
    """
    Modelo para a resposta do endpoint de predição.
    """
    predicted_rating: float    