from flask import Blueprint, render_template
from flask import current_app as app

from .db import DB
from .forms import Form

# Blueprint Configuration
neo4j_cleaner_bp = Blueprint(
    'neo4j_cleaner_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@neo4j_cleaner_bp.route('/neo4j', methods=['GET', 'POST'])
def neo4j():
    form = Form()
    if form.validate_on_submit():
        db = DB(
            uri=app.config['NEO4J_URI'],
            username=app.config['NEO4J_USER'],
            password=app.config['NEO4J_PASSWORD']
        )

        output = db.execute_user_query(form.query.data)

        try:
            output = db.execute_user_query(form.query.data)
        except Exception as e:
            form.query.errors.append(f'Parser error: {str(e)}')
            return render_template('neo4j.html', form=form)

        if form.search.data:
            form.editor.data = output
            return render_template('neo4j.html', form=form)

        try:
            db.replace_subgraph(form.editor.data)
        except Exception as e:
            form.editor.errors.append(
                f'Contents in the editor box are incorrectly formatted. Error: {str(e)}')

    return render_template('neo4j.html', form=form)
