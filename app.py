import streamlit as st
import chess, chess.svg, random, time
from streamlit.components.v1 import html

st.set_page_config(page_title='Pocket Chess Coach', layout='wide')

if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
if 'history' not in st.session_state:
    st.session_state.history = []
if 'white_time' not in st.session_state:
    st.session_state.white_time = 300
if 'black_time' not in st.session_state:
    st.session_state.black_time = 300
if 'last_tick' not in st.session_state:
    st.session_state.last_tick = time.time()
if 'timed' not in st.session_state:
    st.session_state.timed = False

st.title('♟️ Pocket Chess Coach')

with st.sidebar:
    st.header('Game Options')
    theme = st.selectbox('Board Theme', ['brown','green','blue','gray'])
    minutes = st.selectbox('Timer (minutes)', [1,3,5,10], index=2)
    if st.button('New Timed Game'):
        st.session_state.board = chess.Board()
        st.session_state.history=[]
        st.session_state.white_time=minutes*60
        st.session_state.black_time=minutes*60
        st.session_state.timed=True
    if st.button('New Casual Game'):
        st.session_state.board = chess.Board()
        st.session_state.history=[]
        st.session_state.timed=False
    if st.button('Resign'):
        st.warning('You resigned. Start a new game anytime.')
        st.session_state.board = chess.Board()
        st.session_state.history=[]

board = st.session_state.board
colors = {'brown':'#b58863','green':'#769656','blue':'#6b8fb3','gray':'#888888'}
svg = chess.svg.board(board=board, size=520, colors={'square dark': colors[theme]})
html(svg, height=540)

if st.session_state.timed and not board.is_game_over():
    now = time.time()
    diff = int(now - st.session_state.last_tick)
    if diff > 0:
        if board.turn == chess.WHITE:
            st.session_state.white_time -= diff
        else:
            st.session_state.black_time -= diff
        st.session_state.last_tick = now

col1,col2 = st.columns(2)
col1.metric('White Time', f"{max(0,st.session_state.white_time)//60}:{max(0,st.session_state.white_time)%60:02d}")
col2.metric('Black Time', f"{max(0,st.session_state.black_time)//60}:{max(0,st.session_state.black_time)%60:02d}")

move = st.text_input('Enter move in UCI format (e2e4)')
if st.button('Play Move'):
    try:
        m = chess.Move.from_uci(move.strip())
        if m in board.legal_moves:
            san = board.san(m)
            board.push(m)
            st.session_state.history.append(san)
            # simple bot reply
            if not board.is_game_over():
                bot = random.choice(list(board.legal_moves))
                san2 = board.san(bot)
                board.push(bot)
                st.session_state.history.append(san2)
        else:
            st.error('Illegal move')
    except:
        st.error('Invalid format')

st.subheader('Move History')
st.write(' | '.join(st.session_state.history[-20:]))

st.subheader('Game Summary')
if board.is_checkmate():
    st.success('Checkmate reached.')
elif board.is_stalemate():
    st.info('Stalemate.')
elif board.is_check():
    st.warning('King is in check.')
else:
    st.write('Develop pieces, castle early, control the center.')

st.caption('Tip: use moves like e2e4, g1f3, e7e8q for promotion.')
