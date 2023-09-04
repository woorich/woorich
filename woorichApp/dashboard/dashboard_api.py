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
print(df_apart)


# 분석5: 해당 동의 가장 최근(2022) 아파트 평균 가격 및 6억 이상 아파트 비율
def avg_apartment_prices(dong_code):
    # 입력 받은 행정동 명에 해당하는 행을 필터링
    dong_row = df_apart[df_apart['dong_code'] == int(dong_code)]
    print(type(dong_code))
    print(df_apart.info())
    if dong_row.empty:
        return "행정동을 찾을 수 없습니다."

    # 해당 행정동의 2022년 평균 아파트 가격을 계산
    avg_price_2022 = dong_row[dong_row['year'] == 2022]['avg_price'].mean()

    # 해당 행정동의 6억 이상 아파트 비율을 계산
    total_apartments = dong_row[dong_row['year'] == 2022]['~1'] + dong_row[dong_row['year'] == 2022]['1~2'] + dong_row[dong_row['year'] == 2022]['2~3'] + dong_row[dong_row['year'] == 2022]['3~4'] + dong_row[dong_row['year'] == 2022]['4~5'] + dong_row[dong_row['year'] == 2022]['5~6'] + dong_row[dong_row['year'] == 2022]['6~']
    apartments_over_6 = dong_row[dong_row['year'] == 2022]['6~']
    over_6_ratio = apartments_over_6.sum() / total_apartments.sum()

    # 결과 출력
    result = f"해당 행정동의 2022년 평균 아파트 가격: {avg_price_2022:,.2f}원"
    result += f"\n해당 행정동의 2022년 6억 이상 아파트 비율: {over_6_ratio:.2%}"

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
                title=f"해당 행정동의 아파트 가격 변화 추이")

    fig.update_layout(yaxis_tickformat=",.0f")

    # 그래프 커스터 마이징
    fig.update_layout(xaxis_title="분기", yaxis_title="아파트 가격 변화")

    graphJSON =  json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # return fig.show()
    return graphJSON

