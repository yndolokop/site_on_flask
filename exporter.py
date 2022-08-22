import csv
import sqlite3
import pandas as pd


requirements =   [{'count': 532, 'name': 'Python', 'percent': '99.4'},
                  {'count': 418, 'name': 'Работа в команде', 'percent': '78.1'},
                  {'count': 383, 'name': 'Разработка ПО', 'percent': '71.6'},
                  {'count': 306, 'name': 'PostgreSQL', 'percent': '57.2'},
                  {'count': 275, 'name': 'Git', 'percent': '51.4'},
                  {'count': 269, 'name': 'Docker', 'percent': '50.3'},
                  {'count': 245, 'name': 'Удаленная работа', 'percent': '45.8'},
                  {'count': 240, 'name': 'SQL', 'percent': '44.9'},
                  {'count': 219, 'name': 'Linux', 'percent': '40.9'},
                  {'count': 209, 'name': 'Django', 'percent': '39.1'},
                  {'count': 168, 'name': 'Django Framework', 'percent': '31.4'},
                  {'count': 131, 'name': 'Redis', 'percent': '24.5'},
                  {'count': 122, 'name': 'FastAPI', 'percent': '22.8'},
                  {'count': 120, 'name': 'RabbitMQ', 'percent': '22.4'},
                  {'count': 112, 'name': 'Rest API', 'percent': '20.9'},
                  {'count': 110, 'name': 'JavaScript', 'percent': '20.6'},
                  {'count': 96, 'name': 'Английский язык', 'percent': '17.9'},
                  {'count': 90, 'name': 'ООП', 'percent': '16.8'},
                  {'count': 84, 'name': 'Работа с базами данных', 'percent': '15.7'},
                  {'count': 79, 'name': 'Celery', 'percent': '14.8'},
                  {'count': 79, 'name': 'celery', 'percent': '14.8'},
                  {'count': 79, 'name': 'ClickHouse', 'percent': '14.8'},
                  {'count': 76, 'name': 'gitlab', 'percent': '14.2'},
                  {'count': 73, 'name': 'AioHTTP', 'percent': '13.6'},
                  {'count': 72, 'name': 'Анализ данных', 'percent': '13.5'},
                  {'count': 71, 'name': 'СУБД', 'percent': '13.3'},
                  {'count': 60, 'name': 'MongoDB', 'percent': '11.2'},
                  {'count': 59, 'name': 'SQLAlchemy', 'percent': '11.0'},
                  {'count': 54, 'name': 'go', 'percent': '10.1'},
                  {'count': 47, 'name': 'Confluence', 'percent': '8.8'},
                  {'count': 42, 'name': 'Elasticsearch', 'percent': '7.9'},
                  {'count': 40, 'name': 'C++', 'percent': '7.5'},
                  {'count': 39, 'name': 'Nginx', 'percent': '7.3'},
                  {'count': 33, 'name': 'Pandas', 'percent': '6.2'},
                  {'count': 31, 'name': 'apache', 'percent': '5.8'},
                  {'count': 30, 'name': 'golang', 'percent': '5.6'},
                  {'count': 27, 'name': 'Tornado', 'percent': '5.0'},
                  {'count': 25, 'name': 'Numpy', 'percent': '4.7'},
                  {'count': 22, 'name': 'Atlassian Jira', 'percent': '4.1'},
                  {'count': 19, 'name': 'TCP/IP', 'percent': '3.6'},
                  {'count': 18, 'name': 'C#', 'percent': '3.4'},
                  {'count': 15, 'name': 'HTML5', 'percent': '2.8'},
                  {'count': 12, 'name': 'CSS3', 'percent': '2.2'},
                  {'count': 10, 'name': 'Tensorflow', 'percent': '1.9'},
                  {'count': 9, 'name': 'UDP', 'percent': '1.7'},
                  {'count': 7, 'name': 'Keras', 'percent': '1.3'},
                  {'count': 6, 'name': 'Лидерство', 'percent': '1.1'},
                  {'count': 6, 'name': 'gunicorn', 'percent': '1.1'},
                  {'count': 3, 'name': 'Rust', 'percent': '0.6'},
                  {'count': 2, 'name': 'Stock market', 'percent': '0.4'},
                  {'count': 2, 'name': 'Алготрейдинг', 'percent': '0.4'},
                  {'count': 1, 'name': 'Algotrading', 'percent': '0.2'},
                  {'count': 1, 'name': 'dosker', 'percent': '0.2'}]


def save_csv(req):
    keys = requirements[0].keys()
    with open('requirements.csv', 'w', encoding='utf8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(req)


save_csv(requirements)

data = pd.read_csv('requirements.csv')
print(data)


# Connecting to the geeks database
connection = sqlite3.connect('db/hh.sqlite')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# Table Definition
create_table = '''CREATE TABLE IF NOT EXISTS skills(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                count INTEGER NOT NULL,
                percent INTEGER NOT NULL);
                '''

# Creating the table into our
# database
cursor.execute(create_table)

# Opening the person-records.csv file
file = open('requirements.csv')

# Reading the contents of the
# person-records.csv file
contents = csv.reader(file)

# SQL query to insert data into the
# person table
insert_records = "INSERT INTO skills (name, count, percent) VALUES(?, ?, ?)"

# Importing the contents of the file
# into our person table
cursor.executemany(insert_records, contents)

# SQL query to retrieve all data from
# the person table To verify that the
# data of the csv file has been successfully
# inserted into the table
select_all = "SELECT * FROM skills"
rows = cursor.execute(select_all).fetchall()

# Output to the console screen
for r in rows:
    print(r)

# Committing the changes
connection.commit()

# closing the database connection
connection.close()


