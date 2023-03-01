from flask import render_template
from web_app import app
from web_app import cd

@app.route('/index')
def index():
    return render_template('/index.html')

@app.route('/upload')
def upload():
    return render_template('/upload.html')

@app.route('/check_vegetable_growth')
def check_vegetable_growth():
    plot_img = cd.plot_data()
    return render_template('/check_vegetable_growth.html', plot_img = plot_img)