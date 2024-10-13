import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Type'])

st.title('Personal Finance Tracker')

# Input form
with st.form('transaction_form'):
    date = st.date_input('Date', datetime.now())
    category = st.selectbox('Category', ['Food', 'Transportation', 'Housing', 'Entertainment', 'Others'])
    amount = st.number_input('Amount', min_value=0.01, format='%f')
    transaction_type = st.radio('Type', ['Expense', 'Income'])
    
    submitted = st.form_submit_button('Add Transaction')
    if submitted:
        new_transaction = pd.DataFrame({
            'Date': [date],
            'Category': [category],
            'Amount': [amount],
            'Type': [transaction_type]
        })
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)

# Display transactions
st.subheader('Transactions')
st.dataframe(st.session_state.transactions)

# Visualizations
if not st.session_state.transactions.empty:
    st.subheader('Spending by Category')
    expenses = st.session_state.transactions[st.session_state.transactions['Type'] == 'Expense']
    fig = px.pie(expenses, values='Amount', names='Category', title='Expense Distribution')
    st.plotly_chart(fig)

    st.subheader('Income vs Expenses')
    total_income = st.session_state.transactions[st.session_state.transactions['Type'] == 'Income']['Amount'].sum()
    total_expenses = expenses['Amount'].sum()
    fig = px.bar(x=['Income', 'Expenses'], y=[total_income, total_expenses], title='Income vs Expenses')
    st.plotly_chart(fig)

# Balance calculation
balance = st.session_state.transactions[st.session_state.transactions['Type'] == 'Income']['Amount'].sum() - \
          st.session_state.transactions[st.session_state.transactions['Type'] == 'Expense']['Amount'].sum()
st.subheader(f'Current Balance: ${balance:.2f}')