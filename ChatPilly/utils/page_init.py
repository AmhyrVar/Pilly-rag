import os
from typing import Literal
import streamlit as st  # noqa

REDIRECT_URL = os.environ.get("REDIRECT_URL")


def page_init(page_title: str, layout: Literal["centered", "wide"] = "wide") -> None:
    # page format
    
    st.set_page_config(
        page_title=page_title,
        layout=layout,
        
        
    )

    # title
    st.title(page_title)
    
