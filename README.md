📘 Pós-Graduação em Machine Learning Engineering - Fase 1

Nome: Marcelo Bertin

Matrícula: RM 368902

---

🧠 Descrição do Projeto

Este projeto foi desenvolvido para o **Fase 1 da Pós-Graduação em Machine Learning Engineering**.  
O objetivo é construir uma solução completa para obtenção e disponibilização de dados de livros, simulando um cenário real em que uma empresa precisa criar sua própria base de dados para um futuro sistema de recomendação.

A solução cobre os seguintes itens — **extração, armazenamento e disponibilização via API** — com arquitetura modular e escalável.

---

🚀 Etapas do Projeto

1️⃣ Extração Automatizada  
O script `scraper.py` navega de forma automatizada no site [books.toscrape.com](https://books.toscrape.com) e coleta informações de cada livro:
- Título  
- Preço  
- Rating
- Disponibilidade  
- Categoria  
- Imagem  

2️⃣ Armazenamento Organizado  
Os dados são processados e armazenados em:
```
data/books.csv
```
Este CSV é a fonte central de dados, garantindo acesso rápido para a aplicação.

3️⃣ Disponibilização via API  
A API, desenvolvida com **FastAPI**, fornece endpoints REST para consulta e análise dos livros.  
Principais rotas:
- 📖 `/books` – Lista todos os livros  
- 📊 `/stats/overview` – Estatísticas gerais  
- 🤖 `/api/v1/ml` - Para machine learning
- 🔐 `/api/v1/auth` - Protege endpoints sensíveis

4️⃣ Segurança e Controle  
Endpoints administrativos usam **JWT (JSON Web Token)** para autenticação, garantindo que apenas usuários autorizados executem certas ações.

---

📂 Estrutura de Pastas

```
📁 WebScraping
├── api/
│   ├── main.py
│   ├── models.py
│   ├── security.py
│   ├── config.py
│
├── data/
│   └── books.csv
│
├── scripts/
│   └── scraper.py
│
├── requirements.txt
└── README.md
```

---

🧩 Tecnologias Utilizadas

| Categoria | Ferramenta |
|------------|-------------|
| Linguagem | Python |
| Framework API | FastAPI |
| Manipulação de dados | Pandas |
| Extração Web | Requests + BeautifulSoup |
| Autenticação | JWT (via PyJWT) |

---

▶️ [Vídeo explicativo no YouTube](https://www.youtube.com/watch?v=1WPQ0RhtLfY)

---

🏗️ Arquitetura da Solução

A arquitetura é dividida em três camadas:

🔹 1. Coleta de Dados (`scraper.py`)  
Responsável por extrair os dados brutos e gerar o arquivo CSV.  
Pode ser executado de forma independente da API, apenas localmente. 
Futuramente será feita pelo enpoint `/api/v1/scraping/trigger`.

🔹 2. Armazenamento (`data/books.csv`)  
Serve como base de dados primária do sistema.  
Futuramente poderá ser substituída por PostgreSQL ou MongoDB.

🔹 3. Serviço (API)  
- `main.py` → Inicializa a API e define as rotas.  
- `models.py` → Define os modelos de dados (Pydantic).  
- `security.py` → Implementa autenticação JWT.  
- `config.py` → Gerencia variáveis de ambiente (.env).

---

![Diagrama da Arquitetura](./diagrama.png)

---

🔄 Fluxo de Dados

1. O scraper coleta e salva os dados no CSV.  
2. A API lê o CSV e carrega as informações em memória.  
3. O usuário consome os endpoints via HTTP.  
4. Rotas autenticadas controlam operações administrativas.

---
⚙️ Instruções de instalação e configuração

🖥️ Execução Local 

✅ Pré-requisitos
- Python 3.9+
- Pip instalado

Instalação

```bash
git clone https://github.com/marcelob15/WebScraping.git
cd WebScraping
python -m venv venv
venv\Scripts\activate        # No Windows
source venv/bin/activate       # No Linux/Mac
pip install -r requirements.txt
```

É necessário criar do arquivo .env no diretório principal para as senhas

Exemplo arquivo .env
```
SECRET_KEY="a8eca3f9d1d0e4c7f8b6c8d4e3fb8c7d6e5f4"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Credenciais do usuário administrador padrão
DEFAULT_ADMIN_PASSWORD="testlearning"
```


---
⚙️ Instruções para execução local

**1️⃣ Executar o scraper (opcional):**
```bash
python scripts/scraper.py
```

**2️⃣ Iniciar a API:**
Caso a porta 9000 esteja em uso na máquina local, use outra porta

```bash
uvicorn api.main:app --reload --port 9000
```


**3️⃣ Acesse a documentação do Swagger:**
👉 [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs)


---

🌐 Instruções para Execução em Produção

O servidor escolhido para hospedagem foi https://vercel.com

A página principal tem um link para entrar na documentação do Swagger do FastApi

👉 [http://web-scraping-khaki.vercel.app/](http://web-scraping-khaki.vercel.app/)

ou 

☁️ Por este link para a documentação do Swagger do FastApi
Acesse:  
👉 [http://web-scraping-khaki.vercel.app/docs](http://web-scraping-khaki.vercel.app/docs)

---

🧾 Documentação das Rotas da API

📚 Endpoints Core

| Método | Endpoint | Descrição |
|--------|-----------|-----------|
| GET | `/api/v1/books` | Lista todos os livros |
| GET | `/api/v1/books/{id}` | Detalhes de um livro específico |
| GET | `/api/v1/books/search?title={t}&category={c}` | Busca livros |
| GET | `/api/v1/categories` | Lista categorias |
| GET | `/api/v1/health` | Verifica status da API |

📈 Endpoints de Insights

| Método | Endpoint | Descrição |
|--------|-----------|-----------|
| GET | `/api/v1/stats/overview` | Estatísticas gerais |
| GET | `/api/v1/stats/categories` | Estatísticas por categoria |
| GET | `/api/v1/books/top-rated` | Livros com maior rating |
| GET | `/api/v1/books/price-range?min=&max=` | Filtra por preço |

📊 Endpoints ML-Ready

| Método | Endpoint | Descrição |
|--------|-----------|-----------|
|GET |  `/api/v1/ml/features ` |	Dados formatados para features de modelos ML |
|GET |  `/api/v1/ml/training-data ` |	Dataset para treinamento de modelos ML |
|POST |	 `/api/v1/ml/predictions ` |	Endpoint para receber predições do modelo |

🔐 Endpoints de Autenticação

| Método | Endpoint | Descrição |
|--------|-----------|-----------|
| POST | `/api/v1/auth/login` | Gera token JWT |
| POST | `/api/v1/auth/refresh` | Renova token |
| POST | `/api/v1/scraping/trigger` | Simula WebScraping |

🔑 Credenciais para login

| Credenciais para login | Valor |
|------------------------|-------------------|
| username | admin |
| password | machinelearning |

---
💬 Exemplos de uso em Deploy (Request/Response)

Cada exemplo inclui uma chamada real com `curl`, o método HTTP, e um exemplo de resposta (`Response body`).

Formato dos exemplos, Linux
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/health'   -H 'accept: application/json'
```

Para windows, coloque --ssl-no-revoke como no exemplo abaixo e troque aspas simples por aspas duplas
```
curl.exe --ssl-no-revoke -X "GET"   "https://web-scraping-khaki.vercel.app/api/v1/public/health"   -H "accept: application/json"
```

---

🧩 ENDPOINTS OBRIGATÓRIOS DA API (CORE)

🌐 GET /api/v1/books  
**Descrição:** Lista todos os livros disponíveis na base de dados.

**Exemplo de Request:**
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/books'   -H 'accept: application/json'
```

**Exemplo de Response:**
```
[
  {
    "id": 0,
    "title": "A Light in the Attic",
    "price": "£51.77",
    "rating": 3,
    "availability": 22,
    "category": "Poetry",
    "image_url": "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"
  },
  {
    "id": 1,
    "title": "Tipping the Velvet",
    "price": "£53.74",
    "rating": 1,
    "availability": 20,
    "category": "Historical Fiction",
    "image_url": "https://books.toscrape.com/media/cache/08/e9/08e94f3731d7d6b760dfbfbc02ca5c62.jpg"
  },
  ... (dados 2 a 997)
  {
    "id": 998,
    "title": "1st to Die (Women's Murder Club #1)",
    "price": "£53.98",
    "rating": 1,
    "availability": 1,
    "category": "Mystery",
    "image_url": "https://books.toscrape.com/media/cache/f6/8e/f68e6ae2f9da04fccbde8442b0a1b52a.jpg"
  },
  {
    "id": 999,
    "title": "1,000 Places to See Before You Die",
    "price": "£26.08",
    "rating": 5,
    "availability": 1,
    "category": "Travel",
    "image_url": "https://books.toscrape.com/media/cache/9e/10/9e106f81f65b293e488718a4f54a6a3f.jpg"
  }
]
```

---

🌐 GET /api/v1/books/{id}  
**Descrição:** Retorna detalhes completos de um livro específico pelo ID.

**Exemplo de Request:**
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/books/1'   -H 'accept: application/json'
```

**Exemplo de Response:**
```
{
  "id": 1,
  "title": "Tipping the Velvet",
  "price": "£53.74",
  "rating": 1,
  "availability": 20,
  "category": "Historical Fiction",
  "image_url": "https://books.toscrape.com/media/cache/08/e9/08e94f3731d7d6b760dfbfbc02ca5c62.jpg"
}
```

---

🌐 GET /api/v1/books/search  
**Descrição:** Busca livros por título e/ou categoria.  
**Parâmetros:**  
- title: busca por título parcial  
- category: filtra por categoria  

**Exemplo de Request (busca por título):**
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/books/search?title=Tipping%20the%20Velvet'   -H 'accept: application/json'
```

**Exemplo de Response:**
```
[
  {
    "id": 1,
    "title": "Tipping the Velvet",
    "price": "£53.74",
    "rating": 1,
    "availability": 20,
    "category": "Historical Fiction",
    "image_url": "https://books.toscrape.com/media/cache/08/e9/08e94f3731d7d6b760dfbfbc02ca5c62.jpg"
  }
]
```

**Exemplo de Request (busca por categoria):**
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/books/search?category=Philosophy'   -H 'accept: application/json'
```

**Exemplo de Response:**
```
[
  {
    "id": 34,
    "title": "Sophie's World",
    "price": "£15.94",
    "rating": 5,
    "availability": 18,
    "category": "Philosophy",
    "image_url": "https://books.toscrape.com/media/cache/d7/39/d73914232130fdf90d66f02fd9798f2b.jpg"
  },
  {
    "id": 68,
    "title": "The Death of Humanity: and the Case for Life",
    "price": "£58.11",
    "rating": 4,
    "availability": 16,
    "category": "Philosophy",
    "image_url": "https://books.toscrape.com/media/cache/3f/f6/3ff6fe5d0c5ca7ab2ed8b5971e299caa.jpg"
  },
  {
    "id": 139,
    "title": "The Stranger",
    "price": "£17.44",
    "rating": 4,
    "availability": 15,
    "category": "Philosophy",
    "image_url": "https://books.toscrape.com/media/cache/c8/1a/c81aea97de1daaa0081d96f8564c204c.jpg"
  },
  {
    "id": 462,
    "title": "Proofs of God: Classical Arguments from Tertullian to Barth",
    "price": "£54.21",
    "rating": 1,
    "availability": 8,
    "category": "Philosophy",
    "image_url": "https://books.toscrape.com/media/cache/f6/cb/f6cb2300a1235a344f1c11b2be9a605d.jpg"
  },
  {
    "id": 473,
    "title": "Kierkegaard: A Christian Missionary to Christians",
    "price": "£47.13",
    "rating": 1,
    "availability": 8,
    "category": "Philosophy",
    "image_url": "https://books.toscrape.com/media/cache/bf/90/bf90ad2c3cab628096db8fca010797b4.jpg"
  },
  {
    "id": 541,
    "title": "At The Existentialist Café: Freedom, Being, and apricot cocktails with: Jean-Paul Sartre, Simone de Beauvoir, Albert Camus, Martin Heidegger, Edmund Husserl, Karl Jaspers, Maurice Merleau-Ponty and others",
    "price": "£29.93",
    "rating": 5,
    "availability": 7,
    "category": "Philosophy",
    "image_url": "https://books.toscrape.com/media/cache/ce/da/ceda6d577d0609261f997bd99872013b.jpg"
  },
  {
    "id": 634,
    "title": "Critique of Pure Reason",
    "price": "£20.75",
    "rating": 1,
    "availability": 5,
    "category": "Philosophy",
    "image_url": "https://books.toscrape.com/media/cache/3b/28/3b28ec3663a81d36272a08e5a49644f2.jpg"
  },
  {
    "id": 894,
    "title": "Run, Spot, Run: The Ethics of Keeping Pets",
    "price": "£20.02",
    "rating": 1,
    "availability": 2,
    "category": "Philosophy",
    "image_url": "https://books.toscrape.com/media/cache/8c/bf/8cbf4667b5798cb8195f1e126ddd6a5c.jpg"
  },
]
```

---

🌐 GET /api/v1/categories  
**Descrição:** Lista todas as categorias de livros disponíveis.

**Exemplo de Request:**
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/categories'   -H 'accept: application/json'
```

**Exemplo de Response:**
```
[
  "Poetry",
  "Historical Fiction",
  "Fiction",
  "Mystery",
  "History",
  "Young Adult",
  "Business",
  "Default",
  "Sequential Art",
  "Music",
  "Science Fiction",
  "Politics",
  "Travel",
  "Thriller",
  "Food and Drink",
  "Romance",
  "Childrens",
  "Nonfiction",
  "Art",
  "Spirituality",
  "Philosophy",
  "New Adult",
  "Contemporary",
  "Fantasy",
  "Add a comment",
  "Science",
  "Health",
  "Horror",
  "Self Help",
  "Religion",
  "Christian",
  "Crime",
  "Autobiography",
  "Christian Fiction",
  "Biography",
  "Womens Fiction",
  "Erotica",
  "Cultural",
  "Psychology",
  "Humor",
  "Historical",
  "Novels",
  "Short Stories",
  "Suspense",
  "Classics",
  "Academic",
  "Sports and Games",
  "Adult Fiction",
  "Parenting",
  "Paranormal"
]
```

---

🌐 GET /api/v1/health  
**Descrição:** Verifica o status da API e conectividade com os dados.

**Exemplo de Request:**
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/health'   -H 'accept: application/json'
```

**Exemplo de Response:**
```
{
  "status": "ok",
  "data_loaded": true,
  "books_count": 1000
}
```

---

📊 ENDPOINTS OPCIONAIS DA API (INSIGHTS)

🌐 GET /api/v1/stats/overview  
**Descrição:** Retorna estatísticas gerais da coleção (total, preço médio e distribuição de ratings).

**Exemplo de Request:**
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/stats/overview'   -H 'accept: application/json'
```

**Exemplo de Response:**
```
{
  "total_books": 1000,
  "average_price": 35.07,
  "rating_distribution": [
    {"rating": 1, "count": 226},
    {"rating": 2, "count": 196},
    {"rating": 3, "count": 203},
    {"rating": 4, "count": 179},
    {"rating": 5, "count": 196}
  ]
}
```

---

🌐 GET /api/v1/stats/categories  
**Descrição:** Exibe estatísticas detalhadas por categoria (quantidade de livros e preço médio).

**Exemplo de Request:**
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/stats/categories'   -H 'accept: application/json'
```

**Exemplo de Response (trecho):**
```
[
  {
    "category": "Academic",
    "book_count": 1,
    "average_price": 13.12
  },
  {
    "category": "Add a comment",
    "book_count": 67,
    "average_price": 35.8
  },
  {
    "category": "Adult Fiction",
    "book_count": 1,
    "average_price": 15.36
  },
  {
    "category": "Art",
    "book_count": 8,
    "average_price": 38.52
  },
  {
    "category": "Autobiography",
    "book_count": 9,
    "average_price": 37.05
  },
  {
    "category": "Biography",
    "book_count": 5,
    "average_price": 33.66
  },
  {
    "category": "Business",
    "book_count": 12,
    "average_price": 32.46
  },
  {
    "category": "Childrens",
    "book_count": 29,
    "average_price": 32.64
  },
  {
    "category": "Christian",
    "book_count": 3,
    "average_price": 42.5
  },
  {
    "category": "Christian Fiction",
    "book_count": 6,
    "average_price": 34.38
  },
  {
    "category": "Classics",
    "book_count": 19,
    "average_price": 36.55
  },
  {
    "category": "Contemporary",
    "book_count": 3,
    "average_price": 36.2
  },
  {
    "category": "Crime",
    "book_count": 1,
    "average_price": 10.97
  },
  {
    "category": "Cultural",
    "book_count": 1,
    "average_price": 36.58
  },
  {
    "category": "Default",
    "book_count": 152,
    "average_price": 34.39
  },
  {
    "category": "Erotica",
    "book_count": 1,
    "average_price": 19.19
  },
  {
    "category": "Fantasy",
    "book_count": 48,
    "average_price": 39.59
  },
  {
    "category": "Fiction",
    "book_count": 65,
    "average_price": 36.07
  },
  {
    "category": "Food and Drink",
    "book_count": 30,
    "average_price": 31.41
  },
  {
    "category": "Health",
    "book_count": 4,
    "average_price": 51.45
  },
  {
    "category": "Historical",
    "book_count": 2,
    "average_price": 22.83
  },
  {
    "category": "Historical Fiction",
    "book_count": 26,
    "average_price": 33.64
  },
  {
    "category": "History",
    "book_count": 18,
    "average_price": 37.29
  },
  {
    "category": "Horror",
    "book_count": 17,
    "average_price": 35.95
  },
  {
    "category": "Humor",
    "book_count": 10,
    "average_price": 33.5
  },
  {
    "category": "Music",
    "book_count": 13,
    "average_price": 35.64
  },
  {
    "category": "Mystery",
    "book_count": 32,
    "average_price": 31.72
  },
  {
    "category": "New Adult",
    "book_count": 6,
    "average_price": 46.38
  },
  {
    "category": "Nonfiction",
    "book_count": 110,
    "average_price": 34.26
  },
  {
    "category": "Novels",
    "book_count": 1,
    "average_price": 54.81
  },
  {
    "category": "Paranormal",
    "book_count": 1,
    "average_price": 15.4
  },
  {
    "category": "Parenting",
    "book_count": 1,
    "average_price": 37.35
  },
  {
    "category": "Philosophy",
    "book_count": 11,
    "average_price": 33.56
  },
  {
    "category": "Poetry",
    "book_count": 19,
    "average_price": 35.97
  },
  {
    "category": "Politics",
    "book_count": 3,
    "average_price": 53.61
  },
  {
    "category": "Psychology",
    "book_count": 7,
    "average_price": 34.22
  },
  {
    "category": "Religion",
    "book_count": 7,
    "average_price": 32.57
  },
  {
    "category": "Romance",
    "book_count": 35,
    "average_price": 33.93
  },
  {
    "category": "Science",
    "book_count": 14,
    "average_price": 33.09
  },
  {
    "category": "Science Fiction",
    "book_count": 16,
    "average_price": 33.8
  },
  {
    "category": "Self Help",
    "book_count": 5,
    "average_price": 40.62
  },
  {
    "category": "Sequential Art",
    "book_count": 75,
    "average_price": 34.57
  },
  {
    "category": "Short Stories",
    "book_count": 1,
    "average_price": 35.88
  },
  {
    "category": "Spirituality",
    "book_count": 6,
    "average_price": 35.1
  },
  {
    "category": "Sports and Games",
    "book_count": 5,
    "average_price": 41.17
  },
  {
    "category": "Suspense",
    "book_count": 1,
    "average_price": 58.33
  },
  {
    "category": "Thriller",
    "book_count": 11,
    "average_price": 31.43
  },
  {
    "category": "Travel",
    "book_count": 11,
    "average_price": 39.79
  },
  {
    "category": "Womens Fiction",
    "book_count": 17,
    "average_price": 36.79
  },
  {
    "category": "Young Adult",
    "book_count": 54,
    "average_price": 35.45
  }
]
```

---

🌐 GET /api/v1/books/top-rated  
**Descrição:** Retorna os livros com melhor avaliação (maior rating).  
**Parâmetro opcional:** limit — número máximo de resultados.

**Exemplo de Request:**
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/books/top-rated?limit=4'   -H 'accept: application/json'
```

**Exemplo de Response:**
```
[
  {
    "id": 4,
    "title": "Sapiens: A Brief History of Humankind",
    "price": "£54.23",
    "rating": 5,
    "availability": 20,
    "category": "History",
    "image_url": "https://books.toscrape.com/media/cache/ce/5f/ce5f052c65cc963cf4422be096e915c9.jpg"
  },
  {
    "id": 12,
    "title": "Set Me Free",
    "price": "£17.46",
    "rating": 5,
    "availability": 19,
    "category": "Young Adult",
    "image_url": "https://books.toscrape.com/media/cache/b8/e9/b8e91bd2fc74c3954118999238abb4b8.jpg"
  },
  {
    "id": 13,
    "title": "Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)",
    "price": "£52.29",
    "rating": 5,
    "availability": 19,
    "category": "Sequential Art",
    "image_url": "https://books.toscrape.com/media/cache/97/27/97275841c81e66d53bf9313cba06f23e.jpg"
  },
  {
    "id": 14,
    "title": "Rip it Up and Start Again",
    "price": "£35.02",
    "rating": 5,
    "availability": 19,
    "category": "Music",
    "image_url": "https://books.toscrape.com/media/cache/81/7f/817f5089c0e6e62738dce2931e7323d3.jpg"
  }
]
```

---

🌐 GET /api/v1/books/price-range  
**Descrição:** Filtra livros dentro de uma faixa de preço.  
**Parâmetros:**  
- min: preço mínimo  
- max: preço máximo  

**Exemplo de Request:**
```
curl -X 'GET'   'https://web-scraping-khaki.vercel.app/api/v1/public/books/price-range?min=7&max=10'   -H 'accept: application/json'
```

**Exemplo de Response (trecho):**
```
[
  {
    "id": 638,
    "title": "An Abundance of Katherines",
    "price": "£10.00",
    "rating": 5,
    "availability": 5,
    "category": "Young Adult",
    "image_url": "https://books.toscrape.com/media/cache/9b/c8/9bc86bc10a6beea536422bbe82e076fb.jpg"
  }
]
```

---

🔐 ENDPOINTS OPCIONAIS DA API (Sistema de Autenticação)

🌐 POST /api/v1/auth/login  
**Descrição:** Autentica um usuário e retorna um access_token e refresh_token.  
**Parâmetros:**  
- Corpo da Requisição (application/x-www-form-urlencoded):
- username: O nome de usuário.
- password: A senha do usuário.
- grant_type: Deve ser "password".


**Exemplo de Request:**
```
curl -X 'POST' \
  'https://web-scraping-khaki.vercel.app/api/v1/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=admin&password=machinelearning&scope=&client_id=string&client_secret=********'
```

**Exemplo de Response (trecho):**
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2MTUyODk4OH0.eXdavUCK-zUMn5FFvKwzk5o7pANGBWfs6fNztHAAEV8",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2MjEzMTk4OH0.PgPVLs0PVqb0AL4s5_d2XXzKBgkIriTzyBoG6S1fPzs",
  "token_type": "bearer"
}
```

🌐 POST /api/v1/auth/refresh  
**Descrição:** Gera um novo `access_token` utilizando um `refresh_token` válido.  
**Parâmetros:**  
- `Authorization`: `Bearer <SEU_REFRESH_TOKEN>`  

**Exemplo de Request:**
```
curl -X 'POST' \
  'https://web-scraping-khaki.vercel.app/api/v1/auth/refresh' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2MTUyODgzOX0.NaJXZBTdt1MdL-CYLb_HmzDGc29Ug0-jZ8dsPmJiAuw' \
  -d ''
```

**Exemplo de Response (trecho):**
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2MTUyOTAyMH0.CxzxaPzI7sWubNNy91KB5VE8bJWV7aTRwsFoI8kZTcI",
  "token_type": "bearer"
}
```


🌐 GET /api/v1/scraping/trigger  
**Descrição:** Dispara o processo de web scraping. Requer autenticação de administrador.  
**Parâmetros:**  
- Authorization: Bearer <SEU_ACCESS_TOKEN>

**Exemplo de Request:**
```
curl -X 'POST' \
  'https://web-scraping-khaki.vercel.app/api/v1/admin/scraping/trigger' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2MTUyNjEwNn0.L8m2ZjIS99vtCbnQL1RLlP4RRDvG_vFikM-eWnT4Dus' \
  -d ''
```

**Exemplo de Response (trecho):**
```
{
  "message": "Processo de scraping iniciado com sucesso!",
  "triggered_by": "admin"
}
```


---

🧠 ENDPOINTS OPCIONAIS DA API (Pipeline ML-Ready)

🌐 GET /api/v1/ml/features  
**Descrição:** Retorna os dados de um item específico, formatados como features (características) para um modelo de ML.  
**Parâmetros:**  
- {id}: O ID do item a ser consultado.  

**Exemplo de Request:**
```
curl -X 'GET' 'https://web-scraping-khaki.vercel.app/api/v1/ml/features/2' -H 'accept: application/json'
```

**Exemplo de Response (trecho):**
```
{
  "id": 2,
  "price_numeric": 50.1,
  "category_features": {
    "category_Academic": 0,
    "category_Add a comment": 0,
    "category_Adult Fiction": 0,
    "category_Art": 0,
    "category_Autobiography": 0,
    "category_Biography": 0,
    "category_Business": 0,
    "category_Childrens": 0,
    "category_Christian": 0,
    "category_Christian Fiction": 0,
    "category_Classics": 0,
    "category_Contemporary": 0,
    "category_Crime": 0,
    "category_Cultural": 0,
    "category_Default": 0,
    "category_Erotica": 0,
    "category_Fantasy": 0,
    "category_Fiction": 1,
    "category_Food and Drink": 0,
    "category_Health": 0,
    "category_Historical": 0,
    "category_Historical Fiction": 0,
    "category_History": 0,
    "category_Horror": 0,
    "category_Humor": 0,
    "category_Music": 0,
    "category_Mystery": 0,
    "category_New Adult": 0,
    "category_Nonfiction": 0,
    "category_Novels": 0,
    "category_Paranormal": 0,
    "category_Parenting": 0,
    "category_Philosophy": 0,
    "category_Poetry": 0,
    "category_Politics": 0,
    "category_Psychology": 0,
    "category_Religion": 0,
    "category_Romance": 0,
    "category_Science": 0,
    "category_Science Fiction": 0,
    "category_Self Help": 0,
    "category_Sequential Art": 0,
    "category_Short Stories": 0,
    "category_Spirituality": 0,
    "category_Sports and Games": 0,
    "category_Suspense": 0,
    "category_Thriller": 0,
    "category_Travel": 0,
    "category_Womens Fiction": 0,
    "category_Young Adult": 0
  }
}
```

🌐 GET /api/v1/ml/training-data  
**Descrição:** Retorna um conjunto de dados brutos para treinamento de modelo.  
**Parâmetros:**  
- limit (opcional): Limita a quantidade de registros retornados. Ex: ?limit=100. 

**Exemplo de Request:**
```
curl -X 'GET' 'https://web-scraping-khaki.vercel.app/api/v1/ml/training-data?limit=2' -H 'accept: application/json'
```

**Exemplo de Response (trecho):**
```
[
  {
    "id": 0,
    "price_numeric": 51.77,
    "category_features": {
      "category_Academic": 0,
      "category_Add a comment": 0,
      "category_Adult Fiction": 0,
      "category_Art": 0,
      "category_Autobiography": 0,
      "category_Biography": 0,
      "category_Business": 0,
      "category_Childrens": 0,
      "category_Christian": 0,
      "category_Christian Fiction": 0,
      "category_Classics": 0,
      "category_Contemporary": 0,
      "category_Crime": 0,
      "category_Cultural": 0,
      "category_Default": 0,
      "category_Erotica": 0,
      "category_Fantasy": 0,
      "category_Fiction": 0,
      "category_Food and Drink": 0,
      "category_Health": 0,
      "category_Historical": 0,
      "category_Historical Fiction": 0,
      "category_History": 0,
      "category_Horror": 0,
      "category_Humor": 0,
      "category_Music": 0,
      "category_Mystery": 0,
      "category_New Adult": 0,
      "category_Nonfiction": 0,
      "category_Novels": 0,
      "category_Paranormal": 0,
      "category_Parenting": 0,
      "category_Philosophy": 0,
      "category_Poetry": 1,
      "category_Politics": 0,
      "category_Psychology": 0,
      "category_Religion": 0,
      "category_Romance": 0,
      "category_Science": 0,
      "category_Science Fiction": 0,
      "category_Self Help": 0,
      "category_Sequential Art": 0,
      "category_Short Stories": 0,
      "category_Spirituality": 0,
      "category_Sports and Games": 0,
      "category_Suspense": 0,
      "category_Thriller": 0,
      "category_Travel": 0,
      "category_Womens Fiction": 0,
      "category_Young Adult": 0
    },
    "target_rating": 3
  },
  {
    "id": 1,
    "price_numeric": 53.74,
    "category_features": {
      "category_Academic": 0,
      "category_Add a comment": 0,
      "category_Adult Fiction": 0,
      "category_Art": 0,
      "category_Autobiography": 0,
      "category_Biography": 0,
      "category_Business": 0,
      "category_Childrens": 0,
      "category_Christian": 0,
      "category_Christian Fiction": 0,
      "category_Classics": 0,
      "category_Contemporary": 0,
      "category_Crime": 0,
      "category_Cultural": 0,
      "category_Default": 0,
      "category_Erotica": 0,
      "category_Fantasy": 0,
      "category_Fiction": 0,
      "category_Food and Drink": 0,
      "category_Health": 0,
      "category_Historical": 0,
      "category_Historical Fiction": 1,
      "category_History": 0,
      "category_Horror": 0,
      "category_Humor": 0,
      "category_Music": 0,
      "category_Mystery": 0,
      "category_New Adult": 0,
      "category_Nonfiction": 0,
      "category_Novels": 0,
      "category_Paranormal": 0,
      "category_Parenting": 0,
      "category_Philosophy": 0,
      "category_Poetry": 0,
      "category_Politics": 0,
      "category_Psychology": 0,
      "category_Religion": 0,
      "category_Romance": 0,
      "category_Science": 0,
      "category_Science Fiction": 0,
      "category_Self Help": 0,
      "category_Sequential Art": 0,
      "category_Short Stories": 0,
      "category_Spirituality": 0,
      "category_Sports and Games": 0,
      "category_Suspense": 0,
      "category_Thriller": 0,
      "category_Travel": 0,
      "category_Womens Fiction": 0,
      "category_Young Adult": 0
    },
    "target_rating": 1
  }
]
```

🌐 POST /api/v1/ml/predictions  
**Descrição:** Recebe um conjunto de features e retorna a predição do modelo.  
**Parâmetros:**  
- Um objeto JSON com as features do item, como price_numeric e category_features.  

**Exemplo de Request:**
```
curl -X 'POST' \
  'http://127.0.0.1:9000/api/v1/ml/predictions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "price_numeric": 25.50,
  "category_features": {
    "category_Science Fiction": 1,
    "category_Fantasy": 0,
    "category_Mystery": 0
  }
}'

```

**Exemplo de Response (trecho):**
```
{
  "predicted_rating": 3.75
}
```

---

📘 Observação:  
Todos os endpoints retornam JSON e seguem o padrão RESTful.  

---

💡 Melhorias Futuras

- Substituir CSV por banco de dados.  
- Implementar paginação e filtros avançados.  
- Implementar a atualização do webscrapping no endpoint /api/v1/scraping/trigger.
- Implementar nos enpoints de ML funções reais.
