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
        collection = Collection(app, form.collection.data)

        try:
            collection.parse_query(form.query.data)
        except Exception as e:
            form.query.errors.append(f'Parser error: {str(e)}')

        output = collection.execute_query()

        if collection.expect_editor:
            form.save.disable = False
        else:
            form.save.disable = True

        if form.search.data:
            form.editor.data = output
            return render_template('mongodb.html', form=form)

        try:
            collection.replace_docs(form.editor.data)
        except Exception as e:
            form.editor.errors.append(
                f'Contents in the editor box are incorrectly formatted. Error: {str(e)}')

    return render_template('mongodb.html', form=form)


@app.route('/neo4j', methods=['GET', 'POST'])
def neo4j():
    return render_template('neo4j.html')
