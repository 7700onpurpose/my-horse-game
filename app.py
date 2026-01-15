import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(page_title="내 귀여운 말 키우기", page_icon="🐴")

# 2. 스타일 꾸미기
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 10px;
    }
    /* 영양소 게이지바 스타일 */
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 게임 상태 초기화 (영양소 추가!)
if 'hunger' not in st.session_state:
    st.session_state.hunger = 50      # 전체 포만감
if 'protein' not in st.session_state:
    st.session_state.protein = 30     # 단백질
if 'carbs' not in st.session_state:
    st.session_state.carbs = 30       # 탄수화물
if 'fat' not in st.session_state:
    st.session_state.fat = 30         # 지방
if 'happiness' not in st.session_state:
    st.session_state.happiness = 50   # 행복도
if 'action' not in st.session_state:
    st.session_state.action = "normal"
if 'message' not in st.session_state:
    st.session_state.message = "안녕? 오늘은 우육면이 땡기는데... 🍜"

# --- 기능 함수들 ---

# 1) 밥 먹기 (메뉴별로 효과가 다름)
def eat_food(menu):
    st.session_state.action = "eating"
    
    # 기본적으로 배는 다 부름
    st.session_state.hunger = min(100, st.session_state.hunger + 20)
    
    if menu == "🥤 단백질 쉐이크":
        st.session_state.protein = min(100, st.session_state.protein + 30)
        st.session_state.message = "득근득근! 단백질이 차오른다! 💪"
    elif menu == "🌾 말먹이":
        st.session_state.protein = min(100, st.session_state.protein + 10)
        st.session_state.carbs = min(100, st.session_state.carbs + 10)
        st.session_state.fat = min(100, st.session_state.fat + 10)
        st.session_state.message = "음~ 건강한 맛이야. 냠냠."
    elif menu == "🍚 밥":
        st.session_state.carbs = min(100, st.session_state.carbs + 30)
        st.session_state.message = "한국인은 밥심이지! 탄수화물 충전!"
    elif menu == "🍶 술":
        st.session_state.fat = min(100, st.session_state.fat + 20)
        st.session_state.happiness = min(100, st.session_state.happiness + 30) # 술 마시면 기분 좋아짐
        st.session_state.message = "캬~ 취한다! 기분이 너무 좋아! 🥴"
    elif menu == "🍜 우육면":
        st.session_state.protein = min(100, st.session_state.protein + 15)
        st.session_state.fat = min(100, st.session_state.fat + 15)
        st.session_state.message = "뜨끈한 국물이 끝내줘요! 호로록!"

# 2) 고슴도치와 데이트
def date_hedgehog():
    if st.session_state.hunger < 20:
        st.session_state.action = "normal"
        st.session_state.message = "배고파서 데이트 나갈 힘도 없어... 💦"
    else:
        st.session_state.hunger = max(0, st.session_state.hunger - 10)
        st.session_state.happiness = min(100, st.session_state.happiness + 20)
        st.session_state.action = "happy"
        st.session_state.message = "고슴도치랑 손잡고 걸었어! 너무 설레! 🦔💖"

# 3) 운동하기 (지방 감소, 배고픔 증가)
def exercise_horse():
    st.session_state.hunger = max(0, st.session_state.hunger - 20)
    st.session_state.fat = max(0, st.session_state.fat - 20)
    st.session_state.protein = min(100, st.session_state.protein + 10) # 근육 증가
    st.session_state.action = "eating" # (운동하는 이미지가 없어서 일단 eating이나 normal 사용)
    st.session_state.message = "으쌰으쌰! 지방을 태우자! 💦 (배고파짐)"

# 4) 잠자기
def sleep_horse():
    st.session_state.action = "normal"
    st.session_state.message = "쿨쿨... 꿀잠 자는 중... 💤"


# --- 화면 구성 ---

st.title("🐴 힙한 말 키우기")
st.info(st.session_state.message)

col1, col2 = st.columns([1.2, 1])

with col1:
    # 이미지 표시 영역
    if st.session_state.action == "eating":
        st.image("eating.png", caption="냠냠 쩝쩝")
    elif st.session_state.action == "happy":
        st.image("happy.png", caption="행복해!")
    else:
        st.image("normal.png", caption="무념무상")

with col2:
    st.write("### 📊 내 상태")
    
    st.write(f"💖 행복도 ({st.session_state.happiness}%)")
    st.progress(st.session_state.happiness / 100)
    
    st.divider()
    
    st.write(f"🥕 **포만감 ({st.session_state.hunger}%)**")
    st.progress(st.session_state.hunger / 100)
    
    # 영양소 상세 게이지 (작게 표현)
    st.caption(f"💪 단백질 {st.session_state.protein}%")
    st.progress(st.session_state.protein / 100)
    
    st.caption(f"🍚 탄수화물 {st.session_state.carbs}%")
    st.progress(st.session_state.carbs / 100)
    
    st.caption(f"🧀 지방 {st.session_state.fat}%")
    st.progress(st.session_state.fat / 100)

st.divider()

# --- 조작 버튼 영역 ---

# 1. 밥 주기 (메뉴 선택)
st.subheader("🍽️ 밥 메뉴 고르기")
menu = st.selectbox("무엇을 먹일까요?", 
                    ["🥤 단백질 쉐이크", "🌾 말먹이", "🍚 밥", "🍶 술", "🍜 우육면"])

if st.button("밥 먹이기 🥄"):
    eat_food(menu)
    st.rerun() # 화면 즉시 갱신

st.markdown("---")

# 2. 활동 버튼들 (3개 나란히)
b1, b2, b3 = st.columns(3)

with b1:
    if st.button("🦔 고슴도치와 데이트"):
        date_hedgehog()
        st.rerun()

with b2:
    if st.button("🏋️‍♀️ 운동하기"):
        exercise_horse()
        st.rerun()

with b3:
    if st.button("💤 잠재우기"):
        sleep_horse()
        st.rerun()
