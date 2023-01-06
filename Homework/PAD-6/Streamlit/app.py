import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(
    layout = 'wide',
    page_title = 'Streamlit Data Application'
)

page = st.sidebar.selectbox('Select page', ['Form', 'Stats'])


if page == 'Form':

    st.title('Name and Surname Survey')
    with st.form('name_and_surname_form'):

        name_text = st.text_input('Name', placeholder='Your name')
        surname_text = st.text_input('Surname', placeholder='Your surname')
        submitted = st.form_submit_button('Submit')

        if submitted:
            if name_text != "" and surname_text != "":
                st.success(f'Form submitted successfully, thank you {name_text} for using Streamlit')
            else:
                st.error('Missing required information')


elif page == 'Stats':

    st.title('CSV Data Explorer')
    data = st.file_uploader('Upload your dataset', type=['csv'])
    if data is not None:
        start_time = time.time()

        with st.progress(0):
            df = pd.read_csv(data, sep=',')
            st.dataframe(df.sample(10))
        end_time = time.time()
        st.success(f'File with {df.shape[0]} rows and {df.shape[1]} columns read successfully in {round(end_time - start_time, 3)} seconds!')

    st.text('')

    if data is not None:
        st.header('Visualize your data')

        graph_type = st.radio('Graph type', ['Scatter Plot', 'Bar Plot'])
        x_column = st.selectbox('X', df.columns[1:])
        y_column = st.selectbox('Y', df.columns[1:])

        col1, col2 = st.columns(2)

        if graph_type == 'Scatter Plot':
            fig = px.scatter(df, x=x_column, y=y_column, title=f'{graph_type}, {x_column} of {y_column}')

        elif graph_type == 'Bar Plot':
            fig = px.bar(df, x=x_column, y=y_column, title=f'{graph_type}, {x_column} of {y_column}')

        else:
            st.text('Graph Type not supported')

        col1.plotly_chart(fig, use_container_width = True)


else:
    st.text('Selection not supported')