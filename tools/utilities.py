import streamlit as st


def load_css():
    with open("tools/style.css") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

    with open("tools/bootstrap.min.css") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

    with open("tools/lime.min.css") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

    st.markdown(
        '<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet"><link '
        'href = "https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap" rel='
        '"stylesheet" >',
        unsafe_allow_html=True)
