from bs4 import BeautifulSoup  # импортируем библиотеку BeautifulSoup
import requests  # импортируем библиотеку requests
import fake_useragent  # импортируем библиотеку fake_useragent
import pandas  # импортируем библиотеку pandas


def parse(link, number, header):
    """title, author, price"""
    title, author, price = "", "", ""
    global sheet
    url = f'{link}&page={number}'  # передаем необходимы URL адрес

    page = requests.get(url, headers=header)  # отправляем запрос методом Get
    print(page.status_code)  # смотрим ответ
    soup = BeautifulSoup(page.text, "html.parser")  # передаем страницу в bs4

    products = soup.find('div', class_='app-products-list').find_all("article")  # находим все книги на странице
    for product in products:  # проходим циклом по содержимому контейнера
        title = product.attrs["data-chg-product-name"]  # название
        if product.find("span", class_="product-card__subtitle") is not None:
            author = product.find("span", class_="product-card__subtitle").attrs["title"]  # автор
        price = product.attrs["data-chg-product-price"]  # цена
        sheet.append([title, author, price])


sheet = []  # лист excel файла
user = fake_useragent.UserAgent().random  # генерируем пользователя
header = {
    'user-agent': user
}
url = 'https://www.chitai-gorod.ru/search?phrase=Python'

page = requests.get(url, headers=header)  # отправляем запрос методом Get
print(page.status_code)  # смотрим ответ
soup = BeautifulSoup(page.text, "html.parser")  # передаем страницу в bs4

if soup.find("div", "chg-app-pagination") is not None:
    last_page = soup.find_all("a", class_="chg-app-pagination__item")[-1].text
else:
    last_page = 1

for page in range(1, int(last_page) + 1):
    parse(url, page, header)

book = pandas.DataFrame(sheet, columns=["Название", "Автор", "Цена"])
book.to_excel('books_python.xlsx', sheet_name="Книги", index=False)
