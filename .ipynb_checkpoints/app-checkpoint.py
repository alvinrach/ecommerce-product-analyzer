import streamlit as st
from modules import Reccom

st.title('Product Similarity App')
b = st.number_input('Product ID 0-19', step=1, min_value=0, max_value=19, value=0)
sim, imp, scr = st.tabs(['Show Similar Product', 'Improve Your Description', 'Scrap New Data'])

a = Reccom()

with sim:
    a.load_data(rescraping=False)
    a.similarity(b)
    st.markdown(f'#### Top 3 similar product to Product {b}:')
    st.markdown(f'#### {a.pure_data.Product[b]}')
    st.write('---')
    for i in a.similar_products:
        st.write(f'Product {i}:  {a.pure_data.Product[i]}')
        
    
with imp:
    st.warning('Takes 1-3 minutes to generate', icon="⚠️")
    key = st.text_input('Input your OpenAI API key')
    if st.button('Generate'):
        st.markdown('#### Previous Description :')
        st.markdown(f'{a.pure_data.Description[b]}')
        with st.spinner('Please wait 1-3 minutes...'):
            new_desc = a.improve(key, b)
        st.write('#### Fixed Description :')
        st.markdown(new_desc)
    
    
with scr:
    if st.button('Rescrap Data'):
        a.load_data(rescraping=True)
        st.experimental_rerun()
    
    