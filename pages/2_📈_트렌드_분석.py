import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import json
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="네이버 트렌드 분석",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS (메인 페이지와 동일한 테마)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    .main, .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif !important;
        color: #e2e8f0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    
    p, span, div, label {
        color: #e2e8f0 !important;
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #94a3b8 !important;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
        color: #ffffff !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
    }
    
    .stTextInput > div > div > input,
    [data-baseweb="input"] input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        padding: 0.75rem 1rem !important;
    }
    
    [data-baseweb="select"] > div {
        background: rgba(30, 41, 59, 0.95) !important;
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
    }
    
    [data-baseweb="select"] span,
    [data-baseweb="select"] div {
        color: #f1f5f9 !important;
    }
    
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [data-baseweb="menu"] > div {
        background: #1e293b !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
    }
    
    [data-baseweb="menu"] li,
    [role="option"] {
        color: #e2e8f0 !important;
        background: #1e293b !important;
    }
    
    [data-baseweb="menu"] li:hover,
    [role="option"]:hover {
        background: rgba(99, 102, 241, 0.3) !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        color: #f8fafc !important;
        background: linear-gradient(135deg, #6366f1, #3b82f6) !important;
    }
    
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 1.25rem;
    }
    
    [data-testid="stMetricLabel"] p {
        color: #94a3b8 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }
    
    .stDateInput > div > div > input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        color: #f1f5f9 !important;
        border-radius: 12px !important;
    }
    
    .stMultiSelect > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 12px !important;
    }
    
    .stMultiSelect span {
        color: #f1f5f9 !important;
    }
    
    /* 상단 툴바 */
    .stAppToolbar, [data-testid="stToolbar"],
    [data-testid="stHeader"], header[data-testid="stHeader"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)


# API 설정
CLIENT_ID = "31NEgSezE98zxrUqxQ09"
CLIENT_SECRET = "dVkHf14lmy"


def get_trend_data(keywords_groups, start_date, end_date, time_unit="month", device="", gender="", ages=[]):
    """네이버 데이터랩 통합검색 트렌드 API 호출"""
    url = "https://openapi.naver.com/v1/datalab/search"
    
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
        "Content-Type": "application/json"
    }
    
    # 요청 바디 구성
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "keywordGroups": keywords_groups
    }
    
    # 선택적 파라미터 추가
    if device:
        body["device"] = device
    if gender:
        body["gender"] = gender
    if ages:
        body["ages"] = ages
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API 오류: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"요청 실패: {str(e)}"


# 메인 타이틀
st.markdown('<h1 class="main-title">📈 네이버 통합검색 트렌드</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">네이버 데이터랩 API를 활용한 검색어 트렌드 분석</p>', unsafe_allow_html=True)

# 사이드바 설정
with st.sidebar:
    st.markdown("### ⚙️ 검색 설정")
    st.markdown("---")
    
    # 기간 설정
    st.markdown("#### 📅 분석 기간")
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "시작일",
            value=datetime.now() - timedelta(days=365),
            max_value=datetime.now()
        )
    
    with col2:
        end_date = st.date_input(
            "종료일",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    # 시간 단위
    time_unit = st.selectbox(
        "시간 단위",
        options=["date", "week", "month"],
        format_func=lambda x: {"date": "일간", "week": "주간", "month": "월간"}.get(x, x),
        index=2
    )
    
    st.markdown("---")
    st.markdown("#### 🎯 필터 설정")
    
    # 디바이스 설정
    device = st.selectbox(
        "디바이스",
        options=["", "pc", "mo"],
        format_func=lambda x: {"": "전체", "pc": "PC", "mo": "모바일"}.get(x, x)
    )
    
    # 성별 설정
    gender = st.selectbox(
        "성별",
        options=["", "m", "f"],
        format_func=lambda x: {"": "전체", "m": "남성", "f": "여성"}.get(x, x)
    )
    
    # 연령대 설정
    age_options = {
        "1": "0~12세",
        "2": "13~18세",
        "3": "19~24세",
        "4": "25~29세",
        "5": "30~34세",
        "6": "35~39세",
        "7": "40~44세",
        "8": "45~49세",
        "9": "50~54세",
        "10": "55~59세",
        "11": "60세 이상"
    }
    
    selected_ages = st.multiselect(
        "연령대 (복수 선택 가능)",
        options=list(age_options.keys()),
        format_func=lambda x: age_options.get(x, x),
        default=[]
    )
    
    st.markdown("---")
    st.markdown("### 📌 사용 안내")
    st.markdown("""
    1. 비교할 키워드 그룹 입력
    2. 분석 기간 및 필터 설정
    3. '트렌드 분석' 버튼 클릭
    4. 그래프로 트렌드 비교
    """)

# 메인 컨텐츠
st.markdown("### 🔤 키워드 그룹 설정")
st.caption("비교하고 싶은 키워드 그룹을 입력하세요. 각 그룹에 여러 키워드를 쉼표로 구분하여 입력할 수 있습니다.")

# 키워드 그룹 입력
num_groups = st.slider("비교할 키워드 그룹 수", min_value=1, max_value=5, value=2)

keyword_groups = []
colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

cols = st.columns(num_groups)
for i in range(num_groups):
    with cols[i]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {colors[i]}33, {colors[i]}22); 
                    border: 1px solid {colors[i]}66; 
                    border-radius: 12px; 
                    padding: 10px; 
                    margin-bottom: 10px;">
            <span style="color: {colors[i]}; font-weight: bold;">그룹 {i+1}</span>
        </div>
        """, unsafe_allow_html=True)
        
        group_name = st.text_input(
            f"그룹명",
            value=f"키워드{i+1}",
            key=f"group_name_{i}",
            label_visibility="collapsed",
            placeholder=f"그룹 {i+1} 이름"
        )
        
        keywords = st.text_input(
            f"키워드",
            key=f"keywords_{i}",
            label_visibility="collapsed",
            placeholder="키워드 (쉼표로 구분)"
        )
        
        if group_name and keywords:
            keyword_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]
            if keyword_list:
                keyword_groups.append({
                    "groupName": group_name,
                    "keywords": keyword_list
                })

# 분석 버튼
st.markdown("")
analyze_button = st.button("📊 트렌드 분석 시작", use_container_width=True)

# 결과 표시
if analyze_button:
    if not keyword_groups:
        st.warning("⚠️ 최소 1개의 키워드 그룹을 입력해주세요!")
    elif start_date >= end_date:
        st.warning("⚠️ 종료일은 시작일보다 이후여야 합니다!")
    else:
        with st.spinner("🔄 트렌드 데이터를 가져오는 중..."):
            data, error = get_trend_data(
                keyword_groups,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
                time_unit,
                device,
                gender,
                selected_ages
            )
        
        if error:
            st.error(f"❌ {error}")
        elif data and "results" in data:
            st.session_state['trend_data'] = data
            st.session_state['trend_groups'] = keyword_groups
            st.success("✅ 트렌드 분석이 완료되었습니다!")

# 저장된 데이터 표시
if 'trend_data' in st.session_state:
    data = st.session_state['trend_data']
    
    st.markdown("---")
    st.markdown("### 📊 트렌드 분석 결과")
    
    # 데이터 변환
    results = data.get("results", [])
    
    if results:
        # 그래프 생성
        fig = go.Figure()
        
        for idx, result in enumerate(results):
            title = result.get("title", f"그룹{idx+1}")
            keywords = result.get("keywords", [])
            data_points = result.get("data", [])
            
            if data_points:
                periods = [dp.get("period", "") for dp in data_points]
                ratios = [dp.get("ratio", 0) for dp in data_points]
                
                fig.add_trace(go.Scatter(
                    x=periods,
                    y=ratios,
                    mode='lines+markers',
                    name=f"{title} ({', '.join(keywords[:2])}{'...' if len(keywords) > 2 else ''})",
                    line=dict(color=colors[idx % len(colors)], width=3),
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title=dict(text="검색어 트렌드 비교", font=dict(color='#f1f5f9', size=20)),
            xaxis=dict(
                title="기간",
                tickfont=dict(color='#e2e8f0'),
                title_font=dict(color='#f1f5f9'),
                gridcolor='rgba(148, 163, 184, 0.1)',
                linecolor='rgba(148, 163, 184, 0.2)'
            ),
            yaxis=dict(
                title="검색량 지수 (상대값)",
                tickfont=dict(color='#e2e8f0'),
                title_font=dict(color='#f1f5f9'),
                gridcolor='rgba(148, 163, 184, 0.1)',
                linecolor='rgba(148, 163, 184, 0.2)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            legend=dict(
                font=dict(color='#e2e8f0'),
                bgcolor='rgba(30, 41, 59, 0.8)',
                bordercolor='rgba(148, 163, 184, 0.2)'
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 통계 요약
        st.markdown("### 📈 통계 요약")
        
        stat_cols = st.columns(len(results))
        for idx, result in enumerate(results):
            title = result.get("title", f"그룹{idx+1}")
            data_points = result.get("data", [])
            
            if data_points:
                ratios = [dp.get("ratio", 0) for dp in data_points]
                
                with stat_cols[idx]:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {colors[idx % len(colors)]}22, {colors[idx % len(colors)]}11); 
                                border: 1px solid {colors[idx % len(colors)]}44; 
                                border-radius: 16px; 
                                padding: 1.5rem;
                                text-align: center;">
                        <h4 style="color: {colors[idx % len(colors)]}; margin-bottom: 1rem;">{title}</h4>
                        <div style="display: flex; justify-content: space-around;">
                            <div>
                                <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">평균</p>
                                <p style="color: #f1f5f9; font-size: 1.5rem; font-weight: bold; margin: 0;">{sum(ratios)/len(ratios):.1f}</p>
                            </div>
                            <div>
                                <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">최고</p>
                                <p style="color: #4ade80; font-size: 1.5rem; font-weight: bold; margin: 0;">{max(ratios):.1f}</p>
                            </div>
                            <div>
                                <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">최저</p>
                                <p style="color: #f87171; font-size: 1.5rem; font-weight: bold; margin: 0;">{min(ratios):.1f}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # 데이터 테이블
        st.markdown("### 📋 상세 데이터")
        
        # 데이터프레임 생성
        all_data = []
        for result in results:
            title = result.get("title", "")
            for dp in result.get("data", []):
                all_data.append({
                    "그룹": title,
                    "기간": dp.get("period", ""),
                    "검색량 지수": dp.get("ratio", 0)
                })
        
        if all_data:
            df = pd.DataFrame(all_data)
            
            # 피벗 테이블 생성
            pivot_df = df.pivot(index="기간", columns="그룹", values="검색량 지수")
            pivot_df = pivot_df.reset_index()
            
            st.dataframe(pivot_df, use_container_width=True, height=300)
            
            # 다운로드 버튼
            csv = pivot_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 트렌드 데이터 다운로드 (CSV)",
                data=csv,
                file_name=f"네이버_트렌드분석_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 2rem 0;">
    <p>📈 네이버 데이터랩 API를 활용한 트렌드 분석 도구</p>
    <p style="font-size: 0.8rem;">Made with Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)

