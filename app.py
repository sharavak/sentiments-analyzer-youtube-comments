import streamlit as st
import scraper
from deep_translator import GoogleTranslator
import plotly.express as px
import plotly.graph_objects as go
from preprocessing import get_sentiment
import pandas as pd
st.set_page_config(
        page_title="Sentiment Analyzer",
        page_icon="https://cdn-icons-png.flaticon.com/512/14511/14511452.png",
    )
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

	    
st.header('Youtube comments Sentiment Analyzer',divider='rainbow')
val=st.text_input(label='Type the youtube url')
if val:
    with st.spinner("Scraping data...") as status:
        comments=scraper.scrape(val)
        text=[]
        for i in comments:
            comment=GoogleTranslator(source='auto', target='en').translate(text=i)
            text.append(comment)
    with st.expander("Show sentiments"):
        pos,neg,neu=get_sentiment(text)
        st.write(f'Total Comments: {len(text)}')
        df =[pos,neg,neu]
        fig = px.pie(values=df,names=['Positive','Negative','Neutral'])
        st.plotly_chart(fig,use_container_width=True)
        df = pd.DataFrame({
            "Sentiments": ["Positive", "Neutral", "Negative"],
            "Values": [pos,neu,neg]
        })
        fig = go.Figure(data=[go.Bar(x=df["Sentiments"], y=df["Values"],textfont=dict(color='black', size=12), marker_color=['green','#64bdfd','#ff9e1c'])])
        fig.update_layout(title="Sentiments", xaxis_title="Sentiments", yaxis_title="Sentiment distribution")
        st.plotly_chart(fig)