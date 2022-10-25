import ast

import requests
import get_IDs_by_name as id
import pprint
import json
import sqlite3

list_ = [{'id': '0', 'name': 'искать везде'},
         {'id': '1', 'name': 'Информационные технологии, интернет, телеком'},
         {'id': '2', 'name': 'Бухгалтерия, управленческий учет, финансы предприятия'},
         {'id': '3', 'name': 'Маркетинг, реклама, PR'},
         {'id': '4', 'name': 'Административный персонал'},
         {'id': '5', 'name': 'Банки, инвестиции, лизинг'},
         {'id': '6', 'name': 'Управление персоналом, тренинги'},
         {'id': '7', 'name': 'Автомобильный бизнес'},
         {'id': '8', 'name': 'Безопасность'},
         {'id': '9', 'name': 'Высший менеджмент'},
         {'id': '10', 'name': 'Добыча сырья'},
         {'id': '11', 'name': 'Искусство, развлечения, масс-медиа'},
         {'id': '12', 'name': 'Консультирование'},
         {'id': '13', 'name': 'Медицина, фармацевтика'},
         {'id': '14', 'name': 'Наука, образование'},
         {'id': '15', 'name': 'Начало карьеры, студенты'},
         {'id': '16', 'name': 'Государственная служба, некоммерческие организации'},
         {'id': '17', 'name': 'Продажи'},
         {'id': '18', 'name': 'Производство, сельское хозяйство'},
         {'id': '19', 'name': 'Страхование'},
         {'id': '20', 'name': 'Строительство, недвижимость'},
         {'id': '21', 'name': 'Транспорт, логистика'},
         {'id': '22', 'name': 'Туризм, гостиницы, рестораны'},
         {'id': '23', 'name': 'Юристы'},
         {'id': '24', 'name': 'Спортивные клубы, фитнес, салоны красоты'},
         {'id': '25', 'name': 'Инсталляция и сервис'},
         {'id': '26', 'name': 'Закупки'},
         {'id': '27', 'name': 'Домашний персонал'},
         {'id': '29', 'name': 'Рабочий персонал'}]


class Parser:
    def __init__(self):
        self.params_no_desc = {}
        self.params_with_desc = {}
        self.total_vacancies = {}
        self.skills = {}

    def get_params_no_desc(self, search_name, region_id, specialization_id):
        if specialization_id == '0':
            self.params_no_desc = {'text': f"NAME:({search_name})", 'area': f"{region_id}"}
        else:
            self.params_no_desc = {'text': f"NAME:({search_name})", 'area': f"{region_id}",
                                   'specialization': f"{specialization_id}"}
        return self.params_no_desc

    def get_params_with_desc(self, search_name, i, region_id, specialization_id):
        if specialization_id == '0':
            self.params_with_desc = {'text': f"NAME:({search_name}) AND DESCRIPTION:({i})", 'area': f"{region_id}"}
        else:
            self.params_with_desc = {'text': f"NAME:({search_name}) AND DESCRIPTION:({i})", 'area': f"{region_id}",
                                     'specialization': f"{specialization_id}"}
        return self.params_with_desc

    @staticmethod
    def get_json_from_api(url, params):
        return requests.get(url, params=params).json()

    def total_vacancy(self, search_name, result):
        self.total_vacancies = dict(keyword=search_name, count=result['found'])
        return self.total_vacancies

    def list_of_skills_from_description(self, result):
        a = []
        items = result['items']
        for element in items:
            url_ = element['url']  # берем из items ccылку на вакансию, проходим и достаем оттуда по ключу навыки.
            result = requests.get(url_).json()
            for p in result['key_skills']:  # по этому ключу достаем навыки.
                a.append(p['name'])
                self.skills = set(a)
        return self.skills

    def skills_search(self, url, result, search_name, region_id, specialization_id):
        final_list_of_counts = []
        for i in self.list_of_skills_from_description(result):
            params = self.get_params_with_desc(search_name, i, region_id, specialization_id)
            result_vacancies = self.get_json_from_api(url, params)
            num_of_one_skill = result_vacancies['found']
            a = dict(name=i, count=num_of_one_skill,
                     percent='{0:.1f}'.format(100 * num_of_one_skill / self.total_vacancies['count']))
            final_list_of_counts.append(a)
            final_list_of_counts = sorted(final_list_of_counts, key=lambda x: x['count'], reverse=True)
        return final_list_of_counts


list1 = [{'id': '9', 'name': 'Buiding'},
         {'id': '10', 'name': 'Security'},
         {'id': '11', 'name': 'Mass Media'},
         {'id': '12', 'name': 'Consulting'},
         {'id': '13', 'name': 'Medical care'}]

list2 = [{'id': '24', 'name': 'Спортивные клубы'},
         {'id': '25', 'name': 'Инсталляция и сервис'},
         {'id': '26', 'name': 'Закупки'},
         {'id': '27', 'name': 'Домашний персонал'},
         {'id': '29', 'name': 'Рабочий персонал'}]

list3 = [{'id': '11', 'name': 'Искусство, развлечения, масс-медиа'},
         {'id': '12', 'name': 'Консультирование'},
         {'id': '13', 'name': 'Медицина, фармацевтика'},
         {'id': '14', 'name': 'Наука, образование'},
         {'id': '15', 'name': 'Начало карьеры, студенты'}]


if __name__ == '__main__':
    url = 'https://api.hh.ru/vacancies?'
    find_id = id.ID()
    pars = Parser()
    field = list_[20]['name']
    specialization_id = find_id.get_specialization_id(field)
    region = 'Петербург'
    search_name = 'прораб'
    region_id = find_id.get_region_id(region)
    params = pars.get_params_no_desc(search_name, region_id, specialization_id)
    result = pars.get_json_from_api(url, params)
    key_count = pars.total_vacancy(search_name, result)
    # requirements = pars.skills_search(url, result, search_name, region_id, specialization_id)
    pprint.pprint(key_count)


    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.executescript("DROP TABLE IF EXISTS countries; CREATE TABLE countries (data json)")
    c.execute("insert into countries(data) values (?)", [json.dumps(list1)])
    c.execute("insert into countries(data) values (?)", [json.dumps(list2)])
    c.execute("insert into countries(data) values (?)", [json.dumps(list3)])

    conn.commit()


    # res = json.loads(c.execute("select * FROM countries where id='2' ").fetchone()[1])
    # res = c.execute("SELECT data FROM countries WHERE JSON_EXTRACT(data, '$') IS NOT NULL")
    res = json.loads(c.execute("select data FROM countries").fetchone()[0])


    conn.close()

    pprint.pprint(res)

