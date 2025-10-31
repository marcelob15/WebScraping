import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urljoin

def get_book_details(book_url):
    """
    Extrai os detalhes de um único livro a partir da sua URL.

    Args:
        book_url (str): A URL da página do livro.

    Returns:
        dict: Um dicionário contendo os detalhes do livro, ou None se ocorrer um erro.
    """
    try:
        response = requests.get(book_url)
        response.raise_for_status()  # Lança uma exceção para códigos de status HTTP ruins
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extração das informações
        title = soup.find('h1').text
        # A tabela de informações do produto contém preço, disponibilidade e UPC
        product_info = {th.text: td.text for th, td in zip(soup.select('table th'), soup.select('table td'))}
        price = product_info.get('Price (incl. tax)')
        availability = product_info.get('Availability')
        # Limpa o texto da disponibilidade para obter apenas o número
        if availability:
            availability = availability.split('(')[1].replace(' available)', '').strip()

        # O rating é dado por uma classe CSS, ex: 'star-rating Three'
        rating_class = soup.select_one('.star-rating')['class'][1]
        ratings_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = ratings_map.get(rating_class, 0)
        
        # A categoria está no breadcrumb
        category = soup.select_one('.breadcrumb li:nth-of-type(3) a').text
        
        # A URL da imagem precisa ser unida com a URL base
        image_relative_url = soup.select_one('#product_gallery img')['src']
        
        # Usando urljoin para construir a URL absoluta
        image_url = urljoin(book_url, image_relative_url)

        return {
            'title': title,
            'price': price,
            'rating': rating,
            'availability': availability,
            'category': category,
            'image_url': image_url,
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {book_url}: {e}")
        return None
    except (AttributeError, IndexError) as e:
        print(f"Erro ao parsear a página {book_url}: {e}")
        return None


def scrape_all_books():
    """
    Realiza o scraping de todos os livros do site books.toscrape.com,
    navegando por todas as páginas.
    
    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um livro.
    """
    base_url = 'https://books.toscrape.com/catalogue/'
    current_page_url = base_url + 'page-1.html'
    all_books_data = []
    page_number = 1

    while current_page_url:
        print(f"Scraping página {page_number}: {current_page_url}")
        response = requests.get(current_page_url, timeout=10)

        if response.status_code != 200:
            print(f"Falha ao acessar a página {page_number}. Status: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontra todos os links de livros na página atual
        book_links = [base_url + a['href'].replace('../', '') for a in soup.select('article.product_pod h3 a')]
        
        for link in book_links:
            book_details = get_book_details(link)
            if book_details:
                all_books_data.append(book_details)
        
        # Verifica se há um botão "next" para a próxima página
        next_button = soup.select_one('.next a')
        if next_button:
            current_page_url = base_url + next_button['href']
            page_number += 1
        else:
            current_page_url = None # Fim da paginação

    return all_books_data


if __name__ == '__main__':
    print("Iniciando o processo de web scraping...")
    books_data = scrape_all_books()
    
    if books_data:
        print(f"Scraping finalizado. Total de {len(books_data)} livros encontrados.")
        
        # Converte a lista de dicionários para um DataFrame do Pandas
        df = pd.DataFrame(books_data)
        
        # Garante que o diretório data exista
        output_dir = 'data'
        os.makedirs(output_dir, exist_ok=True)
        
        # Salva os dados em um arquivo CSV
        output_path = os.path.join(output_dir, 'books.csv')
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"Dados salvos com sucesso em: {output_path}")
    else:
        print("Nenhum livro foi extraído. Verifique o script ou a conexão com a internet.")