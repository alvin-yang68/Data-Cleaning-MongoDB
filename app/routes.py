from flask import render_template, flash

from app import app
from app.forms import Form
from app.mongo import Collection


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/mongodb', methods=['GET', 'POST'])
def mongodb():
    form = Form()
    if form.validate_on_submit():
        condition = eval(form.query.data)
        editor = form.editor.data.strip()
        collection = Collection(app, form.collection.data)
        docs = collection.find_and_jsonify(condition)

        if form.search.data:
            form.editor.data = docs
            return render_template('mongodb.html', form=form)

        collection.replace_many(condition, editor)

    return render_template('mongodb.html', form=form)


@app.route('/neo4j', methods=['GET', 'POST'])
def neo4j():
    return render_template('neo4j.html')
