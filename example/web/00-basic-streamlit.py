"""
# Simple Scene rendering using streamlit.
"""
import streamlit as st

def svg(circleRadius):
    global size
    return f"""<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
    <rect width="100" height="100" fill="grey" />
    <circle cx="50" cy="50" r="{circleRadius}" stroke="green" stroke-width="4" fill="yellow" />
</svg>"""

x = st.slider('x')  # 👈 this is a widget
st.write(svg(x), unsafe_allow_html=True)
