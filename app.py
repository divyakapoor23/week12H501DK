import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from apputil import update_board


st.set_page_config(page_title="Conway's Game of Life", layout="wide")
st.title("Conway's Game of Life")
st.write(
    "Play with the rules we implemented in `update_board`. "
    "Use the controls to seed a board, step it forward, and watch the pattern evolve."
)


# --- Sidebar configuration ----------------------------------------------------
st.sidebar.header("Board Configuration")
rows = st.sidebar.slider("Rows", min_value=5, max_value=30, value=12)
cols = st.sidebar.slider("Columns", min_value=5, max_value=30, value=12)
live_prob = st.sidebar.slider(
    "Initial live cell probability", min_value=0.0, max_value=1.0, value=0.25, step=0.05
)


def init_board(r: int, c: int, p: float) -> np.ndarray:
    """Create a random binary board with probability p of a live cell."""
    return (np.random.rand(r, c) < p).astype(int)


# --- Session state -----------------------------------------------------------
if "board" not in st.session_state:
    st.session_state.board = init_board(rows, cols, live_prob)
    st.session_state.step = 0


def reset_board():
    st.session_state.board = init_board(rows, cols, live_prob)
    st.session_state.step = 0


def clear_board():
    st.session_state.board = np.zeros((rows, cols), dtype=int)
    st.session_state.step = 0


def advance_board(n: int = 1):
    for _ in range(n):
        st.session_state.board = update_board(st.session_state.board)
        st.session_state.step += 1


# Resize the board if the sliders change
current_shape = st.session_state.board.shape
if current_shape != (rows, cols):
    st.session_state.board = init_board(rows, cols, live_prob)
    st.session_state.step = 0


# --- Controls ----------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Step Once"):
        advance_board(1)
with col2:
    n_steps = st.number_input("Steps to advance", min_value=1, max_value=100, value=5, step=1)
    if st.button("Run Steps"):
        advance_board(int(n_steps))
with col3:
    if st.button("Randomize Board"):
        reset_board()
with col4:
    if st.button("Clear Board"):
        clear_board()


# --- Display -----------------------------------------------------------------
st.markdown(f"**Current Step:** {st.session_state.step}")

fig, ax = plt.subplots(figsize=(6, 6))
sns.heatmap(
    st.session_state.board,
    cmap="plasma",
    cbar=False,
    square=True,
    linewidths=0.5,
    linecolor="white",
    ax=ax,
)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Board State")
st.pyplot(fig)


st.caption(
    "Rules: A live cell survives with 2 neighbors; any cell is born with exactly 3 live neighbors."
)
