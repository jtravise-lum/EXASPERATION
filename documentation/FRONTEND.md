# EXABOMINATION Frontend

This document provides a comprehensive overview of the EXABOMINATION frontend, including its architecture, development plan, key components, and visual mockups. The frontend serves as the user interface for the EXABOMINATION system, enabling users to efficiently access and interact with Exabeam's documentation using natural language queries.

## Overview

This document outlines the comprehensive plan for implementing the EXABOMINATION frontend, a user interface that will enable efficient access to Exabeam's documentation through natural language queries. The frontend will work seamlessly with the existing backend RAG system that handles document processing, embeddings, and retrieval.

## Architecture

### Tech Stack

-   **Framework**: Streamlit (as specified in the implementation plan)
-   **Styling**: Custom CSS with responsive design
-   **Authentication**: Simple authentication layer
-   **API Communication**: RESTful API calls to backend
-   **State Management**: Streamlit session state

## Phases of Development

### Core Interface Development

#### 1. Basic Layout and Structure

-   Create application structure with navigation components
-   Implement responsive design for desktop and mobile
-   Design color scheme and typography aligned with Exabeam branding
-   Build header, footer, and navigation sidebar

#### 2. Search Interface

-   Implement natural language query input field with auto-suggestions
-   Add support for query history and saved queries
-   Create search button with loading animation
-   Design clear input field and example query suggestions

#### 3. Results Display

-   Develop clean, readable format for displaying answers
-   Implement source attribution with links to original documentation
-   Create collapsible sections for additional context
-   Add syntax highlighting for code examples and configuration snippets
-   Implement markdown rendering for formatted content

#### 4. User Session Management

-   Create session persistence for query history
-   Implement basic authentication (if required)
-   Add user preferences storage
-   Build session analytics capture

### Enhanced User Experience

#### 1. Interactive Features

-   Add feedback mechanism (thumbs up/down for responses)
-   Implement "copy to clipboard" functionality for code snippets
-   Create "suggest improvement" feature for responses
-   Build "follow-up questions" suggestions based on previous queries
-   Add support for query refinement

#### 2. Result Visualization

-   Implement expandable citations section
-   Create visual indicators for source relevance
-   Design document type badges (parser, use case, data source)
-   Add metadata visualization for retrieved documents
-   Build simple charts for complex numeric responses (when applicable)

#### 3. Advanced Search Options

-   Add filters for document types, vendors, and use cases
-   Implement sorting options for results
-   Create advanced search syntax support
-   Build query builder interface for complex searches
-   Add support for MITRE ATT&CK reference searching

#### 4. Contextual Help

-   Implement tooltips for technical terms
-   Create contextual help panels
-   Build guided tours for new users
-   Add keyboard shortcuts with help overlay
-   Implement search syntax documentation

### Performance and Integration

#### 1. Performance Optimization

-   Implement response caching
-   Add lazy loading for long result sets
-   Create streaming responses for faster initial display
-   Optimize image and asset loading
-   Implement background processing for heavy operations

#### 2. API Integration

-   Create robust API client with error handling
-   Implement request throttling and batching
-   Add request retries with exponential backoff
-   Build connection status indicator
-   Create offline mode with cached results

#### 3. Analytics Dashboard

-   Implement usage metrics visualization
-   Create query pattern analysis
-   Build user activity timeline
-   Add performance monitoring display
-   Implement cost tracking for API usage

#### 4. Administrative Features

-   Create user management interface
-   Implement system status dashboard
-   Add configuration management
-   Build usage reporting tools
-   Create content update scheduling

### Testing and Optimization

#### 1. Automated Testing

-   Implement unit tests for UI components
-   Create integration tests for API communication
-   Build end-to-end testing for critical user flows
-   Add visual regression testing
-   Implement performance benchmarking

#### 2. User Testing

-   Conduct usability studies
-   Implement A/B testing for interface improvements
-   Create user feedback collection
-   Build heatmap analysis for UI interactions
-   Analyze query patterns and failures

#### 3. Accessibility Improvements

-   Ensure WCAG 2.1 AA compliance
-   Implement keyboard navigation
-   Add screen reader support
-   Create high-contrast mode
-   Implement font size adjustments

#### 4. Documentation

-   Create user manual with screenshots
-   Build video tutorials for common tasks
-   Implement interactive help system
-   Create developer documentation for frontend
-   Build troubleshooting guide

### Deployment and Support

#### 1. Deployment Strategy

-   Implement CI/CD pipeline for frontend
-   Create containerized deployment
-   Build environment-specific configurations
-   Implement feature flags for gradual rollout
-   Create backup and disaster recovery procedures

#### 2. Monitoring and Alerts

-   Implement frontend error tracking
-   Create performance monitoring
-   Build user experience monitoring
-   Add real-time alerts for system issues
-   Implement usage threshold notifications

#### 3. Continuous Improvement

-   Create feedback analysis workflow
-   Implement A/B testing framework
-   Build feature request tracking
-   Create user satisfaction measurement
-   Implement usage pattern analysis

## Implementation Timeline

| Phase | Task | Estimated Duration | Priority |
|---|---|---|---|
| 1 | Core Interface Development | 2 weeks | High |
| 2 | Enhanced User Experience | 2 weeks | High |
| 3 | Performance and Integration | 2 weeks | Medium |
| 4 | Testing and Optimization | 1 week | Medium |
| 5 | Deployment and Support | 1 week | Medium |

## Success Metrics

The frontend implementation will be evaluated based on:

1.  **Usability**: Ease of formulating queries and interpreting results
2.  **Performance**: Response time and frontend loading speed
3.  **Accessibility**: Compliance with accessibility standards
4.  **User Satisfaction**: Feedback metrics and retention
5.  **Query Success Rate**: Percentage of queries that yield useful results

## Next Steps

1.  Create UI mockups for core components
2.  Define REST API contract with backend team
3.  Set up development environment with Streamlit
4.  Implement basic search interface prototype
5.  Establish feedback loop with potential users

## Components

## Implementation Plan

### API Backend
- Develop RESTful API with FastAPI
- Implement authentication and authorization
- Create API documentation with Swagger
- Build rate limiting and throttling
- Set up error handling and logging

### Frontend Application
- Create a simple web interface using Streamlit
- Implement user authentication
- Build query input interface
- Design response display with citations
- Develop user feedback mechanism

This document describes the key components of the EXASPERATION frontend application, their functionality, and relationships.

### 1. Main Application

**File:** `app.py`

The main Streamlit application entry point that initializes the user interface and orchestrates the various components.

**Key Responsibilities:**

-   Application initialization and configuration
-   Page routing and navigation
-   Session state management
-   Authentication handling
-   Main layout structure

### 2. Search Interface

**File:** `components/search_interface.py`

The primary search input component where users enter natural language queries.

**Features:**

-   Query input field with auto-suggestions
-   Example queries display
-   Search history tracking
-   Advanced search options toggle
-   Search submit functionality

**States:**

-   Current query text
-   Search in progress indicator
-   Previous queries list

### 3. Results Display

**File:** `components/results_display.py`

Component that renders search results and answers from the backend.

**Features:**

-   Answer rendering with markdown support
-   Source citation display
-   Code snippet formatting
-   Expandable context sections
-   Feedback collection (thumbs up/down)
-   Copy to clipboard functionality

**States:**

-   Current result data
-   Expanded/collapsed sections
-   Feedback state

### 4. Filters Panel

**File:** `components/filters_panel.py`

Component for filtering search results by metadata.

**Features:**

-   Document type selection (parsers, use cases, etc.)
-   Vendor filtering
-   Product filtering
-   Date range selection
-   Clear filters option

**States:**

-   Active filters
-   Available filter options
-   Filter visibility toggle

### 5. User Preferences

**File:** `components/user_preferences.py`

Component for managing user preferences and settings.

**Features:**

-   Theme selection
-   Result display options
-   Query history management
-   API key management (if applicable)
-   Notification settings

**States:**

-   Current preferences
-   Settings visibility toggle

### 6. API Client

**File:** `utils/api_client.py`

Utility for communicating with the backend API.

**Functionality:**

-   Query submission
-   Result fetching
-   Error handling
-   Rate limiting
-   Connection status management

**Methods:**

-   `search(query, filters)`
-   `get_suggestions(partial_query)`
-   `submit_feedback(query_id, feedback)`
-   `get_metadata_options()`

### 7. Analytics Tracker

**File:** `utils/analytics.py`

Component that tracks user interactions for analytics purposes.

**Functionality:**

-   Query tracking
-   Result interaction logging
-   Session timing
-   Feature usage metrics
-   Error reporting

**Methods:**

-   `track_query(query_text, filters)`
-   `track_result_interaction(result_id, interaction_type)`
-   `track_session(session_id, duration)`
-   `report_error(error_type, details)`

### 8. Help System

**File:** `components/help_system.py`

Component providing contextual help and guidance.

**Features:**

-   Tooltips for UI elements
-   Guided tours for new users
-   Search syntax documentation
-   Keyboard shortcuts reference
-   Frequently asked questions

**States:**

-   Current help context
-   Tour progress
-   Help visibility toggle

### 9. Notifications

**File:** `components/notifications.py`

Component for displaying system notifications and alerts.

**Features:**

-   Success messages
-   Error alerts
-   Information notices
-   Loading indicators
-   Toast notifications

**Methods:**

-   `show_success(message)`
-   `show_error(message)`
-   `show_info(message)`
-   `show_loading(message)`

### 10. Authentication

**File:** `utils/auth.py`

Component handling user authentication and session management.

**Features:**

-   Login interface
-   Session tracking
-   Permission management
-   Secure credential handling
-   Session timeout handling

**Methods:**

-   `login(username, password)`
-   `logout()`
-   `check_session()`
-   `get_current_user()`

### Component Relationships
```
                     +----------------+
                     |                |
                     |    app.py      |
                     |                |
                     +-------+--------+
                             |
                             |
        +-------------------+-------------------+
        |                   |                   |
+-------v-------+   +-------v-------+   +-------v-------+
|               |   |               |   |               |
| search_       |   | results_      |   | filters_      |
| interface.py  |   | display.py    |   | panel.py      |
|               |   |               |   |               |
+-------+-------+   +-------+-------+   +---------------+
        |                   |
        |                   |
        |            +------v-------+
        |            |              |
        +----------->| api_client.py|
                     |              |
                     +--------------+
```
### Styling Guidelines

-   Use Exabeam brand colors:
    -   Primary: `#0066CC`
    -   Secondary: `#00A3E0`
    -   Accent: `#FF6B00`
    -   Background: `#F5F7FA`
    -   Text: `#333333`

-   Typography:
    -   Headings: 'Inter', sans-serif
    -   Body: 'Inter', sans-serif
    -   Code: 'Source Code Pro', monospace

-   Component styling:
    -   Consistent padding (16px)
    -   Rounded corners (4px)
    -   Subtle shadows for elevated components
    -   Clear visual hierarchy with whitespace

### State Management

All components should follow these state management practices:

1.  Use Streamlit's session state for persistent data across reruns
2.  Initialize state variables at component startup
3.  Implement clear state update methods
4.  Document state dependencies between components
5.  Handle state initialization for new sessions

## Mockups

This document provides text-based mockups of the key screens in the EXASPERATION frontend application.

### 1. Main Search Interface
```
+---------------------------------------------------------------+
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │                      EXASPERATION                       │  |
|  │  Exabeam Automated Search Assistant Preventing          │  |
|  │  Exasperating Research And Time-wasting In Official Notes  │
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Search Exabeam Documentation                          🔍│  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  Example queries:                                             |
|  • How do I set up the integration with Cisco ACS?            |
|  • What parsers are available for 1Password?                  |
|  • Explain the T1070.001 MITRE technique detection           |
|                                                               |
|  [Advanced Search Options ▼]                                  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Filters:                                                │  |
|  │                                                         │  |
|  │ Document Types:   □ All  □ Use Cases  □ Parsers         │  |
|  │                   □ Data Sources  □ Rules  □ Overview   │  |
|  │                                                         │  |
|  │ Vendors:          □ All  □ Microsoft  □ Cisco           │  |
|  │                   □ Okta  □ Palo Alto  □ AWS  □ More... │  |
|  │                                                         │  |
|  │ Products:         [Select Vendor First]                 │  |
|  │                                                         │  |
|  │ Date Range:       [2023-01-01] to [2025-03-27]          │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  Recent Searches:                                             |
|  • How does the lateral movement use case work?               |
|  • What is the format of Cisco ASA logs?                      |
|  • Windows security event ID 4624                             |
|                                                               |
+---------------------------------------------------------------+
```
### 2. Search Results
```
+---------------------------------------------------------------+
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │                      EXASPERATION                       │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ How does the password reset detection rule work?      🔍│  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  Results for: How does the password reset detection rule work?|
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │                                                         │  |
|  │  The password reset detection rule in Exabeam works by  │  |
|  │  monitoring authentication events that indicate a       │  |
|  │  password has been changed or reset. In Microsoft       │  |
|  │  Active Directory environments, this primarily uses     │  |
|  │  Event ID 4724 (password reset attempt) and Event ID    │  |
|  │  4723 (password change attempt).                        │  |
|  │                                                         │  |
|  │  The rule correlates these events with the user         │  |
|  │  performing the action and the target account. When     │  |
|  │  the action is performed by someone other than the      │  |
|  │  account owner (excluding privileged IT accounts),      │  |
|  │  this may indicate unauthorized password manipulation.  │  |
|  │                                                         │  |
|  │  The rule also looks for password resets from unusual   │  |
|  │  locations or outside normal business hours as          │  |
|  │  potential indicators of suspicious activity.           │  |
|  │                                                         │  |
|  │  📋 [Copy]           👍 Helpful    👎 Not Helpful       │  |
|  │                                                         │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  Sources:                                                     |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ 📄 Password Reset Detection Use Case                    │  |
|  │     Microsoft Active Directory                          │  |
|  │     Relevance: 92%                                      │  |
|  │     [Expand] [View Original]                            │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ 📄 Active Directory Password Events                     │  |
|  │     Parser Documentation                                │  |
|  │     Relevance: 87%                                      │  |
|  │     [Expand] [View Original]                            │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ 📄 Account Manipulation Detection Rule                  │  |
|  │     Security Use Case                                   │  |
|  │     Relevance: 73%                                      │  |
|  │     [Expand] [View Original]                            │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  Suggested Follow-up Questions:                               |
|  • How do I configure password reset alerting?                |
|  • What events are generated during a password reset?         |
|  • How does password reset differ from password change?       |
|                                                               |
+---------------------------------------------------------------+
```
### 3. Expanded Source View
```
+---------------------------------------------------------------+
|                                                               |
|  ← Back to Results                                            |
|                                                               |
|  Source: Password Reset Detection Use Case                    |
|  Type: Use Case Documentation                                 |
|  Vendor: Microsoft                                            |
|  Product: Active Directory                                    |
|  Last Updated: March 10, 2024                                 |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │                                                         │  |
|  │  # Password Reset Detection                             │  |
|  │                                                         │  |
|  │  ## Overview                                            │  |
|  │                                                         │  |
|  │  This use case detects when a user account password     │  |
|  │  is reset by someone other than the account owner,      │  |
|  │  which could indicate account takeover or unauthorized  │  |
|  │  access attempts.                                       │  |
|  │                                                         │  |
|  │  ## Data Sources                                        │  |
|  │                                                         │  |
|  │  * Microsoft Windows Security Events                    │  |
|  │  * Microsoft Azure Active Directory                     │  |
|  │  * Okta Identity Cloud                                  │  |
|  │                                                         │  |
|  │  ## Detection Logic                                     │  |
|  │                                                         │  |
|  │  The rule identifies password reset events through      │  |
|  │  monitoring of the following:                           │  |
|  │                                                         │  |
|  │  ### For Microsoft Active Directory:                    │  |
|  │  * Event ID 4724: An attempt was made to reset an       │  |
|  │    account's password                                   │  |
|  │  * Event ID 4723: An attempt was made to change an      │  |
|  │    account's password                                   │  |
|  │  * Event ID 4738: A user account was changed            │  |
|  │                                                         │  |
|  │  ### For Azure Active Directory:                        │  |
|  │  * ActivityType: Reset password (self-service)          │  |
|  │  * ActivityType: Reset user password                    │  |
|  │                                                         │  |
|  │  ... [Content continues] ...                            │  |
|  │                                                         │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  📋 [Copy Full Content]                                       |
|  📄 [View Original Document]                                  |
|                                                               |
+---------------------------------------------------------------+
```
### 4. Advanced Search Interface
```
+---------------------------------------------------------------+
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │                      EXASPERATION                       │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  Advanced Search                                              |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Query:                                                  │  |
|  │ ┌────────────────────────────────────────────────────┐  │  |
|  │ │password reset detection windows                    │  │  |
|  │ └────────────────────────────────────────────────────┘  │  |
|  │                                                         │  |
|  │ Search Options:                                         │  |
|  │                                                         │  |
|  │ Search Mode:  ○ Natural Language  ● Hybrid  ○ Keyword   │  |
|  │                                                         │  |
|  │ Result Count: [10 ▼]                                    │  |
|  │                                                         │  |
|  │ Result Type:  ○ Answer with Sources                     │  |
|  │               ● Sources Only                            │  |
|  │               ○ Raw Document Chunks                     │  |
|  │                                                         │  |
|  │ Relevance Threshold: [0.7 ▼]                           │  |
|  │                                                         │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Metadata Filters:                                       │  |
|  │                                                         │  |
|  │ Document Types:                                         │  |
|  │ ☑ Use Cases ☑ Parsers ☑ Rules ☐ Overview ☐ Tutorials   │  |
|  │                                                         │  |
|  │ Vendors:                                                │  |
|  │ ☑ Microsoft ☐ Cisco ☐ Okta ☐ Palo Alto ☐ AWS           │  |
|  │ ☐ Show All Vendors                                      │  |
|  │                                                         │  |
|  │ Products:                                               │  |
|  │ ☑ Active Directory ☑ Azure AD ☐ Windows Server         │  |
|  │ ☐ Exchange ☐ Office 365                                 │  |
|  │ ☐ Show All Products                                     │  |
|  │                                                         │  |
|  │ MITRE ATT&CK:                                           │  |
|  │ ☐ Credential Access ☐ Defense Evasion                   │  |
|  │ ☑ Persistence ☐ Privilege Escalation                    │  |
|  │ [Select Techniques...]                                  │  |
|  │                                                         │  |
|  │ Date Range:                                             │  |
|  │ From: [2023-01-01] To: [2025-03-27]                     │  |
|  │                                                         │  |
|  │ [Apply Filters] [Reset]                                 │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  [Search]                                                     |
|                                                               |
+---------------------------------------------------------------+
```
### 5. User Preferences
```
+---------------------------------------------------------------+
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │                      EXASPERATION                       │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  User Preferences                                             |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Display Settings                                        │  |
|  │                                                         │  |
|  │ Theme:              ○ Light  ● Dark  ○ System Default   │  |
|  │                                                         │  |
|  │ Result Display:     ○ Compact  ● Standard  ○ Detailed   │  |
|  │                                                         │  |
|  │ Code Formatting:    ○ Default  ● Syntax Highlighting    │  |
|  │                                                         │  |
|  │ Citation Style:     ○ Inline  ● Footer  ○ Detailed      │  |
|  │                                                         │  |
|  │ Font Size:          ○ Small  ● Medium  ○ Large          │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Search Preferences                                      │  |
|  │                                                         │  |
|  │ Default Search Mode: ○ Natural Language                 │  |
|  │                      ● Hybrid                           │  |
|  │                      ○ Keyword                          │  |
|  │                                                         │  |
|  │ Result Count:        [10 ▼]                            │  |
|  │                                                         │  |
|  │ Show Suggestions:    ● Yes  ○ No                        │  |
|  │                                                         │  |
|  │ Save Search History: ● Yes  ○ No                        │  |
|  │                                                         │  |
|  │ Default Filters:     [Configure Default Filters...]     │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Search History                                          │  |
|  │                                                         │  |
|  │ [Clear Search History]                                  │  |
|  │                                                         │  |
|  │ • How does the password reset detection rule work?      │  |
|  │   March 27, 2025 14:35                                  │  |
|  │   [Delete]                                              │  |
|  │                                                         │  |
|  │ • What parsers are available for 1Password?             │  |
|  │   March 27, 2025 14:20                                  │  |
|  │   [Delete]                                              │  |
|  │                                                         │  |
|  │ • How do I set up the integration with Cisco ACS?       │  |
|  │   March 27, 2025 14:05                                  │  |
|  │   [Delete]                                              │  |
|  │                                                         │  |
|  │ [Show More History...]                                  │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  [Save Preferences] [Reset to Defaults]                       |
|                                                               |
+---------------------------------------------------------------+
```
### 6. Help and Documentation
```
+---------------------------------------------------------------+
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │                      EXASPERATION                       │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  Help and Documentation                                       |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Getting Started                                         │  |
|  │                                                         │  |
|  │ • Introduction to EXASPERATION                          │  |
|  │ • How to formulate effective queries                    │  |
|  │ • Understanding search results                          │  |
|  │ • Using filters and advanced search                     │  |
|  │ • Providing feedback                                    │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Search Tips                                             │  |
|  │                                                         │  |
|  │ • Be specific in your queries                           │  |
|  │ • Include relevant technologies or products             │  |
|  │ • Use technical terms when available                    │  |
|  │ • For parser questions, mention data source             │  |
|  │ • For use cases, mention security concern               │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Advanced Features                                       │  |
|  │                                                         │  |
|  │ • Using MITRE ATT&CK references                         │  |
|  │ • Filtering by metadata                                 │  |
|  │ • Understanding relevance scores                        │  |
|  │ • Saving and organizing search results                  │  |
|  │ • Keyboard shortcuts                                    │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  ┌─────────────────────────────────────────────────────────┐  |
|  │ Frequently Asked Questions                              │  |
|  │                                                         │  |
|  │ • What documentation is included in the system?         │  |
|  │ • How often is the content updated?                     │  |
|  │ • Why am I getting irrelevant results?                  │  |
|  │ • How can I provide feedback on results?                │  |
|  │ • Who should I contact for support?                     │  |
|  │                                                         │  |
|  │ [View All FAQs]                                         │  |
|  └─────────────────────────────────────────────────────────┘  |
|                                                               |
|  Still need help? [Contact Support]                           |
|                                                               |
+---------------------------------------------------------------+
```
### 7. Mobile View (Search Interface)
```
+-----------------------------+
|                             |
|        EXASPERATION         |
|                             |
| ┌-------------------------┐ |
| | Search Documentation  🔍| |
| └-------------------------┘ |
|                             |
| Example queries:            |
| • How do I set up Cisco ACS?|
| • Parsers for 1Password?    |
| • T1070.001 detection       |
|                             |
| [Filters ▼]                 |
|                             |
| ┌-------------------------┐ |
| | Document Types:         | |
| | □ All  □ Use Cases      | |
| | □ Parsers □ Data Sources| |
| |                         | |
| | Vendors:                | |
| | □ All  □ Microsoft      | |
| | □ Cisco  □ More...      | |
| |                         | |
| | [Apply] [Reset]         | |
| └-------------------------┘ |
|                             |
| Recent Searches:            |
| • Lateral movement use case |
| • Cisco ASA logs format     |
| • Windows event ID 4624     |
|                             |
+-----------------------------+

## UI Changes

## Overview
This document details all changes implemented to the EXABOMINATION UI (formerly EXASPERATION), focusing on complete rebranding, content relevance, and UI enhancements.

## 1. Rebranding Changes

### Name Change
- Fully rebranded from "EXASPERATION" to "EXABOMINATION" throughout the application
- Updated all references in headers, titles, and documentation
- Changed browser page title to "EXABOMINATION - Exabeam CIM Documentation Search"

### Focus Change
- Emphasized "Common Information Model" (CIM) as the core content focus
- Added CIM indicator to the header
- Updated footer text to reference the Common Information Model
- Changed the subheader to highlight Exabeam CIM Documentation Search

### Visual Identity
- Maintained the dark theme but with more professional presentation
- Removed "Mad Scientist Mode" checkbox
- Updated header with CIM indicator icon
- Modernized the footer content

## 2. Content-Relevant Example Queries

Updated example queries to reflect the actual Exabeam Common Information Model content:


```
### 8. Mobile View (Results)
```
+-----------------------------+
|                             |
|        EXASPERATION         |
|                             |
| ┌-------------------------┐ |
| | Password reset rule   🔍| |
| └-------------------------┘ |
|                             |
| Results:                    |
|                             |
| ┌-------------------------┐ |
| |                         | |
| | The password reset      | |
| | detection rule works by | |
| | monitoring authentica-  | |
| | tion events that        | |
| | indicate a password has | |
| | been changed or reset.  | |
| |                         | |
| | In Microsoft Active     | |
| | Directory environments, | |
| | this primarily uses     | |
| | Event ID 4724 (password | |
| | reset attempt).         | |
| |                         | |
| | 👍 Helpful  👎 Not     | |
| |                         | |
| └-------------------------┘ |
|                             |
| Sources:                    |
|                             |
| ┌-------------------------┐ |
| | 📄 Password Reset Use   | |
| |   Case                  | |
| |   Relevance: 92%        | |
| |   [Expand]              | |
| └-------------------------┘ |
|                             |
| ┌-------------------------┐ |
| | 📄 AD Password Events   | |
| |   Relevance: 87%        | |
| |   [Expand]              | |
| └-------------------------┘ |
|                             |
| Follow-up Questions:        |
| • Configure alerting?       |
| • Password reset events?    |
|                             |
+-----------------------------+
```
These mockups provide a visual reference for the implementation of the EXASPERATION frontend, showing the key user interface elements, layouts, and interactions across different views and devices.