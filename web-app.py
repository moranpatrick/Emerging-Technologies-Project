import os, re, base64
import numpy as np
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from scipy.misc import imread, imresize

# Adapted From http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "My Unreal Secret Key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload():
    result = {
        "error": False,
        "message": "",
        "digit": -1
    }

    if request.method == 'POST':
        
        file = request.files['file']

        if file.filename == '':
            flash("You Didn't Secect anything to Upload!")
            result["error"] = True
            result["message"] = "No File Name"
            return redirect(request.url)
        if file and allowed_file(file.filename):
            flash("Successfully Uploaded File!")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return render_template("homePage.html")
        else:
            flash("Error uploading file. Accepted file formats are: .png, .jpeg, .gif or .jpg")
                
    return render_template("homePage.html")

@app.route('/predict/', methods=['GET','POST'])
def predict():
    # get data from drawing canvas and save as image
    parseImage(request.get_data())

    # read parsed image back in 8-bit, black and white mode (L)
    x = imread('static/img/output.png', mode='L')
    x = np.invert(x)
    x = imresize(x,(28,28))

    # reshape image data for use in neural network
    x = x.reshape(1,28,28,1)
    return ("Saved!")

def parseImage(imgData):
    # parse canvas bytes and save as output.png
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    with open('static/img/output.png','wb') as output:
        output.write(base64.decodebytes(imgstr))

if __name__ == '__main__':
    app.run(debug=True)
    
