from flask import Flask
from cepik_connector import get_voivodeship_dictionary, get_cars_dataframe

app = Flask(__name__)


@app.route('/')
def main_page():
    voivodeships_dictionary = get_voivodeship_dictionary()
    data = get_cars_dataframe(voivodeships_dictionary)


if __name__ == '__main__':
    app.run()
