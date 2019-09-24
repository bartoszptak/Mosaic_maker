import os
import sys

from flask import Flask, render_template, request, redirect, send_file, after_this_request
from werkzeug.utils import secure_filename

import mosaic as ms

app = Flask(__name__)

app.config['DOWNLOAD_FOLDER'] = os.path.join('data','images')
app.config['TITLE'] = 'Mosaic maker'

@app.route("/")
def index():
   return render_template('index.html', 
                           app_title=app.config['TITLE'],
                           tiles=ms.get_mosaic_list())

@app.route('/makebeautiful', methods=['GET', 'POST'])
def makebeautiful():
    if request.method == 'POST':
        file = request.files['file']
        args = request.form
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        file.save(save_path)

        ms.make_mosaic(save_path, args['tile'].lower(), int(args['size']))
    
        @after_this_request
        def cleanup(response):
            os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'], filename))
            return response

        return send_file(save_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
