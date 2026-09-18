import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 숫자형 열 정리
    numeric_cols = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 장르가 여러 개이면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|", regex=False)
        .str[0]
        .replace("", "미상")
    )

    # 국가 결측치 처리
    df["nation"] = df["nation"].fillna("미상").astype(str)

    # 영화명 결측치 처리
    df["movieNm"] = df["movieNm"].fillna("영화명 미상").astype(str)

    return df


df = load_data()


# =========================================================
# 1. 장르별 영화 편수 - 도넛 그래프
# =========================================================

st.subheader("1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]

fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 이 기간에는 어떤 장르의 영화가 가장 많이 개봉했는지 알 수 있다.",
    key="insight1"
)

st.markdown("---")


# =========================================================
# 2. 장르 안의 영화 - 트리맵
# =========================================================

st.subheader("2. 장르별 영화의 총 관객수")

treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].dropna(subset=["total_audi"]).copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객수",
    custom_data=["movieNm", "total_audi"]
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "총 관객: %{customdata[1]:,.0f}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 장르별로 어떤 영화가 많은 관객을 모았는지 비교할 수 있다.",
    key="insight2"
)

st.markdown("---")


# =========================================================
# 3. 총 관객수 - 히스토그램
# =========================================================

st.subheader("3. 총 관객수의 분포")

hist_df = df[
    ["movieNm", "total_audi"]
].dropna(subset=["total_audi"]).copy()

hist_df = hist_df[hist_df["total_audi"] >= 0]

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=10,
    title="총 관객수 히스토그램",
    labels={
        "total_audi": "총 관객수",
        "count": "영화 편수"
    }
)

fig3.update_layout(
    xaxis_title="총 관객수",
    yaxis_title="영화 편수"
)

st.plotly_chart(fig3, use_container_width=True)

counts, edges = np.histogram(
    hist_df["total_audi"],
    bins=10
)

max_bin_index = int(np.argmax(counts))

bin_start = edges[max_bin_index]
bin_end = edges[max_bin_index + 1]

top_movie_row = hist_df.loc[
    hist_df["total_audi"].idxmax()
]

top_movie = top_movie_row["movieNm"]
top_movie_audi = int(top_movie_row["total_audi"])

st.info(
    f"대부분의 영화는 약 {bin_start:,.0f}명 ~ {bin_end:,.0f}명 구간에 몰려 있으며, "
    f"가장 관객이 많은 영화는 **{top_movie}**로 총 관객 **{top_movie_audi:,}명**입니다."
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 대부분의 영화가 비교적 적은 관객수 구간에 집중되어 있음을 알 수 있다.",
    key="insight3"
)

st.markdown("---")


# =========================================================
# 4. 개봉일 스크린수와 총 관객수 - 산점도
# =========================================================

st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

scatter_df = df[
    ["movieNm", "genre", "first_scrn", "total_audi"]
].dropna(
    subset=["first_scrn", "total_audi"]
).copy()

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객수",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "genre": "장르"
    }
)

fig4.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객수: %{y:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 개봉일 스크린수가 많은 영화일수록 총 관객수도 많은 경향이 나타난다.",
    key="insight4"
)

st.markdown("---")


# =========================================================
# 5. 영화가 10편 이상인 장르 - 박스플롯
# =========================================================

st.subheader("5. 장르별 총 관객수 비교")

genre_10 = df["genre"].value_counts()

valid_genres = genre_10[
    genre_10 >= 10
].index.tolist()

box_df = df[
    df["genre"].isin(valid_genres)
    & df["total_audi"].notna()
].copy()

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    custom_data=["movieNm"],
    title="영화가 10편 이상인 장르의 총 관객수",
    labels={
        "genre": "장르",
        "total_audi": "총 관객수"
    }
)

fig5.update_traces(
    hovertemplate=(
        "영화명: %{customdata[0]}<br>"
        "총 관객수: %{y:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 장르별 총 관객수의 분포와 관객이 특히 많은 영화를 비교할 수 있다.",
    key="insight5"
)

st.markdown("---")


# =========================================================
# 6. 첫 주 관객수를 점 크기로 사용한 버블 산점도
# =========================================================

st.subheader("6. 첫 주 관객수를 나타낸 버블 산점도")

bubble_df = df[
    [
        "movieNm",
        "genre",
        "first_scrn",
        "total_audi",
        "first_week_audi"
    ]
].dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi"
    ]
).copy()

bubble_df["bubble_size"] = bubble_df["first_week_audi"].clip(lower=1)

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="bubble_size",
    color="genre",
    hover_name="movieNm",
    custom_data=["first_week_audi"],
    title="개봉일 스크린수 × 총 관객수 × 첫 주 관객수",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "bubble_size": "첫 주 관객수",
        "genre": "장르"
    },
    size_max=45
)

fig6.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객수: %{y:,}명<br>"
        "첫 주 관객수: %{customdata[0]:,.0f}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 첫 주 관객수가 많은 영화일수록 총 관객수도 많은 경향을 확인할 수 있다.",
    key="insight6"
)

st.markdown("---")


# =========================================================
# 7. 제작 국가 → 장르 - 선버스트 그래프
# =========================================================

st.subheader("7. 제작 국가와 장르의 관계")

sunburst_df = df[
    ["nation", "genre"]
].copy()

sunburst_df["영화 편수"] = 1

fig7 = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    values="영화 편수",
    title="제작 국가 → 장르별 영화 편수"
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 제작 국가에 따라 영화의 장르 구성이 다르다는 것을 알 수 있다.",
    key="insight7"
)

st.markdown("---")


# =========================================================
# 8. 나만의 질문 - 산점도
# =========================================================

my_question = "개봉일 상영횟수가 많은 영화는 첫 주 관객도 많은가?"

st.subheader("8. 나만의 질문")

scatter8_df = df[
    ["movieNm", "first_show", "first_week_audi"]
].dropna(
    subset=["first_show", "first_week_audi"]
).copy()

fig8 = px.scatter(
    scatter8_df,
    x="first_show",
    y="first_week_audi",
    hover_name="movieNm",
    title=my_question,
    labels={
        "first_show": "개봉일 상영횟수",
        "first_week_audi": "첫 주 관객수"
    }
)

fig8.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 상영횟수: %{x:,}회<br>"
        "첫 주 관객수: %{y:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig8, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 개봉일 상영횟수가 많을수록 첫 주 관객수가 많은 경향이 있는지 확인할 수 있다.",
    key="insight8"
)
