import streamlit as st
import json

# 1. 페이지 설정 (여기에 'expanded' 설정을 추가했어요!)
st.set_page_config(
    page_title="내 귀여운 말 키우기", 
    page_icon="🐴", 
    initial_sidebar_state="expanded" # 사이드바를 강제로 펼쳐두는 옵션
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
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 💾 데이터 저장/불러오기 기능 (사이드바) ---
with st.sidebar:
    st.header("💾 데이터 관리")
    st.write("새로고침하면 데이터가 날아가요! 꼭 저장하세요.")
    
    # 1) 현재 상태를 딕셔너리로 만들기
    current_data = {
        "hunger": st.session_state.get("hunger", 50),
        "protein": st.session_state.get("protein", 30),
        "carbs": st.session_state.get("carbs", 30),
        "fat": st.session_state.get("fat", 30),
        "happiness": st.session_state.get("happiness", 50),
        "action": st.session_state.get("action", "normal"),
        "message": st.session_state.get("message", "저장된 데이터를 불러와주세요!")
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
    uploaded_file = st.file_uploader("📂 저장된 파일 불러오기", type=["json"])
    
    if uploaded_file is not None:
        loaded_data = json.load(uploaded_file)
        
        st.session_state.hunger = loaded_data["hunger"]
        st.session_state.protein = loaded_data["protein"]
        st.session_state.carbs = loaded_data["carbs"]
        st.session_state.fat = loaded_data["fat"]
        st.session_state.happiness = loaded_data["happiness"]
        st.session_state.action = loaded_data["action"]
        st.session_state.message = "데이터 복구 완료! 다시 만나서 반가워! 👋"
        
        if 'loaded' not in st.session_state:
             st.session_state.loaded = True
             st.success("데이터를 성공적으로 불러왔습니다!")

# 3. 데이터 초기화
if 'hunger' not in st.session_state:
    st.session_state.hunger = 50      
if 'protein' not in st.session_state:
    st.session_state.protein = 30     
if 'carbs' not in st.session_state:
    st.session_state.carbs = 30       
if 'fat' not in st.session_state:
    st.session_state.fat = 30         
if 'happiness' not in st.session_state:
    st.session_state.happiness = 50   
if 'action' not in st.session_state:
    st.session_state.action = "normal"
if 'message' not in st.session_state:
    st.session_state.message = "안녕? 오늘은 우육면이 땡기는데... 🍜"
if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"

# --- 기능 함수들 ---

def eat_food(menu):
    st.session_state.action = "eating"
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
        st.session_state.happiness = min(100, st.session_state.happiness + 30)
        st.session_state.message = "캬~ 취한다! 기분이 너무 좋아! 🥴"
    elif menu == "🍜 우육면":
        st.session_state.protein = min(100, st.session_state.protein + 15)
        st.session_state.fat = min(100, st.session_state.fat + 15)
        st.session_state.message = "뜨끈한 국물이 끝내줘요! 호로록!"
    
    st.session_state.current_page = "main"

def date_hedgehog():
    if st.session_state.hunger < 20:
        st.session_state.action = "normal"
        st.session_state.message = "배고파서 데이트 나갈 힘도 없어... 💦"
    else:
        st.session_state.hunger = max(0, st.session_state.hunger - 10)
        st.session_state.happiness = min(100, st.session_state.happiness + 20)
        st.session_state.action = "happy"
        st.session_state.message = "고슴도치랑 손잡고 걸었어! 너무 설레! 🦔💖"

def exercise_horse():
    st.session_state.hunger = max(0, st.session_state.hunger - 20)
    st.session_state.fat = max(0, st.session_state.fat - 20)
    st.session_state.protein = min(100, st.session_state.protein + 10)
    st.session_state.action = "eating" 
    st.session_state.message = "으쌰으쌰! 지방을 태우자! 💦 (배고파짐)"

def sleep_horse():
    st.session_state.action = "normal"
    st.session_state.message = "쿨쿨... 꿀잠 자는 중... 💤"

# --- 화면 전환 로직 ---

if st.session_state.current_page == "main":
    st.title("🐴 힙한 말 키우기")
    st.info(st.session_state.message)

    col1, col2 = st.columns([1.2, 1])

    with col1:
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
        st.write(f"🥕 포만감 ({st.session_state.hunger}%)")
        st.progress(st.session_state.hunger / 100)
        
        st.divider()
        st.caption(f"💪 단백질 {st.session_state.protein}%")
        st.progress(st.session_state.protein / 100)
        st.caption(f"🍚 탄수화물 {st.session_state.carbs}%")
        st.progress(st.session_state.carbs / 100)
        st.caption(f"🧀 지방 {st.session_state.fat}%")
        st.progress(st.session_state.fat / 100)

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
        if st.button("🏋️‍♀️ 운동"):
            exercise_horse()
            st.rerun()
    with b4:
        if st.button("💤 잠자기"):
            sleep_horse()
            st.rerun()

elif st.session_state.current_page == "feed":
    st.title("🍽️ 메뉴를 골라주세요")
    st.write("오늘은 무엇을 먹을까요? 신중하게 선택하세요!")
    
    menu = st.radio("메뉴판", 
        ["🥤 단백질 쉐이크", "🌾 말먹이", "🍚 밥", "🍶 술", "🍜 우육면"])

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("이걸로 먹이기! 🥄"):
            eat_food(menu)
            st.rerun()
            
    with c2:
        if st.button("취소 (돌아가기)"):
            st.session_state.current_page = "main"
            st.rerun()
