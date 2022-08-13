
import requests
import pprint
import json


# url = 'https://api.hh.ru/vacancies'
url = f'https://api.hh.ru/vacancies?specialization=1'  # "id":"1","name":"Информационные технологии, интернет, телеком"
# skill = 'аналитик'
page = 0
area = 1


def total_vacancy(skill):
    params = {'text': f"NAME:({skill})", 'area': f'{area}', 'page': f'{page}'}
    result_total_vacancies = requests.get(url, params=params).json()
    total_vacancies = dict(keyword=skill, count=result_total_vacancies['found'])

    return total_vacancies


def list_of_skills(skill):
    skills = []
    a = []
    params = {'text': f"NAME:({skill})", 'area': f'{area}', 'page': f'{page}'}
    result = requests.get(url, params=params).json()
    items = result['items']
    for i in items:
        url_ = i['url']
        result = requests.get(url_).json()
        for k in result['key_skills']:
            a.append(k['name'])
            skills = set(a)
    return list(skills)


def skills_search(skill):
    final_list_of_counts = []
    for i in list_of_skills(skill):
        params = {'text': f"NAME:({skill}) AND DESCRIPTION:({i})", 'area': f"{area}", 'page': f'{page}'}
        result_vacancies = requests.get(url, params=params).json()
        num_of_one_skill = result_vacancies['found']
        a = dict(name=i, count=num_of_one_skill, percent='{0:.1f}'.format(100 * num_of_one_skill / total_vacancy(skill)['count']))
        final_list_of_counts.append(a)

    return sorted(final_list_of_counts, key=lambda x: x['count'], reverse=True)


if __name__ == '__main__':
    # b = dict(total_vacancy('аналитик'), requirements=skills_search('аналитик'))
    # pprint.pprint(b)
    a=skills_search('sql')
    print(a)
    b=total_vacancy('sql')
    print(b)
    with open('skills_list_count.json', 'w') as f:
        json.dump(b, f)