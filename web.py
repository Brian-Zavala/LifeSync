import streamlit as st
# ===== Page Configuration =====
st.set_page_config(page_title="LifeSync", page_icon="🌟", layout="wide", initial_sidebar_state="expanded")

import random
import time
import uuid
from typing import List, Dict, Any
from functions import render_task_distribution, create_unique_key
from Database import (
    create_user, load_user_data,
    add_task as db_add_task, complete_task as db_complete_task,
    update_user_stats)
from css import css_styles
from datetime import datetime, timedelta



css_styles()

# ===== Cached Functions =====
@st.cache_data(ttl=3600)
def get_motivation_quote() -> str:
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson"
    ]
    return random.choice(quotes)

@st.cache_data(ttl=3600)
def get_productivity_tips() -> List[str]:
    return [
        "Break large tasks into smaller, manageable steps.",
        "Use the Pomodoro Technique: Work for 25 minutes, then take a 5-minute break.",
        "Prioritize your tasks using the Eisenhower Matrix.",
        "Minimize distractions by turning off notifications during focus time.",
        "Start your day by tackling the most important or challenging task.",
    ]

@st.cache_resource
def get_reward_options() -> List[Dict[str, Any]]:
    return [
        {'name': 'Coffee Break', 'points': 10},
        {'name': '15min Social Media', 'points': 20},
        {'name': 'Netflix Episode', 'points': 50},
        {'name': 'Treat Yourself', 'points': 100}
    ]

@st.cache_data(ttl=60)
def load_cached_user_data(username: str) -> Dict[str, Any]:
    return load_user_data(username)

# ===== Helper Functions =====
def login_user():
    username = st.session_state.username
    user_data = load_user_data(username)
    if user_data:
        st.session_state.user = username
        st.session_state.update(user_data)
    else:
        st.error("User not found. Please create an account.")

def logout_user():
    st.session_state.clear()
    st.session_state.user = None
    st.success("Logged out successfully!")

def register_user():
    username = st.session_state.new_username
    success, message = create_user(username)
    if success:
        st.success(message)
        st.session_state.username = username
        login_user()
    else:
        st.error(message)

@st.cache_data(ttl=60)
def update_completion_bar():
    total_tasks = len(st.session_state.tasks) + len(st.session_state.completed_tasks)
    completion_rate = (len(st.session_state.completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
    st.session_state.completion_rate = completion_rate

    st.markdown(
        f"""
        <script>
        updateCompletionBar({completion_rate});
        </script>
        """,
        unsafe_allow_html=True
    )

def add_task(task: str, due_date: datetime.date, priority: str, category: str) -> bool:
    if task.strip():
        new_task = {
            "task": task,
            "due_date": due_date.isoformat(),
            "priority": priority,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "id": f"{int(datetime.now().timestamp())}_{uuid.uuid4()}"
        }
        st.session_state.tasks.append(new_task)
        db_add_task(st.session_state.user, new_task)
        st.success(f"Task '{task}' added successfully!")
        update_completion_rate()
        return True
    return False

def complete_task(task_id: str) -> bool:
    task = next((t for t in st.session_state.tasks if t['id'] == task_id), None)
    if task:
        st.session_state.tasks.remove(task)
        st.session_state.completed_tasks.append(task)
        update_streak()
        award_points(task['priority'])
        update_completion_rate()
        if db_complete_task(st.session_state.user, task_id):
            st.success(f"Task '{task['task']}' completed successfully!")
            return True
        else:
            st.error("There was an error completing the task in the database.")
    return False


def update_streak():
    today = datetime.now().date()
    last_completed = datetime.fromisoformat(
        st.session_state.last_completed).date() if st.session_state.last_completed else None

    if last_completed == today - timedelta(days=1):
        st.session_state.streaks += 1
    elif last_completed != today:
        st.session_state.streaks = 1

    st.session_state.last_completed = today.isoformat()
    update_user_stats(st.session_state.user, {
        "streaks": st.session_state.streaks,
        "last_completed": st.session_state.last_completed
    })


def award_points(priority: str):
    points = {"Low": 5, "Medium": 10, "High": 15}
    st.session_state.user_points += points[priority]
    update_user_stats(st.session_state.user, {"user_points": st.session_state.user_points})


def update_completion_rate():
    total_tasks = len(st.session_state.tasks) + len(st.session_state.completed_tasks)
    st.session_state.completion_rate = (
            len(st.session_state.completed_tasks) / total_tasks * 100
    ) if total_tasks > 0 else 0
    update_user_stats(st.session_state.user, {"completion_rate": st.session_state.completion_rate})


def handle_task_completion():
    task_id = st.session_state.get('task_to_complete')
    if task_id:
        if complete_task(task_id):
            st.success("Task completed successfully!")
        else:
            st.error("There was an error completing the task.")
        del st.session_state['task_to_complete']
        time.sleep(0.1)  # Small delay to ensure the UI updates
        st.rerun()


# ===== Main App =====
def main():
    # Initialize session state variables
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    if 'completed_tasks' not in st.session_state:
        st.session_state.completed_tasks = []
    if 'categories' not in st.session_state:
        st.session_state.categories = ["Work", "Personal", "Study", "Health", "Other"]
    if 'streaks' not in st.session_state:
        st.session_state.streaks = 0
    if 'user_points' not in st.session_state:
        st.session_state.user_points = 0
    if 'completion_rate' not in st.session_state:
        st.session_state.completion_rate = 0
    if 'last_completed' not in st.session_state:
        st.session_state.last_completed = None
    if 'logout_key' not in st.session_state:
        st.session_state.logout_key = None

    # Update completion bar on page load
    update_completion_bar()

    if not st.session_state.user:
        render_login_page()
    else:
        render_main_app()


def render_login_page():
    st.markdown("""
        <div class="dynamic-title">
            Welcome to LifeSync
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Login")
        st.text_input("Username", key="username")
        st.button("Login", on_click=login_user, key="login_button")
    with col2:
        st.subheader("Register")
        st.text_input("New Username", key="new_username")
        st.button("Register", on_click=register_user, key="register_button")


def render_main_app():
    # Generate a unique key for the logout button if it doesn't exist
    if st.session_state.logout_key is None:
        st.session_state.logout_key = f"logout_{st.session_state.user}_{int(time.time())}"

    render_completion_gauge()
    render_task_input_form()
    render_task_filters()
    render_tasks()
    render_task_distribution()
    render_rewards_section()
    render_sidebar()


def render_completion_gauge():
    completion_rate = st.session_state.completion_rate
    st.markdown(f"""
        <div class="gauge-container">
            <div class="gauge-bg"></div>
            <div class="gauge-fill" style="transform: rotate({completion_rate * 1.8}deg);"></div>
            <div class="gauge-cover"></div>
            <div class="gauge-percentage">{completion_rate:.0f}%</div>
        </div>
    """, unsafe_allow_html=True)


def render_task_input_form():
    with st.form("quick_add_form"):
        task = st.text_input("Task", key="task_input")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            due_date = st.date_input("Due Date", key="due_date_input")
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High"], key="priority_select")
        with col3:
            category = st.selectbox("Category", st.session_state.categories, key="category_select")
        submitted = st.form_submit_button("Add Task")

    if submitted:
        add_task(task, due_date, priority, category)
        update_completion_bar()


def render_task_filters():
    with st.expander("Task Filters", expanded=False):
        filter_category = st.multiselect(
            "Filter by Category",
            options=st.session_state.categories,
            default=[],
            key=create_unique_key("filter_category_multiselect")
        )
        filter_priority = st.multiselect(
            "Filter by Priority",
            options=["Low", "Medium", "High"],
            default=[],
            key=create_unique_key("filter_priority_multiselect")
        )
        filter_due = st.date_input(
            "Filter by Due Date",
            value=None,
            key=create_unique_key("filter_due_date_input")
        )
    return filter_category, filter_priority, filter_due

def render_tasks():
    filter_category, filter_priority, filter_due = render_task_filters()

    for task in st.session_state.tasks:
        if should_display_task(task, filter_category, filter_priority, filter_due):
            render_task(task)


def should_display_task(task, filter_category, filter_priority, filter_due):
    return (not filter_category or task['category'] in filter_category) and \
        (not filter_priority or task['priority'] in filter_priority) and \
        (not filter_due or task['due_date'] == filter_due.isoformat())


def render_task(task):
    with st.container():
        cols = st.columns([0.1, 2, 1, 1, 1])
        with cols[0]:
            if st.checkbox("", key=f"task_checkbox_{task['id']}"):
                complete_task(task['id'])
                update_completion_bar()
                st.rerun()
        with cols[1]:
            st.markdown(f"**{task['task']}**")
        with cols[2]:
            st.write(f"Due: {task['due_date']}")
        with cols[3]:
            priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            st.write(f"{priority_color[task['priority']]} {task['priority']}")
        with cols[4]:
            st.write(f"📁 {task['category']}")


def render_rewards_section():
    st.markdown("""
        <div style='background-color: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; text-align: center;'>
            <h3 class='points-glow'>Reward Center</h3>
        </div>
        <div style='background-color: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; text-align: center;'>
            <h3 class='points-glow'>You have {points} points to spend!</h3>
        </div>
    """.format(points=st.session_state.user_points), unsafe_allow_html=True)

    reward_cols = st.columns(2)
    for idx, reward in enumerate(get_reward_options()):
        with reward_cols[idx % 2]:
            render_reward(reward, idx)


def render_reward(reward, idx):
    with st.container():
        st.markdown(f"""
            <div class='reward-card'>
                <h4>{reward['name']}</h4>
                <p>{reward['points']} points</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Redeem", key=f"redeem_{reward['name']}_{idx}"):
            handle_reward_redemption(reward)


def handle_reward_redemption(reward):
    if st.session_state.user_points >= reward['points']:
        st.session_state.user_points -= reward['points']
        update_user_stats(st.session_state.user, {"user_points": st.session_state.user_points})
        st.success(f"You've redeemed {reward['name']}!")
        st.balloons()
    else:
        st.error("Not enough points!")


def render_sidebar():
    with st.sidebar:
        st.button("Logout", on_click=logout_user, key=st.session_state.logout_key)

        st.markdown('<h3 class="sidebar-glow">LifeSync Stats</h3>', unsafe_allow_html=True)
        st.metric("🏆 Streak", f"{st.session_state.streaks} days")
        st.metric("💎 Points", st.session_state.user_points)

        st.markdown('<h3 class="sidebar-glow">Daily Inspiration</h3>', unsafe_allow_html=True)
        st.info(get_motivation_quote())

        st.markdown('<h3 class="sidebar-glow">Productivity Tips</h3>', unsafe_allow_html=True)
        st.info(random.choice(get_productivity_tips()))


if __name__ == "__main__":
    main()