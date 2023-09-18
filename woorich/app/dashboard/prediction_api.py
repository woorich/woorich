from woorichApp.dashboard.cache_utils import get_data
import pandas as pd
from prophet import Prophet
import numpy as np
import matplotlib.pyplot as plt

df_model_data = get_data("select * from df_modeldata")
df_service = get_data("select * from df_service")


df_model_data['기간'] = pd.to_datetime(df_model_data['기간'])

# 서비스_업종_코드 CS100001 -> 100001(int)로 변환
df_service['서비스_업종_코드'] = df_service['서비스_업종_코드'].str.replace('CS', '')
df_service['서비스_업종_코드'] = df_service['서비스_업종_코드'].astype(int)

def set_df():
    # '행정동_코드'로 그룹화하여 분리하고 각각의 데이터프레임으로 저장
    grouped = df_model_data.groupby('행정동_코드')
    separated_dfs = [group for _, group in grouped]

    for a in range(len(separated_dfs)):
        first_code = separated_dfs[a]['행정동_코드'].iloc[0]

        grouped_2 = separated_dfs[a].groupby('업종_대분류_코드')
        separated_dfs_2 = [group for _, group in grouped_2]

        for c in range(len(separated_dfs_2)):
            first_code_2 = separated_dfs_2[c]['업종_대분류_코드'].iloc[0]


            # 데이터프레임 이름 만들기
            df_name = f"df_{first_code}_{first_code_2}"

            # 데이터프레임 저장
            globals()[df_name] = separated_dfs_2[c]



#예측모델
def prediction(dong_code, job_code):
  set_df()
  woorich = eval(f'{"df_"+str(dong_code)+"_"+str(job_code)}')

  # 데이터프레임 생성
  data = pd.DataFrame({
      'ds':  woorich['기간'],
      'y':  woorich['분기당_매출_금액'],
      'service_code':  woorich['서비스_업종_코드']
  })

  # 서비스 업종 코드(unique values) 리스트 추출
  service_codes = data['service_code'].unique()

  # Prophet 모델 저장을 위한 딕셔너리
  models = {}

  # 그래프 초기화
  plt.figure(figsize=(20, 8))

  # 예측 결과 저장을 위한 데이터프레임 초기화
  predicted_values = pd.DataFrame(columns=['ds', 'yhat', 'service_code'])


  # top_5_service_names 리스트 초기화
  top_5_service_names = []

  for idx, service_code in enumerate(service_codes):
      # 해당 서비스 업종 코드에 해당하는 데이터 추출
      service_data = data[data['service_code'] == service_code]

      # Prophet 모델 초기화
      model = Prophet(interval_width=0.95)  # interval_width 설정

      # 모델 학습
      model.fit(service_data)

      # 모델 저장
      models[service_code] = model

      # 예측
      future_data = pd.DataFrame({'ds': pd.date_range(start='2022-10-01', periods=5, freq='M')})
      forecast = model.predict(future_data)

      # 예측 결과 데이터프레임에 추가
      predicted_values = pd.concat([predicted_values, forecast[['ds', 'yhat']].tail(1).assign(service_code=service_code)])

  # 예측 결과를 매출 값(yhat) 기준으로 내림차순 정렬
  predicted_values = predicted_values.sort_values(by='yhat', ascending=False)

  # 상위 5개 값을 추출
  top_5_predictions = predicted_values.head(5)

  # 상위 5개 예측값 출력
  print('------예측 매출이 높은 상위 5개 서비스 업종------')
  print(top_5_predictions)
  print('-------------------------------------------------')

  # 상위 5개 예측값을 그래프로 시각화
  for idx, row in top_5_predictions.iterrows():
      service_code = row['service_code']
      model = models[service_code]

      # # 예측 그래프 그리기
      # forecast = model.predict(future_data)
      # plt.plot(forecast['ds'], forecast['yhat'], label=f'Service Code: {service_code}',linewidth=5)

      # df_service에서 '서비스_업종_코드'와 일치하는 '서비스_업종_코드_명' 가져오기
      df_service_filtered = df_service[df_service['서비스_업종_코드'] == service_code]
      if not df_service_filtered.empty:
        service_name = df_service_filtered.iloc[0]['서비스_업종_코드_명']
        print(f'서비스업종코드: {service_code}, 서비스업종명: {service_name}')

        # top_5_service_names 리스트에 추가
        top_5_service_names.append(service_name)


  # # 그래프 레이블 및 범례 설정
  # plt.xlabel('날짜')
  # plt.ylabel('예상 매출')
  # plt.title('예측 매출이 높은 상위 5개 서비스 업종')
  # plt.legend(loc='upper left', fontsize=10)

  # # 그래프 표시
  # plt.show()

  # top_5_service_names 출력
  if top_5_service_names:
    return top_5_service_names
  else:
     return "데이터가 부족합니다."