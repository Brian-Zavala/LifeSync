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

