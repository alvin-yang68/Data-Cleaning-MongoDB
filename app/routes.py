from flask import render_template, flash

from app import app
from app.forms import Form


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/mongodb', methods=['GET', 'POST'])
def mongodb():
    form = Form()
    if form.validate_on_submit():
        flash(f"{form.query.data}")
    return render_template('mongodb.html', form=form)
