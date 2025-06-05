import streamlit as st

def main():
    st.title("Key Findings")

    st.markdown("""
    This section provides a detailed description of the insights found in the dashboard from Ximple’s current situation. These highlights include information on the customer’s profile, sales, and indicators that may warn the company about profiles that could pose a risk. These findings help the company analyze their current situation and improve risk management.

    **Examples of key findings:**
    - **Decrease in Loan Requests Over Time**
    - **Decreasing Repayment Rates**
    - **Average Purchase Value by Payment Type**
    - **Number and Quantity by Payment Type**
    - **Delinquency Rates by Payment Method**
    - **Repayment Rates by Quarter**
    """)
    
if __name__ == "__main__":
    main()

# This code is for the "Key Findings" page in a Streamlit application.