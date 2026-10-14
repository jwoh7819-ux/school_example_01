import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="MBTI 포켓몬 도감", page_icon="🔴", layout="centered")

# 커스텀 CSS (포켓몬 도감 테마)
st.markdown('''
<style>
.stApp {
    background-color: #f4f4f9;
}
h1, h2, h3 {
    color: #E3350D;
    text-align: center;
    font-family: 'Arial Black', sans-serif;
}
.stButton>button {
    background-color: #FFCC00;
    color: #333333;
    font-weight: bold;
    border-radius: 10px;
    border: 2px solid #3366B5;
    width: 100%;
    height: 60px;
    font-size: 18px;
}
.stButton>button:hover {
    background-color: #3366B5;
    color: #FFCC00;
    border: 2px solid #FFCC00;
}
.pokemon-card {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    border: 4px solid #FFCC00;
    text-align: center;
    margin-top: 20px;
}
.emoji-large {
    font-size: 120px;
    line-height: 1.2;
}
.pokemon-name {
    font-size: 32px;
    font-weight: bold;
    color: #E3350D;
    margin: 10px 0;
}
.desc-text {
    font-size: 18px;
    color: #444;
    margin-bottom: 20px;
}
.match-box {
    background-color: #e6f2ff;
    padding: 10px;
    border-radius: 10px;
    color: #3366B5;
    font-weight: bold;
}
</style>
''', unsafe_allow_html=True)

# 포켓몬 데이터 (스탯 포함)
pokemon_data = {
    "ISTJ": {"name": "꼬부기", "emoji": "🐢", "desc": "성실하고 책임감이 강하며 묵묵히 제 할 일을 하는 모습이 꼭 닮았어요.", "match": "ESTP", "stats": [80, 50, 70, 60, 80]},
    "ISFJ": {"name": "이상해씨", "emoji": "🍃", "desc": "따뜻하고 다정하며 주변 사람들을 묵묵히 챙기는 평화주의자예요.", "match": "ESFP", "stats": [70, 60, 60, 70, 70]},
    "INFJ": {"name": "라프라스", "emoji": "🌊", "desc": "신비롭고 깊은 내면을 가졌으며, 다른 사람을 돕는 것을 좋아해요.", "match": "ENFP", "stats": [90, 40, 60, 90, 50]},
    "INTJ": {"name": "뮤츠", "emoji": "👽", "desc": "냉철한 분석력과 뛰어난 지능을 가진 똑똑한 전략가 스타일이에요.", "match": "ENTP", "stats": [70, 90, 60, 100, 40]},
    "ISTP": {"name": "나무지기", "emoji": "🦎", "desc": "쿨하고 무심한 듯 보이지만 뛰어난 관찰력과 순발력을 자랑해요.", "match": "ESTJ", "stats": [50, 80, 50, 40, 90]},
    "ISFP": {"name": "푸린", "emoji": "🎤", "desc": "감수성이 풍부하고 따뜻하며 예술적인 영혼을 가졌어요.", "match": "ESFJ", "stats": [90, 30, 40, 80, 40]},
    "INFP": {"name": "메타몽", "emoji": "💟", "desc": "유연하고 상상력이 풍부하며 상대방에게 잘 맞춰주는 배려심 깊은 성격이에요.", "match": "ENFJ", "stats": [60, 40, 50, 90, 60]},
    "INTP": {"name": "야돈", "emoji": "🦥", "desc": "호기심이 많고 느긋해 보이지만, 머릿속엔 심오한 세계가 펼쳐져 있어요.", "match": "ENTJ", "stats": [80, 50, 60, 80, 30]},
    "ESTP": {"name": "피카츄", "emoji": "⚡", "desc": "에너지가 넘치고 호기심이 많아 어디서든 주인공이 되는 스타일!", "match": "ISTJ", "stats": [50, 70, 40, 60, 100]},
    "ESFP": {"name": "토게피", "emoji": "🥚", "desc": "밝고 명랑해서 주변 사람들을 즐겁게 해주는 최고의 분위기 메이커예요.", "match": "ISFJ", "stats": [60, 40, 50, 80, 70]},
    "ENFP": {"name": "이브이", "emoji": "🦊", "desc": "무한한 가능성을 가지고 있고 언제나 에너지가 넘치며 활발해요.", "match": "INFJ", "stats": [70, 60, 50, 70, 80]},
    "ENTP": {"name": "팬텀", "emoji": "👻", "desc": "장난기가 많고 독창적이며 번뜩이는 아이디어로 모두를 놀라게 해요.", "match": "INTJ", "stats": [60, 80, 40, 90, 80]},
    "ESTJ": {"name": "리자몽", "emoji": "🔥", "desc": "리더십이 뛰어나고 목표를 향해 뜨겁게 돌진하는 열정적인 성격이에요.", "match": "ISTP", "stats": [70, 90, 70, 60, 80]},
    "ESFJ": {"name": "럭키", "emoji": "🌸", "desc": "천사 같은 마음씨로 사람들을 보살피고 돕는 것을 가장 큰 기쁨으로 여겨요.", "match": "ISFP", "stats": [100, 30, 60, 70, 50]},
    "ENFJ": {"name": "가디", "emoji": "🐶", "desc": "충성심이 강하고 다정하며, 사람들을 긍정적인 방향으로 이끌어줘요.", "match": "INFP", "stats": [70, 80, 60, 70, 70]},
    "ENTJ": {"name": "루카리오", "emoji": "🐺", "desc": "카리스마가 넘치고 결단력이 있으며, 어떤 어려움도 당당히 뚫고 나갑니다.", "match": "INTP", "stats": [70, 90, 60, 80, 90]}
}

# 레이더 차트 그리기 함수
def draw_radar_chart(stats):
    categories = ['체력(HP)', '공격력(E/I)', '방어력(S/N)', '특수공격(T/F)', '스피드(J/P)']
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=stats + [stats[0]], # 폐곡선을 위해 첫 값 추가
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(255, 204, 0, 0.5)',
        line=dict(color='#E3350D', width=2)
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

# 사이드바 네비게이션
st.sidebar.title("메뉴 📜")
menu = st.sidebar.radio("이동할 메뉴를 선택하세요:", ["🏠 홈", "🧪 MBTI 진단하기", "📖 전체 포켓몬 도감"])

if menu == "🏠 홈":
    st.title("MBTI 포켓몬 도감 🔍")
    st.markdown("<p style='text-align: center; font-size: 1.2em;'>나의 성격은 어떤 포켓몬과 닮았을까?<br>지금 바로 진단해보고 도감을 채워보세요!</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("진단 시작하기 🚀"):
            st.session_state.menu_override = "🧪 MBTI 진단하기"
            st.rerun()
    with col2:
        if st.button("도감 구경하기 📚"):
            st.session_state.menu_override = "📖 전체 포켓몬 도감"
            st.rerun()
            
elif menu == "🧪 MBTI 진단하기" or st.session_state.get('menu_override') == "🧪 MBTI 진단하기":
    st.session_state.menu_override = None
    st.title("🧪 성격 진단 테스트")
    
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.mbti_result = ""
        
    questions = [
        {"q": "주말이 다가왔습니다! 당신의 선택은?", "a": ("친구들과 신나게 놀러 간다! (E)", "E"), "b": ("집에서 뒹굴거리며 쉰다. (I)", "I")},
        {"q": "새로운 게임을 시작할 때 당신은?", "a": ("일단 튜토리얼부터 꼼꼼히 읽어본다. (S)", "S"), "b": ("감으로 부딪히며 배운다. (N)", "N")},
        {"q": "친구가 '나 우울해서 화분 샀어'라고 한다면?", "a": ("무슨 화분 샀어? 물은 얼마나 줘? (T)", "T"), "b": ("왜 우울해? 무슨 일 있었어? (F)", "F")},
        {"q": "여행을 떠나기 전날 밤, 당신은?", "a": ("시간별로 계획을 짜고 짐을 다 싸뒀다. (J)", "J"), "b": ("내일 아침에 싸면 되지~ 하고 잔다. (P)", "P")}
    ]
    
    if st.session_state.step < 4:
        q = questions[st.session_state.step]
        st.markdown(f"### Q{st.session_state.step + 1}. {q['q']}")
        
        if st.button(q['a'][0]):
            st.session_state.mbti_result += q['a'][1]
            st.session_state.step += 1
            st.rerun()
            
        if st.button(q['b'][0]):
            st.session_state.mbti_result += q['b'][1]
            st.session_state.step += 1
            st.rerun()
            
        st.progress((st.session_state.step) / 4)
        
    else:
        mbti = st.session_state.mbti_result
        data = pokemon_data[mbti]
        
        st.markdown(f"<h2 style='color:#3366B5;'>당신의 포켓몬은...</h2>", unsafe_allow_html=True)
        
        st.markdown(f'''
        <div class="pokemon-card">
            <div class="emoji-large">{data['emoji']}</div>
            <div class="pokemon-name">{mbti} {data['name']}</div>
            <div class="desc-text">{data['desc']}</div>
            <div class="match-box">💖 찰떡 궁합: {data['match']}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("### 📊 능력치 분석")
        st.plotly_chart(draw_radar_chart(data['stats']), use_container_width=True)
        
        if st.button("다시 테스트하기 🔄"):
            st.session_state.step = 0
            st.session_state.mbti_result = ""
            st.rerun()

elif menu == "📖 전체 포켓몬 도감" or st.session_state.get('menu_override') == "📖 전체 포켓몬 도감":
    st.session_state.menu_override = None
    st.title("📖 포켓몬 MBTI 도감")
    
    mbti_list = list(pokemon_data.keys())
    cols = st.columns(4)
    
    for i, mbti in enumerate(mbti_list):
        with cols[i % 4]:
            data = pokemon_data[mbti]
            if st.button(f"{data['emoji']} {mbti}", key=f"btn_{mbti}"):
                st.session_state.selected_pokedex = mbti
                
    if 'selected_pokedex' in st.session_state:
        mbti = st.session_state.selected_pokedex
        data = pokemon_data[mbti]
        st.markdown("---")
        st.markdown(f"### {mbti} 상세 정보")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f'''
            <div class="pokemon-card" style="margin-top: 0;">
                <div class="emoji-large" style="font-size: 80px;">{data['emoji']}</div>
                <div class="pokemon-name">{data['name']}</div>
                <div class="desc-text" style="font-size: 14px;">{data['desc']}</div>
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.plotly_chart(draw_radar_chart(data['stats']), use_container_width=True)
