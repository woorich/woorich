# 방법1. Dash로 대시보드를 작성해서 Flask 서버와 연동
# https://kibua20.tistory.com/212 
# pip install dash 후
# python dashboard_api.py 로 실행해보세요.

# from dash import Dash, html, dcc, callback, Output, Input
# import plotly.express as px
# import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# app = Dash(__name__)

# app.layout = html.Div([
#     html.H1(children='Title of Dash App', style={'textAlign':'center'}),
#     dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
#     dcc.Graph(id='graph-content')
# ])

# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):
#     dff = df[df.country==value]
#     return px.line(dff, x='year', y='pop')

# if __name__ == '__main__':
#     app.run(debug=True)


# 방법 2. Plotly 함수를 직접 삽입
# 참고: https://blog.heptanalytics.com/flask-plotly-dashboard/
# https://github.com/yvonnegitau/flask-Dashboard
import plotly
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import numpy as np
import json

import pymysql
import pandas as pd
import os

RDS_HOST = os.getenv('RDS_HOST')
RDS_PORT = 3306
RDS_USERNAME = os.getenv('RDS_USERNAME')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_DB_NAME1 = os.getenv('RDS_DB_NAME1')


conn = pymysql.connect(
    host=RDS_HOST,     # MySQL Server Address
    port=RDS_PORT,          # MySQL Server Port
    user=RDS_USERNAME,      # MySQL username
    passwd=RDS_PASSWORD,    # password for MySQL username
    db=RDS_DB_NAME1,   # Database name
    charset='utf8mb4'
)

df_apart = pd.read_sql("select * from df_apart",conn)
df_store = pd.read_sql("select * from df_store",conn)
df_facility = pd.read_sql("select * from df_facility",conn)

# 분석0: 행정동별 상권 개수
def zone_num(dong_code):
   df_zone = df_store[df_store['행정동_코드']==int(dong_code)]
   a = df_zone[('상권_코드')].nunique()
   b = df_zone[('상권_코드_명')].unique()
   return f"해당 행정동에는 총 {a}개의 상권이 있습니다. 목록: {b}"


# 분석1: 행정동별 가장 점포수가 많은 업종
def by_loc(dong_code):
    def service_max(i):
       return i.value_counts().index[0]
    df_temp = df_store[df_store['행정동_코드']==int(dong_code)]
    a = df_temp.groupby('행정동명').agg({'점포_수' : 'max', '서비스_업종_코드_명_x': service_max}).reset_index()
    return f"{a['행정동명'].iloc[0]}의 가장 많은 업종은 {a['서비스_업종_코드_명_x'].iloc[0]}이며 총 {a['점포_수'].iloc[0]}개의 점포가 있습니다"


# 분석2: 행정동 내 업종 대분류별 업소 수
def store_num(dong_code):
    df_temp = df_store[df_store['행정동_코드']==int(dong_code)]
    #업종별 점포수의 합
    df_filtered = df_temp.groupby(['업종_대분류'])[['점포_수']].sum().squeeze()

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
    df_filtered= df_store[(df_store['행정동_코드']==int(dong_code)) & (df_store['업종_대분류'] == job_code)]
    df = df_filtered.groupby(['기준_년_코드', '기준_분기_코드'])[['점포_수']].sum()
    if df.empty:
        return "데이터가 없습니다."
    
    x=list(range(12))

    for i in range(12):
        x[i]=(f'202{i//4}'+'_'+f'{(i%4)+1}')
    colors = ['점포 수']
    for template in ["simple_white"]:
        fig = px.line(df, x=x, y='점포_수',
              labels={'기준_분기_코드': '분기', '점포_수': '점포 수'},
              title='분기별 업소 수 추이',
              template=template)
    fig.update_xaxes(title_text='시기')
    fig.update_traces(line_width=4,line_dash='dash',line_color='rgb(128,177,211)')
    # fig.show()
    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# 분석4: 주요 시설 현황
def facility_num(dong_code):
    df_filtered_1 = df_facility.loc[(df_facility['기준_년_코드'] == 2022) & (df_facility['기준_분기_코드'] == 4) & (df_facility['행정동_코드'] == int(dong_code))].groupby(['행정동명'])[['관공서_수', '은행_수', '종합병원_수', '일반_병원_수', '약국_수', '유치원_수',
       '초등학교_수', '중학교_수', '고등학교_수', '대학교_수', '백화점_수', '슈퍼마켓_수', '극장_수',
       '숙박_시설_수', '공항_수', '철도_역_수', '버스_터미널_수', '지하철_역_수', '버스_정거장_수']].sum().squeeze()
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

# 분석5: 해당 동의 가장 최근(2022) 아파트 평균 가격 및 6억 이상 아파트 비율
def avg_apartment_prices(dong_code):
    # 입력 받은 행정동 명에 해당하는 행을 필터링
    dong_row = df_apart[df_apart['dong_code'] == int(dong_code)]
    if dong_row.empty:
        return "행정동을 찾을 수 없습니다."

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
    # return fig.show()
    return graphJSON


# 분석 7: 해당 동의 가장 최근(2022) 66㎡(약 20평) 미만 비율 리턴하는 함수
def less_than_66(dong_code):
   dong_row = df_apart[df_apart['dong_code'] == int(dong_code)]
   if dong_row.empty:
      return "행정동을 찾을 수 없습니다."

  # 해당 행정동의 2022년 1인 가구 비율을 계산
   total_apartments = dong_row[dong_row['year'] == 2022]['~66sm'] + dong_row[dong_row['year'] == 2022]['66~99sm'] + dong_row[dong_row['year'] == 2022]['99~132sm'] + dong_row[dong_row['year'] == 2022]['132~165sm'] + dong_row[dong_row['year'] == 2022]['165sm~']
   apartment_less_than_66 = dong_row[dong_row['year'] == 2022]['~66sm']
   less_than_ratio = apartment_less_than_66.sum() / total_apartments.sum()

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
    # return fig.show()
    return graphJSON