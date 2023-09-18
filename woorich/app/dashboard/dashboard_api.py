import plotly
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import numpy as np
import json
from app.dashboard.cache_utils import get_data

df_store = get_data("select 행정동_코드, 상권_코드, 상권_코드_명, 행정동명, 점포_수, 서비스_업종_코드_명, 업종_대분류_코드, 업종_대분류, 기준_년_코드, 기준_분기_코드 from df_store")
df_facility = get_data("select 기준_년_코드, 기준_분기_코드, 행정동_코드, 행정동명, 관공서_수, 은행_수, 종합병원_수, 일반_병원_수, 약국_수, 유치원_수, 초등학교_수, 중학교_수, 고등학교_수, 대학교_수, 백화점_수, 슈퍼마켓_수, 극장_수, 숙박_시설_수, 공항_수, 철도_역_수, 버스_터미널_수, 지하철_역_수, 버스_정거장_수 from df_facility")
df_apart = get_data("select dong_code, year, quarter, avg_price, `~1`, `1~2`, `2~3`, `3~4`, `4~5`, `5~6`, `6~`, `~66sm`, `66~99sm`, `99~132sm`, `132~165sm`, `165sm~` from df_apart")
df_map_info = get_data("select 행정동_코드, 행정동명, 엑스좌표_값, 와이좌표_값, 상권_코드, 상권_구분_코드_명, 상권_코드_명 from df_map_info")
df_rs_population = get_data("select 행정동_코드, 기준_년_코드, 기준_분기_코드, `총 상주인구 수`, `총 가구 수`, `남성연령대 10 상주인구 수`, `남성연령대 20 상주인구 수`, `남성연령대 30 상주인구 수`, `남성연령대 40 상주인구 수`, `남성연령대 50 상주인구 수`, `남성연령대 60 이상 상주인구 수`, `여성연령대 10 상주인구 수`, `여성연령대 20 상주인구 수`, `여성연령대 30 상주인구 수`, `여성연령대 40 상주인구 수`, `여성연령대 50 상주인구 수`, `여성연령대 60 이상 상주인구 수`, 행정동명 from df_rs_population")
df_rs_income = get_data("select 행정동_코드, 시군구_코드, 행정동명, 시군구명, 월_평균_소득_금액 from df_rs_income")
df_lifepop = get_data("select 기준_년_코드, 기준_분기_코드, 행정동_코드, 행정동명, 총_생활인구_수, 상권_코드, 상권_코드_명, 남성_생활인구_수, 여성_생활인구_수, 총_생활인구_수, 연령대_10_생활인구_수, 연령대_20_생활인구_수, 연령대_30_생활인구_수, 연령대_40_생활인구_수, 연령대_50_생활인구_수, 연령대_60_이상_생활인구_수, 시간대_1_생활인구_수, 시간대_2_생활인구_수, 시간대_3_생활인구_수, 시간대_4_생활인구_수, 시간대_5_생활인구_수, 시간대_6_생활인구_수, 월요일_생활인구_수, 화요일_생활인구_수, 수요일_생활인구_수, 목요일_생활인구_수, 금요일_생활인구_수, 토요일_생활인구_수, 일요일_생활인구_수 from df_lifepop")
df_sales = get_data("select * from df_sales")
df_total_sales = get_data("select 지출_총금액, 행정동_코드 from df_total_sales")
df_income_consume = get_data("select * from df_income_consume")
df_workpop = get_data("select 기준_년_코드, 기준_분기_코드, 행정동_코드, 총_직장인구_수, 상권_코드, 상권_코드_명 from df_workpop")

# 환경분석
# 분석0: 행정동별 상권 개수
def zone_num(dong_code):
   df_zone = df_store[df_store['행정동_코드']==int(dong_code)]
   a = df_zone[('상권_코드')].nunique()
   b = df_zone[('상권_코드_명')].unique()
   return [a, b]


# 분석1: 행정동별 가장 점포수가 많은 업종
def by_loc(dong_code):
    def service_max(i):
        return i.value_counts().index[0]
    df_temp = df_store[df_store['행정동_코드']==int(dong_code)]
    a = df_temp.groupby('행정동명').agg({'점포_수' : 'max', '서비스_업종_코드_명': service_max}).reset_index()
    return {"업종명" : a['서비스_업종_코드_명'].iloc[0], "최대업종점포수" : a['점포_수'].iloc[0]}


# 분석2: 행정동 내 업종 대분류별 업소 수
def store_num(dong_code):
    df_temp = df_store[df_store['행정동_코드']==int(dong_code)]

    #업종별 점포수의 합
    df_filtered = df_temp.groupby(['업종_대분류'])[['점포_수']].sum().squeeze()

    if df_filtered.empty:
                print("분석2: 데이터가 존재하지 않습니다.")
                return None

    colors = ["서비스업", "소매업", "외식업"]
    for template in ["simple_white"]:
        fig = px.bar(df_filtered, color=colors, color_discrete_map={
                "서비스업": "rgb(190,168,218)",
                "소매업": "rgb(251,128,114)",
                "외식업": "rgb(141,211,199)"
                }
                 ,template=template)

    #바차트 제목, x축, y축 텍스트 추가
    fig.update_layout(title_text= "업종별 점포 수")
    fig.update_xaxes(title_text='업종')
    fig.update_yaxes(title_text='점포 수')

    # 막대 두께 조정
    fig.update_layout(bargap=0.7)

    # figure 실행
    # fig.show()
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # return fig.show()
    return graphJSON

# 분석3: 업종별 업소 수 3년 추이
def store_num_trend(dong_code, job_code):
    jobs = ['', '외식업', '서비스업', '소매업']
    traces = []
    
    colors = ["rgb(141,211,199)", "rgb(190,168,218)", "rgb(251,128,114)"]  # specify colors for each trace
    
    for i in range(1, 4):
        df_filtered= df_store[(df_store['행정동_코드']==int(dong_code)) & (df_store['업종_대분류_코드'] == i)]
        
        if df_filtered.empty:
            print("분석3: 데이터가 존재하지 않습니다.")
            continue
        
        df = df_filtered.groupby(['기준_년_코드', '기준_분기_코드'])[['점포_수']].sum()
        
        x = [f'202{i//4}_{(i%4)+1}' for i in range(24)]
        
        trace = {
            'x': x,
            'y': df['점포_수'].tolist(),
            'mode': 'lines',
            'name': f'{jobs[i]}',
            'line': {'color': colors[i-1], 'width': 4}
        }
        
        traces.append(trace)
    
    layout = {
        'title': '분기별 업종들 업소 수 추이',
        'xaxis': {'title': '시기'},
        'yaxis': {'title': '점포 수'},
        'template': 'simple_white'
    }
    
    fig = {
        'data': traces,
        'layout': layout
    }
    
    return fig

# 분석4: 주요 시설 현황
def facility_num(dong_code, year, quarter):
    df_filtered_1 = df_facility.loc[(df_facility['기준_년_코드'] == int(year)) & (df_facility['기준_분기_코드'] == int(quarter)) & (df_facility['행정동_코드'] == int(dong_code))].groupby(['행정동명'])[['관공서_수', '은행_수', '종합병원_수', '일반_병원_수', '약국_수', '유치원_수',
       '초등학교_수', '중학교_수', '고등학교_수', '대학교_수', '백화점_수', '슈퍼마켓_수', '극장_수',
       '숙박_시설_수', '공항_수', '철도_역_수', '버스_터미널_수', '지하철_역_수', '버스_정거장_수']].sum().squeeze()
    
    if df_filtered_1.empty:
        print("분석4: 데이터가 존재하지 않습니다.")
        return None

    for template in ["simple_white"]:
        fig = px.bar(data_frame=df_filtered_1, color_discrete_sequence=px.colors.qualitative.Set3, template=template)

    #바차트 제목, x축, y축 텍스트 추가
    fig.update_layout(title_text= "선택지역의 업종 대분류별 업소 수")
    fig.update_xaxes(title_text='업종 분류')
    fig.update_yaxes(title_text='개수')

    #figure 실행
    # fig.show()
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# 아파트 분석
# 분석5: 해당 동의 가장 최근(2022) 아파트 평균 가격 및 6억 이상 아파트 비율
def avg_apartment_prices(dong_code):
    # 입력 받은 행정동 명에 해당하는 행을 필터링
    dong_row = df_apart[df_apart['dong_code'] == int(dong_code)]
    if dong_row.empty:
        print("분석5: 데이터가 존재하지 않습니다.")
        return None

    # 해당 행정동의 2022년 평균 아파트 가격을 계산
    avg_price_2022 = dong_row[dong_row['year'] == 2022]['avg_price'].mean()

    # 해당 행정동의 6억 이상 아파트 비율을 계산
    total_apartments = dong_row[dong_row['year'] == 2022]['~1'] + dong_row[dong_row['year'] == 2022]['1~2'] + dong_row[dong_row['year'] == 2022]['2~3'] + dong_row[dong_row['year'] == 2022]['3~4'] + dong_row[dong_row['year'] == 2022]['4~5'] + dong_row[dong_row['year'] == 2022]['5~6'] + dong_row[dong_row['year'] == 2022]['6~']
    apartments_over_6 = dong_row[dong_row['year'] == 2022]['6~']
    over_6_ratio = apartments_over_6.sum() / total_apartments.sum()

    # 결과 출력
    result = f"2022년 평균 아파트 가격: {avg_price_2022:,.2f}원"
    result += f"<br>2022년 6억 이상 아파트 비율: {over_6_ratio:.2%}"

    return result

# 분석6: 행정동 코드 입력 시, 해당 동의 아파트 가격 추이를 그래프로 리턴하는 함수
def visualize_avg_apt_prices(dong_code):
    year_quarter = []
    list_num = []
    for year in  range(2017,2023):
        for quarter in range(1, 5):
            filtered_df = df_apart[
            (df_apart['dong_code'] == int(dong_code)) &
            (df_apart['year'] == year) &
            (df_apart['quarter'] == quarter)
            ]

            if filtered_df.empty:
                print("분석6: 데이터가 존재하지 않습니다.")
                return None

            # filtered_df에서 아파트 가격 평균 구함
            avg_price_sum = filtered_df['avg_price'].sum()
            list_num.append(avg_price_sum)
            year_quarter.append(f'{str(year), str(quarter)}')

    # 그래프 x축, y축, title 지정
    fig = px.line(x=year_quarter, y=list_num,
                title=f"아파트 가격 변화 추이")

    fig.update_layout(yaxis_tickformat=",.0f")

    # 그래프 커스터 마이징
    fig.update_layout(xaxis_title="분기", yaxis_title="아파트 가격 변화")

    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# 분석 7: 해당 동의 가장 최근(2022) 66㎡(약 20평) 미만 비율 리턴하는 함수
def less_than_66(dong_code):
    dong_row = df_apart[df_apart['dong_code'] == int(dong_code)]

    if dong_row.empty:
        print("분석7: 데이터가 존재하지 않습니다.")
        return None

      # 해당 행정동의 2022년 데이터 필터
    dong_row_2022 = dong_row[dong_row['year'] == 2022]

    # 데이터가 없는 경우 체크
    if dong_row_2022.empty:
        print("분석7: 2022년 데이터가 존재하지 않습니다.")
        return None
    
    print("dong_row_2022: ", dong_row_2022)

    # 2022년 전체 아파트 수 계산
    total_apartments = dong_row_2022[['~66sm', '66~99sm', '99~132sm', '132~165sm', '165sm~']].sum(axis=1)
    print("total_apartments: ", total_apartments)

    # 데이터가 없거나 전체 합계가 0인 경우 체크
    if total_apartments.sum() == 0:
        print("분석7: 2022년 전체 아파트 수가 0입니다.")
        return None

    # 2022년 66m² 미만 아파트 수 계산
    apartment_less_than_66 = dong_row_2022['~66sm'].sum()
    print("apartment_less_than_66: ", apartment_less_than_66)

    # 비율 계산
    less_than_ratio = apartment_less_than_66 / total_apartments.sum()

    result = f"66㎡ 미만 아파트 비율: {less_than_ratio:.2%}"
    return result

# 분석 8: 해당 동의 20평 미만 아파트 가구수 추이
def visualize_less_than_66(dong_code):
    year_quarter = []
    list_num = []
    for year in  range(2017,2023):
        for quarter in range(1, 5):
            filtered_df = df_apart[
            (df_apart['dong_code'] == int(dong_code)) &
            (df_apart['year'] == year) &
            (df_apart['quarter'] == quarter)
            ]

            if filtered_df.empty:
                print("분석8: 데이터가 존재하지 않습니다.")
                return None

            # filtered_df에서 아파트 가격 평균 구함
            sm_sum = filtered_df['~66sm'].sum()
            list_num.append(sm_sum)
            year_quarter.append(f'{str(year), str(quarter)}')

    # 그래프 x축, y축, title 지정
    fig = px.line(x=year_quarter, y=list_num,
                title=f"66㎡(약 20평) 미만 아파트 가구수 추이")

    fig.update_layout(yaxis_tickformat=",.0f")

    # 그래프 커스터 마이징
    fig.update_layout(xaxis_title="분기", yaxis_title="66㎡ 미만 아파트 가구수 변화")

    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# 매출분석
# 분석 9: 총 매출 내용
def print_total_sales(dong_code):
    dong_info = df_map_info.loc[(df_map_info['행정동_코드']==int(dong_code))].drop(columns=['엑스좌표_값', '와이좌표_값'])
    df_dong_total_sales = df_total_sales[df_total_sales['행정동_코드']==int(dong_code)]
    df_dong_income_consume = pd.merge(left=dong_info, right=df_income_consume, how='left', \
                                      on=['상권_코드', '상권_구분_코드_명', '상권_코드_명'], sort=False)
    dong_consume_avg = df_dong_income_consume['지출_총금액'].sum()/df_dong_income_consume['지출_총금액'].count()
    dong_sales_avg = df_dong_total_sales['지출_총금액'].sum()/df_dong_total_sales['지출_총금액'].count()
    seoul_sales_avg = df_total_sales['지출_총금액'].sum()/df_total_sales['지출_총금액'].count() # 계산 전 가상의 값, 전체 데이터셋의 지출에 null값이 있다고 해서 계산 못 한 상태
    return {"월 평균 지출": dong_consume_avg, "서울시 평균 지출": seoul_sales_avg}


# 분석 10: 요일별 매출 비교
def compare_sales_by_day(dong_code, year, quarter):
    dong_info = df_map_info.loc[(df_map_info['행정동_코드']==dong_code)].drop(columns=['엑스좌표_값', '와이좌표_값'])
    df_dong_sales = pd.merge(left=dong_info, right=df_sales, how='left', \
                             on=['상권_코드', '상권_구분_코드_명', '상권_코드_명'], sort=False)
    # 시간 조건1 정의
    cond1 = (df_dong_sales['기준_년_코드']==year)
    # 시간 조건2 정의
    cond2 = (df_dong_sales['기준_분기_코드']==quarter)

    df_dong_sales_set_time = df_dong_sales[cond1 & cond2]
    df_result = pd.DataFrame({})

    for code in dong_info['상권_코드']:
        df = df_dong_sales_set_time.loc[df_dong_sales_set_time['상권_코드']==code]

        if df.empty:
            return "분석10: df 데이터가 존재하지 않습니다."
        
        df_top = df.sort_values(by=['분기당_매출_금액'], axis=0).iloc[0]
        df_top = pd.DataFrame(df_top).T
        df_result = pd.concat([df_result, df_top], ignore_index=True)

    
    line_chart_title = f'{df["행정동명"].iloc[0]}의 상권별 최대 매출 업종 요일 별 비교 추이'
    df_result.iloc[:, 14:21].columns = list(map(lambda x:x[:-8], df_result.iloc[:,14:21].columns))
    df_real_result = df_result.iloc[:, 14:21]
    df_real_result.columns = list(map(lambda x:x[:-8], df_result.iloc[:,14:21].columns))
    df_real_result.index = df_result['상권_코드_명']
    df_real_result.T

    for template in ["simple_white"]:
        fig = px.line(data_frame= df_real_result.T, title=line_chart_title, template=template)

    fig.update_traces(line_width=5)
    
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# 분석 11: 업종별 매출 비율
def show_sales_rate(dong_code,year,quarter):
    dong_info = df_map_info.loc[(df_map_info['행정동_코드']==int(dong_code))].drop(columns=['엑스좌표_값', '와이좌표_값'])
    df_dong_income_consume = pd.merge(left=dong_info, right=df_income_consume, how='left', \
                                      on=['상권_코드', '상권_구분_코드_명', '상권_코드_명'], sort=False)
    # 시간 조건1 정의
    cond1 = (df_dong_income_consume['기준_년_코드']==year)

    # 시간 조건2 정의
    cond2 = (df_dong_income_consume['기준_분기_코드']==quarter)
    df_dong_income_consume = df_dong_income_consume[cond1 & cond2]
    total_consume_by_sector = df_dong_income_consume.iloc[:, -9:]

    ratio = list(total_consume_by_sector.sum()/total_consume_by_sector.count()) # 평균
    labels = list(map(lambda x: x[:-7], total_consume_by_sector.columns))

    # df_dong_income_consume이 비어 있지 않을 경우
    if df_dong_income_consume.empty:
        return "분석 11: 데이터가 존재하지 않습니다."

    pie_chart_title = f"{df_dong_income_consume['행정동명'].iloc[0]} 의 분류별 지출 총금액 비율"
    fig = px.pie(values = ratio, names=labels, title=pie_chart_title)

    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# 주거인구 분석
# 분석 12: 행정동별 주거인구 수
def total_rspop(dong_code, year, quarter):
    # 행정동_코드, 기준_년_코드, 기준_분기_코드가 같은 행끼리 filtered_df 데이터프레임 생성
    filtered_df = df_rs_population[
    (df_rs_population['행정동_코드'] == int(dong_code)) &
    (df_rs_population['기준_년_코드'] == int(year)) &
    (df_rs_population['기준_분기_코드'] == int(quarter))
    ]
    print(df_rs_population['행정동_코드'].dtype)
    #입력한 것과 일치하는 데이터가 없으면
    if filtered_df.empty:
        print("분석 12: 데이터가 존재하지 않습니다.")
        return None
    
    # filtered_df에서 총 상주인구 수 총합 구하기
    total_rspop_sum = filtered_df['총 상주인구 수'].sum()

    # 행정동_코드로 들어온 입력을 행정동명으로 출력하기
    dong_name = df_rs_population[(df_rs_population['행정동_코드']==int(dong_code))]['행정동명'].iloc[0]

    #텍스트로 출력
    return total_rspop_sum

# 분석 13: 주거 인구 수 변화 추이
def total_rspop_line(dong_code):
    year_quarter = []
    list_num = []
    for year in  range(2017,2023):
        for quarter in range(1, 5, 1):
            filtered_df = df_rs_population[
            (df_rs_population['행정동_코드'] == int(dong_code)) &
            (df_rs_population['기준_년_코드'] == year) &
            (df_rs_population['기준_분기_코드'] == quarter)
            ]

            #입력한 것과 일치하는 데이터가 없으면
            if filtered_df.empty:
                print("분석 12: 데이터가 존재하지 않습니다.")
                return None

            # 입력된 행정동코드로 행정동명 도출하기
            dong_name = df_rs_population[(df_rs_population['행정동_코드']==int(dong_code))]['행정동명'].iloc[0]

            # filtered_df에서 총 상주인구 수 총합 구하기
            total_rspop_sum = filtered_df['총 상주인구 수'].sum()
            list_num.append(total_rspop_sum)
            year_quarter.append(f'{str(year), str(quarter)}')

    # 그래프 x축, y축, title, label 지정
    fig = px.line(x=year_quarter, y=list_num)

    # 그래프 커스터 마이징
    fig.update_layout(
        xaxis_title="분기",
        yaxis_title="총 주거 인구수 변화"
        )
    
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# 분석 14: 성별, 연령대별 1위
def max_rspop(dong_code, year, quarter):
    # 행정동_코드, 기준_년_코드, 기준_분기_코드가 같은 행끼리 filtered_df 데이터프레임 생성
    filtered_df = df_rs_population[
    (df_rs_population['행정동_코드'] == int(dong_code)) &
    (df_rs_population['기준_년_코드'] == int(year)) &
    (df_rs_population['기준_분기_코드'] == int(quarter))
    ]

    #입력한 것과 일치하는 데이터가 없으면
    if filtered_df.empty:
        print("분석 14: 데이터가 존재하지 않습니다.")
        return None

    # filtered_df에서 성별, 연령대 인구수 총합 구하기
    sum_M_10s = filtered_df['남성연령대 10 상주인구 수'].sum()
    sum_M_20s = filtered_df['남성연령대 20 상주인구 수'].sum()
    sum_M_30s = filtered_df['남성연령대 30 상주인구 수'].sum()
    sum_M_40s = filtered_df['남성연령대 40 상주인구 수'].sum()
    sum_M_50s = filtered_df['남성연령대 50 상주인구 수'].sum()
    sum_M_60s = filtered_df['남성연령대 60 이상 상주인구 수'].sum()
    sum_W_10s = filtered_df['여성연령대 10 상주인구 수'].sum()
    sum_W_20s = filtered_df['여성연령대 20 상주인구 수'].sum()
    sum_W_30s = filtered_df['여성연령대 30 상주인구 수'].sum()
    sum_W_40s = filtered_df['여성연령대 40 상주인구 수'].sum()
    sum_W_50s = filtered_df['여성연령대 50 상주인구 수'].sum()
    sum_W_60s = filtered_df['여성연령대 60 이상 상주인구 수'].sum()

    # 딕셔너리 만들기
    sums = {
    '10대 남성': sum_M_10s,
    '20대 남성': sum_M_20s,
    '30대 남성': sum_M_30s,
    '40대 남성': sum_M_40s,
    '50대 남성': sum_M_50s,
    '60대 이상 남성': sum_M_60s,
    '10대 여성': sum_W_10s,
    '20대 여성': sum_W_20s,
    '30대 여성': sum_W_30s,
    '40대 여성': sum_W_40s,
    '50대 여성': sum_W_50s,
    '60대 이상 여성': sum_W_60s
    }

    # 딕셔너리에서 성별, 연령대 인구수의 총합이 가장 큰 컬럼 구하기
    column_with_max_sum = max(sums, key=sums.get)

    # 행정동코드로 들어온 입력을 행정동명으로 출력하기
    dong_name = df_rs_population[(df_rs_population['행정동_코드']==int(dong_code))]['행정동명'].iloc[0]

    # 비율 추가
    total_rspop_sum = filtered_df['총 상주인구 수'].sum()
    max_ratio = max(sums.values()) / total_rspop_sum

    # 텍스트로 출력
    return {"1위 분류":column_with_max_sum, "1위 분포율": max_ratio}

# 분석 15: 총 가구 세대 수
def total_household(dong_code, year, quarter):
    # 행정동_코드, 기준_년_코드, 기준_분기_코드가 같은 행끼리 filtered_df 데이터프레임 생성
    filtered_df = df_rs_population[
        (df_rs_population['행정동_코드'] == int(dong_code)) &
        (df_rs_population['기준_년_코드'] == int(year)) &
        (df_rs_population['기준_분기_코드'] == int(quarter))
        ]
    
    #입력한 것과 일치하는 데이터가 없으면
    if filtered_df.empty:
        print("분석 15: 데이터가 존재하지 않습니다.")
        return None
    
    # filtered_df에서 총 가구 수 총합 구하기
    total_household_sum = filtered_df['총 가구 수'].sum()

    # 행정동_코드로 들어온 입력을 행정동명으로 출력하기
    dong_name = df_rs_population[(df_rs_population['행정동_코드']==int(dong_code))]['행정동명'].iloc[0]

    # 텍스트로 출력
    return total_household_sum
 
# 분석 16: 총 가구 세대 수 추이
def total_household_line(dong_code):
    year_quarter = []
    list_num = []
    for year in  range(2017,2023):
        for quarter in range(1, 5, 1):
            filtered_df = df_rs_population[
            (df_rs_population['행정동_코드'] == int(dong_code)) &
            (df_rs_population['기준_년_코드'] == year) &
            (df_rs_population['기준_분기_코드'] == quarter)
            ]

            #입력한 것과 일치하는 데이터가 없으면
            if filtered_df.empty:
                print("분석 16: 데이터가 존재하지 않습니다.")
                return None

            # filtered_df에서 총 상주인구 수 총합 구하기
            total_rspop_sum = filtered_df['총 가구 수'].sum()
            list_num.append(total_rspop_sum)
            year_quarter.append(f'{str(year), str(quarter)}')

    dong_name = df_rs_population[(df_rs_population['행정동_코드']==int(dong_code))]['행정동명'].iloc[0]

    # 그래프 x축, y축, title, label 지정
    fig = px.line(x=year_quarter, y=list_num)

    # 그래프 커스터 마이징
    fig.update_layout(
        xaxis_title="분기",
        yaxis_title="총 가구 수 변화"
    )
    
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# 분석 17: 행정동별 소득구간
def income_avg(dong_code):
    gu_code = df_rs_income[df_rs_income['행정동_코드'] == int(dong_code)]['시군구_코드'].iloc[0]

    #행정동_코드로 들어온 입력을 행정동명으로 출력하기
    dong_name = df_rs_income[(df_rs_income['행정동_코드']==int(dong_code))]['행정동명'].iloc[0]
    gu_name = df_rs_income[(df_rs_income['행정동_코드']==int(dong_code))]['시군구명'].iloc[0]
    # 입력된 dong_code에 해당하는 시군구코드 찾아서 같은 시군구만 존재하는 데이터프레임 생성
    filtered_df = df_rs_income[(df_rs_income['행정동_코드'] == int(dong_code)) | (df_rs_income['시군구_코드'] == gu_code)]

    #입력한 것과 일치하는 데이터가 없으면
    if filtered_df.empty:
        print("분석 17: 데이터가 존재하지 않습니다.")
        return None

    # 소득금액을 소득구간으로 변환
    def categorize_income(income):
        income_brackets = [
          (1224311, 1441526),
          (1441527, 1707397),
          (1707398, 2020851),
          (2020852, 2440599),
          (2440600, 2983558),
          (2983559, 3741082),
          (3741083, 4890361),
          (4890362, 6945811),
          (6945812, float('inf'))
          ]

        for i, (lower, upper) in enumerate(income_brackets):
            if lower <= income <= upper:
                return i+2
        return 10
    # 동, 구, 시별 평균 소득금액 계산
    average_income_dong = filtered_df[filtered_df['행정동_코드'] == int(dong_code)]['월_평균_소득_금액'].mean().round(2)
    average_income_gu= filtered_df[filtered_df['시군구_코드'] == gu_code]['월_평균_소득_금액'].mean().round(2)
    average_income_si = df_rs_income['월_평균_소득_금액'].mean().round(2)

    # Categorize incomes
    categorized_income_dong = categorize_income(average_income_dong)
    categorized_income_gu = categorize_income(average_income_gu)
    categorized_income_si = categorize_income(average_income_si)

    # 그래프 색상 설정
    colors = ['행정동평균', '행정구평균', '서울시평균']
    for template in ["simple_white"]:
        fig = px.bar(
        x=[f'{dong_name}평균', f'{gu_name}평균', '서울시평균'],
        y=[categorized_income_dong, categorized_income_gu, categorized_income_si],
        labels={'x': '지역 범위', 'y': '소득 구간'},
        template=template,
        color=colors,
        color_discrete_map={
                "행정동평균": "rgb(190,168,218)",
                "행정구평균": "rgb(251,128,114)",
                "서울시평균": "rgb(141,211,199)"
                },
        title=f'{dong_name}의 소득 구간'
        )
    # y축 범위 고정
    fig.update_yaxes(range=[1, 10])

    # 막대 두께 조정
    fig.update_layout(bargap=0.7)
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return [categorized_income_dong, graphJSON]

# 생활인구 분석
# 분석 18: 생활인구 가장 많은 상권 3개
def get_lifepop_info(year, quarter, dong_code):
    filtered_df = df_lifepop[(df_lifepop['기준_년_코드'] == year) & (df_lifepop['기준_분기_코드'] == quarter) & (df_lifepop['행정동_코드'] == dong_code)]

    #입력한 것과 일치하는 데이터가 없으면
    if filtered_df.empty:
        return "해당 조건에 맞는 데이터가 없습니다."

    lifepop_value = filtered_df['총_생활인구_수'].sum()  # 조건에 맞는 값들의 총합
    print(f"총 생활인구 수: {lifepop_value}명")


    # 컬럼 '총_생활인구_수'가 많은 상위 3개의 '상권_코드', '상권_코드_명' 그리고 해당 컬럼들의 행 값을 출력
    top_lifepop = filtered_df.nlargest(3, '총_생활인구_수')[['상권_코드', '상권_코드_명', '총_생활인구_수']]

    print("총 생활인구 수가 많은 상위 상권 정보:")
    for index, row in top_lifepop.iterrows():
        code = row['상권_코드']
        name = row['상권_코드_명']
        lifepop = row['총_생활인구_수']
        print(f"상권 코드: {code}, 상권명: {name}, 생활인구 수: {lifepop}명")
# 그래프 색상 설정
    colors = ['행정동평균', '행정구평균', '서울시평균']
    for template in ["simple_white"]:
    # plotly를 사용하여 막대 그래프 생성
      fig = px.bar(top_lifepop, x='상권_코드_명', y='총_생활인구_수', title='상위 상권 코드별 생활인구 수',
                 template=template,
                 color=colors,
                 color_discrete_map={
                "행정동평균": "rgb(190,168,218)",
                "행정구평균": "rgb(251,128,114)",
                "서울시평균": "rgb(141,211,199)"
                })
    fig.update_layout(bargap=0.7)
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# 분석 19: 가장 많은 성별(수, 비율)
def get_genlifepop_info(year, quarter, dong_code):
    filtered_df = df_lifepop[(df_lifepop['기준_년_코드'] == year) & (df_lifepop['기준_분기_코드'] == quarter) & (df_lifepop['행정동_코드'] == int(dong_code))]

    if filtered_df.empty:
        print("분석 19: 데이터가 존재하지 않습니다.")
        return None

    # 1. '총_생활인구_수'의 해당 행 값에서 '남성_생활인구_수'와 '여성_생활인구_수'의 비율 출력
    male_lifepop = filtered_df['남성_생활인구_수'].sum()
    female_lifepop = filtered_df['여성_생활인구_수'].sum()
    total_lifepop = filtered_df['총_생활인구_수'].sum()

    # 값이 스칼라인지 확인
    if isinstance(male_lifepop, pd.Series):
        male_lifepop = male_lifepop.iloc[0]
    if isinstance(female_lifepop, pd.Series):
        female_lifepop = female_lifepop.iloc[0]
    if isinstance(total_lifepop, pd.Series):
        total_lifepop = total_lifepop.iloc[0]

    male_ratio = male_lifepop / total_lifepop
    female_ratio = female_lifepop / total_lifepop


    # 2. '남성_생활인구_수'의 해당 행 값에서 '여성_생활인구_수'의 해당 행 값을 뺐을 때,
    # 값이 음수가 나오면 '여성'을 출력하고 양수가 나오면 '남성'을 출력
    gender_difference = male_lifepop - female_lifepop

    if gender_difference < 0:
        gender_result = "여성"
        lifepop_gender_value = filtered_df['여성_생활인구_수'].sum()
    else:
        gender_result = "남성"
        lifepop_gender_value = filtered_df['남성_생활인구_수'].sum()

    # 확인: 값이 스칼라인지 확인
    if isinstance(lifepop_gender_value, pd.Series):
        lifepop_gender_value = lifepop_gender_value.iloc[0]

    # 남성과 여성 비율을 파이차트로 시각화
    gender_ratio_data = pd.DataFrame({'성별': ['남성', '여성'], '비율': [male_ratio, female_ratio]})
    fig = px.pie(gender_ratio_data, values='비율', names='성별', title=f"{year}년 {quarter}분기 행정동 코드{dong_code}의 남성/여성 비율")
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return [f"생활인구는 {gender_result}이 {lifepop_gender_value} 명으로 더 많습니다.", f"남성 비율: {male_ratio:.2%}, 여성 비율: {female_ratio:.2%}", graphJSON]

# 분석 20: 가장 많은 연령대(수, 비율)
def get_lifepop_age(year, quarter, dong_code):

    # 중복된 열 제거
    df_lifepop_copy = df_lifepop.loc[:, ~df_lifepop.columns.duplicated()].copy()
    print(df_lifepop)
    # 컬럼명 변경
    df_lifepop_copy.rename(columns={
          '연령대_10_생활인구_수': '10대',
          '연령대_20_생활인구_수': '20대',
          '연령대_30_생활인구_수': '30대',
          '연령대_40_생활인구_수': '40대',
          '연령대_50_생활인구_수': '50대',
          '연령대_60_이상_생활인구_수': '60대이상'}, inplace=True)

    # 해당 연도, 분기, 동 코드에 맞는 데이터 추출
    filtered_df = df_lifepop_copy[(df_lifepop_copy['기준_년_코드'] == year) & (df_lifepop_copy['기준_분기_코드'] == quarter) & (df_lifepop_copy['행정동_코드'] == int(dong_code))]

    if filtered_df.empty:
        print("분석 20: 데이터가 존재하지 않습니다.")
        return None

    age_columns = ['10대', '20대', '30대', '40대', '50대', '60대이상']
    
    # 연령대별 생활인구 수의 비율 계산
    total_lifepop = filtered_df['총_생활인구_수'].sum()
    ratios = filtered_df[age_columns] / total_lifepop
    data_lifeage = pd.DataFrame(ratios.sum())

    # 가장 큰 비율 값을 가진 컬럼 찾기 :해당 행에서 가장 큰 비율을 가진 연령대를 확인하고 그 비율 값 찾기
    max_ratio_gender_column = ratios.idxmax(axis=1) # idxmax() 함수 -> 주어진 축(axis)을 따라 가장 큰 값을 가지는 열의 인덱스를 반환!!
    max_ratio_gender_value = ratios.max(axis=1).sum()

    # 소수점 비율을 정수로 변환하여 출력
    max_ratio_gender_value_percentage = int(max_ratio_gender_value * 100)  # 비율을 백분율로 표현하기 위해 100을 곱하고 정수로 변환


    # Plotly 파이차트 생성
    fig = px.pie(data_lifeage,values=data_lifeage[0], names=data_lifeage.index,
        title=f"연령대별 생활인구 수의 비율 ({year}년 {quarter}분기, 동 코드: {dong_code})"
        )
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return [f"가장 많은 연령대({max_ratio_gender_value_percentage}%): {max_ratio_gender_column.values[0]}", graphJSON]

# 분석 21: 생활인구 가장 많은 시간대
def get_lifepop_time(year, quarter, dong_code):
    # 컬럼명 변경
    df_lifepop.rename(columns={
        '시간대_1_생활인구_수': '00~06시',
        '시간대_2_생활인구_수': '06~11시',
        '시간대_3_생활인구_수': '11~14시',
        '시간대_4_생활인구_수': '14~17시',
        '시간대_5_생활인구_수': '17~21시',
        '시간대_6_생활인구_수': '21~24시'}, inplace=True)

    filtered_df = df_lifepop[(df_lifepop['기준_년_코드'] == year) & (df_lifepop['기준_분기_코드'] == quarter) & (df_lifepop['행정동_코드'] == int(dong_code))]

    if filtered_df.empty:
        print("분석 21: 데이터가 존재하지 않습니다.")
        return None

    # 각 시간대별 생활인구 수 컬럼 선택
    lifepop_time_columns = ['00~06시', '06~11시', '11~14시', '14~17시', '17~21시', '21~24시']

    # 각 시간대별 생활인구 수의 총합 계산
    total_population = filtered_df[lifepop_time_columns].sum()

    # 결과 출력
    print("각 시간대별 생활인구 수:")
    for col, total in total_population.items():
        print(f"{col}: {total}")

    # 가장 큰 총합을 가진 컬럼명 출력
    max_column = total_population.idxmax()

    # 결과를 그래프로 표시
    fig = px.line(x=total_population.index, y=total_population.values, labels={'x': '시간대', 'y': '생활인구 수'},color_discrete_sequence=['red'],markers=True)
    fig.update_layout(title=f"{year}년 {quarter}분기 {dong_code} 행정동의 각 시간대별 생활인구 수",xaxis_tickangle=-45)
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return [f"가장 많은 시간대: {max_column}", graphJSON]

# 분석 22: 생활인구 가장 많은 시간대
def get_lifepop_day(year, quarter, dong_code):
    # 컬럼명 변경
    df_lifepop.rename(columns={
        '월요일_생활인구_수': '월요일',
        '화요일_생활인구_수': '화요일',
        '수요일_생활인구_수': '수요일',
        '목요일_생활인구_수': '목요일',
        '금요일_생활인구_수': '금요일',
        '토요일_생활인구_수': '토요일',
        '일요일_생활인구_수':'일요일'}, inplace=True)
    
    # 조건에 맞는 데이터 필터링
    filtered_df = df_lifepop[(df_lifepop['기준_년_코드'] == year) & (df_lifepop['기준_분기_코드'] == quarter) & (df_lifepop['행정동_코드'] == int(dong_code))]

    if filtered_df.empty:
        print("분석 22: 데이터가 존재하지 않습니다.")
        return None

    day_columns = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    # 각 요일별 생활인구 수의 총합 계산
    total_per_day = filtered_df[day_columns].sum()

    # 가장 큰 총합을 가진 요일 찾기
    max_day = total_per_day.idxmax()

    # 요일별 비율 계산
    mon_lifepop = filtered_df['월요일'].sum()
    tue_lifepop = filtered_df['화요일'].sum()
    wed_lifepop = filtered_df['수요일'].sum()
    thu_lifepop = filtered_df['목요일'].sum()
    fri_lifepop = filtered_df['금요일'].sum()
    sat_lifepop = filtered_df['토요일'].sum()
    sun_lifepop = filtered_df['일요일'].sum()
    total_lifepop = filtered_df['총_생활인구_수'].sum()

    total_lifepop= total_lifepop[0]
    mon_ratio = mon_lifepop / total_lifepop
    tue_ratio = tue_lifepop / total_lifepop
    wed_ratio = wed_lifepop / total_lifepop
    thu_ratio = thu_lifepop / total_lifepop
    fri_ratio = fri_lifepop / total_lifepop
    sat_ratio = sat_lifepop / total_lifepop
    sun_ratio = sun_lifepop / total_lifepop

    
    # 각 요일별 생활인구 수 막대 그래프 그리기
    day_labels = ['월', '화', '수', '목', '금', '토', '일']
    fig_bar = px.bar(x=day_labels, y=total_per_day, labels={'x': '요일', 'y': '생활인구 수'}, title='각 요일별 생활인구 수')

    # 행정동의 요일 비율 파이 차트 그리기
    ratios = [mon_ratio, tue_ratio, wed_ratio, thu_ratio, fri_ratio, sat_ratio, sun_ratio]
    print(list(ratios))
    data2 = pd.DataFrame(zip(day_labels, ratios), columns=['요일', '비율'])
    # 파이차트 요일 순서대로 출력하기
    fig_pie = px.pie(data2, names='요일', values='비율', title='행정동의 요일 비율',category_orders={'요일':['월', '화', '수', '목', '금', '토', '일']})
    graphJSON =  json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)

    return [list(zip(day_columns, total_per_day)), max_day, graphJSON]

# 분석 23: 2022년도 4분기 총 생활인구 수
def get_lifepop_recent(dong_code, year, quarter):
    filtered_df = df_lifepop[
    (df_lifepop['행정동_코드'] == int(dong_code)) &
    (df_lifepop['기준_년_코드'] == int(year)) &
    (df_lifepop['기준_분기_코드'] == int(quarter))]

    #입력한 것과 일치하는 데이터가 없으면
    if filtered_df.empty:
        print("분석 23: 데이터가 존재하지 않습니다.")
        return None

    # filtered_df에서 총 상주인구 수 총합 구하기
    total_lifepop = filtered_df['총_생활인구_수'].sum()

    return f"총 생활인구 수: {total_lifepop}명"

# 분석 24: 총 생활인구 수 변화
def get_lifepop_line(dong_code):
    year_quarter = []
    list_num = []

    for year in range(2017, 2023):
        for quarter in range(1, 5):
            filtered_df = df_lifepop[
                (df_lifepop['행정동_코드'] == int(dong_code)) &
                (df_lifepop['기준_년_코드'] == year) &
                (df_lifepop['기준_분기_코드'] == quarter)]

            if not filtered_df.empty:
                # 입력된 행정동코드로 행정동명 도출하기
                dong_name = df_lifepop[(df_lifepop['행정동_코드'] == int(dong_code))]['행정동명'].iloc[0]

                # filtered_df에서 총 생활인구 수 총합 구하기
                lifepop_value = filtered_df['총_생활인구_수'].sum().iloc[0]
                list_num.append(int(lifepop_value))  # 숫자로 변환
            else:
                lifepop_value = 0  # or some default value
                list_num.append(lifepop_value)  # add default value to list

            year_quarter.append(f"{year}_{quarter}")

    if not list_num:
        print("분석 24: 데이터가 존재하지 않습니다.")
        return None

    # 그래프 x축, y축, title, label 지정
    fig = px.line(x=year_quarter, y=list_num,
                  title=f"{dong_name}의 총 생활인구 수 변화", color_discrete_sequence=['black'], markers=True)

    # 그래프 커스터 마이징
    fig.update_layout(
        xaxis_title="분기",
        yaxis_title="총 생활인구 수 변화"
    )
    # 꺾은선 그래프 출력
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# 직장인구
# 분석 25: 직장인구 수, 가장 많은 상위 3개 상권
def get_workpop_info(year, quarter, dong_code):
    filtered_df = df_workpop[(df_workpop['기준_년_코드'] == year) & (df_workpop['기준_분기_코드'] == quarter) & (df_workpop['행정동_코드'] == int(dong_code))]

    if filtered_df.empty:
        print("분석 25: 데이터가 존재하지 않습니다.")
        return None

    workpop_value = filtered_df['총_직장인구_수'].sum()

    top_workpop = filtered_df.nlargest(3, '총_직장인구_수')[['상권_코드','상권_코드_명','총_직장인구_수']]
    for index, row in top_workpop.iterrows():
        code = row['상권_코드']
        name = row['상권_코드_명']
        workpop = row['총_직장인구_수']

    fig = px.bar(top_workpop, x='상권_코드_명', y='총_직장인구_수', title='상위 상권 코드별 직장인구 수',color_discrete_sequence=['green'])
    fig.update_layout(bargap=0.7)
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return [f"총 직장인구 수: {workpop_value}명", f"직장인구 수가 많은 상위 상권: 상권명:{name}, 직장인구 수:{workpop}명", graphJSON]