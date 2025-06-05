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

    team_members = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "img", "TheTeam.png")
    )

    st.image(team_members, use_container_width=True)

    st.markdown("---")
    tagline = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "img", "tagline.jpeg")
    )
    st.image(tagline)

if __name__ == "__main__":
    main()