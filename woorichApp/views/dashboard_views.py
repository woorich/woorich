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
    from woorichApp.dashboard.dashboard_api import (
        zone_num,
        by_loc,
        store_num,
        store_num_trend,
        facility_num,
        avg_apartment_prices,
        visualize_avg_apt_prices,
        less_than_66,
        visualize_less_than_66
    )
    dong_code = request.args.get('dong_code')
    dong = request.args.get('dong')
    gu = request.args.get('gu')
    job_code = request.args.get('job_code')
    
    text_result0 = zone_num(dong_code)
    text_result1 = by_loc(dong_code)
    bar2 = store_num(dong_code)
    bar3 = store_num_trend(dong_code, job_code)
    bar4 = facility_num(dong_code)

    text_result5 = avg_apartment_prices(dong_code)
    bar6 = visualize_avg_apt_prices(dong_code)
    text_result7 = less_than_66(dong_code)
    bar8 = visualize_less_than_66(dong_code)
    
    return render_template(
        'dashboard/analysis-report.html',
        dong_code=dong_code,
        dong=dong,
        gu=gu,
        apart_text0=text_result0,
        apart_text1=text_result1,
        plot2=bar2,
        plot3=bar3,
        plot4=bar4,
        apart_text5=text_result5,
        plot6=bar6,
        apart_text7=text_result7,
        plot8=bar8,
    )


