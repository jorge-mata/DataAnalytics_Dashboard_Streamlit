import streamlit as st
import pandas as pd
import os

def main():
    st.title("ML Models for Credit Risk Prediction")

    st.header("Introduction")
    st.write(
        """
        Our OSF, Ximple, has tasked us with solving the risk prediction problem in a loan environment by integrating machine learning models to identify key characteristics and risk factors affecting loan repayment. 
        We are working with two databases containing information such as brands sold by borrowers, total sales, client income, and repayment history.
        """
    )

    with st.expander("See key variables used in the models"):
        st.write(
            """
            The following variables were identified as key features for credit risk prediction and model training:
            """
        )
        st.markdown(
            """
            - `loan_request_id`
            - `external_account_id`
            - `approved`
            - `total_importe`
            - `year`
            - `quarter`
            - `quarterpercentage`
            - `month`
            - `num_delinquencies`
            - `ever_delinquent`
            - `most_purchased_category`
            - `medio_pago`
            - `canal`
            - `riskclient`
            - `dias_entre_compras`
            - `delta_importe`
            - `promedio_cliente`
            - `temporada_alta_relativa`
            - `es_temporada_alta_real`
            - `promedio_temporada_alta`
            - `temporada_alta_ajustada`
            - `fecha_afiliacion`
            """
        )

    # Cards with short explanations
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("### Random Forest")
            st.caption("Ensemble of Decision Trees")
            st.write(
                "Random Forest is an ensemble method that builds multiple decision trees and combines their outputs for improved accuracy. It is robust to overfitting and can handle both numerical and categorical variables."
            )
    with col2:
        with st.container(border=True):
            st.markdown("### Logistic Regression")
            st.caption("Probability-Based Classification")
            st.write(
                "Logistic Regression estimates the probability of a binary outcome, making it suitable for predicting loan repayment. It is interpretable and efficient for high-dimensional data."
            )
    with col3:
        with st.container(border=True):
            st.markdown("### XGBoost")
            st.caption("Gradient Boosted Trees")
            st.write(
                "XGBoost is a powerful boosting algorithm that builds trees sequentially, focusing on correcting errors from previous trees. It is highly effective for complex datasets and handles missing values well."
            )

    st.markdown("---")

    # Metrics tables
    st.header("**Random Forest**")
    st.write(
        """
        These metrics are derived from the Random Forest model's performance across different data splits (80-20, 75-25, 70-30).
        The following tables summarize the model's precision, recall, F1 score, support, and AUC for each split.
        Afterwards, we see the ROC curve for the Random Forest model.
        """
    )

    st.markdown("**Performance Metrics**")
    rf_data = {
        "Split": ["80-20", "75-25", "70-30"],
        "Precision": ["0.77 / 0.37", "0.79 / 0.48", "0.77 / 0.45"],
        "Recall": ["0.88 / 0.22", "0.90 / 0.27", "0.91 / 0.21"],
        "F1 score": ["0.82 / 0.27", "0.84 / 0.34", "0.84 / 0.29"],
        "Support": ["233 / 79", "291 / 98", "349 / 118"],
        "AUC": ["0.5658", "0.5758", "0.5900"]
    }
    st.table(pd.DataFrame(rf_data))

    ROCRF = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "img", "ROCRF.png")
    )
    st.image(ROCRF)

    st.header("**Logistic Regression**")
    st.write(
        """
        These metrics are derived from the Logistic Regression model's performance across different data splits (80-20, 75-25, 70-30).
        The following tables summarize the model's precision, recall, F1 score, support, and AUC for each split.
        Afterwards, we see the ROC curve for the Logistic Regression model.
        """
    )

    st.markdown("**Performance Metrics**")
    lr_data = {
        "Split": ["80-20", "75-25", "70-30"],
        "SMOTE": ["0.6500", "0.6280", "0.5933"],
        "Precision": ["0.98 / 0.22", "0.99 / 0.21", "0.99 / 0.20"],
        "Recall": ["0.62 / 0.90", "0.59 / 0.96", "0.55 / 0.97"],
        "F1 score": ["0.76 / 0.35", "0.74 / 0.35", "0.71 / 0.33"],
        "Support": ["179 / 21", "224 / 26", "269 / 31"],
        "AUC": ["0.81", "0.79", "0.75"]
    }
    st.table(pd.DataFrame(lr_data))

    ROCLR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "img", "ROCLR.png")
    )
    st.image(ROCLR)


    st.header("**XGBoost**")
    st.write(
        """
        These metrics are derived from the XGBoost model's performance across different data splits (80-20, 75-25, 70-30).
        The following tables summarize the model's precision, recall, F1 score, support, and AUC for each split.
        Afterwards, we see the ROC curve for the XGBoost model.
        """
    )

    st.markdown("**Performance Metrics**")
    xgb_data = {
        "Split": ["80-20", "75-25", "70-30"],
        "Precision": ["0.80 / 0.33", "0.81 / 0.33", "0.82 / 0.32"],
        "Recall": ["0.69 / 0.47", "0.65 / 0.53", "0.61 / 0.58"],
        "F1 score": ["0.74 / 0.39", "0.72 / 0.40", "0.70 / 0.42"],
        "Support": ["236 / 76", "295 / 94", "354 / 113"],
        "AUC": ["0.6217", "0.6417", "0.6240"]
    }
    st.table(pd.DataFrame(xgb_data))

    ROCXG = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "img", "ROCXG.png")
    )
    st.image(ROCXG)

    st.header("Project Goals")
    st.markdown(
        """
        - **Improve data analysis techniques** to enhance the accuracy of risk models.
        - **Identify and prioritize the most relevant variables** influencing creditworthiness.
        - **Create a dynamic dashboard** for data, insights, and risk prediction visualization.
        """
    )

    st.header("Scenario Development")
    st.write(
        """
        Our team is developing models using **Random Forest**, **Logistic Regression**, and **XGBoost** to answer:
        *How can we optimize credit risk prediction by identifying the most relevant variables that influence loan repayment, and use machine learning models to improve prediction accuracy and visualization for decision-making?*
        """
    )

    st.markdown(
        """
        - **Random Forest:** Builds multiple decision trees and combines their outputs for improved accuracy. Handles large datasets with many variables and provides feature importance scores.
        - **Logistic Regression:** Calculates the probability of a binary outcome (e.g., first payment default). Offers fast insights and helps measure feature significance.
        - **XGBoost:** Sequentially builds an ensemble of decision trees, improving on previous trees. Handles complex relationships, avoids overfitting, and manages missing data effectively.
        """
    )

    st.header("Conclusion")
    st.write(
        """
        By combining Random Forest, Logistic Regression, and XGBoost, we are building a robust credit risk prediction system for Ximple. 
        Each model brings unique strengths, and together they provide a strong foundation for accurate and actionable risk assessment.
        """
    )

if __name__ == "__main__":
    main()