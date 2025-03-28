"""Main Streamlit application for EXABOMINATION."""

import streamlit as st
from typing import Dict, Any
import time

# Import components
from frontend.components.search_interface import search_interface, query_history_sidebar
from frontend.components.results_display import results_display
from frontend.components.filters_panel import filters_panel

# Import API client
from frontend.utils.api_client import api_client
from frontend.api.models import SearchFilters, SearchOptions, ErrorResponse

# Import configuration
from frontend.config import (
    DEFAULT_MAX_RESULTS,
    DEFAULT_THRESHOLD,
    DEFAULT_INCLUDE_METADATA,
    DEFAULT_RERANK
)

# Set page config
st.set_page_config(
    page_title="EXABOMINATION - Exabeam CIM Documentation Search",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    /* Main color scheme */
    :root {
        --primary-color: #0f4880;
        --secondary-color: #00b3e6;
        --accent-color: #ffcc00; 
        --dark-bg: #121621;
        --text-color: #ffffff;
        --panel-bg: #1e2639;
    }
    
    /* Base styling */
    .main {
        background-color: var(--dark-bg);
        color: var(--text-color);
        font-family: 'Courier New', monospace;
    }
    
    .sidebar .sidebar-content {
        background-color: var(--panel-bg);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background-color: var(--panel-bg);
        border: 2px solid var(--secondary-color);
        border-radius: 5px;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 15px rgba(0, 179, 230, 0.5);
    }
    
    .main-header h1 {
        margin: 0;
        font-weight: 700;
        color: var(--accent-color);
        font-family: 'Impact', sans-serif;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(255, 204, 0, 0.7);
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
        font-style: italic;
    }
    
    /* Card styling with improved aesthetics */
    .card {
        background-color: var(--panel-bg);
        border-radius: 8px;
        border: 1px solid var(--secondary-color);
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 179, 230, 0.3);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 6px 16px rgba(0, 179, 230, 0.4);
    }
    
    /* Source card styling */
    .source-card {
        background-color: rgba(30, 38, 57, 0.8);
        border-radius: 8px;
        border: 1px solid var(--secondary-color);
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .source-card:hover {
        box-shadow: 0 0 20px rgba(0, 179, 230, 0.6);
        transform: translateY(-3px);
    }
    
    .source-card .metadata-tag {
        display: inline-block;
        background-color: rgba(15, 72, 128, 0.7);
        color: var(--text-color);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .source-card .relevance-meter {
        height: 4px;
        background-color: var(--accent-color);
        position: absolute;
        bottom: 0;
        left: 0;
    }
    
    /* Button styling */
    .stButton button {
        background-color: var(--primary-color);
        color: var(--text-color);
        font-weight: 500;
        border-radius: 5px;
        border: 1px solid var(--secondary-color);
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        font-family: 'Courier New', monospace;
    }
    
    .stButton button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 0 15px rgba(0, 179, 230, 0.7);
        transform: translateY(-2px);
    }
    
    /* Search box styling */
    .stTextInput > div > div > input {
        background-color: var(--panel-bg) !important;
        color: var(--text-color) !important;
        border-radius: 5px;
        border: 1px solid var(--secondary-color) !important;
        padding: 0.75rem 1rem;
        box-shadow: 0 0 10px rgba(0, 179, 230, 0.3);
        font-family: 'Courier New', monospace;
    }
    
    /* Sources styling */
    .source-header {
        background-color: rgba(15, 72, 128, 0.5);
        padding: 0.75rem 1rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        border-left: 4px solid var(--secondary-color);
    }
    
    /* Lightning animation */
    @keyframes lightning {
        0% { opacity: 0; }
        10% { opacity: 1; }
        20% { opacity: 0; }
        30% { opacity: 1; }
        40% { opacity: 0; }
        100% { opacity: 0; }
    }
    
    .lightning {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.1);
        pointer-events: none;
        animation: lightning 5s infinite;
        z-index: 1000;
        display: none;
    }
    
    /* Loading animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        height: 60px;
    }
    
    .tesla-coil {
        width: 50px;
        height: 60px;
        background-color: var(--secondary-color);
        position: relative;
        border-radius: 5px 5px 20px 20px;
        overflow: hidden;
    }
    
    .tesla-coil:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, transparent, rgba(0, 179, 230, 0.8));
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: translateY(60px); }
        50% { transform: translateY(0); }
        100% { transform: translateY(60px); }
    }
    
    .spark {
        position: absolute;
        width: 20px;
        height: 4px;
        background-color: var(--accent-color);
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 0 0 10px var(--accent-color);
        animation: spark 0.5s infinite;
    }
    
    @keyframes spark {
        0% { width: 0; opacity: 0; }
        50% { width: 20px; opacity: 1; }
        100% { width: 0; opacity: 0; }
    }
    
    /* Logo placeholder */
    .logo-placeholder {
        padding: 1.5rem;
        margin-bottom: 1rem;
        text-align: center;
        background: linear-gradient(135deg, var(--panel-bg), var(--primary-color));
        border-radius: 5px;
        border: 1px solid var(--secondary-color);
        box-shadow: 0 0 10px rgba(0, 179, 230, 0.3);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid var(--secondary-color);
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.8rem;
    }
    
    /* API Connection indicator */
    .api-indicator {
        position: fixed;
        bottom: 15px;
        right: 15px;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        opacity: 0.8;
        z-index: 999;
        box-shadow: 0 0 5px currentColor;
    }
    
    .api-indicator.connected {
        background-color: #4CAF50;
        border: 1px solid #2E7D32;
    }
    
    .api-indicator.disconnected {
        background-color: #F44336;
        border: 1px solid #B71C1C;
    }
    
    .api-indicator.unknown {
        background-color: #FF9800;
        border: 1px solid #E65100;
    }
    
    /* Pulse animation for API indicator */
    @keyframes api-pulse {
        0% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.7; }
    }
    
    .api-indicator {
        animation: api-pulse 2s infinite ease-in-out;
    }
    
    /* Tooltip for API indicator */
    .api-indicator-container {
        position: fixed;
        bottom: 15px;
        right: 15px;
        z-index: 999;
    }
    
    .api-tooltip {
        position: absolute;
        bottom: 25px;
        right: 0;
        background-color: var(--panel-bg);
        color: var(--text-color);
        padding: 5px 10px;
        border-radius: 4px;
        font-size: 12px;
        white-space: nowrap;
        opacity: 0;
        transition: opacity 0.3s ease;
        border: 1px solid var(--secondary-color);
        box-shadow: 0 0 5px rgba(0, 179, 230, 0.5);
        pointer-events: none;
    }
    
    .api-indicator-container:hover .api-tooltip {
        opacity: 1;
    }
</style>

<div class="lightning" id="lightning"></div>

<script>
// Trigger lightning occasionally
function triggerLightning() {
    setTimeout(function() {
        document.getElementById('lightning').style.display = 'block';
        setTimeout(function() {
            document.getElementById('lightning').style.display = 'none';
            triggerLightning();
        }, 500);
    }, Math.random() * 20000 + 5000); // Random timing between 5-25 seconds
}

triggerLightning();
</script>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    if "search_error" not in st.session_state:
        st.session_state.search_error = None
    if "loading" not in st.session_state:
        st.session_state.loading = False
    if "metadata_options" not in st.session_state:
        st.session_state.metadata_options = None
    if "current_query" not in st.session_state:
        st.session_state.current_query = ""
    if "api_status" not in st.session_state:
        st.session_state.api_status = "unknown"  # "connected", "disconnected", or "unknown"

# Initialize session state
init_session_state()

# Check API availability
def check_api_status():
    """Check if API is available."""
    try:
        # Use the is_api_available method from api_client
        api_available = api_client.is_api_available()
        st.session_state.api_status = "connected" if api_available else "disconnected"
    except Exception as e:
        st.session_state.api_status = "disconnected"
        
# Run API check on startup
check_api_status()

# Import HTTPClient to make direct API calls without caching
import httpx
import json
from frontend.api.models import SearchRequest

# Define search function without using the cached method
def perform_search(query: str, filters: Dict[str, Any]):
    """Perform search using direct API call to avoid caching issues."""
    # Set loading state
    st.session_state.loading = True
    st.session_state.search_error = None
    
    # Debug container
    debug_container = st.empty()
    
    # Convert filters dict to SearchFilters object
    search_filters = SearchFilters(**filters) if filters else None
    
    # Create search options
    search_options = SearchOptions(
        max_results=DEFAULT_MAX_RESULTS,
        include_metadata=DEFAULT_INCLUDE_METADATA,
        rerank=DEFAULT_RERANK,
        threshold=DEFAULT_THRESHOLD
    )
    
    try:
        # Create search request
        search_request = SearchRequest(
            query=query,
            filters=search_filters,
            options=search_options
        )
        
        # Make direct API call instead of using the cached method
        url = f"{api_client.base_url}/search"
        
        # Create a client with timeout
        client = httpx.Client(timeout=api_client.timeout)
        
        # Make the request
        response = client.post(
            url,
            headers=api_client.headers,
            content=search_request.model_dump_json()
        )
        
        # Update API status to connected on successful call
        st.session_state.api_status = "connected"
        
        # Process the response
        if response.status_code == 200:
            result = SearchResponse.model_validate(response.json())
            st.session_state.search_results = result
        else:
            error_result = ErrorResponse.model_validate(response.json())
            st.session_state.search_error = error_result
            
    except Exception as e:
        # Update API status to disconnected on failed call
        st.session_state.api_status = "disconnected"
        
        # Create an error response
        st.session_state.search_error = ErrorResponse(
            error={
                "code": "internal_error",
                "message": f"The monster refuses to cooperate: {str(e)}",
                "details": {"reason": "exception"}
            },
            request_id="monster_error"
        )
    finally:
        # Reset loading state
        st.session_state.loading = False
        debug_container.empty()

# Function to handle filter changes
def handle_filter_change(filters: SearchFilters):
    """Handle filter changes and re-run search if needed."""
    # Only re-run search if we have a current query
    if st.session_state.current_query:
        perform_search(st.session_state.current_query, filters.model_dump())

# Import additional models needed
from frontend.api.models import (
    MetadataOptionsResponse, 
    ErrorResponse,
    SearchResponse,
    SearchFilters,
    SearchOptions,
    SearchRequest
)

# Logo in sidebar
with st.sidebar:
    # Display logo with styled text
    st.markdown("""
    <div class="logo-placeholder">
        <div style="font-size:2.5rem;margin-bottom:0.5rem;">⚡ 📚</div>
        <h3 style="margin:0;color:#ffcc00;text-shadow:0 0 5px #ffcc00;">EXABOMINATION</h3>
        <p style="font-size:0.8rem;margin:0;color:#00b3e6;font-style:italic;">Exabeam Documentation Search</p>
    </div>
    """, unsafe_allow_html=True)
    # Use dev_mode for simulation only, but don't show the checkbox
    dev_mode = True

# Display the query history in the sidebar
query_history_sidebar()

# Get metadata options for filters
try:
    # Get or create metadata options (with mock fallback)
    if st.session_state.metadata_options is None:
        # If in dev mode and API is not available, use mock data
        if dev_mode:
            st.session_state.metadata_options = MetadataOptionsResponse(
                document_types=["use_case", "parser", "rule", "data_source", "overview", "tutorial"],
                vendors=["microsoft", "cisco", "okta", "palo_alto", "aws"],
                products={
                    "microsoft": ["active_directory", "azure_ad", "exchange_online", "windows"],
                    "cisco": ["asa", "firepower", "ise", "meraki"],
                    "okta": ["identity_cloud"]
                },
                use_cases=["account_takeover", "data_exfiltration", "lateral_movement", "privilege_escalation"],
                date_range={"oldest": "2022-01-15", "newest": "2025-03-27"}
            )
    
    # Use available metadata options 
    filters = filters_panel(handle_filter_change, st.session_state.metadata_options)
except Exception as e:
    st.sidebar.error(f"Could not load filters: {str(e)}")

# Main app layout
st.write("")

# Custom header with improved branding
st.markdown("""
<div class="main-header">
    <h1>EXABOMINATION</h1>
    <p>Exabeam Common Information Model Documentation Search</p>
    <div style="position: absolute; right: 15px; top: 15px; font-size: 1.2rem;">📚 CIM</div>
</div>
""", unsafe_allow_html=True)

# Skip rendering the normal search interface header and render the component in a card
# This is the key change - we're customizing how we render the search_interface component
st.markdown("""<div class="card">""", unsafe_allow_html=True)

# Create container to hold search interface
search_container = st.container()
with search_container:
    # Instead of calling search_interface directly, we'll call it with a custom wrapper
    # that skips rendering the title that contains "EXASPERATION"
    
    # This simulates the core functionality of search_interface without the header
    # The form and other elements that would normally be part of search_interface
    with st.form(key="search_form", clear_on_submit=False):
        col1, col2 = st.columns([6, 1])
        
        with col1:
            query = st.text_input(
                "Enter your question",
                value=st.session_state.get("current_query", ""),
                placeholder="e.g., How does the password reset detection rule work?",
                disabled=st.session_state.loading,
                key="query_input"
            )
        
        with col2:
            submit_button = st.form_submit_button(
                "Search", 
                disabled=st.session_state.loading,
                use_container_width=True,
                type="primary"
            )
        
        # Advanced filters expander (to be implemented)
        with st.expander("Advanced filters", expanded=False):
            st.info("Filter the results with Mad Scientist precision.")
    
    # Process form submission
    if submit_button and query and not st.session_state.loading:
        st.session_state.current_query = query
        
        # Add to query history if not already present
        if "query_history" in st.session_state:
            if query not in st.session_state.query_history:
                st.session_state.query_history = [query] + st.session_state.query_history
                if len(st.session_state.query_history) > 10:  # Limit history size
                    st.session_state.query_history = st.session_state.query_history[:10]
        
        # Call the search callback
        perform_search(query, {})
    
    # Show example queries (moved outside the form)
    from frontend.config import EXAMPLE_QUERIES
    with st.expander("Example questions", expanded=False):
        example_cols = st.columns(2)
        for i, example in enumerate(EXAMPLE_QUERIES):
            with example_cols[i % 2]:
                if st.button(
                    example, 
                    key=f"example_{i}",
                    use_container_width=True,
                    disabled=st.session_state.loading
                ):
                    # Set the example as the current query and trigger search
                    st.session_state.current_query = example
                    perform_search(example, {})

# Close the card div
st.markdown("""</div>""", unsafe_allow_html=True)

# Display loading animation
if st.session_state.loading:
    st.markdown("""
    <div class="loading-container">
        <div class="tesla-coil">
            <div class="spark"></div>
        </div>
        <div style="margin-left:20px;font-family:'Courier New',monospace;">
            <p style="margin:0;font-size:1.2rem;color:#00b3e6;">REANIMATING DOCUMENTATION...</p>
            <p style="margin:0;font-size:0.8rem;color:#ffcc00;font-style:italic;">The monster is thinking</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display results or error
st.markdown("""<div class="card">""", unsafe_allow_html=True)
results_display(
    result=st.session_state.search_results,
    error=st.session_state.search_error
)
st.markdown("""</div>""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>EXABOMINATION - Exabeam Documentation Search © 2025</p>
    <p style="font-size:0.7rem;">Powered by Common Information Model</p>
</div>
""", unsafe_allow_html=True)

# API connection status indicator
status_text = {
    "connected": "API Brain Connected - Power: 100%",
    "disconnected": "API Brain Disconnected - Power: 0%",
    "unknown": "API Brain Status Unknown"
}

st.markdown(f"""
<div class="api-indicator-container">
    <div class="api-indicator {st.session_state.api_status}"></div>
    <div class="api-tooltip">{status_text[st.session_state.api_status]}</div>
</div>
""", unsafe_allow_html=True)

# Check API status periodically (every 60 seconds)
if st.session_state.get('last_api_check', 0) < time.time() - 60:
    check_api_status()
    st.session_state.last_api_check = time.time()
