import streamlit as st
import pandas as pd
import time
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="네이버 블로그 순위",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
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
    .stTextArea > div > div > textarea,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        padding: 0.75rem 1rem !important;
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
    
    /* 상단 툴바 */
    .stAppToolbar, [data-testid="stToolbar"],
    [data-testid="stHeader"], header[data-testid="stHeader"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)


def check_blog_rank(search_query, target_blog_link, max_scroll_attempts=7):
    """Selenium을 사용하여 네이버 블로그 순위 확인"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import NoSuchElementException
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Chrome 옵션 설정 (Headless 모드)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # WebDriver 초기화
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        try:
            # 검색 URL 생성 및 이동
            search_link = f"https://search.naver.com/search.naver?where=view&sm=tab_jum&query={search_query}"
            driver.get(search_link)
            time.sleep(2)
            
            blog_found = False
            current_rank = -1
            link_selector = f'a[href^="{target_blog_link}"]'
            
            for attempt in range(max_scroll_attempts):
                try:
                    element = driver.find_element(By.CSS_SELECTOR, link_selector)
                    
                    # 순위 찾기 (부모 요소로 이동하며 data-cr-rank 속성 탐색)
                    while True:
                        try:
                            rank_text = element.get_attribute("data-cr-rank")
                            if rank_text is not None:
                                current_rank = int(rank_text)
                                blog_found = True
                                break
                            else:
                                element = element.find_element(By.XPATH, "./..")
                        except NoSuchElementException:
                            break
                    
                    if blog_found:
                        break
                        
                except NoSuchElementException:
                    # 스크롤 다운
                    driver.execute_script("window.scrollBy(0, 10000);")
                    time.sleep(3)
            
            return {
                "keyword": search_query,
                "target_url": target_blog_link,
                "found": blog_found,
                "rank": current_rank if blog_found else None,
                "error": None
            }
            
        finally:
            driver.quit()
            
    except ImportError as e:
        return {
            "keyword": search_query,
            "target_url": target_blog_link,
            "found": False,
            "rank": None,
            "error": f"필요한 패키지가 설치되지 않았습니다: selenium, webdriver-manager를 설치해주세요."
        }
    except Exception as e:
        return {
            "keyword": search_query,
            "target_url": target_blog_link,
            "found": False,
            "rank": None,
            "error": str(e)
        }


# 메인 타이틀
st.markdown('<h1 class="main-title">📝 네이버 블로그 순위 확인</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">네이버 VIEW 검색에서 블로그 포스트의 순위를 확인합니다</p>', unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.markdown("### ⚙️ 검색 설정")
    st.markdown("---")
    
    max_scroll = st.slider(
        "최대 스크롤 횟수",
        min_value=3,
        max_value=15,
        value=7,
        help="순위를 찾기 위해 스크롤할 최대 횟수"
    )
    
    st.markdown("---")
    st.markdown("### 📌 사용 안내")
    st.markdown("""
    1. 검색할 키워드 입력
    2. 확인할 블로그 URL 입력
    3. '순위 확인' 버튼 클릭
    4. 결과 확인 및 다운로드
    """)
    
    st.markdown("---")
    st.markdown("### ⚠️ 주의사항")
    st.markdown("""
    - 블로그 URL은 정확히 입력
    - 키워드와 URL 수가 동일해야 함
    - 첫 실행 시 ChromeDriver 다운로드 필요
    """)

# 메인 컨텐츠
st.markdown("### 🔤 키워드 및 블로그 URL 입력")
st.caption("각 줄에 하나씩 키워드와 블로그 URL을 입력하세요. 순서가 일치해야 합니다.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔍 검색 키워드")
    keywords_input = st.text_area(
        "키워드 목록",
        placeholder="python flask\npython selenium\n네이버 블로그 순위",
        height=200,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("#### 🔗 블로그 URL")
    urls_input = st.text_area(
        "URL 목록",
        placeholder="https://blog.naver.com/username/123456789\nhttps://blog.naver.com/username/987654321\nhttps://blog.naver.com/username/111111111",
        height=200,
        label_visibility="collapsed"
    )

st.markdown("")

# 분석 버튼
check_button = st.button("🔍 순위 확인 시작", use_container_width=True)

if check_button:
    # 입력값 파싱
    keywords = [kw.strip() for kw in keywords_input.strip().split("\n") if kw.strip()]
    urls = [url.strip() for url in urls_input.strip().split("\n") if url.strip()]
    
    if not keywords:
        st.warning("⚠️ 최소 1개의 키워드를 입력해주세요!")
    elif not urls:
        st.warning("⚠️ 최소 1개의 블로그 URL을 입력해주세요!")
    elif len(keywords) != len(urls):
        st.warning(f"⚠️ 키워드 수({len(keywords)}개)와 URL 수({len(urls)}개)가 일치하지 않습니다!")
    else:
        st.markdown("---")
        st.markdown("### 🔄 순위 확인 중...")
        
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, (keyword, url) in enumerate(zip(keywords, urls)):
            status_text.markdown(f"**확인 중:** '{keyword}' ({idx+1}/{len(keywords)})")
            
            with st.spinner(f"'{keyword}' 키워드의 블로그 순위를 확인하는 중..."):
                result = check_blog_rank(keyword, url, max_scroll)
                results.append(result)
            
            progress_bar.progress((idx + 1) / len(keywords))
        
        status_text.markdown("**✅ 순위 확인 완료!**")
        
        # 세션에 결과 저장
        st.session_state['blog_rank_results'] = results

# 결과 표시
if 'blog_rank_results' in st.session_state:
    results = st.session_state['blog_rank_results']
    
    st.markdown("---")
    st.markdown("### 📊 순위 확인 결과")
    
    # 통계 요약
    found_count = sum(1 for r in results if r['found'])
    top10_count = sum(1 for r in results if r['found'] and r['rank'] and r['rank'] <= 10)
    
    stat_cols = st.columns(4)
    with stat_cols[0]:
        st.metric("🔎 총 검색", f"{len(results)}개")
    with stat_cols[1]:
        st.metric("✅ 발견", f"{found_count}개")
    with stat_cols[2]:
        st.metric("🏆 TOP 10", f"{top10_count}개")
    with stat_cols[3]:
        avg_rank = sum(r['rank'] for r in results if r['found'] and r['rank']) / found_count if found_count > 0 else 0
        st.metric("📈 평균 순위", f"{avg_rank:.1f}위" if avg_rank > 0 else "-")
    
    st.markdown("---")
    
    # 개별 결과 카드
    for result in results:
        if result['error']:
            st.error(f"❌ **{result['keyword']}**: {result['error']}")
        elif result['found']:
            rank = result['rank']
            if rank <= 10:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(34, 197, 94, 0.2)); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0; color: #f1f5f9;">🔍 {result['keyword']}</h4>
                            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0.5rem 0;">{result['target_url'][:70]}...</p>
                        </div>
                        <div style="font-size: 2.5rem; font-weight: 700; color: #4ade80;">{rank}위</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(59, 130, 246, 0.1)); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0; color: #f1f5f9;">🔍 {result['keyword']}</h4>
                            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0.5rem 0;">{result['target_url'][:70]}...</p>
                        </div>
                        <div style="font-size: 2.5rem; font-weight: 700; color: #818cf8;">{rank}위</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(248, 113, 113, 0.1)); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #f1f5f9;">🔍 {result['keyword']}</h4>
                        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0.5rem 0;">{result['target_url'][:70]}...</p>
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #f87171;">순위권 밖</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 데이터프레임 및 다운로드
    st.markdown("### 📋 상세 데이터")
    
    df = pd.DataFrame([{
        "키워드": r['keyword'],
        "블로그 URL": r['target_url'],
        "순위": r['rank'] if r['found'] else "순위권 밖",
        "발견 여부": "O" if r['found'] else "X",
        "오류": r['error'] if r['error'] else ""
    } for r in results])
    
    st.dataframe(df, use_container_width=True)
    
    # 다운로드 버튼
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 결과 다운로드 (CSV)",
        data=csv,
        file_name=f"네이버_블로그순위_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 2rem 0;">
    <p>📝 네이버 VIEW 검색 블로그 순위 확인 도구</p>
    <p style="font-size: 0.8rem;">Made with Streamlit & Selenium</p>
</div>
""", unsafe_allow_html=True)

