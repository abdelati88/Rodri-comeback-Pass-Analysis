# ⚽ Football Analytics Dashboard: Rodri vs Sunderland

An interactive data visualization tool built with **Python** and **Streamlit** to analyze player performance, focusing on passing networks and spatial dominance.

## 📊 Project Overview
This dashboard provides a tactical breakdown of **Rodri's** performance in the match against Sunderland. It transforms raw event data into actionable insights using advanced visualization techniques.

**Live Demo:** [Click Here to View App] https://rodri-comeback-pass-analysis88.streamlit.app/

## 🛠 Tech Stack
* **Python:** Core logic and data processing.
* **Streamlit:** Web framework for the interactive UI.
* **Mplsoccer:** Drawing state-of-the-art football pitches and heatmaps.
* **Pandas & NumPy:** Data manipulation and Pythagorean calculations for pass distances.
* **Matplotlib:** Underlying plotting library.

## 🚀 Key Features

### 1. Progressive Pass Logic
Calculates "Progressive Passes" based on specific rules:
* **Defensive Half:** Must move the ball at least **15m** towards the goal.
* **Attacking Half:** Must move the ball at least **10m** towards the goal.
* **Box Entries:** Any pass into the penalty box is automatically progressive.

### 2. Visualization Modes
* **Pass Map:** Displays pass trajectories (Successful vs. Progressive) with directional arrows.
* **Zone Heatmap:** A grid-based heatmap showing player activity density across different pitch zones.

### 3. Dynamic Filtering
* Filter by pass outcome (Successful, Unsuccessful, Progressive).
* Toggle between different visualization modes.

## 📂 How to Run Locally

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YourUsername/Rodri-Analytics-Dashboard.git](https://github.com/YourUsername/Rodri-Analytics-Dashboard.git)
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    streamlit run app.py
    ```

---
*Created by [Your Name]*
