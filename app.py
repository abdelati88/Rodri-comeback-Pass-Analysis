import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np

# --------------------------------------------------------
# --------------------------------------------------------
st.set_page_config(page_title="Rodri vs sunderland", layout="wide", page_icon="⚽")

st.markdown("""
<style>
    
    .stApp {
        background-color: #0e1117;
    }
   
    div[data-testid="stMetric"] {
        background-color: #1E1E1E;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
        
       
        height: 130px; 
        display: flex;
        flex-direction: column;
        justify-content: center; 
        align-items: center; 
        text-align: center; 
    }
    div[data-testid="stMetricLabel"] {
        color: #aaaaaa;
        font-size: 14px;
    }
    div[data-testid="stMetricValue"] {
        color: #00ff85; 
        font-size: 26px;
        font-weight: bold;
    }
    
    .dataframe {
        font-size: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# --------------------------------------------------------
@st.cache_data
#@st.cache_data
def load_data():
    try:
        df = pd.read_csv('match_3.csv')
    except FileNotFoundError:
        return None

    cols = ['X', 'Y', 'X2', 'Y2']
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')


    
    goal_x = 0
    goal_y = 40

    df['dist_start'] = np.sqrt((goal_x - df['X'])**2 + (goal_y - df['Y'])**2)
    df['dist_end'] = np.sqrt((goal_x - df['X2'])**2 + (goal_y - df['Y2'])**2)

    df['prog_dist'] = df['dist_start'] - df['dist_end']

  
    df['x_progression'] = df['X'] - df['X2']

    df['is_in_box'] = (df['X2'] <= 18) & (df['Y2'] >= 18) & (df['Y2'] <= 62)

    # ----------------------------------------------------
    # ----------------------------------------------------
    
    
    cond_defensive = df['X'] > 60   
    cond_attacking = df['X'] <= 60  
    
    conditions = [cond_defensive, cond_attacking]
    choices = [15, 10] 
    
    df['required_dist'] = np.select(conditions, choices, default=10)

    # ----------------------------------------------------
    # ----------------------------------------------------
    condition_A = (df['prog_dist'] >= df['required_dist']) & (df['x_progression'] > 5)
    condition_B = df['is_in_box'] == True
    
    df['is_progressive'] = (df['Outcome'] == 'Successful') & (condition_A | condition_B)

    return df
df = load_data()

if df is None:
    st.error("⚠️ not found ")
    st.stop()

# --------------------------------------------------------
# --------------------------------------------------------
st.sidebar.header("Filter Panel ⚙️")

all_players = df['Player'].unique()
#selected_player = st.sidebar.selectbox("Select Player:", all_players)


selected_player = all_players[0]
st.sidebar.markdown(f"### 👤 Player: **{selected_player}**")
player_df = df[df['Player'] == selected_player]

viz_option = st.sidebar.radio("Visualization Mode:", 
                              ["Pass Map (Analysis)", "Heatmap (Zones)"])

pass_filter = st.sidebar.multiselect("Show Passes:", 
                                     ["Normal Pass", "Unsuccessful", "Progressive"],  # غيرنا الاسم هنا
                                     default=["Normal Pass", "Progressive"])
# --------------------------------------------------------
# --------------------------------------------------------
st.title(f"📊 Player Analysis: {selected_player}")
st.markdown("---")


total_passes = len(player_df)
succ_passes = len(player_df[player_df['Outcome'] == 'Successful'])
prog_passes = len(player_df[player_df['is_progressive'] == True])
box_entries = len(player_df[(player_df['is_in_box'] == True) & (player_df['Outcome'] == 'Successful')])

accuracy = (succ_passes / total_passes * 100) if total_passes > 0 else 0
prog_ratio = (prog_passes / succ_passes * 100) if succ_passes > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Passes", total_passes)
col2.metric("Accuracy", f"{accuracy:.1f}%")
col3.metric("Progressive Passes", prog_passes, f"{prog_ratio:.1f}% of Succ.")
col4.metric("Penalty Box Entries", box_entries)

st.markdown("---")

# --------------------------------------------------------
# --------------------------------------------------------
c1, c2 = st.columns([3, 1]) 
with c1:
    st.subheader(f"Pitch View - {viz_option}")
    
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#1b1b1b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(12, 8))

    if viz_option == "Pass Map (Analysis)":
        if "Unsuccessful" in pass_filter:
            fail = player_df[player_df['Outcome'] != 'Successful']
            pitch.lines(fail.X, fail.Y, fail.X2, fail.Y2, ax=ax, color='red', alpha=0.3, label='Failed')
            pitch.scatter(fail.X2, fail.Y2, ax=ax, c='red', s=20, alpha=0.3)

        if "Normal Pass" in pass_filter:
            succ_normal = player_df[(player_df['Outcome'] == 'Successful') & (player_df['is_progressive'] == False)]
            pitch.lines(succ_normal.X, succ_normal.Y, succ_normal.X2, succ_normal.Y2, ax=ax, color='white', alpha=0.1, label='Normal Pass')
        if "Progressive" in pass_filter:
            prog = player_df[player_df['is_progressive'] == True]
            pitch.arrows(prog.X, prog.Y, prog.X2, prog.Y2, ax=ax, width=3, headwidth=4, color='#FFD700', label='Progressive', zorder=2)
            pitch.scatter(prog.X2, prog.Y2, ax=ax, c='white', edgecolors='#FFD700', s=50, zorder=3)

        ax.legend(facecolor='#1b1b1b', edgecolor='white', labelcolor='white', loc='upper left')

    elif viz_option == "Heatmap (Zones)":
        
        kde = pitch.kdeplot(
            player_df.X, 
            player_df.Y, 
            ax=ax, 
            levels=100, 
            shade=True, 
            cmap='hot', 
            alpha=0.7,
            thresh=0.05  
        )
    st.pyplot(fig)

# --------------------------------------------------------
# --------------------------------------------------------
with c2:
    st.subheader("Logic Check 🧐")
    st.write("progression passes:")
    debug_cols = ['X', 'X2', 'prog_dist', 'required_dist', 'is_in_box']
    prog_debug = player_df[player_df['is_progressive'] == True][debug_cols].head(10)
    st.dataframe(prog_debug)
    
    st.info("""
    **Rules Applied:**
    - **Defensive Half:** Must gain **15m**.
    - **Attacking Half:** Must gain **10m**.
    - **Forward Move:** X > 5 units.
    - **Box Entry:** Always Progressive.
    """)
    
    # --------------------------------------------------------
# --------------------------------------------------------
st.markdown("---")
st.subheader("📺 Match Highlights & Analysis")

with st.expander("Show Match Highlights (video)"):
    try:
        video_file = open('rodri_highlights.mp4', 'rb') 
        video_bytes = video_file.read()
        
        col_video, col_text = st.columns([2, 1])
        
        with col_video:
            st.video(video_bytes)
            
        with col_text:
            st.write(" Minute 0:43: Example of a line-breaking progressive pass")
            
    except FileNotFoundError:
        st.warning(" not found ")