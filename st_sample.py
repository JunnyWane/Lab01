import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import pandas as pd
import os

col_1, col_2, col_3 = st.columns([1,2,1])

st.header('데이터시각화 과제 3')
with col_3:
    st.write('B771027 왕현준')
st.divider()
st.subheader('대한민국 시군구 출생률 지도')

################################# map 코드

## 시군구별 출생아수 데이터 불러오기
df_birth = pd.read_csv("devided_birth.csv")

## 필요한 열만 선택
df_birth = df_birth[['시군구별', '2023']]

## 열 이름 변경
df_birth.columns = ['행정구', '출생수']

## 첫째 행 목록명으로 되어있어 삭제
df_birth = df_birth.drop(index=0).reset_index(drop=True)

## 출생아수 > 출생률 데이터로 변환
df_birth['출생수'] = pd.to_numeric(df_birth['출생수'])
df_birth['출생률'] = df_birth['출생수']/1000 # 출생률 = 출생아수/1000

## geojason 파일 불러오기
gdf_korea = gpd.read_file('korea.json')

## 다시 필요한 열만 선택
df_birth = df_birth[['행정구', '출생률']]

## '시'명 제거하기
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('수원시 ', '', regex=False)
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('성남시 ', '', regex=False)
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('안양시 ', '', regex=False)
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('안산시 ', '', regex=False)
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('고양시 ', '', regex=False)
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('용인시 ', '', regex=False)
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('청주시 ', '', regex=False)
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('천안시 ', '', regex=False)
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('전주시 ', '', regex=False)
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('포항시 ', '', regex=False)
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('창원시 ', '', regex=False)

## '세종특별자치시'를 '세종시'로 변경
gdf_korea['SIG_KOR_NM'] = gdf_korea['SIG_KOR_NM'].str.replace('세종특별자치시', '세종시')


## 중심좌표 설정
center = [36.2024, 127.4612] # 전국지도이므로, 대한민국 중심인 충북 옥천 청성면으로 설정

## 지도 생성
m = folium.Map(location=center, zoom_start=7, tiles='cartodbpositron')

## Choropleth 맵핑
folium.Choropleth(
    geo_data=gdf_korea,  # geojson 파일 설정
    data=df_birth,  # 맵핑할 데이터
    columns=('행정구', '출생률'),  # data에서 이용할 열 설정
    key_on='feature.properties.SIG_KOR_NM',  # geojson에서 매핑할 열 설정
    fill_color='BuPu',  # 색상 설정
    fill_opacity=0.7,  # 채우기 투명도
    line_opacity=0.5,  # 선 투명도
    legend_name='출생률'  # 범례 이름
).add_to(m)

folium_static(m)

############################
st.write('')
st.write('')
st.text('!. 분명히 출생률은 인구수를 고려하지 않은 절대적 지표라 그런지, 인구가 높은 지역이 높은 경향성을 보이는 듯 함')
st.text('!. 그렇다면, 인구수가 높은 지역이 출생률이 낮다면, 특징적인 지역으로 예상해볼 수 있을 듯 함')
