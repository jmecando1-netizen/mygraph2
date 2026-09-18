import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

df = pd.read_csv(DATA_URL)

# 장르가 여러 개 있으면 첫 번째 장르만 사용
df["genre"] = df["genre"].fillna("").astype(str).str.split("|").str[0]

# 장르별 영화 편수
genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]

# 전체 영화 수
total_movies = genre_count["영화 편수"].sum()

# 비율 계산
genre_count["비율"] = genre_count["영화 편수"] / total_movies * 100

st.subheader("1. 장르별 영화 편수")

fig = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 이 기간에는 어떤 장르의 영화가 가장 많이 개봉했는지 알 수 있다."
)

st.markdown("---")
