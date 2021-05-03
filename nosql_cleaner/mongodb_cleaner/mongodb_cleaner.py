from flask import Blueprint, render_template
from flask import current_app as app

from .db import DB
from .forms import Form

# Blueprint Configuration
mongodb_cleaner_bp = Blueprint(
    'mongodb_cleaner_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@mongodb_cleaner_bp.route('/mongodb', methods=['GET', 'POST'])
def mongodb():
    form = Form()
    if form.validate_on_submit():
        db = DB(form.collection.data)

        try:
            output = db.execute_user_query(form.query.data)
        except Exception as e:
            form.query.errors.append(f'Parser error: {str(e)}')
            return render_template('mongodb.html', form=form)

        form.save.disable = False if db.expect_replacement else True

        if form.search.data:
            form.editor.data = output
            return render_template('mongodb.html', form=form)

        try:
            db.replace_docs(form.editor.data)
        except Exception as e:
            form.editor.errors.append(
                f'Contents in the editor box are incorrectly formatted. Error: {str(e)}')

    return render_template('mongodb.html', form=form)
