from flask import Blueprint, render_template, request

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
def index():
    return render_template('dashboard/index.html')

@bp.route('/report')
def report():
    from app.dashboard.dashboard_api import (
        zone_num,
        by_loc,
        store_num,
        store_num_trend,
        facility_num,
        avg_apartment_prices,
        visualize_avg_apt_prices,
        less_than_66,
        visualize_less_than_66,
        print_total_sales,
        compare_sales_by_day,
        show_sales_rate,
        total_rspop,
        total_rspop_line,
        max_rspop,
        total_household,
        total_household_line,
        income_avg,
        get_lifepop_info,
        get_genlifepop_info,
        get_lifepop_age,
        get_lifepop_time,
        get_lifepop_day,
        get_lifepop_recent,
        get_lifepop_line,
        get_workpop_info
    )
    dong_code = request.args.get('dong_code')
    dong = request.args.get('dong')
    gu = request.args.get('gu')
    job_code = request.args.get('job_code')
    year = request.args.get('year')
    quarter = request.args.get('quarter')
    
    text_result0 = zone_num(dong_code)
    text_result1 = by_loc(dong_code)
    bar2 = store_num(dong_code)
    bar3 = store_num_trend(dong_code, job_code)
    bar4 = facility_num(dong_code)

    text_result5 = avg_apartment_prices(dong_code)
    bar6 = visualize_avg_apt_prices(dong_code)
    text_result7 = less_than_66(dong_code)
    bar8 = visualize_less_than_66(dong_code)
    text_result9 = print_total_sales(dong_code)
    bar10 = compare_sales_by_day(dong_code, year, quarter)
    bar11 = show_sales_rate(dong_code, year, quarter)
    text_result12 = total_rspop(dong_code)
    bar13 = total_rspop_line(dong_code)
    text_result14 = max_rspop(dong_code)
    text_result15 = total_household(dong_code)
    bar16 = total_household_line(dong_code)
    text_bar17 = income_avg(dong_code)
    bar18 = get_lifepop_info(year, quarter, dong_code)
    text_text_bar19 = get_genlifepop_info(year, quarter, dong_code)
    text_bar20 = get_lifepop_age(year, quarter, dong_code)
    text_bar21 = get_lifepop_time(year, quarter, dong_code)
    text_text_bar22 = get_lifepop_day(year, quarter, dong_code)
    text_result23 = get_lifepop_recent(dong_code)
    bar24 = get_lifepop_line(dong_code)
    text_text_bar25 = get_workpop_info(year, quarter, dong_code)



    return render_template(
        'dashboard/analysis-report.html',
        dong_code=dong_code,
        dong=dong,
        gu=gu,
        apart_text0 = text_result0,
        apart_text1 = text_result1,
        plot2 = bar2,
        plot3 = bar3,
        plot4 = bar4,
        apart_text5 = text_result5,
        plot6 = bar6,
        apart_text7 = text_result7,
        plot8 = bar8,
        apart_text9 = text_result9,
        plot10 = bar10,
        plot11 = bar11,
        apart_text12 = text_result12,
        plot13 = bar13,
        apart_text14 = text_result14,
        apart_text15 = text_result15,
        plot16 = bar16,
        text_plot17 = text_bar17,
        plot18 = bar18,
        text_text_plot19 = text_text_bar19,
        text_plot20 = text_bar20,
        text_plot21 = text_bar21,
        text_text_plot22 = text_text_bar22,
        apart_text23 = text_result23,
        plot24 = bar24,
        text_text_plot25 = text_text_bar25
    )

