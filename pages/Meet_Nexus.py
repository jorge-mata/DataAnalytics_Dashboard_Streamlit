import streamlit as st
import os

def main():
    st.markdown("<h1 style='text-align: center;'>Meet Nexus</h1>", unsafe_allow_html=True)
    st.markdown(" ")

    team = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "img", "team.png")
    )
    st.image(team)

    st.markdown(" ")
    st.markdown(
        "<h2 style='text-align: center;'>Meet the Team Behind Nexus</h2>",
        unsafe_allow_html=True,
    )

    # 5 columns for team members
    cols = st.columns(5)
    team_files = [
        ("Andy.jpg", "Andy"),
        ("Dany.png", "Dany"),
        ("Emi.png", "Emi"),
        ("Jorge.png", "Jorge"),
        ("Luis.png", "Luis"),
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
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="#0A66C2" class="bi bi-linkedin" viewBox="0 0 16 16">
          <path d="M0 1.146C0 .513.324 0 .725 0h14.55c.401 0 .725.513.725 1.146v13.708c0 .633-.324 1.146-.725 1.146H.724A.723.723 0 0 1 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.521-1.248-1.342-1.248-.822 0-1.357.54-1.357 1.248 0 .694.52 1.248 1.327 1.248h.014zm4.908 8.212h2.4V9.359c0-.215.016-.43.08-.584.175-.43.573-.877 1.242-.877.876 0 1.226.662 1.226 1.634v3.862h2.4V9.23c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.014a5.4 5.4 0 0 1 .014-.025V6.169h-2.4c.03.7 0 7.225 0 7.225z"/>
        </svg>
      </a>
    </div>
    """

    for col, (filename, name), url in zip(cols, team_files, linkedin_urls):
        img_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "img", filename)
        )
        col.image(img_path, use_container_width=True)
        col.markdown(linkedin_icon_template.format(url=url), unsafe_allow_html=True)

    st.markdown("---")
    tagline = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "img", "tagline.jpeg")
    )
    st.image(tagline)

if __name__ == "__main__":
    main()