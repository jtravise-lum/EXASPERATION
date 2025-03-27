# EXASPERATION Frontend Mockups

This document provides text-based mockups of the key screens in the EXASPERATION frontend application.

## 1. Main Search Interface

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

## 2. Search Results

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

## 3. Expanded Source View

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

## 4. Advanced Search Interface

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

## 5. User Preferences

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

## 6. Help and Documentation

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

## 7. Mobile View (Search Interface)

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
```

## 8. Mobile View (Results)

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