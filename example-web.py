"""
# My first app
Here's our first attempt at using data to create a table:
"""

import time, streamlit as st

size= 40

@st.fragment
def release_the_balloons():
    global size
    #st.button("Release the balloons", help="Fragment rerun")
    st.balloons()
    time.sleep(10)
    if size == 40 :
        size= 20
    else :
        size= 20
    st.rerun()

#with st.spinner("Inflating balloons..."):
#    time.sleep(5)

#st.button("Inflate more balloons", help="Full rerun")

def svg(circleRadius):
    global size
    return f"""<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
    <rect width="100" height="100" fill="grey" />
    <circle cx="{circleRadius}" cy="{circleRadius}" r="{size}" stroke="green" stroke-width="4" fill="yellow" />
</svg>"""

x = st.slider('x')  # 👈 this is a widget
st.write(svg(x), unsafe_allow_html=True)


release_the_balloons()
