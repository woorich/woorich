from flask import Blueprint, url_for, request, flash
from sqlalchemy.sql.functions import current_user
from werkzeug.utils import redirect
from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def Woorich():
    return 'Woorich'


@bp.route('/')
def index():
    return render_template('index.html')