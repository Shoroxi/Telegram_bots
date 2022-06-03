""" Смешнявки """
import re
import bs4
import requests


def get_text_messages(tg, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Собака":
        tg.send_photo(chat_id, photo=get_dog())

    elif ms_text == "Лиса":
        tg.send_photo(message.chat.id, get_fox())

    elif ms_text == "Погода":
        tg.send_message(chat_id, get_weather())

    elif ms_text == "Quotes":
        response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
        data = response.json()

        tg.send_message(chat_id, text=data)

    elif ms_text == "Книга":
        tg.send_message(chat_id, get_book())


def get_book():
    """ Книжка с сайта рандомизатора """
    book = None

    source_url = 'https://readly.ru/books/i_am_lucky/?show=1'
    page = requests.get(source_url)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    ###########################################################
    # Картиночки отдельно, но ссылка поддерживает превью, так что пофиг
    #
    # for a in soup.select('img[src*=".jpg"]'):
    #     book = ("https://readly.ru" + a.get('src'))
    ###########################################################
    for b in soup.select("h3 > a"):
        book = ("https://readly.ru" + str(b.get('href')))
    return book


def get_weather():
    """ Узнать погоду """
    # api.openweathermap - Даю настройки на спб, пользователь ничего не задает
    # Просто лень
    text = ""
    city_id = 524901
    appid = "23c4212791ee0292bc06a9bace0987dc"

    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    if res.status_code == 200:
        data = res.json()
        text += f"Погода для: {data['name']}(id:{data['id']}) координаты: N{data['coord']['lat']}, E{data['coord']['lon']} Яндекс: https://yandex.ru/maps/?ll={data['coord']['lon']},{data['coord']['lat']}&z=12&l=map\n"
        text += f"Погодная обстановка: {data['weather'][0]['description']}\n"
        text += f"Температура: {data['main']['temp']}  ощущается {data['main']['feels_like']} (min: {data['main']['temp_min']}, max: {data['main']['temp_max']})\n"
    else:
        text = res.text
    return text


def get_dog():
    """ Рандомная собака """
    url = None
    contents = requests.get('https://random.dog/woof.json').json()
    image_url = contents['url']

    # вроде тг все и так переварит, но пускай
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''

    while file_extension not in allowed_extension:
        url = image_url
        file_extension = re.search("([^.]*)$", url).group(1).lower()

    return url


def get_fox():
    """ Рандомный лис """
    contents = requests.get('https://randomfox.ca/floof/').json()
    image_url = contents['image']
    return image_url