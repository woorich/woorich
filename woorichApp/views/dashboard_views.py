from flask import Blueprint, render_template, request

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
def index():
    return render_template('dashboard/index.html')

# @bp.route('/report')
# def report():
#     dong_code = request.args.get('dong_code')
#     dong = request.args.get('dong')
#     gu = request.args.get('gu')
    
#     # Use dong_code and dong_name to retrieve the necessary data for your report
#     # You can also retrieve other parameters as needed
    
#     return render_template('dashboard/analysis-report.html', dong_code=dong_code, dong=dong, gu=gu)

@bp.route('/report')
def report():
    from woorichApp.dashboard.dashboard_api import visualize_avg_apt_prices, avg_apartment_prices
    dong_code = request.args.get('dong_code')
    dong = request.args.get('dong')
    gu = request.args.get('gu')
    
    # Use dong_code and dong_name to retrieve the necessary data for your report
    # You can also retrieve other parameters as needed
    bar = visualize_avg_apt_prices(dong_code)
    text_result = avg_apartment_prices(dong_code)
    return render_template('dashboard/analysis-report.html', dong_code=dong_code, dong=dong, gu=gu, plot=bar, apart_text=text_result)

@bp.route('/report/environment?dong_code=<int:dong_code>&dong=<dong>&gu=<gu>')
def report_environment(dong_code, dong, gu):
    return render_template('dashboard/environment-analysis.html', dong_code=dong_code, dong=dong, gu=gu)

@bp.route('/report/population?dong_code=<int:dong_code>&dong=<dong>&gu=<gu>')
def report_population(dong_code, dong, gu):
    return render_template('dashboard/population-analysis.html', dong_code=dong_code, dong=dong, gu=gu)

@bp.route('/report/sales?dong_code=<int:dong_code>&dong=<dong>&gu=<gu>')
def report_sales(dong_code, dong, gu):
    return render_template('dashboard/sales-analysis.html', dong_code=dong_code, dong=dong, gu=gu)

