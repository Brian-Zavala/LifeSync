import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random
import base64

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
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
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

    .st-bv {
        color: #ffffff;
    }

    .st-cx {
        background-color: rgba(255, 255, 255, 0.1);
        border: none;
        color: #ffffff;
    }

    .st-bz {
        color: #ffffff;
    }

    .st-hq {
        background-color: #7e57c2;
        color: #ffffff;
    }
    /* Animated sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            45deg,
            rgba(72, 52, 212, 0.7),
            rgba(48, 51, 107, 0.7),
            rgba(95, 39, 205, 0.7),
            rgba(87, 75, 144, 0.7)
        ) !important;
        background-size: 400% 400% !important;
        animation: gradientShift 15s ease infinite !important;
    }

    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    /* Ensure text visibility in sidebar widgets */
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stSelectbox select,
    [data-testid="stSidebar"] .stDateInput input {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* Style for placeholder text */
    [data-testid="stSidebar"] .stTextInput input::placeholder,
    [data-testid="stSidebar"] .stSelectbox select::placeholder,
    [data-testid="stSidebar"] .stDateInput input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    /* Ensure dropdown options are visible */
    [data-testid="stSidebar"] .stSelectbox option {
        background-color: #2c3e50;
        color: #ffffff;
    }

    /* Style for labels */
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* Particle effect container */
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

    /* Ensure sidebar content is above particles */
    [data-testid="stSidebar"] > div {
        position: relative;
        z-index: 1;
    }

    /* Improved spacing for sidebar widgets */
    .sidebar .element-container {
        margin-bottom: 20px !important;
    }

    .sidebar .stSelectbox, .sidebar .stTextInput, .sidebar .stDateInput {
        margin-bottom: 10px !important;
    }

    .sidebar .stForm {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
    }

    .sidebar .stForm > div {
        margin-bottom: 15px !important;
    }

    .sidebar-title {
        animation: pulse-sidebar 2s infinite;
        border-radius: 10px;
        padding: 10px;
        display: inline-block;
    }

    /* Pulse effect for Productivity Insights */
    @keyframes pulse-insights {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }

    .insights-title {
        animation: pulse-insights 3s ease-in-out infinite;
        display: inline-block;
    }

    /* Animated gauge styles */
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

    /* Improved spacing for sidebar widgets */
    .sidebar .element-container {
        margin-bottom: 20px !important;
    }

    .sidebar .stSelectbox, .sidebar .stTextInput, .sidebar .stDateInput {
        margin-bottom: 10px !important;
    }

    .sidebar .stForm {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
    }

    .sidebar .stForm > div {
        margin-bottom: 15px !important;
    }
[data-testid="stSidebar"] .element-container,
[data-testid="stSidebar"] .stTextInput,
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stDateInput {
    margin-bottom: 20px !important;
}

[data-testid="stSidebar"] .stForm > div {
    margin-bottom: 20px !important;
}

[data-testid="stSidebar"] .stForm {
    padding: 20px !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
}

        /* Animated sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            45deg,
            rgba(76, 175, 80, 0.7),  /* Green */
            rgba(33, 150, 243, 0.7)  /* Blue */
        ) !important;
        background-size: 200% 200% !important;
        animation: gradientShift 15s ease infinite !important;
    }

    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    /* Glowing effect for sidebar elements */
    [data-testid="stSidebar"] .element-container {
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

    /* Ensure text visibility in sidebar widgets */
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stSelectbox select,
    [data-testid="stSidebar"] .stDateInput input {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* Style for placeholder text */
    [data-testid="stSidebar"] .stTextInput input::placeholder,
    [data-testid="stSidebar"] .stSelectbox select::placeholder,
    [data-testid="stSidebar"] .stDateInput input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    /* Ensure dropdown options are visible */
    [data-testid="stSidebar"] .stSelectbox option {
        background-color: #2c3e50;
        color: #ffffff;
    }

    /* Style for labels */
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* Particle effect container */
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

    /* Ensure sidebar content is above particles */
    [data-testid="stSidebar"] > div {
        position: relative;
        z-index: 1;
    }

    /* Pulsating effect for the "Quick Add Task" button */
    [data-testid="stSidebar"] .stButton > button {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(255, 255, 255, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
        }
    }
    /* Improved layout for filter widgets */
    .filter-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 20px;
    }

    .filter-item {
        flex: 1 1 200px;
    }
    /* Hide Streamlit Toolbar */
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
            const rgb = bgColor.match(/\d+/g).map(Number);
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

# Create placeholders for dynamic content
task_list_placeholder = st.empty()
gauge_placeholder = st.empty()
pie_chart_placeholder = st.empty()
rewards_placeholder = st.empty()

# Helper Functions

def add_task(task, due_date, priority, category):
    if task.strip():
        new_task = {
            "task": task,
            "due_date": due_date,
            "priority": priority,
            "category": category,
            "created_at": datetime.now(),
            "id": base64.b64encode(task.encode()).decode()
        }
        st.session_state.tasks.append(new_task)
        st.success(f"Task '{task}' added successfully!")
        update_completion_rate()
        return True
    return False


def complete_task(task_id):
    task_index = next((index for (index, d) in enumerate(st.session_state.tasks) if d["id"] == task_id), None)
    if task_index is not None:
        completed_task = st.session_state.tasks.pop(task_index)
        completed_task['completed_at'] = datetime.now()
        st.session_state.completed_tasks.append(completed_task)
        update_streak()
        award_points(completed_task['priority'])
        update_completion_rate()


def update_streak():
    today = datetime.now().date()
    if st.session_state.last_completed == today - timedelta(days=1):
        st.session_state.streaks += 1
    elif st.session_state.last_completed != today:
        st.session_state.streaks = 1
    st.session_state.last_completed = today


def award_points(priority):
    points = {"Low": 5, "Medium": 10, "High": 15}
    st.session_state.user_points += points[priority]


def get_motivation_quote():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson"
    ]
    return random.choice(quotes)


def update_completion_rate():
    total_tasks = len(st.session_state.tasks) + len(st.session_state.completed_tasks)
    st.session_state.completion_rate = (
                len(st.session_state.completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0


def update_task_list():
    with task_list_placeholder.container():
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
                            st.rerun()
                    with col_task:
                        st.markdown(f"**{task['task']}**")
                    with col_due:
                        due_date = task.get('due_date', 'Not set')
                        st.write(
                            f"Due: {due_date.strftime('%Y-%m-%d') if isinstance(due_date, datetime) else due_date}")
                    with col_priority:
                        priority = task.get('priority', 'Medium')
                        priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                        st.write(f"{priority_color.get(priority, '⚪')} {priority}")
                    with col_category:
                        category = task.get('category', 'Uncategorized')
                        st.write(f"📁 {category}")


def update_gauge():
    gauge_placeholder.markdown(f"""
    <div class="gauge-container">
        <div class="gauge-bg"></div>
        <div class="gauge-fill" style="transform: rotate({180 - st.session_state.completion_rate * 1.8}deg);"></div>
        <div class="gauge-cover"></div>
        <div class="gauge-percentage">{st.session_state.completion_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)


def update_pie_chart():
    with pie_chart_placeholder.container():
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


def update_rewards():
    with rewards_placeholder.container():
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
                        st.success(f"You've redeemed {reward['name']}!")
                    else:
                        st.error("Not enough points!")


# Main app layout
def main():
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
                    st.rerun()

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📋 Dashboard")

        # Task filters
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)

        # Initialize filter states if they don't exist
        if 'filter_category' not in st.session_state:
            st.session_state.filter_category = []
        if 'filter_priority' not in st.session_state:
            st.session_state.filter_priority = []
        if 'filter_due' not in st.session_state:
            st.session_state.filter_due = None

        # Category filter
        st.session_state.filter_category = st.multiselect(
            "Filter by Category",
            options=st.session_state.categories,
            default=st.session_state.filter_category
        )

        # Priority filter
        st.session_state.filter_priority = st.multiselect(
            "Filter by Priority",
            options=["Low", "Medium", "High"],
            default=st.session_state.filter_priority
        )

        # Due date filter
        st.session_state.filter_due = st.date_input(
            "Filter by Due Date",
            value=st.session_state.filter_due
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
                            st.rerun()
                    with col_task:
                        st.markdown(f"**{task['task']}**")
                    with col_due:
                        due_date = task.get('due_date', 'Not set')
                        st.write(
                            f"Due: {due_date.strftime('%Y-%m-%d') if isinstance(due_date, datetime) else due_date}")
                    with col_priority:
                        priority = task.get('priority', 'Medium')
                        priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                        st.write(f"{priority_color.get(priority, '⚪')} {priority}")
                    with col_category:
                        category = task.get('category', 'Uncategorized')
                        st.write(f"📁 {category}")

    with col2:
        st.markdown('<h2 class="insights-title">📊 Productivity Insights</h2>', unsafe_allow_html=True)

        # Task completion rate
        st.markdown(f"""
        <div class="gauge-container">
            <div class="gauge-bg"></div>
            <div class="gauge-fill" style="transform: rotate({180 - st.session_state.completion_rate * 1.8}deg);"></div>
            <div class="gauge-cover"></div>
            <div class="gauge-percentage">{st.session_state.completion_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

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
                        st.success(f"You've redeemed {reward['name']}!")
                    else:
                        st.error("Not enough points!")


if __name__ == "__main__":
    main()