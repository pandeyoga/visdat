import streamlit as st
from bokeh.embed import server_document

# Get the script and div for the Bokeh application
bokeh_script = server_document('https://raw.githubusercontent.com/pandeyoga/visdat/main/spotify.py')

# Render the Bokeh application in Streamlit
st.bokeh_chart(bokeh_script, use_container_width=True)
