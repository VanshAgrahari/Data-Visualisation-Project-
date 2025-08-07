import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
df=pd.read_csv('india-census.csv')


def Country_Analysis(op1,op2):

   # Correct use of scatter_mapbox
    
    st.write('Geographcal distribution of {},{}.'.format(op1,op2))
    fig = px.scatter_mapbox(df,
                        lat="Latitude",
                        lon="Longitude",
                            zoom=3,mapbox_style="carto-positron",width=700,height=900,size=op1,color=op2,hover_name='District',color_continuous_scale='aggrnyl')

    # Show the map
    st.plotly_chart(fig,use_container_width=True)
    

    # grouped bar chart
    st.write('Stacked bar graph of {}.'.format(op1))
    fig=px.bar(df,x='State',y=op1,color='District',text_auto=True)
    st.plotly_chart(fig)
    
    st.write('Stacked bar graph of {}.'.format(op2))
    fig=px.bar(df,x='State',y=op2,color='District',text_auto=True)
    st.plotly_chart(fig)
   

   
#    sunburst plot
    st.write('sunburst bar graph of {}.'.format(op1))
  
    fig=px.sunburst(df,path=['State','District'],values=op1,color=op1)
    st.plotly_chart(fig)

    st.write('sunburst bar graph of {}.'.format(op2))
    fig=px.sunburst(df,path=['State','District'],values=op2,color=op2)
    st.plotly_chart(fig)

   
    #   Similar to Literacy rate

    if op1!='Population':

        st.write('bar graph of {}.'.format(op1))
        temp_df1=df.groupby('State')[op1].sum().reset_index()
        temp_df2=df.groupby('State')['Population'].sum().reset_index()

        temp_df=temp_df1.merge(temp_df2,on='State')
        s='{} Percentage'.format(op1)
        temp_df[s]=(temp_df[op1]/temp_df['Population'])*100
        fig=px.bar(temp_df,x='State',y=s,text_auto=True,color='Population',color_continuous_scale='hot')
        st.plotly_chart(fig)
    
    if op2!='Population':
        st.write('bar graph of {}.'.format(op2))
        temp2_df1=df.groupby('State')[op2].sum().reset_index()
        temp2_df2=df.groupby('State')['Population'].sum().reset_index()

        temp2_df=temp2_df1.merge(temp2_df2,on='State')
        s='{} Percentage'.format(op2)
        temp2_df[s]=(temp2_df[op2]/temp2_df['Population'])*100
        fig=px.bar(temp2_df,x='State',y=s,text_auto=True,color='Population',color_continuous_scale='hot')
        st.plotly_chart(fig)

     # comparison
    st.write('comparable bar graph of {},{}.'.format(op1,op2))
    df1=df.groupby('State')[op1].sum().reset_index()
    df2=df.groupby('State')[op2].sum().reset_index()
    temp_df=df1.merge(df2,on='State')
    fig=px.bar(temp_df,x='State',y=[op1,op2],barmode='group',color_continuous_scale='viridis')
    st.plotly_chart(fig)

    # treemap
    st.write('Tree Map graph of {},{}.'.format(op1,op2))
    fig=px.treemap(df,path=[px.Constant('India'),'State','District'],values=op1,color=op2,color_continuous_scale='viridis')
    st.plotly_chart(fig)
   
    # histogram
    st.write('Histogram  graph of {}.'.format(op1))
    fig=px.histogram(df,x=op1,text_auto=True)
    st.plotly_chart(fig)

    st.write('Histogram  graph of {}.'.format(op2))
    fig=px.histogram(df,x=op2,text_auto=True)
    st.plotly_chart(fig)


def State_Analysis(state,op1,op2):

    temp_df=df[df['State']==state]
    st.subheader('Our State {}:'.format(state))
   
    if state=='Bihar':
     temp_df=temp_df[ ~(temp_df['District code']==515)]
    
    col1,col2=st.columns(2)
    with col1:
        st.metric('Total Population of {}'.format(state),str(round(temp_df['Population'].sum()/1000000))+str('M'))
    with col2:
        st.metric('Total Districts in {}'.format(state),temp_df.shape[0])

    col1,col2,col3,col4=st.columns(4)

    with col1:
     st.metric('Total {} people'.format(op1),str(round(temp_df[op1].sum()/1000000))+str('M'))
    with col2:
     st.metric('Total {} people'.format(op2),str(round(temp_df[op2].sum()/1000000))+str('M')) 
    with col3:
     st.metric('Average {} people'.format(op1),str(round(temp_df[op1].mean()/1000000))+str('M'))   
    with col4:
     st.metric('Average {} people'.format(op2),str(round(temp_df[op2].mean()/1000000))+str('M')) 

    st.subheader('Geographical Analysis of {}'.format(state))
    fig=px.scatter_mapbox(temp_df,lat='Latitude',lon='Longitude',mapbox_style='carto-positron',zoom=3,width=600,height=900,size=op1,color=op2,color_continuous_scale='magma',hover_name='District')
    st.plotly_chart(fig)


    st.subheader('Bar graph of {} in {}'.format(op1,state))
    fig= px.bar(temp_df,x='District',y=op1,color='Population')
    st.plotly_chart(fig)

    st.subheader('Bar graph of {} in {}'.format(op2,state))
    fig= px.bar(temp_df,x='District',y=op2,color='Population')
    st.plotly_chart(fig)

    st.subheader('Sunburst graph  of {} on basis of {}'.format(state,op1))
    fig=px.sunburst(temp_df,path=['District'],values=op1,width=600,height=670)
    st.plotly_chart(fig)

    st.subheader('Sunburst graph  of {} on basis of {}'.format(state,op2))
    fig=px.sunburst(temp_df,path=['District'],values=op2,width=600,height=670)
    st.plotly_chart(fig)


    # grouped bar chart
    st.subheader('Grouped bar  graph  of {} on basis of comparison between  {} and {}'.format(state,op1,op2))
    fig=px.bar(temp_df,x='District',y=[op1,op2],barmode='group',color_continuous_scale='greens')
    st.plotly_chart(fig)

    # stacked bar chart
    st.subheader('Stacked bar  graph  of {} on basis of  {} and {}'.format(state,op1,op2))
    fig=px.bar(temp_df,x='District',y=[op1,op2],color_continuous_scale='greens')
    st.plotly_chart(fig)

    # scatter
    st.subheader('Scatter graph  of {} on basis of {} and {}'.format(state,op1,op2))
    fig=px.scatter(temp_df,x=op1,y=op2,color='District',hover_name='District')
    st.plotly_chart(fig)
    


    # treeMap
    st.subheader('TreeMap graph  of {} on basis of {} and {}'.format(state,op1,op2))
    fig=px.treemap(temp_df,path=[px.Constant(state),'District'],values=op1,color=op2,color_continuous_scale='hot')
    st.plotly_chart(fig)



st.set_page_config(page_title='India Analysis:Census-2011',page_icon='india image.jpg',layout='wide')

st.sidebar.header('Perform Analysis')
select1=st.sidebar.selectbox('Choose what yo want to perform',['Choose Option','Overall Analysis','State Wise Analysis'])
if select1=='Choose Option':

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
     st.markdown(
    """
    <h1 style='text-align: center; color: #00FFFF; font-size: 48px;'>
       Welcome to the 2011 Census-Based Analysis of India and its States
    </h1>
    <hr style='border: 2px solid #00FFFF;'>
    """,
    unsafe_allow_html=True
)
     st.markdown(
        """
          ---
        """
     )
     st.image("india image.jpg", use_container_width=True)

    st.markdown(
    """
    <h3 style='text-align: center; color: #2E8B57;'>
    <i>India’s strength lies in its diversity — through data, we understand its progress, and through analysis, we shape its future.</i>
    </h4>
    <hr style='margin-top: 10px; margin-bottom: 10px;'>
    """,

    unsafe_allow_html=True
)
    
    st.markdown("""
<div style='font-size:18px; line-height:1.6; color:#F0F0F0;'>

<h2 style='color:#FFD700;'>Welcome to the Indian Census 2011 Dashboard</h2>

This interactive dashboard, built with <b style='color:#1E90FF;'>Streamlit</b>, brings the <b style='color:#1E90FF;'>2011 Indian Census</b> data to life through intuitive <b style='color:#87CEFA;'>graphs and diagrams</b>.

<br>

<h3 style='color:#FFD700;'>🔍 Explore powerful insights like:</h3>
<ul>
<li>📚 <span style='color:#87CEFA;'>Literacy rates</span> by gender and region</li>
<li>👥 <span style='color:#87CEFA;'>Population distribution</span> across the country</li>
<li>💸 Income-wise <span style='color:#87CEFA;'>Power Parity</span> from ₹45,000 to ₹5,45,000+</li>
<li>🌐 Region-wise and statewise trends via <b>sunbursts</b>, <b>treemaps</b>, <b>bar charts</b>, and <b>maps</b></li>
</ul>

<hr style='border:1px solid #444;'>

<h3 style='color:#FFD700;'>🎯 Use the Sidebar to:</h3>
<ul>
<li>View <b style='color:#87CEFA;'>Overall Analysis</b> for a national-level overview</li>
<li>Switch to <b style='color:#87CEFA;'>Statewise Analysis</b> and select your <b style='color:#87CEFA;'>state and parameters</b> of interest</li>
</ul>

<hr style='border:1px solid #444;'>

<p>This dashboard makes vast census data <b style='color:#87CEFA;'>simple</b>, <b style='color:#87CEFA;'>visual</b>, and <b style='color:#87CEFA;'>interactive</b> — perfect for students, researchers, analysts, and the simply curious.</p>

<blockquote style='font-size:16px; color:#FFD700;'><b>Created by Vansh Agrahari</b> — Dive in, discover the data, and see the story India tells.</blockquote>

</div>
""", unsafe_allow_html=True)



elif select1=='Overall Analysis':
    st.header('India Analysis Based On Census 2011')
    L=list(df.columns)
    L.insert(5,'Choose option')
    op1='Choose Option'
    op2='Choose Option'
    op1=st.sidebar.selectbox('Choose Parameter 1',L[5:])
    if(op1!='Choose option'):
        L1=L
        L1.remove(op1)
        op2=st.sidebar.selectbox('Choose Paraenter 2',L1[6:])
    else:
        op2=st.sidebar.selectbox('Choose Parameter 2',L[6:])
    btn=st.sidebar.button('See Result')
        
    if btn:
            Country_Analysis(op1,op2)    
    else:
        pass

elif select1=='State Wise Analysis':
    states=list(df['State'].unique())

    st.header('State Analysis Based On Census 2011')  
    state=st.sidebar.selectbox('Select State',states)
    L3=list(df.columns)
    L3.insert(6,'Choose option')
    op3='Choose Option'
    op4='Choose Option'
    op3=st.sidebar.selectbox('Choose Parameter 1',L3[6:])
    if(op3!='Choose option'):
        L4=L3
        L4.remove(op3)
        op4=st.sidebar.selectbox('Choose Paraenter 2',L4[6:])
    else:
        op4=st.sidebar.selectbox('Choose Parameter 2',L3[6:])
    btn=st.sidebar.button('See Result')

    if btn:
        State_Analysis(state,op3,op4)
    






