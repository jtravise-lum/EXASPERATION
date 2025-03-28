"""Component for filtering search results."""

import streamlit as st
from typing import Callable, Dict, Any, List, Optional
from datetime import datetime

from frontend.api.models import SearchFilters, MetadataOptionsResponse

def filters_panel(on_change: Callable[[SearchFilters], None], metadata_options: MetadataOptionsResponse) -> SearchFilters:
    """Display a panel of filters for search results.
    
    Args:
        on_change: Callback function when filters change
        metadata_options: Available metadata options from API
        
    Returns:
        Current filter settings
    """
    with st.sidebar:
        st.markdown("### Search Filters")
        
        # Initialize filters if not in session state
        if "filters" not in st.session_state:
            st.session_state.filters = {
                "document_types": [],
                "vendors": [],
                "products": [],
                "use_cases": [],
                "min_date": None,
                "max_date": None
            }
        
        # Create filter sections
        with st.expander("Document Types", expanded=False):
            if metadata_options and metadata_options.document_types:
                st.session_state.filters["document_types"] = st.multiselect(
                    "Select document types:",
                    options=metadata_options.document_types,
                    default=st.session_state.filters.get("document_types", [])
                )
            else:
                st.info("No document types available")
        
        with st.expander("Vendors & Products", expanded=False):
            if metadata_options and metadata_options.vendors:
                # First select vendors
                selected_vendors = st.multiselect(
                    "Select vendors:",
                    options=metadata_options.vendors,
                    default=st.session_state.filters.get("vendors", [])
                )
                st.session_state.filters["vendors"] = selected_vendors
                
                # Then show products for selected vendors
                if selected_vendors and metadata_options.products:
                    all_products = []
                    for vendor in selected_vendors:
                        if vendor in metadata_options.products:
                            all_products.extend(metadata_options.products[vendor])
                    
                    st.session_state.filters["products"] = st.multiselect(
                        "Select products:",
                        options=all_products,
                        default=[p for p in st.session_state.filters.get("products", []) if p in all_products]
                    )
            else:
                st.info("No vendor data available")
        
        with st.expander("Use Cases", expanded=False):
            if metadata_options and metadata_options.use_cases:
                st.session_state.filters["use_cases"] = st.multiselect(
                    "Select use cases:",
                    options=metadata_options.use_cases,
                    default=st.session_state.filters.get("use_cases", [])
                )
            else:
                st.info("No use case data available")
        
        with st.expander("Date Range", expanded=False):
            if metadata_options and metadata_options.date_range:
                # Parse dates from strings
                try:
                    oldest = datetime.fromisoformat(metadata_options.date_range["oldest"].split("T")[0])
                    newest = datetime.fromisoformat(metadata_options.date_range["newest"].split("T")[0])
                    
                    min_date = st.date_input(
                        "From:",
                        value=datetime.fromisoformat(st.session_state.filters.get("min_date", oldest.isoformat())).date() if st.session_state.filters.get("min_date") else oldest.date(),
                        min_value=oldest.date(),
                        max_value=newest.date()
                    )
                    
                    max_date = st.date_input(
                        "To:",
                        value=datetime.fromisoformat(st.session_state.filters.get("max_date", newest.isoformat())).date() if st.session_state.filters.get("max_date") else newest.date(),
                        min_value=oldest.date(),
                        max_value=newest.date()
                    )
                    
                    st.session_state.filters["min_date"] = min_date.isoformat()
                    st.session_state.filters["max_date"] = max_date.isoformat()
                except (ValueError, KeyError):
                    st.error("Invalid date range format")
            else:
                st.info("No date range data available")
        
        # Add a button to apply filters
        if st.button("Apply Filters", use_container_width=True):
            # Convert to SearchFilters object
            filters = SearchFilters(
                document_types=st.session_state.filters["document_types"] if st.session_state.filters["document_types"] else None,
                vendors=st.session_state.filters["vendors"] if st.session_state.filters["vendors"] else None,
                products=st.session_state.filters["products"] if st.session_state.filters["products"] else None,
                use_cases=st.session_state.filters["use_cases"] if st.session_state.filters["use_cases"] else None,
                min_date=st.session_state.filters["min_date"] if st.session_state.filters.get("min_date") else None,
                max_date=st.session_state.filters["max_date"] if st.session_state.filters.get("max_date") else None
            )
            on_change(filters)
        
        # Add a button to reset filters
        if st.button("Reset Filters", use_container_width=True):
            st.session_state.filters = {
                "document_types": [],
                "vendors": [],
                "products": [],
                "use_cases": [],
                "min_date": None,
                "max_date": None
            }
            # Create empty filters
            filters = SearchFilters()
            on_change(filters)
            st.rerun()
    
    # Return current filters
    return SearchFilters(
        document_types=st.session_state.filters["document_types"] if st.session_state.filters["document_types"] else None,
        vendors=st.session_state.filters["vendors"] if st.session_state.filters["vendors"] else None,
        products=st.session_state.filters["products"] if st.session_state.filters["products"] else None,
        use_cases=st.session_state.filters["use_cases"] if st.session_state.filters["use_cases"] else None,
        min_date=st.session_state.filters["min_date"] if st.session_state.filters.get("min_date") else None,
        max_date=st.session_state.filters["max_date"] if st.session_state.filters.get("max_date") else None
    )