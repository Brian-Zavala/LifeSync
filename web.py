import streamlit as st
import functions

todos = functions.get_todos()


def add_todo():
    todo = st.session_state["new_todo"] + "\n"
    todos.append(todo)
    functions.write_todos(todos)




st.title("Araceli's To-Do's")
st.subheader("Get Shit Done For Cash!")
st.write("Nobody Plans To Fail, But Those Who Do Not Plan Fail")

for index, todo in enumerate(todos):
    checkbox = st.checkbox(todo, key=todo)
    if checkbox:
        todos.pop(index)
        functions.write_todos(todos)
        del st.session_state[todo]
        st.experimental_rerun()


st.text_input(label="", placeholder="Add a new to-do...",
              on_change=add_todo, key='new_todo')

