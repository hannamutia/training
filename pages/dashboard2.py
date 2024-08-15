import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title = "Dashboard Loans Analysis",
    layout = "centered"
)


#Import Data
loan = pd.read_pickle('data_input\loan_clean')
loan.head()



## ----- LOAN PERFORMANCE ------
st.subheader('Loan Performance')

# **1. Loan Condition Analysis**

loan_condition_counts = loan['loan_condition'].value_counts()

loan_pie = px.pie(
    loan_condition_counts,
    names=loan_condition_counts.index,
    values=loan_condition_counts.values,
    hole=0.4,
    labels={
        'loan_condition': 'Loan Condition',
        'value': 'Number of Loans'
    },
    title='Distribution of Loans by Condition',
    template="seaborn",
)

# **2. Grade Distribution**

grade_counts = loan['grade'].value_counts(sort=False)

grade_bar = px.bar(
    grade_counts,
    x=grade_counts.index,
    y=grade_counts.values,
    labels={
        'grade': 'Grade',
        'y': 'Number of Loans'
    },
    title='Distribution of Loans by Grade',
    template="seaborn",
)


### ------- Display Dashboard

with st.expander("Show/Hide", expanded=True):
    performance1, performance2 = st.columns(2)

    with performance1:
        st.plotly_chart(loan_pie)

    with performance2:
        st.plotly_chart(grade_bar)


st.subheader('Loan Amount Distribution')

###1. Loan Amount Distribution

### Select Box
condition = st.selectbox("Select Loan Condition", ['Good Loan','Bad Loan'])

loan_condition = loan[loan['loan_condition'] == condition]

loan_hist = px.histogram(loan_condition, 
    x='loan_amount',
    color = 'term',
    nbins = 20,
    template='seaborn',
    title = 'Loan Amount Distribution by Condition',
    labels={
        'loan_amount':'Loan Amount',
        'term':'Loan Term'
	}
)

loan_box = px.box(loan_condition, 
    x='purpose',
    y = 'loan_amount',
    color = 'term',
    template='seaborn',
    title = 'Loan Amount Distribution by Purpose',
    labels={
        'loan_amount':'Loan Amount',
        'term':'Loan Term',
        'purpose' : 'Purpose'
	}
).update_xaxes(tickangle=90)

tab1, tab2 = st.tabs([
        'Loan Amount Distribution by Condition',
        'Loan Amount Distribution by Purpose'
    ])
    
with tab1:
    st.plotly_chart(loan_hist)
with tab2:
    st.plotly_chart(loan_box)
