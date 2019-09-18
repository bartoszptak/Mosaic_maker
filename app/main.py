from flask import Flask, render_template, request
import mosaic as ms


app = Flask(__name__)

APP_TITLE = 'Mosaic maker'

@app.route("/")
def index():
   return render_template('index.html', 
                           app_title=APP_TITLE,
                           tiles=ms.get_mosaic_list())

@app.route('/makebeautiful', methods=['POST'])
def makebeautiful():
    pass

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')