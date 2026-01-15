import streamlit as st
import json

# 1. 페이지 설정
st.set_page_config(
    page_title="내 귀여운 말 키우기", 
    page_icon="🐴", 
    initial_sidebar_state="expanded"
)

# 2. 스타일 꾸미기
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-size: 16px;
        font-weight: bold;
    }
    /* 게이지바 색상 (기본 초록) */
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 💾 데이터 저장/불러오기 기능 ---
with st.sidebar:
    st.header("💾 데이터 관리")
    st.write("새로고침하면 데이터가 날아가요! 꼭 저장하세요.")
    
    # 1) 현재 상태 저장 (새로운 근육/체지방 데이터 추가!)
    current_data = {
        "hunger": st.session_state.get("hunger", 50),
        "protein": st.session_state.get("protein", 30),
        "carbs": st.session_state.get("carbs", 30),
        "fat": st.session_state.get("fat", 30),
        "happiness": st.session_state.get("happiness", 50),
        
        # 새로 추가된 신체 스펙
        "upper_muscle": st.session_state.get("upper_muscle", 10),
        "lower_muscle": st.session_state.get("lower_muscle", 10),
        "body_fat": st.session_state.get("body_fat", 20),
        
        "action": st.session_state.get("action", "normal"),
        "message": st.session_state.get("message", "데이터 불러오기 대기 중...")
    }
    
    # 2) 다운로드 버튼
    json_string = json.dumps(current_data)
    st.download_button(
        label="💾 내 말 상태 저장하기",
        file_name="my_horse_data.json",
        mime="application/json",
        data=json_string,
    )
    
    st.divider()
    
    # 3) 업로드 버튼
    uploaded_file = st.file_uploader("📂 저장된 말 상태 불러오기", type=["json"])
    
    if uploaded_file is not None:
        loaded_data = json.load(uploaded_file)
        
        st.session_state.hunger = loaded_data["hunger"]
        st.session_state.protein = loaded_data["protein"]
        st.session_state.carbs = loaded_data["carbs"]
        st.session_state.fat = loaded_data["fat"]
        st.session_state.happiness = loaded_data["happiness"]
        
        # 신체 스펙 불러오기 (혹시 옛날 파일이라 없으면 기본값 10)
        st.session_state.upper_muscle = loaded_data.get("upper_muscle", 10)
        st.session_state.lower_muscle = loaded_data.get("lower_muscle", 10)
        st.session_state.body_fat = loaded_data.get("body_fat", 20)
        
        st.session_state.action = loaded_data["action"]
        st.session_state.message = "데이터 복구 완료! 헬창 말 가보자고! 💪"
        
        if 'loaded' not in st.session_state:
             st.session_state.loaded = True
             st.success("데이터를 성공적으로 불러왔습니다!")

# 3. 데이터 초기화 (변수가 없으면 기본값 생성)
if 'hunger' not in st.session_state: st.session_state.hunger = 50      
if 'protein' not in st.session_state: st.session_state.protein = 30     
if 'carbs' not in st.session_state: st.session_state.carbs = 30       
if 'fat' not in st.session_state: st.session_state.fat = 30         
if 'happiness' not in st.session_state: st.session_state.happiness = 50   

# ★ 새로 추가된 신체 스펙 초기화
if 'upper_muscle' not in st.session_state: st.session_state.upper_muscle = 10
if 'lower_muscle' not in st.session_state: st.session_state.lower_muscle = 10
if 'body_fat' not in st.session_state: st.session_state.body_fat = 20

if 'action' not in st.session_state: st.session_state.action = "normal"
if 'message' not in st.session_state: st.session_state.message = "안녕? 오늘은 3대 500 치고 싶은 날이야."
if 'current_page' not in st.session_state: st.session_state.current_page = "main"

# --- 기능 함수들 ---

def eat_food(menu):
    st.session_state.action = "eating"
    st.session_state.hunger = min(100, st.session_state.hunger + 20)
    
    # 밥 먹을 때 지방 섭취량에 따라 '체지방'도 같이 늘어나는 로직 추가!
    fat_increase = 0 
    
    if menu == "🥤 단백질 쉐이크":
        st.session_state.protein = min(100, st.session_state.protein + 30)
        st.session_state.message = "근성장에 단백질은 필수지! 💪"
    elif menu == "🌾 말먹이":
        st.session_state.protein = min(100, st.session_state.protein + 10)
        st.session_state.carbs = min(100, st.session_state.carbs + 10)
        st.session_state.fat = min(100, st.session_state.fat + 10)
        fat_increase = 5
        st.session_state.message = "건강한 식단이다."
    elif menu == "🍚 밥":
        st.session_state.carbs = min(100, st.session_state.carbs + 30)
        st.session_state.protein = min(100, st.session_state.protein + 10)
        st.session_state.message = "탄수화물 로딩 완료!"
    elif menu == "🍶 술":
        st.session_state.fat = min(100, st.session_state.fat + 20)
        st.session_state.happiness = min(100, st.session_state.happiness + 30)
        fat_increase = 15 # 술은 살이 많이 찜
        st.session_state.message = "오늘만 치팅데이다.. 🥴"
    elif menu == "🍜 우육면":
        st.session_state.protein = min(100, st.session_state.protein + 15)
        st.session_state.fat = min(100, st.session_state.fat + 15)
        fat_increase = 10
        st.session_state.message = "국물까지 싹 비웠다.."
    
    # 실제 체지방 증가 적용
    if fat_increase > 0:
        st.session_state.body_fat = min(100, st.session_state.body_fat + fat_increase)
        st.session_state.message += f" (체지방 +{fat_increase} 🔺)"
    
    st.session_state.current_page = "main"

def date_hedgehog():
    if st.session_state.hunger < 20:
        st.session_state.action = "normal"
        st.session_state.message = "배고파서 못 나가... 근손실 올 거 같아... 💦"
    else:
        st.session_state.hunger = max(0, st.session_state.hunger - 10)
        st.session_state.happiness = min(100, st.session_state.happiness + 20)
        st.session_state.action = "happy"
        st.session_state.message = "고슴도치가 내 근육 멋있대! 🦔💖"

# 운동하기 함수 (메뉴별 분기 처리)
def do_exercise(type):
    st.session_state.action = "eating" # 운동 이미지가 없어서 일단 eating으로 대체
    st.session_state.hunger = max(0, st.session_state.hunger - 20) # 배고픔 증가
    
    if type == "💪 상체 조지기":
        st.session_state.upper_muscle = min(100, st.session_state.upper_muscle + 10)
        st.session_state.body_fat = max(0, st.session_state.body_fat - 5)
        st.session_state.message = "벤치프레스 성공! 가슴이 웅장해진다! (상체근육🔺 체지방🔻)"
        
    elif type == "🦵 하체 조지기":
        st.session_state.lower_muscle = min(100, st.session_state.lower_muscle + 10)
        st.session_state.body_fat = max(0, st.session_state.body_fat - 5)
        st.session_state.message = "스쿼트 하다가 다리 풀렸다.. (하체근육🔺 체지방🔻)"
        
    elif type == "🏃 유산소 태우기":
        st.session_state.body_fat = max(0, st.session_state.body_fat - 15)
        st.session_state.happiness = max(0, st.session_state.happiness - 5) # 유산소는 힘드니까 행복도 약간 감소 ㅋㅋ
        st.session_state.message = "런닝머신 1시간.. 지방이 불타고 있다.. (체지방 대폭 하락🔻)"

    st.session_state.current_page = "main"

def sleep_horse():
    st.session_state.action = "normal"
    st.session_state.message = "근육은 쉴 때 성장한다... 굿나잇 💤"

# --- 화면 전환 로직 ---

if st.session_state.current_page == "main":
    # ================= [메인 화면] =================
    st.title("🐴 힙한 말 키우기")
    st.info(st.session_state.message)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        # 상태에 따른 이미지 표시
        if st.session_state.action == "eating":
            st.image("eating.png", caption="벌크업 중")
        elif st.session_state.action == "happy":
            st.image("happy.png", caption="포징 잡는 중")
        else:
            st.image("normal.png", caption="근손실 걱정 중")

    with col2:
        st.write("### 📊 내 상태")
        st.write(f"💖 행복도 ({st.session_state.happiness}%)")
        st.progress(st.session_state.happiness / 100)
        st.write(f"🥕 포만감 ({st.session_state.hunger}%)")
        st.progress(st.session_state.hunger / 100)
        
        st.divider()
        st.write("**🥗 영양소 밸런스**")
        st.caption(f"단백질 {st.session_state.protein}% | 탄수화물 {st.session_state.carbs}% | 지방 {st.session_state.fat}%")
        st.progress(st.session_state.protein / 100) # 대표로 단백질만 보여주거나, 3개 다 보여줘도 됨
        
        st.divider()
        st.write("**💪 인바디 (Body Check)**")
        
        st.caption(f"👕 상체 근육: {st.session_state.upper_muscle}%")
        st.progress(st.session_state.upper_muscle / 100)
        
        st.caption(f"👖 하체 근육: {st.session_state.lower_muscle}%")
        st.progress(st.session_state.lower_muscle / 100)
        
        # 체지방은 빨간색 느낌이 나면 좋은데 CSS 없이는 어려우니 기본으로
        st.caption(f"🐷 체지방률: {st.session_state.body_fat}%")
        st.progress(st.session_state.body_fat / 100)

    st.markdown("---")
    
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("🍽️ 밥 주기"):
            st.session_state.current_page = "feed"
            st.rerun()
    with b2:
        if st.button("🦔 데이트"):
            date_hedgehog()
            st.rerun()
    with b3:
        if st.button("🏋️‍♀️ 운동하기"): # 여기를 누르면 exercise 화면으로 이동!
            st.session_state.current_page = "exercise"
            st.rerun()
    with b4:
        if st.button("💤 잠자기"):
            sleep_horse()
            st.rerun()

elif st.session_state.current_page == "feed":
    # ================= [식당 화면] =================
    st.title("🍽️ 식단 관리")
    st.write("근성장을 위해 무엇을 먹을까요?")
    
    menu = st.radio("메뉴판", 
        ["🥤 단백질 쉐이크", "🌾 말먹이", "🍚 밥", "🍶 술", "🍜 우육면"])

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("이걸로 먹이기! 🥄"):
            eat_food(menu)
            st.rerun()
    with c2:
        if st.button("돌아가기"):
            st.session_state.current_page = "main"
            st.rerun()

elif st.session_state.current_page == "exercise":
    # ================= [헬스장 화면] =================
    st.title("🏋️‍♀️ 헬스장 입장")
    st.write("오늘은 어디를 조질까요? (운동을 하면 배가 고파집니다)")
    
    # 운동 종류 선택
    ex_menu = st.radio("운동 루틴 선택", 
        ["💪 상체 조지기", "🦵 하체 조지기", "🏃 유산소 태우기"])

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("운동 시작! 🔥"):
            do_exercise(ex_menu)
            st.rerun()
    with c2:
        if st.button("도망가기 (메인으로)"):
            st.session_state.current_page = "main"
            st.rerun()
