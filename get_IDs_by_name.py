import requests
import pprint

# [{'id': '0', 'name': 'везде'},
#  {'id': '1', 'name': 'Информационные технологии, интернет, телеком'},
#  {'id': '2', 'name': 'Бухгалтерия, управленческий учет, финансы предприятия'},
#  {'id': '3', 'name': 'Маркетинг, реклама, PR'},
#  {'id': '4', 'name': 'Административный персонал'},
#  {'id': '5', 'name': 'Банки, инвестиции, лизинг'},
#  {'id': '6', 'name': 'Управление персоналом, тренинги'},
#  {'id': '7', 'name': 'Автомобильный бизнес'},
#  {'id': '8', 'name': 'Безопасность'},
#  {'id': '9', 'name': 'Высший менеджмент'},
#  {'id': '10', 'name': 'Добыча сырья'},
#  {'id': '11', 'name': 'Искусство, развлечения, масс-медиа'},
#  {'id': '12', 'name': 'Консультирование'},
#  {'id': '13', 'name': 'Медицина, фармацевтика'},
#  {'id': '14', 'name': 'Наука, образование'},
#  {'id': '15', 'name': 'Начало карьеры, студенты'},
#  {'id': '16', 'name': 'Государственная служба, некоммерческие организации'},
#  {'id': '17', 'name': 'Продажи'},
#  {'id': '18', 'name': 'Производство, сельское хозяйство'},
#  {'id': '19', 'name': 'Страхование'},
#  {'id': '20', 'name': 'Строительство, недвижимость'},
#  {'id': '21', 'name': 'Транспорт, логистика'},
#  {'id': '22', 'name': 'Туризм, гостиницы, рестораны'},
#  {'id': '23', 'name': 'Юристы'},
#  {'id': '24', 'name': 'Спортивные клубы, фитнес, салоны красоты'},
#  {'id': '25', 'name': 'Инсталляция и сервис'},
#  {'id': '26', 'name': 'Закупки'},
#  {'id': '27', 'name': 'Домашний персонал'},
#  {'id': '29', 'name': 'Рабочий персонал'}]

class ID:
    def __init__(self):

        self.area_list = []
        self.field_id = 2
        self.region_id = int
        self.region_text = ""
        self.field_list = []

    def get_specialization_list(self):
        area_result = requests.get('https://api.hh.ru/specializations').json()  # страница со списком сфер деятельности
        c = []  # список для хранения названий сфер деятельности и специальностей. Например, Бухгалтерия или Маркетинг
        b = {'id': '0', 'name': 'искать везде'}  # элемент поиска 'везде', добавим в список с. Парсер будет искать везде, если
        # id специализации будет 0.

        for i in area_result:
            c.append(dict(id=i['id'], name=i['name']))
        # pprint.pprint(c)
        c.append(b)
        self.area_list = sorted(c, key=lambda x: int(x['id']))
        return self.area_list

    def get_specialization_id(self, field_name):
        """Формирует список из словарей областей деятельности, который будем подавать в выпадающий
        список меню на странице поиска"""

        for i in self.get_specialization_list():
            if i['name'] == field_name:
                self.field_id = i['id']
                return self.field_id  # возвращает id области деятельности

    def get_region_id(self, region_name):  # принимает регион, проверяет его на правильность и возвращает id региона
        params = {'text': region_name}
        region_result = requests.get('https://api.hh.ru/suggests/areas', params=params).json()  # регионы
        if region_result["items"]:
            self.region_id = region_result["items"][0]["id"]
        else:
            raise ValueError("Регион не найден.")
        return self.region_id

    def check_region_name(self, region_name):  # проверяет введеный пользователем регион в списке регионов из api
        params = {'text': region_name}
        region_result = requests.get('https://api.hh.ru/suggests/areas', params=params).json()  # регионы
        pprint.pprint(region_result)
        if region_result["items"]:

            self.region_text = region_result["items"][0]["text"]
        else:
            raise ValueError("Регион не найден.")
        return self.region_text  # возвращает текст, если регион найден


if __name__ == '__main__':
    pass

