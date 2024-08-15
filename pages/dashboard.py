import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title = "Dashboard Loans Analysis",
    layout = "centered"
)

st.title("Financial Insight Dashboard : Loan Performance & Trends")

st.markdown("---")

st.sidebar.header("Dashboard Filters and Features")

# List of Features
st.sidebar.markdown(
'''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
'''
)

#Import Data
loan = pd.read_pickle('data_input\loan_clean')
loan.head()

#st.metric('Total Loans', f"{ loan.id.count():,.0f}")

#st.metric('Total Loan Amount', f"${ loan.loan_amount.sum():,.0f}")

with st.container(border=True):
 # First row of two columns
    col1, col2 = st.columns(2)

 # Metrics for the first row
    col1.metric("Total Loans", f"{loan.shape[0]:,}")
    col1.metric("Total Loan Amount", f"${loan['loan_amount'].sum():,.0f}")

    col2.metric("Average Interest Rate", f"{loan['interest_rate'].mean():.0f}%")
    col2.metric("Average Loan Amount", f"${loan['loan_amount'].mean():,.0f}")

# **1. Loans Issued Over Time**

data_agg = loan.groupby(['issue_date']).count()['id'].reset_index()

loans_issued = px.line(
    data_agg,
    x='issue_date',
    y='id',
    markers=True,
    title='Number of Loans Issued Over Time',
    labels={
        'issue_date': 'Issue Date',
        'id': 'Number of Loans'
    },
    template='seaborn'
)

# **2. Loan Amount Over Time**

loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()

loan_amount = px.line(
    loan_date_sum,
    markers=True,
    title = 'Loans Amount Over Time',
    labels ={
        'issue_date' : 'Issue Date',
        'value' : 'Number of Loans'
    },
    template = 'seaborn'
).update_layout(showlegend=False)

# **3. Issue Date Analysis**
loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count().reset_index()

issue_date = px.bar(
    loan_day_count,
    x = 'issue_weekday',
    y = 'loan_amount',
    text='loan_amount',
    title = 'Distribution of Loans by Day of the Week',
    labels = {
        'loan_amount':'Number of Loans',
        'issue_weekday' : 'Day of the Week'
    },
    category_orders={'issue_weekday': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']},
    template = 'seaborn'
).update_layout(showlegend=False)

###Display Dashboard
tab1, tab2, tab3 = st.tabs([
        'Loans Issued Over Time',
        'Loan Amount Over Time',
        'Issue Date Analysis'
    ])
    
with tab1:
    st.plotly_chart(loans_issued)
with tab2:
    st.plotly_chart(loan_amount)
with tab3:
    st.plotly_chart(issue_date)

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


# st.subheader('Loan Amount Distribution')

# ###1. Loan Amount Distribution

# ### Select Box
# condition = st.selectbox("Select Loan Condition", ['Good Loan','Bad Loan'])

# loan_condition = loan[loan['loan_condition'] == condition]

# loan_hist = px.histogram(loan_condition, 
#     x='loan_amount',
#     color = 'term',
#     nbins = 20,
#     template='seaborn',
#     title = 'Loan Amount Distribution by Condition',
#     labels={
#         'loan_amount':'Loan Amount',
#         'term':'Loan Term'
# 	}
# )

# loan_box = px.box(loan_condition, 
#     x='purpose',
#     y = 'loan_amount',
#     color = 'term',
#     template='seaborn',
#     title = 'Loan Amount Distribution by Purpose',
#     labels={
#         'loan_amount':'Loan Amount',
#         'term':'Loan Term',
#         'purpose' : 'Purpose'
# 	}
# ).update_xaxes(tickangle=90)

# tab1, tab2 = st.tabs([
#         'Loan Amount Distribution by Condition',
#         'Loan Amount Distribution by Purpose'
#     ])
    
# with tab1:
#     st.plotly_chart(loan_hist)
# with tab2:
#     st.plotly_chart(loan_box)
