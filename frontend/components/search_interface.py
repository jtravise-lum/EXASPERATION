"""Component for the EXASPERATION search interface."""

import streamlit as st
from typing import Callable, Dict, Any, List, Optional
import time

from frontend.config import EXAMPLE_QUERIES

def search_interface(on_search: Callable[[str, Dict[str, Any]], None], loading: bool = False) -> str:
    """Display the search interface with query input and submit button.
    
    Args:
        on_search: Callback function to handle search
        loading: Whether the search is currently loading
        
    Returns:
        The current query
    """
    st.title("EXABOMINATION")
    st.subheader("Exabeam Common Information Model Documentation Search")
    
    # Create form for search input
    with st.form(key="search_form"):
        # Query input
        query = st.text_area(
            "Enter your question about Exabeam documentation:",
            value=st.session_state.get("current_query", ""),
            height=100,
            max_chars=1000,
            placeholder="e.g., How does the password reset detection rule work?"
        )
        
        # Submit button
        col1, col2 = st.columns([4, 1])
        with col1:
            submit_button = st.form_submit_button(
                label="Search",
                type="primary",
                use_container_width=True,
                disabled=loading
            )
    
    # Display loading indicator
    if loading:
        with st.spinner("Searching documentation..."):
            # Add a small delay to make the spinner visible
            time.sleep(0.1)
    
    # Show example queries
    with st.expander("Example questions you can ask", expanded=not st.session_state.get("current_query")):
        cols = st.columns(2)
        for i, example in enumerate(EXAMPLE_QUERIES):
            col_idx = i % 2
            with cols[col_idx]:
                if st.button(example, key=f"example_{i}", use_container_width=True):
                    # Set query and trigger search
                    st.session_state.current_query = example
                    on_search(example, {})
                    st.rerun()
    
    # Handle form submission
    if submit_button and query:
        # Store current query in session state
        st.session_state.current_query = query
        # Call search function
        on_search(query, {})
    
    return st.session_state.get("current_query", "")

def query_history_sidebar() -> None:
    """Display the query history in the sidebar."""
    # Initialize query history if not exists
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    
    # Add current query to history if not already added
    current_query = st.session_state.get("current_query")
    if current_query and current_query not in st.session_state.query_history:
        # Add to beginning of list
        st.session_state.query_history.insert(0, current_query)
        # Limit history size
        if len(st.session_state.query_history) > 10:
            st.session_state.query_history = st.session_state.query_history[:10]
    
    # Display query history
    if st.session_state.query_history:
        st.sidebar.markdown("### Recent Queries")
        for i, query in enumerate(st.session_state.query_history):
            if st.sidebar.button(f"{query[:40]}{'...' if len(query) > 40 else ''}", key=f"history_{i}"):
                st.session_state.current_query = query
                st.rerun()
        
        # Clear history button
        if st.sidebar.button("Clear History", key="clear_history"):
            st.session_state.query_history = []
            st.rerun()