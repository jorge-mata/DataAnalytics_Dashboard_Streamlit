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

    st.markdown("---")
    st.header("Detailed Insights")

    st.markdown("""
    - **Decrease in Loan Requests Over Time**  
      On each quarter, there is a steady decline in the number of new loan applications.
                
    - **Decreasing Repayment Rates**  
      In the first quarter, repayment rates have fallen from over 80% in early 2024 to around 56%.

    - **Average Purchase Value by Payment Type**  
      There is a higher average purchase amounts in payment types like “Document” and “Meses sin Intereses”. While “Efectivo” and electronic wallet transactions have a tendency to be similar.

    - **Number and Quantity by Payment Type**  
      Cash remains the most common payment method in terms of transaction count, followed by “Préstamo Ximple” and credit cards, revealing client preferences for liquidity.

    - **Delinquency Rates by Payment Method**  
      Loans paid via “Préstamo Ximple” and credit cards exhibit higher delinquency percentages.

    - **Repayment Rates by Quarter**  
      Quarterly repayment performance varies significantly, with the strongest rates in 2024 Q1 (80.9%) and the weakest in 2025 Q1 (56.1%).
    """)

if __name__ == "__main__":
    main()

# This code is for the "Key Findings" page in a Streamlit application.