import sqlite3
import requests
from bs4 import BeautifulSoup


# Список URL для парсинга
URLS = [
    "https://all-events.ru/events/calendar/city-is-nizhniy_novgorod/",
    # Сюда можешь добавлять свои ссылки, только вряд ли у тебя в консоль что-то влезет
]

# Здесь попытка инициалзации sql lite
DB_PATH = 'parsed_data.db'

# здесь я создаю бд
# Стркутура бд:
# url 
# спаршенный контент
def init_db(path: str):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS pages (
            url TEXT PRIMARY KEY,
            content TEXT
        )
        '''
    )
    conn.commit()
    return conn

# функция, которая парсит информацию
def fetch_content(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.body
        print(body)
        return body.get_text(separator=' ', strip=True) if body else ''
    except requests.RequestException as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ''

# сохраняет информацию в бд
def save_to_db(conn: sqlite3.Connection, url: str, content: str):
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO pages (url, content)
        VALUES (?, ?)
        ON CONFLICT(url) DO UPDATE SET content=excluded.content;
        '''
        , (url, content)
    )
    conn.commit()

# просто здесь происходит парсинг
def main():
    conn = init_db(DB_PATH)
    for url in URLS:
        print(f"Парсинг: {url}")
        content = fetch_content(url)
        if content:
            save_to_db(conn, url, content)
            print(f"Сохранено: {url}\n")
        else:
            print(f"Пустой контент для {url}\n")
    conn.close()

if __name__ == '__main__':
    main()
