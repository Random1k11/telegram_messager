from flask import Flask, request



app = Flask(__name__)



@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        print(r)



if __name__ == '__main__':
    app.run(debug=True)
