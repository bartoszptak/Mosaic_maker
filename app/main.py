from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import mosaic as ms
import os

app = Flask(__name__)

APP_TITLE = 'Mosaic maker'

@app.route("/")
def index():
   return render_template('index.html', 
                           app_title=APP_TITLE,
                           tiles=ms.get_mosaic_list())

@app.route('/makebeautiful', methods=['GET', 'POST'])
def makebeautiful():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('data','images', filename))

    return render_template('index.html', 
                           app_title=APP_TITLE,
                           tiles=ms.get_mosaic_list())

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')