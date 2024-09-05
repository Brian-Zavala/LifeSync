import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, date
import random
import time
import json
import os
from dateutil import parser

# ===== Page Configuration =====
st.set_page_config(page_title="LifeSync", page_icon="🌟", layout="wide", initial_sidebar_state="expanded")

# ===== Custom CSS =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }

    .dynamic-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        position: relative;
        overflow: hidden;
    }

    .dynamic-title span {
        display: inline-block;
        opacity: 0;
        transform: translateY(1em);
        transition: opacity 0.8s, transform 0.8s;
    }

    .dynamic-title::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to bottom right,
            rgba(255, 255, 255, 0) 0%,
            rgba(255, 255, 255, 0.1) 50%,
            rgba(255, 255, 255, 0) 100%
        );
        animation: rotate 10s linear infinite;
    }

    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .st-bw {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    .st-emotion-cache-16txtl3 {
        padding: 1.5rem;
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }

    .st-emotion-cache-16txtl3:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.45);
    }

    .task-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }

    .task-card:hover {
        background-color: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }

    .reward-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        backdrop-filter: blur(5px);
        text-align: center;
        transition: all 0.3s ease;
    }

    .reward-card:hover {
        background-color: rgba(255, 255, 255, 0.2);
        transform: scale(1.05);
    }

    .st-bv, .st-bz {
        color: #ffffff;
    }

    .st-cx {
        background-color: rgba(255, 255, 255, 0.1);
        border: none;
        color: #ffffff;
    }

    .st-hq {
        background-color: #7e57c2;
        color: #ffffff;
    }

    /* Sidebar styles */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            45deg,
            rgba(76, 175, 80, 0.95),
            rgba(33, 150, 243, 0.95)
        ) !important;
        background-size: 200% 200% !important;
        animation: gradientShift 15s ease infinite !important;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    [data-testid="stSidebar"] .element-container {
        margin-bottom: 20px !important;
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
    }

    [data-testid="stSidebar"] .element-container:hover {
        transform: translateY(-5px);
    }

    [data-testid="stSidebar"] .element-container::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #4CAF50, #2196F3);
        z-index: -1;
        filter: blur(10px);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    [data-testid="stSidebar"] .element-container:hover::before {
        opacity: 1;
    }
    /* Glowing animated input styles for sidebar */
  @keyframes glowing {
    0% { background-position: 0 0; }
    50% { background-position: 400% 0; }
    100% { background-position: 0 0; }
  }

  [data-testid="stSidebar"] .stTextInput input,
  [data-testid="stSidebar"] .stDateInput input {
    color: #000000 !important;
    background: linear-gradient(90deg, #ff00ff, #088F8F, #00ffff, #ff00ff);
    background-size: 400% 400%;
    border: none !important;
    border-radius: 5px;
    padding: 5px 15px;
    transition: all 120s ease;
    animation: glowing 90s ease infinite;
  }

  [data-testid="stSidebar"] .stTextInput input::placeholder,
  [data-testid="stSidebar"] .stDateInput input::placeholder {
    color: rgba(0, 0, 0, 0.7) !important;
  }

  [data-testid="stSidebar"] .stTextInput input:focus,
  [data-testid="stSidebar"] .stDateInput input:focus {
    outline: none;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
  }

  /* Style for priority and category selectboxes */
  [data-testid="stSidebar"] div[data-baseweb="select"] {
    background: linear-gradient(90deg, #ff00ff, #088F8F, #00ffff, #ff00ff);
    background-size: 400% 400%;
    border: none !important;
    border-radius: 5px;
    padding: 10px 15px;
    transition: all 120s ease;
    animation: glowing 90s ease infinite;
  }

  [data-testid="stSidebar"] div[data-baseweb="select"] div[role="button"] {
    color: #000000 !important;
  }

  [data-testid="stSidebar"] div[data-baseweb="select"] div[role="button"]::placeholder {
    color: rgba(0, 0, 0, 0.7) !important;
  }

  [data-testid="stSidebar"] div[data-baseweb="select"] div[role="button"]:focus {
    outline: none;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
  }

  /* Style for dropdown options */
  [data-testid="stSidebar"] div[data-baseweb="select"] ul {
    background: linear-gradient(90deg, #ff00ff, #088F8F, #00ffff, #ff00ff);
    background-size: 400% 400%;
    border: none !important;
    border-radius: 5px;
    padding: 10px 15px;
    transition: all 120s ease;
    animation: glowing 90s ease infinite;
  }

  [data-testid="stSidebar"] div[data-baseweb="select"] ul li {
    color: #000000;
  }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 255, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
    }

    /* Particle effect */
    [data-testid="stSidebar"] .particles {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 0;
    }

    [data-testid="stSidebar"] .particle {
        position: absolute;
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        pointer-events: none;
    }

    [data-testid="stSidebar"] > div {
        position: relative;
        z-index: 1;
    }

    /* Insights and sidebar title effects */
    .insights-title {
        animation: pulse-insights 3s ease-in-out infinite;
        display: inline-block;
    }

    @keyframes pulse-insights {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .sidebar-title {
        animation: pulse-sidebar 2s infinite;
        border-radius: 10px;
        padding: 10px;
        display: inline-block;
    }

    @keyframes pulse-sidebar {
        0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 255, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
    }

    /* Gauge styles */
    .gauge-container {
        position: relative;
        width: 200px;
        height: 100px;
        margin: 0 auto;
        overflow: hidden;
    }

    .gauge-bg {
        width: 200px;
        height: 100px;
        background: conic-gradient(from 180deg, #4CAF50 0deg, #2196F3 180deg, #9E9E9E 360deg);
        border-radius: 100px 100px 0 0;
    }

    .gauge-fill {
        position: absolute;
        top: 0;
        left: 0;
        width: 200px;
        height: 100px;
        background: #9E9E9E;
        border-radius: 100px 100px 0 0;
        transform-origin: center bottom;
        transition: transform 1s ease-out;
    }

    .gauge-cover {
        position: absolute;
        top: 10px;
        left: 10px;
        width: 180px;
        height: 90px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 90px 90px 0 0;
        backdrop-filter: blur(5px);
    }

    .gauge-percentage {
        position: absolute;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: white;
    }

    /* Filter container */
    .filter-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 20px;
    }

    .filter-item {
        flex: 1 1 200px;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: ;}
    footer {visibility: hidden;}
    header {visibility: ;}
</style>
""", unsafe_allow_html=True)

# Add custom dynamic title and particle effect
st.markdown("""
<script>
    function createParticles() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;

        let particlesContainer = sidebar.querySelector('.particles');
        if (!particlesContainer) {
            particlesContainer = document.createElement('div');
            particlesContainer.className = 'particles';
            sidebar.appendChild(particlesContainer);
        }

        // Clear existing particles
        particlesContainer.innerHTML = '';

        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.width = Math.random() * 4 + 'px';
            particle.style.height = particle.style.width;
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDuration = Math.random() * 3 + 2 + 's';
            particle.style.animationDelay = Math.random() * 5 + 's';
            particlesContainer.appendChild(particle);
        }
    }

    function adjustTextColor() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;

        const inputs = sidebar.querySelectorAll('input, select');
        inputs.forEach(input => {
            const bgColor = window.getComputedStyle(input).backgroundColor;
            const rgb = bgColor.match(/d+/g).map(Number);
            const brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000;
            input.style.color = brightness > 125 ? 'black' : 'white';
        });
    }

    // Run on load and whenever the DOM changes
    document.addEventListener('DOMContentLoaded', () => {
        createParticles();
        adjustTextColor();
    });
    const observer = new MutationObserver(() => {
        createParticles();
        adjustTextColor();
    });
    observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)
# Your LifeSync title
st.markdown('<h1 class="dynamic-title">LifeSync</h1>', unsafe_allow_html=True)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = []
if 'streaks' not in st.session_state:
    st.session_state.streaks = 0
if 'last_completed' not in st.session_state:
    st.session_state.last_completed = None
if 'categories' not in st.session_state:
    st.session_state.categories = ['Work', 'Personal', 'Shopping', 'Health', 'Finance']
if 'rewards' not in st.session_state:
    st.session_state.rewards = [
        {'name': 'Coffee Break', 'points': 10},
        {'name': '15min Social Media', 'points': 20},
        {'name': 'Netflix Episode', 'points': 50},
        {'name': 'Treat Yourself', 'points': 100}
    ]
if 'user_points' not in st.session_state:
    st.session_state.user_points = 0
if 'completion_rate' not in st.session_state:
    st.session_state.completion_rate = 0


# Custom JSON Encoder to handle date objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def get_data_dir():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create a 'data' directory in the same location as the script
    data_dir = os.path.join(script_dir, 'data')
    # Create the directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def save_app_data():
    data = {
        "tasks": st.session_state.tasks,
        "completed_tasks": st.session_state.completed_tasks,
        "streaks": st.session_state.streaks,
        "last_completed": st.session_state.last_completed,
        "categories": st.session_state.categories,
        "rewards": st.session_state.rewards,
        "user_points": st.session_state.user_points,
        "completion_rate": st.session_state.completion_rate,
        "filter_category": st.session_state.filter_category,
        "filter_priority": st.session_state.filter_priority,
        "filter_due": st.session_state.filter_due
    }
    file_path = os.path.join(get_data_dir(), "app_data.json")
    with open(file_path, "w") as file:
        json.dump(data, file, cls=CustomJSONEncoder)
    print(f"Data saved to: {file_path}")


# Function to load all app data
def load_app_data():
    file_path = os.path.join(get_data_dir(), "app_data.json")
    try:
        with open(file_path, "r") as file:
            content = file.read().strip()
            if content:  # Check if the file is not empty
                data = json.loads(content)
                # ... (existing code to load other data)

                # Initialize filter states
                st.session_state.filter_category = data.get("filter_category", [])
                st.session_state.filter_priority = data.get("filter_priority", [])
                st.session_state.filter_due = parser.parse(data.get("filter_due")).date() if data.get(
                    "filter_due") else None
            else:
                print(f"The file at {file_path} is empty. Initializing with default values.")
                initialize_default_values()
    except FileNotFoundError:
        print(f"No existing data file found at {file_path}. Starting with default values.")
        initialize_default_values()
    except json.JSONDecodeError:
        print(f"Invalid JSON in {file_path}. Starting with default values.")
        initialize_default_values()


def initialize_default_values():
    st.session_state.tasks = []
    st.session_state.completed_tasks = []
    st.session_state.streaks = 0
    st.session_state.last_completed = None
    st.session_state.categories = ['Work', 'Personal', 'Shopping', 'Health', 'Finance']
    st.session_state.rewards = [
        {'name': 'Coffee Break', 'points': 10},
        {'name': '15min Social Media', 'points': 20},
        {'name': 'Netflix Episode', 'points': 50},
        {'name': 'Treat Yourself', 'points': 100}
    ]
    st.session_state.user_points = 0
    st.session_state.completion_rate = 0
    st.session_state.filter_category = []
    st.session_state.filter_priority = []
    st.session_state.filter_due = None


# Load app data at the start
load_app_data()

# Create placeholders for dynamic content
task_list_placeholder = st.empty()
gauge_placeholder = st.empty()
pie_chart_placeholder = st.empty()
rewards_placeholder = st.empty()


# Helper Functions


def add_task(task, due_date, priority, category):
    if task.strip():
        # Generate a unique ID using timestamp and random number
        unique_id = f"{int(time.time())}_{random.randint(1000, 9999)}"
        new_task = {
            "task": task,
            "due_date": due_date,
            "priority": priority,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "id": unique_id
        }
        st.session_state.tasks.append(new_task)
        save_app_data()
        st.success(f"Task '{task}' added successfully!")
        update_completion_rate()
        return True
    return False


def complete_task(task_id):
    task_index = next((index for (index, d) in enumerate(st.session_state.tasks) if d["id"] == task_id), None)
    if task_index is not None:
        completed_task = st.session_state.tasks.pop(task_index)
        completed_task["completed_at"] = datetime.now().isoformat()
        st.session_state.completed_tasks.append(completed_task)
        save_app_data()
        update_streak()
        award_points(completed_task["priority"])
        update_completion_rate()


def update_streak():
    today = datetime.now().date()
    if st.session_state.last_completed == today - timedelta(days=1):
        st.session_state.streaks += 1
    elif st.session_state.last_completed != today:
        st.session_state.streaks = 1
    st.session_state.last_completed = today
    save_app_data()


def award_points(priority):
    points = {"Low": 5, "Medium": 10, "High": 15}
    st.session_state.user_points += points[priority]
    save_app_data()


def get_motivation_quote():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson"
    ]
    return random.choice(quotes)


def update_gauge():
    gauge_placeholder.markdown(f"""
    <div class="gauge-container">
        <div class="gauge-bg"></div>
        <div class="gauge-fill" style="transform: rotate({180 - st.session_state.completion_rate * 1.8}deg);"></div>
        <div class="gauge-cover"></div>
        <div class="gauge-percentage">{st.session_state.completion_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)


def update_completion_rate():
    total_tasks = len(st.session_state.tasks) + len(st.session_state.completed_tasks)
    st.session_state.completion_rate = (
            len(st.session_state.completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
    save_app_data()
    update_gauge()


# Main app layout
def main():
    load_app_data()
    update_completion_rate()
    # Sidebar
    with st.sidebar:
        st.markdown('<h2 class="sidebar-title">LifeSync Central</h2>', unsafe_allow_html=True)

        # User stats
        user_stats_col1, user_stats_col2 = st.columns(2)
        with user_stats_col1:
            st.metric("🏆 Streak", f"{st.session_state.streaks} days")
        with user_stats_col2:
            st.metric("💎 Points", st.session_state.user_points)

        # Motivation
        st.subheader("💪 Daily Inspiration")
        st.info(get_motivation_quote())

        # Quick Add Task
        st.subheader("⚡ Quick Add Task")
        with st.form(key="quick_add_form"):
            task = st.text_input("Task")
            due_date = st.date_input("Due Date")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            category = st.selectbox("Category", st.session_state.categories)

            submitted = st.form_submit_button("Add Task")
            if submitted:
                if add_task(task, due_date, priority, category):
                    update_gauge()

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📋 Dashboard")

        # Task filters
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.session_state.filter_category = st.multiselect(
            "Filter by Category",
            options=st.session_state.categories,
            default=st.session_state.get('filter_category', [])
        )
        st.session_state.filter_priority = st.multiselect(
            "Filter by Priority",
            options=["Low", "Medium", "High"],
            default=st.session_state.get('filter_priority', [])
        )
        st.session_state.filter_due = st.date_input(
            "Filter by Due Date",
            value=st.session_state.get('filter_due')
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Display tasks
        for task in st.session_state.tasks:
            if (not st.session_state.filter_category or task.get('category',
                                                                 'Uncategorized') in st.session_state.filter_category) and \
                    (not st.session_state.filter_priority or task.get('priority',
                                                                      'Medium') in st.session_state.filter_priority) and \
                    (not st.session_state.filter_due or task.get('due_date') == st.session_state.filter_due):
                with st.container():
                    col_check, col_task, col_due, col_priority, col_category = st.columns([0.1, 2, 1, 1, 1])
                    with col_check:
                        if st.checkbox("", key=f"task_{task['id']}", on_change=complete_task, args=(task['id'],)):
                            update_gauge()
                    with col_task:
                        st.markdown(f"**{task['task']}**")
                    with col_due:
                        due_date = task.get('due_date', 'Not set')
                        st.write(f"Due: {due_date.strftime('%Y-%m-%d') if isinstance(due_date, date) else due_date}")
                    with col_priority:
                        priority = task.get('priority', 'Medium')
                        priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                        st.write(f"{priority_color.get(priority, '⚪')} {priority}")
                    with col_category:
                        category = task.get('category', 'Uncategorized')
                        st.write(f"📁 {category}")

    with col2:
        update_gauge()

        st.markdown('<h2 class="insights-title">📊 Productivity</h2>', unsafe_allow_html=True)

        # Task distribution by category
        if st.session_state.tasks:
            try:
                df = pd.DataFrame(st.session_state.tasks)
                df['category'] = df['category'].fillna('Uncategorized')
                category_counts = df.groupby('category').size().reset_index(name='count')
                fig_pie = px.pie(category_counts, values='count', names='category',
                                 title='Task Distribution by Category')
                fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white", 'family': "Arial"})
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            except Exception as e:
                st.error(f"An error occurred while creating the category distribution chart: {str(e)}")
        else:
            st.info("Add some tasks to see your task distribution!")

        # Rewards section
        st.subheader("🎁 Rewards Center")
        st.write(f"You have {st.session_state.user_points} points to spend!")
        for reward in st.session_state.rewards:
            col1, col2, col3 = st.columns([1.8, 0.8, 1.4])
            with col1:
                st.write(reward['name'])
            with col2:
                st.write(f"{reward['points']} points")
            with col3:
                if st.button("Redeem", key=f"redeem_{reward['name']}"):
                    if st.session_state.user_points >= reward['points']:
                        st.session_state.user_points -= reward['points']
                        save_app_data()
                        st.success(f"You've redeemed {reward['name']}!")
                    else:
                        st.error("Not enough points!")
    save_app_data()


if __name__ == "__main__":
    main()
