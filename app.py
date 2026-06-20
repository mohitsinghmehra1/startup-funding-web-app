import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout = "wide", page_title = 'Startup Analysis')

try:
    df = pd.read_csv('dataset/cleaned_startup_funding.csv')
    print("CSV loaded successfully")
    df['Date'] = pd.to_datetime(df['Date'])
    df['year'] = df['Date'].dt.year
except FileNotFoundError:
    st.error('The dataset is not avaliable.....')
else:
    def load_investor_details(name: str):
        if name is None:
            st.title('PLESE ENTER THE REQUIRED FIELD......', text_alignment='center')
            return
            
        st.title(name)

        st.space('small')
        
        investment = df[df['Investors Name'].str.contains(name)][['Date', 'Startup Name', 'Industry Vertical','Location', 'InvestmentnType', 'Amount', 'year']]
        big_investment = investment.groupby('Startup Name')['Amount'].sum().sort_values(ascending = False).head()
        sector_investment = investment.groupby(investment['Industry Vertical'])['Amount'].sum()
        stage_investment = investment.groupby(investment['InvestmentnType'])['Amount'].sum()
        city_investment = investment.groupby(investment['Location'])['Amount'].sum()
        year_wise_investment = investment.groupby('year')['Amount'].sum().sort_index()
            
        st.subheader('RECENT INVESTMENT')
        st.dataframe(investment.iloc[:,:-1].head())
        
        st.subheader('BIGGEST INVESTMENT')
        fig, ax = plt.subplots()
        ax.bar(big_investment.index, big_investment.values)
        ax.set_xlabel('Startup')
        ax.set_ylabel('Amount Invested in Crores')
        st.pyplot(fig)
        
        col1, col2, col3 = st.columns(3, border=True)
        with col1: 
            st.subheader('SECTOR INVESTMENT IN')
            fig1, ax1 = plt.subplots()
            ax1.pie(sector_investment, labels = sector_investment.index, autopct='%1.1f%%')
            st.pyplot(fig1)
        
        with col2:
            st.subheader('STAGE INVESTMENT')
            fig3, ax3 = plt.subplots()
            ax3.pie(stage_investment, labels = stage_investment. index, autopct='%1.1f%%')
            st.pyplot(fig3)

        with col3:
            st.subheader('CITY INVESTMENT')
            fig4, ax4 = plt.subplots()
            ax4.pie(city_investment, labels = city_investment. index, autopct='%1.1f%%')
            st.pyplot(fig4)
        
        st.subheader('YEAR WISE AMOUNT INVESTMENT')
        fig5, ax5 = plt.subplots()
        ax5.plot(year_wise_investment.index, year_wise_investment.values)
        ax5.set_xticks([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
        st.pyplot(fig5)
    
    def load_overall_details():
        total_funding = round(df['Amount'].sum())
        max_investment = round(df.groupby('Startup Name')['Amount'].max().sort_values(ascending = False).head(1).values[0])
        avg_investment = round(df.groupby('Startup Name')['Amount'].sum().mean())
        total_investmnet = df['Startup Name'].nunique()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Total Investment', f'₹ {total_funding} Cr')
        with col2:
            st.metric('Max Investment', f'₹ {max_investment} Cr')
        with col3:
            st.metric('Avg Investment',f'₹ {avg_investment} Cr')
        with col4:
            st.metric('Total Investment in Startups', total_investmnet)
        
        
        st.space('medium')


        st.subheader('MONTH BY MONTH INVESTMENST ANALYSIS', text_alignment='center')
        st.space('small')
        print(df.info())
        df['month'] = df['Date'].dt.month_name()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        df['month'] = pd.Categorical(df['month'],categories = month_order,ordered = True)
        x = df.groupby(['year','month'])

        selected_option = st.selectbox('Select Type', ['TOTAL INVESTMENT', 'NUMBER OF INVESTMNETS'], index = None)
        if selected_option == 'TOTAL INVESTMENT':
            temp = x['Amount'].sum().sort_index(level = ['year', 'month']).reset_index().rename(columns = {'Amount': 'y'})
        elif selected_option == 'NUMBER OF INVESTMNETS':
            temp = x['Startup Name'].nunique().sort_index(level=['year', 'month']).reset_index().rename(columns = {'Startup Name': 'y'})
        else:
            return 
        
        temp['month_year'] = temp['month'].astype('str') + '-' + temp['year'].astype('str')    
        fig, ax = plt.subplots()
        ax.plot(temp['month_year'], temp['y'])
        plt.xticks(ax.get_xticks()[::5],rotation = 90)
        st.pyplot(fig)

    # Constructing the sidebar
    with st.sidebar:
        st.title('STARTUP FUNDING ANALYSIS', anchor='title-styling')
        st.space('medium')
        option = st.selectbox('SELECT ANALYSIS', ['OVERALL ANALYSIS', 'INVESTOR ANALYSIS', 'STARTUP ANALYSIS'], index = None)

    if option == 'OVERALL ANALYSIS':
        load_overall_details()

    elif option == 'INVESTOR ANALYSIS':
        with st.sidebar:
            investors_name = pd.Series(df['Investors Name'].str.split(',').sum()).unique()
            investor = st.selectbox('SELECT INVESTOR', investors_name, index = None)
            submitted = st.button('FIND ANALYSIS DETAILS....')
        
        if submitted:
            load_investor_details(investor)

    elif option == 'STARTUP ANALYSIS':
        st.title(option)
        with st.sidebar:
            startup_companys_name = pd.Series(df['Startup Name'].str.split(',').sum()).unique()
            statup_cmp = st.selectbox('SELECT STARTUP NAME',startup_companys_name, index = None)
            submitted = st.button('FIND ANALYSIS DETAILS...')
