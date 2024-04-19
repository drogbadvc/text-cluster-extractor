import streamlit as st
from tools.utilities import load_css
from views.dashboard import dashboard

st.set_page_config(page_title="Analyzing and Quickview Link Weights", layout="wide")

load_css()


class Model:
    menuTitle = "Sparrow"
    option1 = "Dashboard"


def menu_item():
    return f"""
    <ul class="accordion-menu">
        <li class="sidebar-title">Apps</li>
        <li><a href="index.html" class="active"><i class="material-icons">dashboard</i>Dashboard</a></li>
    </ul> """


def header_item():
    return f"""
        <div class="lime-header"> 
            <nav class="navbar navbar-expand-lg"> 
                <section data-testid="collapsedControl" class="material-design-hamburger navigation-toggle"> 
                    <a href="#" class="button-collapse material-design-hamburger__icon"> 
                        <span class="material-design-hamburger__layer material-design-hamburger__icon--from-arrow">
                        </span></a> 
                </section> 
                <a class="navbar-brand" href="#">Lime</a> 
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" 
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"> 
                <i class="material-icons">keyboard_arrow_down</i> 
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <div class="form-inline my-2 my-lg-0 header-bread" id="search">
                <ol class="breadcrumb breadcrumb-separator-1">
                    <li class="breadcrumb-item"><a href="#">Pages</a></li>
                    <li class="breadcrumb-item active" aria-current="page">Dashboard</li>
                </ol>                    </div>
                    <ul class="navbar-nav ml-auto">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle theme-settings-link" href="#">
                                <i class="material-icons">layers</i>
                            </a>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <i class="material-icons">more_vert</i>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-right">
                                <li><a class="dropdown-item" href="#">Account</a></li>
                                <li><a class="dropdown-item" href="#">Settings</a></li>
                                <li class="divider"></li>
                                <li><a class="dropdown-item" href="#">Log Out</a></li>

                            </ul>
                        </li>
                    </ul>
                </div>

            </nav>
    </div>"""


def view(model):
    st.markdown(header_item(), unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(menu_item(), unsafe_allow_html=True)

    dashboard()


view(Model())
