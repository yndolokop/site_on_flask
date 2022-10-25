import requests
import pprint
import sqlite3
import json

countries_api_res = requests.get('http://api.worldbank.org/countries?format=json&per_page=100')
countries = countries_api_res.json()[1]

# print(len(countries))

# pprint.pprint(countries)

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS countries (id integer PRIMARY KEY AUTOINCREMENT, data json)")

c.execute("insert into countries values (?)", [json.dumps(countries)])
conn.commit()


c.execute(f"SELECT JSON_EXTRACT (data, '$') FROM countries")
# c.execute(f"SELECT * FROM countries")
a = c.fetchall()
json.loads(a)

pprint.pprint((a))

# conn.close()

