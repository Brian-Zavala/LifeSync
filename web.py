import streamlit as st
from datetime import datetime, timedelta
import random
import time
import uuid
from functions import render_task_distribution, render_completion_bar
from Database import (
    create_user, load_user_data,
    add_task as db_add_task, complete_task as db_complete_task,
    update_user_stats)

# ===== Page Configuration =====
st.set_page_config(page_title="LifeSync", page_icon="🌟", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
        box-sizing: border-box;
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
   /* Completion Bar Styles */
.completion-bar-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 15px;
    background-color: rgba(255, 255, 255, 0.2);
    z-index: 1000;
    overflow: hidden;
}

.completion-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
    transition: width 1s ease-in-out;
    position: relative;
}

.completion-bubbles {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.bubble {
    position: absolute;
    background-color: rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
    /* Productivity Gauge Styles */
    .productivity-gauge {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        margin-top: 10px;
    }

    .productivity-gauge h3 {
        color: white;
        margin-bottom: 5px;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .dynamic-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #fff, 0 0 20px #ff00de, 0 0 35px #ff00de, 0 0 40px #ff00de, 0 0 50px #ff00de, 0 0 75px #ff00de;
        }
        to {
            text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #ff00de, 0 0 70px #ff00de, 0 0 80px #ff00de, 0 0 100px #ff00de, 0 0 150px #ff00de;
        }
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
        transition: all 0.3s ease;
    }

    .st-bw:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.45);
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
        animation: fadeIn 0.5s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
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
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .reward-card:hover {
        background-color: rgba(255, 255, 255, 0.2);
        animation: none;
        transform: scale(1.1);
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

    /* Custom checkbox */
    input[type="checkbox"] {
        appearance: none;
        -webkit-appearance: none;
        width: 20px;
        height: 20px;
        border: 2px solid #ffffff;
        border-radius: 50%;
        outline: none;
        transition: all 0.3s ease;
        position: relative;
        cursor: pointer;
    }

    input[type="checkbox"]:checked {
        background-color: #4CAF50;
        border-color: #4CAF50;
    }

    input[type="checkbox"]:checked::before {
        content: '✓';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #ffffff;
        font-size: 14px;
    }

    /* Gauge styles */
    .gauge-container {
        position: relative;
        width: 100px;
        height: 50px;
        margin: 0 auto;
        overflow: hidden;
    }

    .gauge-bg {
        width: 100px;
        height: 50px;
        background: conic-gradient(from 180deg, #4CAF50 0deg, #2196F3 180deg, #9E9E9E 360deg);
        border-radius: 50px 50px 0 0;
    }

    .gauge-fill {
        position: absolute;
        top: 0;
        left: 0;
        width: 100px;
        height: 50px;
        background: #9E9E9E;
        border-radius: 50px 50px 0 0;
        transform-origin: center bottom;
        transition: transform 1s ease-out;
    }

    .gauge-cover {
        position: absolute;
        top: 5px;
        left: 5px;
        width: 90px;
        height: 45px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 45px 45px 0 0;
        backdrop-filter: blur(5px);
    }

    .gauge-percentage {
        position: absolute;
        bottom: 5px;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        color: white;
    }

    /* Custom glow effect for points text */
    .points-glow {
        color: #00ffff;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff;
        animation: points-pulse 2s infinite;
    }

    @keyframes points-pulse {
        0% { text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff; }
        50% { text-shadow: 0 0 15px #00ffff, 0 0 25px #00ffff, 0 0 35px #00ffff, 0 0 45px #00ffff; }
        100% { text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff; }
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

    [data-testid="stSidebar"] .stTextInput > div > div > input,
    [data-testid="stSidebar"] .stSelectbox > div > div > div,
    [data-testid="stSidebar"] .stDateInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 5px !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebar"] .stTextInput > div > div > input:hover,
    [data-testid="stSidebar"] .stSelectbox > div > div > div:hover,
    [data-testid="stSidebar"] .stDateInput > div > div > input:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 5px !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
    }

    [data-testid="stSidebar"] .stMarkdown p {
        color: white !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebar"] .stMarkdown p:hover {
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important;
    }

    .sidebar-glow {
        animation: sidebarGlow 2s ease-in-out infinite alternate;
    }

    @keyframes sidebarGlow {
        from {
            text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #fff, 0 0 20px #00ffff, 0 0 35px #00ffff, 0 0 40px #00ffff;
        }
        to {
            text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #00ffff, 0 0 55px #00ffff, 0 0 60px #00ffff;
        }
    }
    /* Custom styles for selectboxes and other widgets */
    .stSelectbox, .stTextInput, .stDateInput {
        background: linear-gradient(45deg, #ff00de, #00ffff);
        border-radius: 10px;
        padding: 2px;
    }

    .stSelectbox > div, .stTextInput > div, .stDateInput > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .stSelectbox > div:hover, .stTextInput > div:hover, .stDateInput > div:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }

    /* Mobile-friendly styles */
    @media (max-width: 768px) {
        .dynamic-title {
            font-size: 2rem;
        }
        .st-bw {
            padding: 15px;
        }
        .st-emotion-cache-16txtl3 {
            padding: 1rem;
        }
    }
        /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Adjust the app container to fill the screen */
    .stApp {
        margin-top: -80px;
    }
        /* Base styles for input widgets */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stDateInput > div > div > input {
        background: linear-gradient(45deg, rgba(255, 0, 222, 0.3), rgba(0, 255, 255, 0.3));
        color: white !important;
        border-radius: 5px !important;
        transition: all 0.3s ease !important;
        border: none !important;
    }

    /* Hover and focus styles for input widgets */
    .stTextInput > div > div > input:hover,
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:hover,
    .stDateInput > div > div > input:hover,
    .stDateInput > div > div > input:focus {
        background: linear-gradient(45deg, rgba(255, 0, 222, 0.5), rgba(0, 255, 255, 0.5));
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
    }

    /* Custom class for glowing effect */
    .widget-glow {
        animation: widget-glow 2s ease-in-out infinite alternate;
    }

    @keyframes widget-glow {
        from {
            box-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #00ffff, 0 0 20px #00ffff;
        }
        to {
            box-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #00ffff, 0 0 40px #00ffff;
        }
 
    /* Custom checkbox styles */
    .stCheckbox {
        position: relative;
        padding-left: 35px;
        margin-bottom: 12px;
        cursor: pointer;
        font-size: 22px;
        user-select: none;
    }

    .stCheckbox input {
        position: absolute;
        opacity: 0;
        cursor: pointer;
        height: 0;
        width: 0;
    }

    .stCheckbox > div {
        position: absolute;
        top: 0;
        left: 0;
        height: 25px;
        width: 25px;
        background-color: #eee;
        border-radius: 50%;
        transition: all 0.3s ease;
    }

    .stCheckbox:hover input ~ div {
        background-color: #ccc;
    }

    .stCheckbox input:checked ~ div {
        background-color: #2196F3;
        animation: pulse 0.5s ease-out;
    }

    .stCheckbox input:checked ~ div::after {
        content: "";
        position: absolute;
        display: block;
        left: 9px;
        top: 5px;
        width: 5px;
        height: 10px;
        border: solid white;
        border-width: 0 3px 3px 0;
        transform: rotate(45deg);
        animation: check 0.3s ease-out;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }

    @keyframes check {
        0% { height: 0; }
        100% { height: 10px; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="completion-bar-container">
    <div class="completion-bar" id="completionBar">
        <div class="completion-bubbles" id="completionBubbles"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# JavaScript for updating the completion bar
st.markdown("""
<script>
    function updateCompletionBar(percentage) {
        const bar = document.getElementById('completionBar');
        bar.style.width = percentage + '%';
        
        const bubbles = document.getElementById('completionBubbles');
        const bubbleCount = Math.floor(percentage / 5);  // One bubble for every 5%
        bubbles.innerHTML = '';
        
        for (let i = 0; i < bubbleCount; i++) {
            const bubble = document.createElement('div');
            bubble.className = 'bubble';
            bubble.style.left = Math.random() * 100 + '%';
            bubble.style.top = Math.random() * 100 + '%';
            bubble.style.width = Math.random() * 10 + 5 + 'px';
            bubble.style.height = bubble.style.width;
            bubble.style.animationDelay = Math.random() * 2 + 's';
            bubbles.appendChild(bubble);
        }
    }
</script>
""", unsafe_allow_html=True)

st.markdown("""
<script>
// Function to toggle the sidebar
function toggleSidebar() {
    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
    const sidebarContent = sidebar.querySelector('[data-testid="stSidebarContent"]');
    if (sidebarContent.style.width === '0px' || sidebarContent.style.width === '') {
        sidebarContent.style.width = '350px';
        sidebar.style.width = '350px';
        sidebar.style.opacity = 1;
        sidebar.style.pointerEvents = 'auto';
    } else {
        sidebarContent.style.width = '0px';
        sidebar.style.width = '0px';
        sidebar.style.opacity = 0;
        sidebar.style.pointerEvents = 'none';
    }
}

// Function to apply glow effect to dynamic elements
function applyGlowEffect() {
    const glowElements = document.querySelectorAll('.points-glow');
    glowElements.forEach(elem => {
        elem.style.textShadow = `
            0 0 10px #00ffff,
            0 0 20px #00ffff,
            0 0 30px #00ffff,
            0 0 40px #00ffff
        `;
    });
}

// Function to enhance hover effects
function enhanceHoverEffects() {
    const hoverElements = document.querySelectorAll('.stSelectbox > div, .stTextInput > div, .stDateInput > div');
    hoverElements.forEach(elem => {
        elem.addEventListener('mouseenter', () => {
            elem.style.transform = 'translateY(-2px)';
            elem.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.3)';
        });
        elem.addEventListener('mouseleave', () => {
            elem.style.transform = 'translateY(0)';
            elem.style.boxShadow = 'none';
        });
    });
}

// Function to animate task cards
function animateTaskCards() {
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach((card, index) => {
        card.style.animation = `fadeIn 0.5s ease-out ${index * 0.1}s`;
    });
}

// Function to initialize custom scrollbar
function initCustomScrollbar() {
    document.body.style.scrollbarWidth = 'thin';
    document.body.style.scrollbarColor = '#4CAF50 #1E1E1E';
}

// Function to enhance sidebar effects
function enhanceSidebarEffects() {
    const sidebarElements = document.querySelectorAll('[data-testid="stSidebar"] .stTextInput, [data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stDateInput, [data-testid="stSidebar"] .stButton');
    sidebarElements.forEach(elem => {
        elem.addEventListener('mouseenter', () => {
            elem.style.transform = 'translateY(-2px)';
            elem.style.boxShadow = '0 4px 10px rgba(0, 0, 0, 0.2)';
        });
        elem.addEventListener('mouseleave', () => {
            elem.style.transform = 'translateY(0)';
            elem.style.boxShadow = 'none';
        });
    });

    const sidebarTexts = document.querySelectorAll('[data-testid="stSidebar"] .stMarkdown p');
    sidebarTexts.forEach(text => {
        text.addEventListener('mouseenter', () => {
            text.style.textShadow = '0 0 10px rgba(255, 255, 255, 0.5)';
        });
        text.addEventListener('mouseleave', () => {
            text.style.textShadow = 'none';
        });
    });
}

// Function to apply sidebar glow
function applySidebarGlow() {
    const glowElements = document.querySelectorAll('.sidebar-glow');
    glowElements.forEach(elem => {
        elem.style.animation = 'sidebarGlow 2s ease-in-out infinite alternate';
    });
}

// Function to enhance widgets with dynamic effects
function enhanceWidgets() {
    const widgets = document.querySelectorAll('.stTextInput > div > div > input, .stSelectbox > div > div > div, .stDateInput > div > div > input');

    widgets.forEach(widget => {
        widget.addEventListener('mouseenter', () => {
            widget.style.background = 'linear-gradient(45deg, rgba(255, 0, 222, 0.7), rgba(0, 255, 255, 0.7))';
            widget.classList.add('widget-glow');
        });

        widget.addEventListener('mouseleave', () => {
            widget.style.background = 'linear-gradient(45deg, rgba(255, 0, 222, 0.3), rgba(0, 255, 255, 0.3))';
            widget.classList.remove('widget-glow');
        });

        widget.addEventListener('focus', () => {
            widget.style.background = 'linear-gradient(45deg, rgba(255, 0, 222, 0.7), rgba(0, 255, 255, 0.7))';
            widget.classList.add('widget-glow');
        });

        widget.addEventListener('blur', () => {
            widget.style.background = 'linear-gradient(45deg, rgba(255, 0, 222, 0.3), rgba(0, 255, 255, 0.3))';
            widget.classList.remove('widget-glow');
        });

        // For touch devices
        widget.addEventListener('touchstart', () => {
            widget.style.background = 'linear-gradient(45deg, rgba(255, 0, 222, 0.7), rgba(0, 255, 255, 0.7))';
            widget.classList.add('widget-glow');
        });

        widget.addEventListener('touchend', () => {
            widget.style.background = 'linear-gradient(45deg, rgba(255, 0, 222, 0.3), rgba(0, 255, 255, 0.3))';
            widget.classList.remove('widget-glow');
        });
    });
}

// Main function to run all custom scripts
function runCustomScripts() {
    applyGlowEffect();
    enhanceHoverEffects();
    animateTaskCards();
    initCustomScrollbar();
    enhanceSidebarEffects();
    applySidebarGlow();
    enhanceWidgets();
}

// Add click event listener to the toggle button
const toggleButton = document.querySelector('.sidebar-toggle');
if (toggleButton) {
    toggleButton.addEventListener('click', toggleSidebar);
}

// Run custom scripts when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', runCustomScripts);

// Re-run custom scripts when Streamlit re-renders the page
const observer = new MutationObserver(runCustomScripts);
observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)


# Helper Functions
def login_user():
    username = st.session_state.username
    user_data = load_user_data(username)
    if user_data:
        st.session_state.user = username
        for key, value in user_data.items():
            st.session_state[key] = value
        st.success("Logged in successfully!")
    else:
        st.error("User not found. Please create an account.")


def logout_user():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
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


def add_task(task, due_date, priority, category):
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


# Update the complete_task function
def complete_task(task_id):
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
    if st.session_state.last_completed == (today - timedelta(days=1)).isoformat():
        st.session_state.streaks += 1
    elif st.session_state.last_completed != today.isoformat():
        st.session_state.streaks = 1
    st.session_state.last_completed = today.isoformat()
    update_user_stats(st.session_state.user, {
        "streaks": st.session_state.streaks,
        "last_completed": st.session_state.last_completed
    })


def award_points(priority):
    points = {"Low": 5, "Medium": 10, "High": 15}
    st.session_state.user_points += points[priority]
    update_user_stats(st.session_state.user, {"user_points": st.session_state.user_points})


def update_completion_rate():
    total_tasks = len(st.session_state.tasks) + len(st.session_state.completed_tasks)
    st.session_state.completion_rate = (
            len(st.session_state.completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
    update_user_stats(st.session_state.user, {"completion_rate": st.session_state.completion_rate})


def get_motivation_quote():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson"
    ]
    return random.choice(quotes)


def handle_task_completion():
    task_id = st.session_state.get('task_to_complete')
    if task_id:
        if complete_task(task_id):
            st.success(f"Task completed successfully!")
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

    # Update completion bar on page load
    update_completion_bar()
    if 'logout_key' not in st.session_state:
        st.session_state.logout_key = None



    if not st.session_state.user:
        st.markdown("""
             <div class="dynamic-title">
                 Welcome to LifeSync
             </div>
         """, unsafe_allow_html=True)
        # Login/Register UI
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Login")
            st.text_input("Username", key="username")
            st.button("Login", on_click=login_user, key="login_button")
        with col2:
            st.subheader("Register")
            st.text_input("New Username", key="new_username")
            st.button("Register", on_click=register_user, key="register_button")
    else:
        # Generate a unique key for the logout button if it doesn't exist
        if st.session_state.logout_key is None:
            st.session_state.logout_key = f"logout_{st.session_state.user}_{int(time.time())}"

        col_title, col_gauge = st.columns([3, 1])
        with col_title:
            st.subheader("⚡ Quick Add Task")

        completion_rate = st.session_state.completion_rate
        st.markdown(f"""
            <div class="gauge-container">
                <div class="gauge-bg"></div>
                <div class="gauge-fill" style="transform: rotate({completion_rate * 1.8}deg);"></div>
                <div class="gauge-cover"></div>
                <div class="gauge-percentage">{completion_rate:.0f}%</div>
            </div>
        """, unsafe_allow_html=True)

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

        st.header("📋 Dashboard")

        # Task filters
        with st.expander("Task Filters", expanded=False):
            filter_category = st.multiselect(
                "Filter by Category",
                options=st.session_state.categories,
                default=[],
                key="filter_category_multiselect"
            )
            filter_priority = st.multiselect(
                "Filter by Priority",
                options=["Low", "Medium", "High"],
                default=[],
                key="filter_priority_multiselect"
            )
            filter_due = st.date_input(
                "Filter by Due Date",
                value=None,
                key="filter_due_date_input"
            )

        # Display tasks
        for index, task in enumerate(st.session_state.tasks):
            if (not filter_category or task['category'] in filter_category) and \
                    (not filter_priority or task['priority'] in filter_priority) and \
                    (not filter_due or task['due_date'] == filter_due.isoformat()):
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

        # Render task distribution and completion bar
        render_task_distribution()
        render_completion_bar()

        # Rewards section
        st.subheader("🎁 Rewards Center")
        st.markdown(f"""
            <div style='background-color: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; text-align: center;'>
                <h3 class='points-glow'>You have {st.session_state.user_points} points to spend!</h3>
            </div>
            """, unsafe_allow_html=True)

        reward_cols = st.columns(2)
        for idx, reward in enumerate(st.session_state.rewards):
            with reward_cols[idx % 2]:
                with st.container():
                    st.markdown(f"""
                        <div class='reward-card'>
                            <h4>{reward['name']}</h4>
                            <p>{reward['points']} points</p>
                        </div>
                        """, unsafe_allow_html=True)
                    if st.button("Redeem", key=f"redeem_{reward['name']}_{idx}"):
                        if st.session_state.user_points >= reward['points']:
                            st.session_state.user_points -= reward['points']
                            update_user_stats(st.session_state.user, {"user_points": st.session_state.user_points})
                            st.success(f"You've redeemed {reward['name']}!")
                            st.balloons()
                        else:
                            st.error("Not enough points!")

        # Productivity Tips
        st.subheader("💡 Productivity Tips")
        tips = [
            "Break large tasks into smaller, manageable steps.",
            "Use the Pomodoro Technique: Work for 25 minutes, then take a 5-minute break.",
            "Prioritize your tasks using the Eisenhower Matrix.",
            "Minimize distractions by turning off notifications during focus time.",
            "Start your day by tackling the most important or challenging task.",
        ]
        tip_index = random.randint(0, len(tips) - 1)
        st.info(tips[tip_index])

        # Sidebar
        with st.sidebar:
            st.markdown('<h2 class="sidebar-glow">LifeSync Menu</h2>', unsafe_allow_html=True)
            st.button("Logout", on_click=logout_user, key=st.session_state.logout_key)

            st.markdown('<h3 class="sidebar-glow">User Stats</h3>', unsafe_allow_html=True)
            st.metric("🏆 Streak", f"{st.session_state.streaks} days")
            st.metric("💎 Points", st.session_state.user_points)

            st.markdown('<h3 class="sidebar-glow">Daily Inspiration</h3>', unsafe_allow_html=True)
            st.info(get_motivation_quote())


# ===== Main Execution =====
if __name__ == "__main__":
    main()
