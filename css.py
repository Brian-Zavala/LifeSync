import streamlit as st

def css_styles():
    st.markdown("""
    <style>
     * {
        overflow-anchor: none !important;
        }
        


    /* Base styles and imports */
    
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');
    
    
    * {
        font-family: 'Poppins', sans-serif;
        box-sizing: border-box;
    }
    
    body {
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
    
    /* Login Container Styles */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    .login-title {
        font-size: 2.5rem;
        margin: 1rem 0;
        color: #ffffff;
        text-align: center;
    }
    
    .login-form {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        width: 100%;
        max-width: 400px;
    }
    
    /* Button Styles */
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2, #667eea);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
    
    /* Dynamic Title Styles */
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

/* Triangle container */
.dynamic-title::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: -1;
    opacity: 0.3;
    background: 
        /* First row of triangles */
        linear-gradient(45deg, transparent 50%, #00ffff 50%, transparent 51%) 0 0/20px 20px,
        linear-gradient(-45deg, transparent 50%, #ff00de 50%, transparent 51%) 10px 0/20px 20px,
        /* Second row of triangles */
        linear-gradient(45deg, transparent 50%, #ff00de 50%, transparent 51%) 10px 10px/20px 20px,
        linear-gradient(-45deg, transparent 50%, #00ffff 50%, transparent 51%) 0 10px/20px 20px;
    animation: triangleMove 20s linear infinite;
}

/* Individual glowing triangles */
.dynamic-title::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: -1;
    background: 
        radial-gradient(2px at 5px 5px, #00ffff, transparent),
        radial-gradient(2px at 15px 15px, #ff00de, transparent),
        radial-gradient(2px at 25px 5px, #00ffff, transparent),
        radial-gradient(2px at 5px 25px, #ff00de, transparent);
    background-size: 30px 30px;
    animation: triangleGlow 4s ease-in-out infinite alternate;
}

@keyframes glow {
    from {
        text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #fff, 0 0 20px #ff00de;
    }
    to {
        text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #ff00de;
    }
}

@keyframes triangleMove {
    0% {
        background-position: 
            0 0,
            10px 0,
            10px 10px,
            0 10px;
    }
    100% {
        background-position: 
            20px 20px,
            30px 20px,
            30px 30px,
            20px 30px;
    }
}

@keyframes triangleGlow {
    0% {
        opacity: 0.3;
        transform: scale(1);
    }
    50% {
        opacity: 0.6;
        transform: scale(1.05);
    }
    100% {
        opacity: 0.3;
        transform: scale(1);
    }
}
    
    /* Card and Widget Styles */
    .st-bw, .st-emotion-cache-16txtl3 {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    .st-bw:hover, .st-emotion-cache-16txtl3:hover {
        transform: translateY(-6px) translateY(2px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.45);
    }
    
    /* Task and Reward Card Styles */
    .task-card, .reward-card {
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
        text-align: center;
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
    
    /* Sidebar Styles */
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
    
    

    
    input[type="checkbox"]:checked {
        background-color: #4CAF50;
        border-color: #4CAF50;
    }
    
    input[type="checkbox"]:checked::before {
        content: '✓';
        position: relative;
        color: #ffffff;
        font-size: 14px;
    }
    
    /* Gauge Styles */
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
    
    /* Points Glow Effect */
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
    
    /* Input Widget Styles */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stDateInput > div > div > input {
        background: linear-gradient(45deg, rgba(255, 0, 222, 0.3), rgba(0, 255, 255, 0.3));
        color: white !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        border: none !important;
        padding: 10px !important;
    }
    
    .stTextInput > div > div,
    .stSelectbox > div > div,
    .stDateInput > div > div {
        position: relative;
        overflow: hidden;
        border-radius: 12px;
    }
    
    .stTextInput > div > div::before,
    .stSelectbox > div > div::before,
    .stDateInput > div > div::before {
        display: none;
        );
        animation: rotate-glow 4s linear infinite;
        z-index: 0;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stTextInput > div > div:hover::before,
    .stTextInput > div > div:focus-within::before,
    .stSelectbox > div > div:hover::before,
    .stDateInput > div > div:hover::before,
    .stDateInput > div > div:focus-within::before {
        opacity: 1;
    }
    
    @keyframes rotate-glow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Custom Checkbox Styles */
    .stCheckbox {
        position: relative;
        cursor: pointer;
        font-size: 16px;
        user-select: none;
        display: flex;
        align-items: center;
    }
    
    .stCheckbox > label {
        display: flex;
        position: relative;
        cursor: pointer;
    }
    
    .stCheckbox > label::before {
        content: "";
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 30px;
        height: 30px;
        background-color: #2c3e50;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(52, 152, 219, 0.5);
    }
    
    /* Continuation of Custom Checkbox Styles */
    .stCheckbox > label::after {
        content: "";
        position: absolute;
        left: 5px;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        border-radius: 12px;
        background: conic-gradient(
            from 0deg,
            transparent 0%,
            transparent 25%,
            #3498db 25%,
            #3498db 50%,
            transparent 50%,
            transparent 75%,
            #3498db 75%,
            #3498db 100%
        );
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stCheckbox:hover > label::after {
        opacity: 1;
        animation: rotate 4s linear infinite;
    }
    
    .stCheckbox input:checked + label::before {
        background-color: #3498db;
        animation: pulse 0.5s ease-out;
    }
    
    .stCheckbox input:checked + label > span::after {
        content: "";
        position: absolute;
        display: block;
        left: 11px;
        top: 7px;
        width: 6px;
        height: 12px;
        border: solid white;
        border-width: 0 3px 3px 0;
        transform: rotate(45deg);
        animation: check 0.3s ease-out;
    }
    
    @keyframes rotate {
        0% { transform: translateY(-50%) rotate(0deg); }
        100% { transform: translateY(-50%) rotate(360deg); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(52, 152, 219, 0.7); }
        50% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(52, 152, 219, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(52, 152, 219, 0); }
    }
    
    @keyframes check {
        0% { height: 0; }
        100% { height: 12px; }
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
        margin-top: -76px;
    }
    
    /* JavaScript Optimizations */
    <script>
    // Function to update the completion bar
    function updateCompletionBar(percentage) {
        const bar = document.getElementById('completionBar');
        const bubbles = document.getElementById('completionBubbles');
        
        bar.style.width = `${percentage}%`;
        
        bubbles.innerHTML = '';
        const bubbleCount = Math.floor(percentage / 5);
        
        for (let i = 0; i < bubbleCount; i++) {
            const bubble = document.createElement('div');
            bubble.className = 'bubble';
            bubble.style.left = `${Math.random() * 100}%`;
            bubble.style.top = `${Math.random() * 100}%`;
            bubble.style.width = `${Math.random() * 10 + 5}px`;
            bubble.style.height = bubble.style.width;
            bubble.style.animationDelay = `${Math.random() * 2}s`;
            bubbles.appendChild(bubble);
        }
    }
    
    // Function to toggle the sidebar
    function toggleSidebar() {
        const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        const sidebarContent = sidebar.querySelector('[data-testid="stSidebarContent"]');
        const isOpen = sidebarContent.style.width !== '0px' && sidebarContent.style.width !== '';
        
        sidebarContent.style.width = isOpen ? '0px' : '350px';
        sidebar.style.width = isOpen ? '0px' : '350px';
        sidebar.style.opacity = isOpen ? 0 : 1;
        sidebar.style.pointerEvents = isOpen ? 'none' : 'auto';
    }
    
    // Function to apply glow effect to dynamic elements
    function applyGlowEffect() {
        document.querySelectorAll('.points-glow').forEach(elem => {
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
        document.querySelectorAll('.stSelectbox > div, .stTextInput > div, .stDateInput > div').forEach(elem => {
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
        document.querySelectorAll('.task-card').forEach((card, index) => {
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
    
        document.querySelectorAll('[data-testid="stSidebar"] .stMarkdown p').forEach(text => {
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
        document.querySelectorAll('.sidebar-glow').forEach(elem => {
            elem.style.animation = 'sidebarGlow 2s ease-in-out infinite alternate';
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
    document.querySelector('.sidebar-toggle')?.addEventListener('click', toggleSidebar);
    
    // Run custom scripts when the DOM is fully loaded
    document.addEventListener('DOMContentLoaded', runCustomScripts);
    
    // Re-run custom scripts when Streamlit re-renders the page
    const observer = new MutationObserver(runCustomScripts);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)
