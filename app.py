import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(page_title="내 귀여운 말 키우기", page_icon="🐴")

# 2. 스타일 꾸미기 (버튼 예쁘게)
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        background-color: #FFD700;
        color: black;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 게임 상태(기억력) 초기화
if 'hunger' not in st.session_state:
    st.session_state.hunger = 50  # 배고픔 (0~100)
if 'happiness' not in st.session_state:
    st.session_state.happiness = 50  # 행복도 (0~100)
if 'action' not in st.session_state:
    st.session_state.action = "normal"  # 현재 상태 (normal, eating, happy)
if 'message' not in st.session_state:
    st.session_state.message = "안녕? 나는 너의 말이야! 🥕"

# 4. 행동 함수 (버튼 누르면 실행됨)
def feed_horse():
    st.session_state.hunger = min(100, st.session_state.hunger + 20)
    st.session_state.happiness = min(100, st.session_state.happiness + 5)
    st.session_state.action = "eating" # 그림을 먹는 모습으로 변경
    st.session_state.message = "냠냠! 당근 너무 맛있어! 🥕"

def play_horse():
    if st.session_state.hunger < 20:
        st.session_state.action = "normal"
        st.session_state.message = "배가 고파서 뛸 힘이 없어... 꼬르륵 💦"
    else:
        st.session_state.hunger = max(0, st.session_state.hunger - 10)
        st.session_state.happiness = min(100, st.session_state.happiness + 20)
        st.session_state.action = "happy" # 그림을 신난 모습으로 변경
        st.session_state.message = "히힝! 신난다! 더 놀자! 🎶"

def sleep_horse():
    st.session_state.action = "normal"
    st.session_state.message = "쿨쿨... 잠을 자니 개운해. 💤"

# 5. 화면 보여주기
st.title("🐴 우리집 말 키우기")
st.info(st.session_state.message) # 말의 대사창

col1, col2 = st.columns([1, 1])

with col1:
    # 상태에 따라 다른 그림 보여주기
    # 주의: 파일 이름이 정확해야 이미지가 뜹니다!
    if st.session_state.action == "eating":
        st.image("eating.png", caption="오물오물")
    elif st.session_state.action == "happy":
        st.image("happy.png", caption="폴짝폴짝")
    else:
        st.image("normal.png", caption="말똥말똥")

with col2:
    st.write("---")
    st.write(f"**🥕 포만감: {st.session_state.hunger}%**")
    st.progress(st.session_state.hunger / 100)
    
    st.write(f"**💖 행복도: {st.session_state.happiness}%**")
    st.progress(st.session_state.happiness / 100)
    st.write("---")

# 버튼 배치
b1, b2, b3 = st.columns(3)
with b1:
    st.button("🥕 밥 주기", on_click=feed_horse)
with b2:
    st.button("🎾 놀아주기", on_click=play_horse)
with b3:
    st.button("💤 잠재우기", on_click=sleep_horse)
