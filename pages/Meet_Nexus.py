import streamlit as st
import os

def main():
    st.markdown("<h1 style='text-align: center;'>Meet Nexus</h1>", unsafe_allow_html=True)
    st.markdown(" ")

    # Center the team image
    team_url = "https://github.com/jorge-mata/DataAnalytics_Dashboard_Streamlit/blob/main/img/team.png?raw=true"
    st.markdown(
        f"""
        <div style='display: flex; justify-content: center;'>
            <img src="{team_url}" style="max-width: 1300px; width: 100%;" />
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(" ")
    st.markdown(
        "<h2 style='text-align: center;'>Meet the Team Behind Nexus</h2>",
        unsafe_allow_html=True,
    )

    # 5 columns for team members
    cols = st.columns(5)
    team_files = [
        ("https://github.com/jorge-mata/DataAnalytics_Dashboard_Streamlit/blob/main/img/Andy.jpg?raw=true", "Andrea Alvarado"),
        ("https://github.com/jorge-mata/DataAnalytics_Dashboard_Streamlit/blob/main/img/Dany.png?raw=true", "Daniela Hernández"),
        ("https://github.com/jorge-mata/DataAnalytics_Dashboard_Streamlit/blob/main/img/Emi.png?raw=true", "Emiliano Salinas"),
        ("https://github.com/jorge-mata/DataAnalytics_Dashboard_Streamlit/blob/main/img/Jorge.png?raw=true", "Jorge Mata"),
        ("https://github.com/jorge-mata/DataAnalytics_Dashboard_Streamlit/blob/main/img/Luis.png?raw=true", "Luis Manzanares"),
    ]

    # LinkedIn URLs for each team member
    linkedin_urls = [
        "https://www.linkedin.com/in/andreaalvaradom/",
        "http://www.linkedin.com/in/daniela-hern%C3%A1ndez-27b47a292",
        "https://www.linkedin.com/in/emiliano-salinas-del-bosque-406bb8357/",
        "https://www.linkedin.com/in/jorge-mata-825003358",
        "https://www.linkedin.com/in/luis-fernando-manzanares-sanchez/",
    ]

    # Bootstrap LinkedIn icon SVG as a clickable link
    linkedin_icon_template = """
    <div style='text-align: center; margin-top: 4px;'>
      <a href="{url}" target="_blank" rel="noopener noreferrer">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-linkedin" viewBox="0 0 16 16">
        <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z"/>
        </svg>
      </a>
    </div>
    """

    for col, (img_url, name), url in zip(cols, team_files, linkedin_urls):
        col.markdown(
            f"""
            <div style='display: flex; justify-content: center;'>
                <img src="{img_url}" style="width: 100%; max-width: 400px; border-radius: 8px;" />
            </div>
            """,
            unsafe_allow_html=True
        )
        col.markdown(f"<div style='text-align: center; font-weight: bold; margin-top: 8px;'>{name}</div>", unsafe_allow_html=True)
        col.markdown(linkedin_icon_template.format(url=url), unsafe_allow_html=True)

    st.markdown("---")
    tagline_url = "https://github.com/jorge-mata/DataAnalytics_Dashboard_Streamlit/blob/main/img/tagline.jpeg?raw=true"
    st.markdown(
        f"""
        <div style='display: flex; justify-content: center;'>
            <img src="{tagline_url}" style="max-width: 1600px; width: 100%; border-radius: 8px;" />
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()