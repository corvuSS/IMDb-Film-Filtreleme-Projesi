import concurrent.futures
from imdb import IMDb
from googletrans import Translator

def fetch_movie_details(movie):
    ia = IMDb()
    movie_id = movie.movieID
    movie_details = ia.get_movie(movie_id)
    baslik = movie_details.get('title', 'N/A')
    yil = movie_details.get('year', 'N/A')
    puan = movie_details.get('rating', 'N/A')
    ozet = movie_details.get('plot', ['N/A'])[0]
    
    try:
        puan = float(puan) if puan and puan != 'N/A' else 0.0
    except (ValueError, TypeError):
        puan = 0.0
    
    return {
        'Baslik': baslik,
        'Yil': yil,
        'IMDb Puani': puan,
        'Ozet': ozet
    }

def translate_to_turkish(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='tr')
    return translation.text

def get_movies_by_keyword(keyword, max_results=10):
    ia = IMDb()
    movies = ia.search_movie(keyword)

    if not movies:
        return []

    movies = movies[:max_results]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_movie_details, movies))

    # IMDb puanına göre sıralama
    sorted_movies = sorted(results, key=lambda x: x['IMDb Puani'], reverse=True)


    # Özetleri Türkçe'ye çevirme
    for movie in sorted_movies:
        if movie['Ozet'] != 'N/A':
            movie['Ozet'] = translate_to_turkish(movie['Ozet'])

    return sorted_movies

def display_movies(movies):
    for movie in movies:
        print(f"Başlık: {movie['Baslik']}")
        print(f"Yıl: {movie['Yil']}")
        print(f"IMDb Puanı: {movie['IMDb Puani']}")
        print(f"Özet: {movie['Ozet']}")
        print("-" * 50)

if __name__ == "__main__":
    keyword = input("Anahtar kelimeyi giriniz: ")

    movies = get_movies_by_keyword(keyword)
    if movies:
        display_movies(movies)
    else:
        print("Anahtar kelime ile eşleşen film bulunamadı.")
