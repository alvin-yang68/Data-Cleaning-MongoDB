from flask import render_template, flash

from app import app
from app.forms import MongoForm, Neo4jForm
from app.mongo_db import MongoDriver
from app.neo4j_db import Neo4jDriver


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/mongodb', methods=['GET', 'POST'])
def mongodb():
    form = MongoForm()
    if form.validate_on_submit():
        driver = MongoDriver(app, form.collection.data)

        try:
            output = driver.execute_user_query(form.query.data)
        except Exception as e:
            form.query.errors.append(f'Parser error: {str(e)}')
            return render_template('mongodb.html', form=form)

        form.save.disable = False if driver.expect_replacement else True

        if form.search.data:
            form.editor.data = output
            return render_template('mongodb.html', form=form)

        try:
            driver.replace_docs(form.editor.data)
        except Exception as e:
            form.editor.errors.append(
                f'Contents in the editor box are incorrectly formatted. Error: {str(e)}')

    return render_template('mongodb.html', form=form)


@app.route('/neo4j', methods=['GET', 'POST'])
def neo4j():
    form = Neo4jForm()
    if form.validate_on_submit():
        driver = Neo4jDriver(app)

        output = driver.execute_user_query(form.query.data)

        try:
            output = driver.execute_user_query(form.query.data)
        except Exception as e:
            form.query.errors.append(f'Parser error: {str(e)}')
            return render_template('neo4j.html', form=form)

        if form.search.data:
            form.editor.data = output
            return render_template('neo4j.html', form=form)

        try:
            driver.replace_subgraph(form.editor.data)
        except Exception as e:
            form.editor.errors.append(
                f'Contents in the editor box are incorrectly formatted. Error: {str(e)}')

    return render_template('neo4j.html', form=form)
