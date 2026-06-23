import streamlit as st
import time

def svg(circleRadius):
    global size
    return f"""<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
    <rect width="100" height="100" fill="grey" />
    <circle cx="50" cy="50" r="{circleRadius}" stroke="green" stroke-width="4" fill="yellow" />
</svg>"""

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)
c = st.empty()

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  c.write( svg(i), unsafe_allow_html=True )
  time.sleep(0.1)

'...and now we\'re done!'
