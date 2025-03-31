"""Component for displaying search results and error messages."""

import streamlit as st
from typing import Optional, Dict, Any, List

from frontend.api.models import SearchResponse, ErrorResponse, SourceDocument
from frontend.config import SHOW_API_ERRORS, ENABLE_MOCK_FALLBACKS, COLORS

def results_display(result: Optional[SearchResponse], error: Optional[ErrorResponse]) -> None:
    """Display search results or error messages.
    
    Args:
        result: Search response from API
        error: Error response from API
    """
    if result is not None:
        # Display the answer
        st.markdown(f"### Answer")
        st.markdown(result.answer)
        
        # Display document sources
        if result.sources and len(result.sources) > 0:
            st.markdown("---")
            st.markdown("### Sources")
            
            for i, source in enumerate(result.sources):
                with st.expander(f"{source.title}", expanded=False):
                    # Use our custom source card styling
                    st.markdown(f'''
                    <div class="source-card" style="margin-bottom: 1.5rem;">
                        <div class="relevance-meter" style="width: {int(source.relevance_score * 100)}%; background-color: {COLORS['accent']};"></div>
                        <div style="margin-bottom: 1rem;">
                            <span class="metadata-tag">{source.metadata.document_type if source.metadata else 'Unknown'}</span>
                            {f'<span class="metadata-tag">{source.metadata.vendor}</span>' if source.metadata and source.metadata.vendor else ''}
                            {f'<span class="metadata-tag">{source.metadata.product}</span>' if source.metadata and source.metadata.product else ''}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Display the content with better formatting
                    st.markdown(source.content)
                    
                    # Add relevance score and citation functionality
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.caption(f"Relevance: {source.relevance_score:.2f}")
                    with cols[1]:
                        if st.button(f"Cite Source #{i+1}", key=f"cite_{source.id}", use_container_width=True):
                            citation = f"{source.title} (ID: {source.chunk_id})"
                            st.toast(f"Copied citation: {citation}")
                        
        # Show suggested queries
        if result.suggested_queries and len(result.suggested_queries) > 0:
            st.markdown("---")
            st.markdown("### Try these related queries:")
            cols = st.columns(min(3, len(result.suggested_queries)))
            for i, query in enumerate(result.suggested_queries):
                col_idx = i % len(cols)
                with cols[col_idx]:
                    if st.button(query, key=f"suggest_{i}"):
                        st.session_state.current_query = query
                        st.rerun()
        
        # If this was mock data, show a warning
        if ENABLE_MOCK_FALLBACKS and result.sources and result.sources[0].metadata and result.sources[0].metadata.document_type == "mock":
            st.warning("⚠️ This result contains mock data because the API is unavailable")
            
    elif error is not None:
        # Display error in a more user-friendly way
        st.error("Error Processing Query")
        
        # Show friendly error based on error code
        if error.error.get("code") == "connection_error":
            st.error("⚠️ Could not connect to the search API. Please try again later.")
        elif error.error.get("code") == "authentication_error":
            st.error("⚠️ Authentication error. Please check your API key.")
        elif error.error.get("code") == "rate_limit_error":
            st.error("⚠️ Rate limit exceeded. Please try again in a few minutes.")
        elif error.error.get("code") == "internal_error":
            st.error("⚠️ Internal server error. Our team has been notified.")
        else:
            st.error(f"⚠️ {error.error.get('message', 'An unknown error occurred')}")
            
        # Show detailed error information for developers/admins
        if SHOW_API_ERRORS:
            with st.expander("Technical Details"):
                st.json({
                    "error_code": error.error.get("code"),
                    "error_message": error.error.get("message"),
                    "request_id": error.request_id,
                    "details": error.error.get("details", {})
                })
                st.info("If this error persists, please contact support with the request ID shown above.")
        
        # Show suggested recovery actions
        st.markdown("### Suggestions:")
        st.markdown("1. Try simplifying your query")
        st.markdown("2. Check your network connection")
        st.markdown("3. Verify that the API is running")
    
    # If no results and no error, show empty state
    elif st.session_state.get("current_query"):
        st.info("No results found. Please try a different query.")
        
        # Show some example queries to help the user
        st.markdown("### Try these example queries:")
        examples = [
            "How does Exabeam detect lateral movement?",
            "What is a data source?",
            "How do I set up Active Directory monitoring?",
            "Explain privilege escalation detection"
        ]
        cols = st.columns(2)
        for i, example in enumerate(examples):
            col_idx = i % 2
            with cols[col_idx]:
                if st.button(example, key=f"empty_suggest_{i}"):
                    st.session_state.current_query = example
                    st.rerun()