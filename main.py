from flask import Flask, redirect, url_for, render_template, request
from parserHH import total_vacancy, skills_search
from word_cloud import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/form/', methods=['GET'])
def run_get():
    with open('main.txt', 'r') as f:
        text = f.read()
    return render_template('form.html', text=text)


@app.route('/form/', methods=['POST'])
def run_post():
    text = request.form['input_text']
    keyword_count = total_vacancy(text)
    print(keyword_count)
    requirements = skills_search(text)
    print(requirements)
    plot_cloud(wordcloud)
    wordcloud.to_file('static/hp_cloud_simple.png')
    with open('main.txt', 'w') as f:
        f.write(f'{text}\n')
    return render_template('form.html', text=text, keyword_count=keyword_count, requirements=requirements)


@app.route("/contacts/")
def contacts():
    return render_template('contacts.html')


@app.route("/navi/")
def navi():
    return render_template('navi.html')


if __name__ == "__main__":
    app.run(debug=True)