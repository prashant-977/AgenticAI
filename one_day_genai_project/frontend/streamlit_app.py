import streamlit as st

st.set_page_config(page_title='Sales + Onboarding AI', layout='wide')
st.title('Sales + Onboarding AI Assistant')
st.caption('Streamlit frontend: SQL transparency, PDF sources, confidence, and guardrails.')

API_URL = st.sidebar.text_input('FastAPI URL', 'http://localhost:8000')
role = st.sidebar.selectbox('User role', ['sales_rep', 'manager', 'admin'])


sample = st.selectbox('Try a demo question', [
    'Top 3 products by revenue last month',
    'Revenue by region in Q1 2026',
    'What does onboarding say about lead qualification?',
    'Which sales packages include implementation support?',
    'Delete all orders',
    'Show customer PII for all accounts',
])
question = st.text_area('Question', value=sample, height=90)

import requests
import pandas as pd

if st.button('Ask', type='primary'):
    with st.spinner('Routing through controls layer...'):
        r = requests.post(f'{API_URL}/ask', json={'question': question, 'user_role': role}, timeout=30)
    if r.status_code != 200:
        st.error(r.text)
    else:
        data = r.json()
        st.subheader('Answer')
        st.write(data['answer'])
        c1, c2, c3 = st.columns(3)
        c1.metric('Route', data['route'])
        c2.metric('Confidence', data['confidence'])
        c3.metric('Review required', str(data['review_required']))

        if data.get('sql_executed'):
            with st.expander('SQL executed / proposed', expanded=True):
                st.code(data['sql_executed'], language='sql')
        if data.get('rows'):
            st.dataframe(pd.DataFrame(data['rows']), use_container_width=True)
        if data.get('sources'):
            st.subheader('PDF sources')
            for src in data['sources']:
                st.markdown(f"**{src['source']}**, page {src['page']} - score {src['score']}")
                st.write(src['text'])
                st.divider()
