import streamlit as st
import os

def main():
    st.title("Acerca de")
    st.markdown(" ")  # Line break after title

    # Row 1: Image on the right, intro on the left (less margin)
    row1_col1, row1_col2 = st.columns([3, 2], gap="small")
    with row1_col1:
        st.header("Business Understanding")
        st.markdown("---")
        st.write("""
        During this course, we had the opportunity to work with Ximple, a fintech that is facing various challenges, specially when it comes to risk management. 
        The company is looking to improve its risk management processes, particularly in identifying potential clients who may not repay their loans, thus posing a risk to the business.""")
    with row1_col2:
        img_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "img", "Ximple-Card-2048x1072.webp")
        )
        st.image(img_path, use_container_width=True)

    # Row 2: Header left, text right (less margin)
    st.markdown("---")
    row2_col1, row2_col2 = st.columns([1, 3], gap="small")
    with row2_col1:
        st.header("Problem Statement")
    with row2_col2:
        st.write("""
            One of the main challenges is improving its credit risk assessment models. The main problem is to assess the creditworthiness of small business owners to predict loan repayment likelihood.
            The goal is to develop a machine learning model that can accurately predict which clients are likely to default on their loans, allowing Ximple to make informed decisions about loan approvals and risk management.
        """)

    # Row 3: Header left, text right (less margin)
    st.markdown("---")
    row3_col1, row3_col2 = st.columns([1, 3], gap="small")
    with row3_col1:
        st.header("Storytelling")
    with row3_col2:
        st.write("""
        A continuación, se muestran los pasos y evidencias del trabajo realizado junto a Xavier. Esta página web ofrece una explicación breve de todos los entregables previos, comenzando por quién es Ximple, el planteamiento del problema, los hallazgos en la base de datos proporcionada, los modelos de machine learning desarrollados, la creación del dashboard y, finalmente, las recomendaciones finales derivadas del proyecto.

        **Home / Acerca de**
        - En esta sección, es fundamental mostrar el conocimiento del equipo sobre la empresa (¿quién es Ximple? ¿cuáles son sus retos?), proporcionando un contexto que permita entender el trabajo realizado y demostrar una clara comprensión del negocio.
        - Posteriormente, se describe la situación actual de Ximple, identificando los factores cruciales (internos y externos) y presentando una visión general del análisis FODA.
        - El núcleo del proyecto es el planteamiento del problema: cómo puede la empresa gestionar el riesgo que representan algunos clientes debido al incumplimiento en el pago de préstamos.
        - Finalmente, se introduce la solución propuesta, ofreciendo solo un adelanto, ya que las siguientes páginas profundizarán en cada parte de la solución.
        """)
    st.markdown("---")

if __name__ == "__main__":
    main()

# This code is for the "Acerca de" page in a Streamlit application.