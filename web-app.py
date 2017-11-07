import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename

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
def upload_file():
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            flash("You Uploaded Nothing")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            flash("Successfully Uploaded File!")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("homePage.html")
        else:
            flash("Error uploading file. Accepted file formats are: .png, .jpeg, .gif or .jpg")
                
    return render_template("homePage.html")

if __name__ == '__main__':
    app.run(debug=True)
    
