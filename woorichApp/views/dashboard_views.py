from flask import Blueprint, render_template, request

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
def index():
    return render_template('dashboard/index.html')

@bp.route('/report')
def report():
    dong_code = request.args.get('dong_code')
    dong_name = request.args.get('dong_name')
    
    # Use dong_code and dong_name to retrieve the necessary data for your report
    # You can also retrieve other parameters as needed
    
    return render_template('dashboard/analysis-report.html', dong_code=dong_code, dong_name=dong_name)