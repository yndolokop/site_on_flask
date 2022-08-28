import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words
from parserHH import list_of_skills

# wikipedia.set_lang("ru")
# wiki = wikipedia.page('Гарри Поттер')
#
# text = wiki.content
#
# text = re.sub(r'==.*?==+', '', text)  # удаляем лишние символы
# text = text.replace('\n', '')  # удаляем знаки разделения на абзацы

url = f'https://api.hh.ru/vacancies?specialization=1'  # "id":"1","name":"Информационные технологии, интернет, телеком"
# skill = 'sql'
page = 1
area = 1


def plot_cloud(wordcloud):
    # Устанавливаем размер картинки
    plt.figure(figsize=(40, 30))
    # Показать изображение
    plt.imshow(wordcloud)
    # Без подписей на осях
    plt.axis("off")


STOPWORDS_RU = get_stop_words('russian')

# Генерируем облако слов
wordcloud = WordCloud(width=380,
                      height=1500,
                      random_state=1,
                      background_color='black',
                      margin=20,
                      colormap='Pastel1',
                      collocations=True,
                      stopwords=STOPWORDS_RU)

# Рисуем картинку
# plot_cloud(wordcloud)
# wordcloud.to_file('static/images/hp_cloud_simple.png')