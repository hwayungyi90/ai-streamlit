import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import time
import hashlib
import hmac
import base64
from bs4 import BeautifulSoup
import urllib.parse

# 페이지 설정
st.set_page_config(
    page_title="네이버 키워드 분석 도구",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    /* ===== 기본 배경 ===== */
    .main, .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* ===== 전역 텍스트 스타일 ===== */
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
    
    /* ===== 메인 타이틀 ===== */
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 40px rgba(56, 189, 248, 0.3);
    }
    
    .subtitle {
        color: #94a3b8 !important;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* ===== 마크다운 텍스트 ===== */
    .stMarkdown, .stMarkdown p, .stMarkdown span,
    [data-testid="stMarkdownContainer"], 
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span {
        color: #e2e8f0 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #f8fafc !important;
    }
    
    /* ===== 캡션 스타일 ===== */
    .stCaption, [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p,
    small, .st-emotion-cache-1gulkj5 {
        color: #94a3b8 !important;
    }
    
    /* ===== 버튼 ===== */
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
        background: linear-gradient(135deg, #818cf8 0%, #60a5fa 100%);
    }
    
    /* ===== 입력창 ===== */
    .stTextInput > div > div > input,
    [data-baseweb="input"] input,
    [data-baseweb="base-input"] input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        padding: 0.75rem 1rem !important;
        caret-color: #38bdf8 !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    
    .stTextInput > div > div > input:focus,
    [data-baseweb="input"] input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    
    [data-baseweb="base-input"] {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border-radius: 12px !important;
    }
    
    /* 입력창 아이콘 */
    [data-baseweb="input"] svg,
    [data-baseweb="base-input"] svg,
    .stTextInput svg {
        fill: #94a3b8 !important;
        color: #94a3b8 !important;
    }
    
    [data-baseweb="input"] button svg {
        fill: #94a3b8 !important;
    }
    
    /* ===== 셀렉트박스 ===== */
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
    
    [data-baseweb="select"] svg {
        fill: #94a3b8 !important;
    }
    
    /* 드롭다운 팝오버 (옵션 리스트) */
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div {
        background: #1e293b !important;
        background-color: #1e293b !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* 드롭다운 메뉴 */
    [data-baseweb="menu"],
    [data-baseweb="menu"] > div,
    ul[role="listbox"],
    ul[role="listbox"] > li {
        background: #1e293b !important;
        background-color: #1e293b !important;
    }
    
    [data-baseweb="menu"] li,
    ul[role="listbox"] li,
    [role="option"] {
        color: #e2e8f0 !important;
        background: #1e293b !important;
    }
    
    [data-baseweb="menu"] li:hover,
    ul[role="listbox"] li:hover,
    [role="option"]:hover,
    [data-baseweb="menu"] li[aria-selected="true"],
    [role="option"][aria-selected="true"] {
        background: rgba(99, 102, 241, 0.3) !important;
        color: #ffffff !important;
    }
    
    /* 옵션 텍스트 */
    [data-baseweb="menu"] li span,
    [data-baseweb="menu"] li div,
    ul[role="listbox"] li span,
    ul[role="listbox"] li div {
        color: #e2e8f0 !important;
    }
    
    /* Streamlit selectbox 옵션 */
    .stSelectbox [data-baseweb="select"] ul,
    .stSelectbox [data-baseweb="popover"] {
        background: #1e293b !important;
    }
    
    /* ===== 상단 메인 메뉴 (햄버거 메뉴) ===== */
    [data-testid="stMainMenu"] > div,
    [data-testid="stMainMenuPopover"],
    [data-testid="stMainMenuPopover"] > div {
        background: #1e293b !important;
        background-color: #1e293b !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5) !important;
    }
    
    [data-testid="stMainMenuPopover"] ul,
    [data-testid="stMainMenuPopover"] li {
        background: #1e293b !important;
        color: #e2e8f0 !important;
    }
    
    [data-testid="stMainMenuPopover"] li:hover {
        background: rgba(99, 102, 241, 0.2) !important;
        color: #ffffff !important;
    }
    
    [data-testid="stMainMenuPopover"] span,
    [data-testid="stMainMenuPopover"] p,
    [data-testid="stMainMenuPopover"] div {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stMainMenuPopover"] svg {
        fill: #94a3b8 !important;
        color: #94a3b8 !important;
    }
    
    /* 메뉴 구분선 */
    [data-testid="stMainMenuPopover"] hr {
        border-color: rgba(148, 163, 184, 0.2) !important;
    }
    
    /* ===== 사이드바 ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] li {
        color: #cbd5e1 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(148, 163, 184, 0.2) !important;
    }
    
    /* ===== 탭 ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        background: transparent;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #e2e8f0 !important;
        background: rgba(99, 102, 241, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        color: #f8fafc !important;
        background: linear-gradient(135deg, #6366f1, #3b82f6) !important;
    }
    
    /* ===== 메트릭 카드 ===== */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 1.25rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    
    [data-testid="stMetricLabel"] p {
        color: #94a3b8 !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }
    
    /* ===== 데이터프레임 ===== */
    [data-testid="stDataFrame"] {
        background: rgba(30, 41, 59, 0.5) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
    
    /* ===== 알림 박스 ===== */
    .stSuccess, [data-testid="stAlert"][data-type="success"] {
        background: rgba(34, 197, 94, 0.15) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        color: #86efac !important;
    }
    
    .stWarning, [data-testid="stAlert"][data-type="warning"] {
        background: rgba(234, 179, 8, 0.15) !important;
        border: 1px solid rgba(234, 179, 8, 0.3) !important;
        color: #fde047 !important;
    }
    
    .stError, [data-testid="stAlert"][data-type="error"] {
        background: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #fca5a5 !important;
    }
    
    .stInfo, [data-testid="stAlert"][data-type="info"] {
        background: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #93c5fd !important;
    }
    
    [data-testid="stAlert"] p {
        color: inherit !important;
    }
    
    /* ===== 다운로드 버튼 ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%) !important;
        transform: translateY(-2px) !important;
    }
    
    /* ===== 스피너 ===== */
    .stSpinner > div {
        color: #818cf8 !important;
    }
    
    /* ===== 구분선 ===== */
    hr {
        border-color: rgba(148, 163, 184, 0.2) !important;
    }
    
    /* ===== 링크 ===== */
    a {
        color: #60a5fa !important;
    }
    
    a:hover {
        color: #93c5fd !important;
    }
    
    /* ===== 상단 툴바 (stAppToolbar) ===== */
    .stAppToolbar, [data-testid="stToolbar"],
    [data-testid="stHeader"], header[data-testid="stHeader"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stAppToolbar button, [data-testid="stToolbar"] button,
    header button {
        color: #94a3b8 !important;
    }
    
    .stAppToolbar button:hover, [data-testid="stToolbar"] button:hover,
    header button:hover {
        color: #f1f5f9 !important;
        background: rgba(99, 102, 241, 0.2) !important;
    }
    
    .stAppToolbar svg, [data-testid="stToolbar"] svg,
    header svg {
        fill: #94a3b8 !important;
        color: #94a3b8 !important;
    }
    
    /* 상단 데코레이션 라인 */
    [data-testid="stDecoration"] {
        background: linear-gradient(90deg, #6366f1, #3b82f6, #38bdf8) !important;
    }
    
    /* 메뉴 버튼 */
    [data-testid="stMainMenu"] button {
        color: #94a3b8 !important;
    }
    
    [data-testid="stMainMenu"] button:hover {
        color: #f1f5f9 !important;
    }
</style>
""", unsafe_allow_html=True)


# 로그 관련 함수
def init_log():
    """로그 세션 상태 초기화"""
    if 'logs' not in st.session_state:
        st.session_state['logs'] = []

def add_log(message, log_type="info"):
    """로그 메시지 추가
    log_type: info, success, warning, error
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    type_icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "api": "🔗",
        "data": "📊"
    }
    
    icon = type_icons.get(log_type, "📝")
    log_entry = f"[{timestamp}] {icon} {message}"
    
    st.session_state['logs'].append({
        "time": timestamp,
        "type": log_type,
        "message": message,
        "full": log_entry
    })
    
    # 최대 100개의 로그만 유지
    if len(st.session_state['logs']) > 100:
        st.session_state['logs'] = st.session_state['logs'][-100:]

def clear_logs():
    """로그 초기화"""
    st.session_state['logs'] = []

# 로그 초기화
init_log()

# 앱 시작 로그 (최초 실행시만)
if 'app_started' not in st.session_state:
    st.session_state['app_started'] = True
    add_log("네이버 키워드 분석 도구가 시작되었습니다.", "success")
    add_log("키워드를 입력하고 '키워드 분석 시작' 버튼을 클릭하세요.", "info")


class Signature:
    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
        return base64.b64encode(hash.digest()).decode('utf-8')


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, secret_key)
    
    return {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Timestamp': timestamp,
        'X-API-KEY': api_key,
        'X-Customer': str(customer_id),
        'X-Signature': signature
    }


def get_keyword_results(hint_keywords, api_key, secret_key, customer_id):
    BASE_URL = 'https://api.naver.com'
    uri = '/keywordstool'
    method = 'GET'
    
    # 띄어쓰기를 쉼표로 변환 (네이버 API는 쉼표로 키워드 구분)
    # 여러 공백을 하나로 정리하고 쉼표로 변환
    processed_keywords = ','.join(hint_keywords.split())
    
    add_log(f"키워드 처리: '{hint_keywords}' → '{processed_keywords}'", "info")
    add_log(f"API 요청 시작: {BASE_URL}{uri}", "api")
    
    params = {
        'hintKeywords': processed_keywords,
        'showDetail': '1'
    }
    
    try:
        start_time = time.time()
        r = requests.get(
            BASE_URL + uri,
            params=params,
            headers=get_header(method, uri, api_key, secret_key, customer_id)
        )
        elapsed_time = round((time.time() - start_time) * 1000)
        
        add_log(f"API 응답 수신 (응답시간: {elapsed_time}ms, 상태코드: {r.status_code})", "api")
        
        if r.status_code == 200:
            data = r.json()
            if 'keywordList' in data:
                df = pd.DataFrame(data['keywordList'])
                add_log(f"데이터 파싱 완료: {len(df)}개 키워드 발견", "success")
                return df, None
            else:
                add_log("키워드 데이터를 찾을 수 없습니다.", "warning")
                return None, "키워드 데이터를 찾을 수 없습니다."
        else:
            add_log(f"API 오류 발생: {r.status_code}", "error")
            return None, f"API 오류: {r.status_code} - {r.text}"
    except Exception as e:
        add_log(f"요청 실패: {str(e)}", "error")
        return None, f"요청 실패: {str(e)}"


def format_number(num):
    """숫자를 읽기 쉬운 형태로 포맷"""
    if pd.isna(num) or num == '< 10':
        return num
    try:
        num = int(num)
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)
    except:
        return num


def get_related_keywords(keyword):
    """네이버 연관 검색어 크롤링"""
    try:
        add_log(f"연관 검색어 크롤링 시작: '{keyword}'", "api")
        
        # URL 인코딩
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={encoded_keyword}"
        
        # User-Agent 헤더 추가
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        start_time = time.time()
        response = requests.get(url, headers=headers)
        elapsed_time = round((time.time() - start_time) * 1000)
        
        add_log(f"네이버 검색 페이지 응답 (응답시간: {elapsed_time}ms)", "api")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 연관 검색어 찾기 (여러 선택자 시도)
            related_keywords = []
            
            # 방법 1: 연관 검색어 영역
            related_area = soup.find_all("li", {"class": "item"})
            for item in related_area:
                link = item.find("a", {"class": "keyword"})
                if link:
                    related_keywords.append(link.text.strip())
            
            # 방법 2: 다른 선택자 시도
            if not related_keywords:
                related_area = soup.find_all("a", {"class": "keyword"})
                for item in related_area:
                    text = item.text.strip()
                    if text and text not in related_keywords:
                        related_keywords.append(text)
            
            # 방법 3: 연관 검색어 div 클래스
            if not related_keywords:
                related_div = soup.find("div", {"class": "related_srch"})
                if related_div:
                    links = related_div.find_all("a")
                    for link in links:
                        text = link.text.strip()
                        if text and text not in related_keywords:
                            related_keywords.append(text)
            
            # 방법 4: tit 클래스 사용
            if not related_keywords:
                tit_divs = soup.find_all("div", {"class": "tit"})
                for div in tit_divs:
                    text = div.text.strip()
                    if text and text not in related_keywords:
                        related_keywords.append(text)
            
            if related_keywords:
                add_log(f"연관 검색어 {len(related_keywords)}개 발견", "success")
                return related_keywords[:10], None  # 최대 10개
            else:
                add_log("연관 검색어를 찾을 수 없습니다.", "warning")
                return [], "연관 검색어를 찾을 수 없습니다."
        else:
            add_log(f"네이버 검색 페이지 오류: {response.status_code}", "error")
            return [], f"페이지 로드 실패: {response.status_code}"
            
    except Exception as e:
        add_log(f"연관 검색어 크롤링 실패: {str(e)}", "error")
        return [], f"크롤링 실패: {str(e)}"


# 메인 타이틀
st.markdown('<h1 class="main-title">🔍 네이버 키워드 분석 도구</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">네이버 광고 API를 활용한 실시간 키워드 검색량 분석</p>', unsafe_allow_html=True)

# 사이드바 - API 설정
with st.sidebar:
    st.markdown("### ⚙️ API 설정")
    st.markdown("---")
    
    # 기본값으로 제공된 API 정보 설정
    customer_id = st.text_input(
        "Customer ID",
        value="2204950",
        help="네이버 광고 Customer ID"
    )
    
    api_key = st.text_input(
        "API Key (액세스라이선스)",
        value="0100000000f4c35bf4af11d3820253798c3a863a5b123a650b85726954905461bdd640d079",
        type="password",
        help="네이버 광고 API 액세스 라이선스"
    )
    
    secret_key = st.text_input(
        "Secret Key (비밀키)",
        value="AQAAAAD0w1v0rxHTggJTeYw6hjpb/9ArAOipTr8CYauAY4QBBQ==",
        type="password",
        help="네이버 광고 API 비밀키"
    )
    
    st.markdown("---")
    st.markdown("### 📌 사용 방법")
    st.markdown("""
    1. API 정보 확인
    2. 분석할 키워드 입력
    3. '키워드 분석' 버튼 클릭
    4. 결과 확인 및 다운로드
    """)
    
    st.markdown("---")
    st.markdown("### 📊 컬럼 설명")
    st.markdown("""
    - **relKeyword**: 연관 키워드
    - **monthlyPcQcCnt**: PC 월간 검색량
    - **monthlyMobileQcCnt**: 모바일 월간 검색량
    - **monthlyAvePcClkCnt**: PC 월평균 클릭수
    - **monthlyAveMobileClkCnt**: 모바일 월평균 클릭수
    - **monthlyAvePcCtr**: PC 월평균 클릭률
    - **monthlyAveMobileCtr**: 모바일 월평균 클릭률
    - **plAvgDepth**: 월평균 노출 광고수
    - **compIdx**: 경쟁 정도 (높음/중간/낮음)
    """)

# 메인 컨텐츠
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 🎯 키워드 입력")
    
    keyword_input = st.text_input(
        "키워드",
        placeholder="키워드 입력 (쉼표 또는 띄어쓰기로 구분, 예: 마케팅,쇼핑몰 또는 마케팅 쇼핑몰)",
        label_visibility="collapsed"
    )
    
    st.caption("💡 여러 키워드는 쉼표(,) 또는 띄어쓰기로 구분해서 입력하세요")
    
    search_button = st.button("🔍 키워드 분석 시작", width='stretch')

# 결과 표시
if search_button:
    if not keyword_input:
        st.warning("⚠️ 키워드를 입력해주세요!")
        add_log("키워드가 입력되지 않았습니다.", "warning")
    elif not all([customer_id, api_key, secret_key]):
        st.warning("⚠️ 사이드바에서 API 정보를 모두 입력해주세요!")
        add_log("API 정보가 누락되었습니다.", "warning")
    else:
        add_log(f"검색 시작: '{keyword_input}'", "info")
        
        # 키워드 API 검색
        with st.spinner("🔄 키워드 데이터를 가져오는 중..."):
            df, error = get_keyword_results(keyword_input, api_key, secret_key, customer_id)
        
        # 네이버 연관 검색어 크롤링 (첫 번째 키워드만)
        first_keyword = keyword_input.split()[0].split(',')[0]
        with st.spinner("🔄 네이버 연관 검색어를 가져오는 중..."):
            related_keywords, related_error = get_related_keywords(first_keyword)
        
        if error:
            st.error(f"❌ {error}")
        elif df is not None and not df.empty:
            st.success(f"✅ 총 {len(df)}개의 연관 키워드를 찾았습니다!")
            add_log(f"검색 완료: {len(df)}개 키워드 로드됨", "success")
            
            # 세션 상태에 저장
            st.session_state['df'] = df
            st.session_state['keyword'] = keyword_input
            st.session_state['related_keywords'] = related_keywords
            st.session_state['search_keyword'] = first_keyword

# 저장된 데이터가 있으면 표시
if 'df' in st.session_state:
    df = st.session_state['df']
    keyword = st.session_state.get('keyword', '')
    related_keywords = st.session_state.get('related_keywords', [])
    search_keyword = st.session_state.get('search_keyword', '')
    
    st.markdown("---")
    
    # 네이버 연관 검색어 섹션
    if related_keywords:
        st.markdown("### 🔗 네이버 연관 검색어")
        st.caption(f"'{search_keyword}' 검색 시 네이버에서 추천하는 연관 검색어입니다. **키워드를 클릭하면 상세 분석 결과를 볼 수 있습니다.**")
        
        # 연관 검색어를 버튼으로 표시 (10개 고정)
        num_cols = 5
        cols = st.columns(num_cols)
        
        for idx, kw in enumerate(related_keywords[:10]):
            with cols[idx % num_cols]:
                if st.button(f"#{idx+1} {kw}", key=f"related_{idx}", width='stretch'):
                    st.session_state['secondary_keyword'] = kw
                    st.session_state['secondary_df'] = None
                    st.session_state['secondary_related'] = None
                    add_log(f"연관 키워드 상세 분석: '{kw}'", "info")
        
        # 2차 연관 검색어 및 분석 결과 표시
        if 'secondary_keyword' in st.session_state and st.session_state['secondary_keyword']:
            secondary_kw = st.session_state['secondary_keyword']
            
            st.markdown(f"### 🔍 '{secondary_kw}' 상세 분석")
            
            # 데이터 로드 (캐싱)
            if st.session_state.get('secondary_df') is None:
                # API 분석 결과 가져오기
                with st.spinner(f"'{secondary_kw}' 키워드 분석 중..."):
                    sec_df, sec_error = get_keyword_results(secondary_kw, api_key, secret_key, customer_id)
                    st.session_state['secondary_df'] = sec_df
                    st.session_state['secondary_error'] = sec_error
                
                # 2차 연관 검색어 가져오기
                with st.spinner(f"'{secondary_kw}' 연관 검색어 수집 중..."):
                    secondary_related, _ = get_related_keywords(secondary_kw)
                    st.session_state['secondary_related'] = secondary_related
            
            sec_df = st.session_state.get('secondary_df')
            sec_error = st.session_state.get('secondary_error')
            secondary_related = st.session_state.get('secondary_related', [])
            
            # 닫기 버튼
            if st.button("❌ 상세 분석 닫기", key="close_secondary"):
                st.session_state['secondary_keyword'] = None
                st.session_state['secondary_df'] = None
                st.session_state['secondary_related'] = None
                st.rerun()
            
            # 2차 연관 검색어 표시
            if secondary_related:
                st.markdown(f"#### 🔄 '{secondary_kw}'의 연관 검색어")
                sec_cols = st.columns(5)
                for idx2, kw2 in enumerate(secondary_related[:10]):
                    with sec_cols[idx2 % 5]:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(34, 197, 94, 0.2)); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 10px 14px; margin-bottom: 10px; text-align: center;">
                            <span style="color: #4ade80; font-weight: bold;">#{idx2+1}</span>
                            <span style="color: #e2e8f0; margin-left: 8px;">{kw2}</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            # API 분석 결과 표시
            if sec_df is not None and not sec_df.empty:
                st.markdown(f"#### 📊 '{secondary_kw}' 키워드 분석 결과")
                st.success(f"✅ {len(sec_df)}개의 연관 키워드를 찾았습니다!")
                
                # 주요 지표
                sec_df_numeric = sec_df.copy()
                for col in ['monthlyPcQcCnt', 'monthlyMobileQcCnt']:
                    if col in sec_df_numeric.columns:
                        sec_df_numeric[col] = pd.to_numeric(sec_df_numeric[col].replace('< 10', '5'), errors='coerce')
                
                metric_cols = st.columns(4)
                with metric_cols[0]:
                    st.metric("🔎 키워드 수", f"{len(sec_df)}개")
                with metric_cols[1]:
                    if 'monthlyPcQcCnt' in sec_df_numeric.columns:
                        st.metric("💻 PC 검색량", format_number(sec_df_numeric['monthlyPcQcCnt'].sum()))
                with metric_cols[2]:
                    if 'monthlyMobileQcCnt' in sec_df_numeric.columns:
                        st.metric("📱 모바일 검색량", format_number(sec_df_numeric['monthlyMobileQcCnt'].sum()))
                with metric_cols[3]:
                    if 'monthlyPcQcCnt' in sec_df_numeric.columns and 'monthlyMobileQcCnt' in sec_df_numeric.columns:
                        st.metric("📊 전체 검색량", format_number(sec_df_numeric['monthlyPcQcCnt'].sum() + sec_df_numeric['monthlyMobileQcCnt'].sum()))
                
                # 데이터 테이블
                st.markdown("##### 📋 상세 데이터")
                
                # 숫자형 변환 및 정렬
                sec_df_display = sec_df.copy()
                numeric_cols = ['monthlyPcQcCnt', 'monthlyMobileQcCnt', 'monthlyAvePcClkCnt', 
                                'monthlyAveMobileClkCnt', 'monthlyAvePcCtr', 'monthlyAveMobileCtr', 'plAvgDepth']
                for col in numeric_cols:
                    if col in sec_df_display.columns:
                        sec_df_display[col] = pd.to_numeric(sec_df_display[col].replace('< 10', '5'), errors='coerce').fillna(0)
                
                if 'monthlyMobileQcCnt' in sec_df_display.columns:
                    sec_df_display = sec_df_display.sort_values(by='monthlyMobileQcCnt', ascending=False)
                
                st.dataframe(sec_df_display, width='stretch', height=300)
                
                # 다운로드 버튼
                sec_csv = sec_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label=f"📥 '{secondary_kw}' 분석 결과 다운로드",
                    data=sec_csv,
                    file_name=f"네이버_키워드분석_{secondary_kw}_{time.strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="download_secondary"
                )
            elif sec_error:
                st.error(f"❌ 분석 실패: {sec_error}")
            else:
                st.info(f"'{secondary_kw}'의 분석 결과가 없습니다.")
        
        st.markdown("---")
    
    # 주요 지표 카드
    st.markdown("### 📈 주요 지표")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 데이터 처리
    df_numeric = df.copy()
    for col in ['monthlyPcQcCnt', 'monthlyMobileQcCnt']:
        if col in df_numeric.columns:
            df_numeric[col] = pd.to_numeric(df_numeric[col].replace('< 10', '5'), errors='coerce')
    
    with col1:
        st.metric(
            label="🔎 총 키워드 수",
            value=f"{len(df):,}개"
        )
    
    with col2:
        if 'monthlyPcQcCnt' in df_numeric.columns:
            total_pc = df_numeric['monthlyPcQcCnt'].sum()
            st.metric(
                label="💻 PC 총 검색량",
                value=format_number(total_pc)
            )
    
    with col3:
        if 'monthlyMobileQcCnt' in df_numeric.columns:
            total_mobile = df_numeric['monthlyMobileQcCnt'].sum()
            st.metric(
                label="📱 모바일 총 검색량",
                value=format_number(total_mobile)
            )
    
    with col4:
        if 'monthlyPcQcCnt' in df_numeric.columns and 'monthlyMobileQcCnt' in df_numeric.columns:
            total_all = df_numeric['monthlyPcQcCnt'].sum() + df_numeric['monthlyMobileQcCnt'].sum()
            st.metric(
                label="📊 전체 검색량",
                value=format_number(total_all)
            )
    
    st.markdown("---")
    
    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["📋 데이터 테이블", "📊 시각화", "⬇️ 다운로드"])
    
    with tab1:
        st.markdown("#### 🔍 키워드 분석 결과")
        
        # 정렬 옵션
        sort_col = st.selectbox(
            "정렬 기준",
            options=['monthlyMobileQcCnt', 'monthlyPcQcCnt', 'relKeyword'],
            format_func=lambda x: {
                'monthlyMobileQcCnt': '모바일 검색량',
                'monthlyPcQcCnt': 'PC 검색량',
                'relKeyword': '키워드명'
            }.get(x, x)
        )
        
        # 정렬을 위한 데이터프레임 복사 및 숫자 변환
        df_display = df.copy()
        
        # 숫자형 컬럼 변환 (< 10 같은 문자열을 5로 대체)
        numeric_cols = ['monthlyPcQcCnt', 'monthlyMobileQcCnt', 'monthlyAvePcClkCnt', 
                        'monthlyAveMobileClkCnt', 'monthlyAvePcCtr', 'monthlyAveMobileCtr', 'plAvgDepth']
        for col in numeric_cols:
            if col in df_display.columns:
                df_display[col] = pd.to_numeric(df_display[col].replace('< 10', '5'), errors='coerce').fillna(0)
        
        # 정렬 수행
        if sort_col in df_display.columns:
            if sort_col == 'relKeyword':
                df_display = df_display.sort_values(by=sort_col, ascending=True)
            else:
                df_display = df_display.sort_values(by=sort_col, ascending=False)
        
        # 데이터프레임 표시
        st.dataframe(
            df_display,
            width='stretch',
            height=400
        )
    
    with tab2:
        st.markdown("#### 📊 검색량 시각화")
        
        # 상위 15개 키워드만 표시
        df_chart = df_numeric.head(15).copy()
        
        if 'relKeyword' in df_chart.columns:
            # 바 차트 - PC vs 모바일 검색량
            fig = go.Figure()
            
            if 'monthlyPcQcCnt' in df_chart.columns:
                fig.add_trace(go.Bar(
                    name='PC 검색량',
                    x=df_chart['relKeyword'],
                    y=df_chart['monthlyPcQcCnt'],
                    marker_color='#7c3aed'
                ))
            
            if 'monthlyMobileQcCnt' in df_chart.columns:
                fig.add_trace(go.Bar(
                    name='모바일 검색량',
                    x=df_chart['relKeyword'],
                    y=df_chart['monthlyMobileQcCnt'],
                    marker_color='#00d4ff'
                ))
            
            fig.update_layout(
                title=dict(text='상위 15개 키워드 검색량 비교', font=dict(color='#f1f5f9', size=18)),
                barmode='group',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=12),
                xaxis=dict(
                    tickangle=45,
                    tickfont=dict(color='#e2e8f0', size=11),
                    title_font=dict(color='#f1f5f9'),
                    gridcolor='rgba(148, 163, 184, 0.1)',
                    linecolor='rgba(148, 163, 184, 0.2)'
                ),
                yaxis=dict(
                    tickfont=dict(color='#e2e8f0', size=11),
                    title_font=dict(color='#f1f5f9'),
                    gridcolor='rgba(148, 163, 184, 0.1)',
                    linecolor='rgba(148, 163, 184, 0.2)'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(color='#e2e8f0')
                )
            )
            
            st.plotly_chart(fig, width='stretch')
            
            # 파이 차트 - PC vs 모바일 비율
            if 'monthlyPcQcCnt' in df_numeric.columns and 'monthlyMobileQcCnt' in df_numeric.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    total_pc = df_numeric['monthlyPcQcCnt'].sum()
                    total_mobile = df_numeric['monthlyMobileQcCnt'].sum()
                    
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=['PC', '모바일'],
                        values=[total_pc, total_mobile],
                        hole=0.5,
                        marker_colors=['#7c3aed', '#00d4ff']
                    )])
                    
                    fig_pie.update_layout(
                        title=dict(text='PC vs 모바일 검색량 비율', font=dict(color='#f1f5f9', size=16)),
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e2e8f0', size=12),
                        legend=dict(font=dict(color='#e2e8f0'))
                    )
                    fig_pie.update_traces(textfont=dict(color='#f1f5f9', size=12))
                    
                    st.plotly_chart(fig_pie, width='stretch')
                
                with col2:
                    # 경쟁도 분포
                    if 'compIdx' in df.columns:
                        comp_counts = df['compIdx'].value_counts()
                        
                        fig_comp = go.Figure(data=[go.Pie(
                            labels=comp_counts.index,
                            values=comp_counts.values,
                            hole=0.5,
                            marker_colors=['#10b981', '#f59e0b', '#ef4444']
                        )])
                        
                        fig_comp.update_layout(
                            title='경쟁도 분포',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#e2e8f0', size=12),
                            legend=dict(font=dict(color='#e2e8f0'))
                        )
                        fig_comp.update_traces(textfont=dict(color='#f1f5f9', size=12))
                        
                        st.plotly_chart(fig_comp, width='stretch')
    
    with tab3:
        st.markdown("#### ⬇️ 데이터 다운로드")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV 다운로드
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 CSV 다운로드",
                data=csv,
                file_name=f"네이버_키워드분석_{keyword}_{time.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                width='stretch'
            )
        
        with col2:
            # Excel 다운로드를 위한 버퍼
            st.download_button(
                label="📥 Excel 다운로드",
                data=csv,
                file_name=f"네이버_키워드분석_{keyword}_{time.strftime('%Y%m%d')}.csv",
                mime="application/vnd.ms-excel",
                width='stretch'
            )
        
        st.info("💡 TIP: CSV 파일은 Excel에서 열 때 UTF-8 인코딩으로 열어주세요.")

# 로그창 (항상 표시)
st.markdown("---")
st.markdown("### 📋 실행 로그")

# 로그 컨트롤 버튼
col_log1, col_log2, col_log3 = st.columns([1, 1, 4])

with col_log1:
    if st.button("🗑️ 로그 초기화", key="clear_log_btn"):
        clear_logs()
        add_log("로그가 초기화되었습니다.", "info")
        st.rerun()

# 로그 표시 영역
if st.session_state.get('logs'):
    log_html = "<div style='background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 1rem; max-height: 250px; overflow-y: auto; font-family: monospace; font-size: 0.85rem;'>"
    
    for log in st.session_state['logs']:
        log_type = log['type']
        color_map = {
            "info": "#60a5fa",
            "success": "#4ade80", 
            "warning": "#fbbf24",
            "error": "#f87171",
            "api": "#c084fc",
            "data": "#2dd4bf"
        }
        color = color_map.get(log_type, "#e2e8f0")
        log_html += f"<div style='color: {color}; margin-bottom: 6px; padding: 6px 8px; background: rgba(0,0,0,0.2); border-radius: 6px;'>{log['full']}</div>"
    
    log_html += "</div>"
    
    st.markdown(log_html, unsafe_allow_html=True)
    st.caption(f"📊 총 {len(st.session_state['logs'])}개의 로그")
else:
    st.markdown("""
    <div style='background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 2rem; text-align: center;'>
        <p style='color: #64748b; margin: 0;'>📝 아직 로그가 없습니다. 키워드를 검색하면 로그가 표시됩니다.</p>
    </div>
    """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 2rem 0;">
    <p>🚀 네이버 광고 API를 활용한 키워드 분석 도구</p>
    <p style="font-size: 0.8rem;">Made with Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)

