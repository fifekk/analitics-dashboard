from flask import Flask

app = Flask(__name__)

@app.route('/')
def main_page():
    # voivodeships_dictionary = get_voivodeship_dictionary()
    # data = get_cars_dataframe(voivodeships_dictionary)
    return 0


if __name__ == '__main__':
    app.run()
