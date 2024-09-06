import streamlit as st
import pandas as pd
import plotly.express as px

def render_task_distribution():
    if st.session_state.tasks:
        st.subheader("Task Distribution")
        df = pd.DataFrame(st.session_state.tasks)
        category_counts = df['category'].value_counts().reset_index()
        category_counts.columns = ['category', 'count']
        fig_pie = px.pie(category_counts, values='count', names='category',
                         title='Tasks by Category')
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white", 'family': "Arial"},
            title={'font': {'size': 24, 'color': 'white'}},
            legend={'font': {'size': 14, 'color': 'white'}},
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(colors=px.colors.qualitative.Pastel),
            textfont_size=14,
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Add some tasks to see your task distribution!")

def render_completion_bar():
    if st.session_state.tasks:
        total_tasks = len(st.session_state.tasks) + len(st.session_state.completed_tasks)
        completed_percentage = (len(st.session_state.completed_tasks) / total_tasks) * 100
        st.markdown(f"""
        <div style='background-color: rgba(255,255,255,0.1); border-radius: 10px; padding: 10px;'>
            <h4 style='text-align: center; color: #4CAF50;'>Overall Progress</h4>
            <div style='background-color: #ddd; border-radius: 5px; height: 20px;'>
                <div style='background-color: #4CAF50; width: {completed_percentage}%; height: 100%; border-radius: 5px; transition: width 1s ease-in-out;'></div>
            </div>
            <p style='text-align: center; color: white;'>{completed_percentage:.1f}% Complete</p>
        </div>
        """, unsafe_allow_html=True)
