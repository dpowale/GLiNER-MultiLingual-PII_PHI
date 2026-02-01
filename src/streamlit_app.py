"""
Streamlit App for testing GLiNER PII/PHI Extraction Service
"""
import streamlit as st
import requests
import json
from typing import List, Optional

# Configuration
DEFAULT_API_URL = "http://localhost:8000"

# Supported PII/PHI entity types
SUPPORTED_ENTITIES = [
    "person",
    "organization", 
    "phone number",
    "address",
    "passport number",
    "email",
    "credit card number",
    "social security number",
    "health insurance id number",
    "date of birth",
    "mobile phone number",
    "bank account number",
    "medication",
    "cpf",
    "driver's license number",
    "tax identification number",
    "medical condition",
    "identity card number",
    "national id number",
    "ip address",
    "email address",
    "iban",
    "credit card cvv",
    "credit card expiration date",
    "pin",
    "security code",
    "medical record number",
    "license plate number",
    "insurance number"
]

# Sample texts for testing
SAMPLE_TEXTS = {
    "Medical Record": """Patient John Smith, DOB: 03/15/1985, was admitted on December 10, 2024. 
Medical Record Number: MRN-2024-78543. SSN: 123-45-6789.
Patient is currently taking Metformin 500mg for Type 2 Diabetes.
Contact: john.smith@email.com, Phone: (555) 123-4567.
Insurance ID: BCBS-98765432. Address: 123 Oak Street, Boston, MA 02101.""",
    
    "Financial Document": """Account holder: Maria Garcia
Bank Account: 1234567890123456
Credit Card: 4532-1234-5678-9012, CVV: 123, Exp: 12/25
IBAN: DE89370400440532013000
Tax ID: 987-65-4321
Email: maria.garcia@company.com
Address: 456 Pine Avenue, New York, NY 10001""",
    
    "Business Contact": """Contact: Dr. Emily Johnson
Organization: Healthcare Solutions Inc.
Phone: +1-800-555-0199
Mobile: (555) 987-6543
Email: emily.johnson@healthsolutions.com
Office: 789 Corporate Blvd, Suite 500, Chicago, IL 60601
Driver's License: D1234567890 (State: IL)""",
    
    "International Document": """Passenger: Ahmed Hassan
Passport Number: AB1234567
National ID: 29001011234567
Date of Birth: January 1, 1990
Address: 15 Tahrir Square, Cairo, Egypt
Phone: +20-123-456-7890
Email: ahmed.hassan@mail.com
CPF: 123.456.789-00"""
}


def check_service_health(api_url: str) -> dict:
    """Check if the GLiNER service is running and healthy."""
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"status": "unreachable", "model_loaded": False}
    except Exception as e:
        return {"status": f"error: {str(e)}", "model_loaded": False}


def extract_entities(api_url: str, text: str, entities: Optional[List[str]], threshold: float) -> dict:
    """Call the extraction API endpoint."""
    try:
        payload = {
            "text": text,
            "threshold": threshold,
            "flat_ner": True
        }
        if entities:
            payload["entities"] = entities
            
        response = requests.post(f"{api_url}/extract", json=payload, timeout=30)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to the API service. Make sure it's running."}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"API Error: {e.response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def highlight_entities(text: str, entities: list) -> str:
    """Create highlighted text with entity annotations."""
    if not entities:
        return text
    
    # Sort entities by start position in reverse order
    sorted_entities = sorted(entities, key=lambda x: x["start"], reverse=True)
    
    # Color mapping for different entity types
    colors = {
        "person": "#FF6B6B",
        "organization": "#4ECDC4",
        "phone number": "#45B7D1",
        "mobile phone number": "#45B7D1",
        "address": "#96CEB4",
        "email": "#FFEAA7",
        "email address": "#FFEAA7",
        "credit card number": "#DDA0DD",
        "social security number": "#FF7F50",
        "date of birth": "#98D8C8",
        "medication": "#F7DC6F",
        "medical condition": "#BB8FCE",
        "passport number": "#85C1E9",
        "driver's license number": "#F8B500",
        "bank account number": "#82E0AA",
        "health insurance id number": "#F1948A",
        "tax identification number": "#AED6F1",
        "medical record number": "#FAD7A0",
        "iban": "#D7BDE2",
        "ip address": "#A9DFBF",
        "national id number": "#F5B7B1",
        "identity card number": "#D5DBDB",
        "cpf": "#ABEBC6",
    }
    
    highlighted = text
    for entity in sorted_entities:
        start = entity["start"]
        end = entity["end"]
        label = entity["label"]
        score = entity["score"]
        color = colors.get(label.lower(), "#E8E8E8")
        
        entity_html = f'<mark style="background-color: {color}; padding: 2px 4px; border-radius: 3px;" title="{label}: {score:.2f}">{text[start:end]}</mark>'
        highlighted = highlighted[:start] + entity_html + highlighted[end:]
    
    return highlighted


def main():
    st.set_page_config(
        page_title="GLiNER PII/PHI Extractor",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 GLiNER PII/PHI Extraction Tester")
    st.markdown("Test the GLiNER MultiLingual PII/PHI extraction service")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    api_url = st.sidebar.text_input("API URL", value=DEFAULT_API_URL)
    
    # Health check
    health = check_service_health(api_url)
    if health["status"] == "healthy":
        st.sidebar.success("✅ Service is healthy")
    elif health["status"] == "unreachable":
        st.sidebar.error("❌ Service unreachable")
        st.sidebar.info("Start the service with: `uvicorn main_service:app --reload`")
    else:
        st.sidebar.warning(f"⚠️ Status: {health['status']}")
    
    # Threshold slider
    threshold = st.sidebar.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Minimum confidence score for entity detection"
    )
    
    # Entity type selection
    st.sidebar.header("🏷️ Entity Types")
    select_all = st.sidebar.checkbox("Select All Entities", value=True)
    
    if select_all:
        selected_entities = SUPPORTED_ENTITIES
    else:
        selected_entities = st.sidebar.multiselect(
            "Select specific entities",
            options=SUPPORTED_ENTITIES,
            default=["person", "email", "phone number", "address", "organization"]
        )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input Text")
        
        # Sample text selector
        sample_choice = st.selectbox(
            "Load sample text",
            options=["Custom"] + list(SAMPLE_TEXTS.keys())
        )
        
        if sample_choice != "Custom":
            default_text = SAMPLE_TEXTS[sample_choice]
        else:
            default_text = ""
        
        input_text = st.text_area(
            "Enter text to analyze",
            value=default_text,
            height=300,
            placeholder="Enter or paste text containing PII/PHI information..."
        )
        
        extract_button = st.button("🔍 Extract Entities", type="primary", use_container_width=True)
    
    with col2:
        st.header("📊 Results")
        
        if extract_button:
            if not input_text.strip():
                st.warning("Please enter some text to analyze.")
            elif health["status"] != "healthy":
                st.error("Cannot extract entities. Please ensure the API service is running.")
            else:
                with st.spinner("Extracting entities..."):
                    result = extract_entities(
                        api_url, 
                        input_text, 
                        selected_entities if not select_all else None,
                        threshold
                    )
                
                if result["success"]:
                    data = result["data"]
                    entities = data["entities"]
                    
                    # Summary metrics
                    metric_cols = st.columns(3)
                    with metric_cols[0]:
                        st.metric("Total Entities", data["entity_count"])
                    with metric_cols[1]:
                        st.metric("Unique Types", len(data["entity_types"]))
                    with metric_cols[2]:
                        if entities:
                            avg_score = sum(e["score"] for e in entities) / len(entities)
                            st.metric("Avg Confidence", f"{avg_score:.2%}")
                        else:
                            st.metric("Avg Confidence", "N/A")
                    
                    # Entity type breakdown
                    if data["entity_types"]:
                        st.subheader("Entity Types Found")
                        for entity_type, count in sorted(data["entity_types"].items()):
                            st.write(f"- **{entity_type}**: {count}")
                    
                    # Detailed entity list
                    if entities:
                        st.subheader("Detected Entities")
                        for i, entity in enumerate(entities, 1):
                            with st.expander(f"{i}. {entity['text']} ({entity['label']})"):
                                st.write(f"**Label:** {entity['label']}")
                                st.write(f"**Text:** `{entity['text']}`")
                                st.write(f"**Position:** {entity['start']} - {entity['end']}")
                                st.progress(entity['score'], text=f"Confidence: {entity['score']:.2%}")
                    else:
                        st.info("No entities found with the current threshold.")
                else:
                    st.error(result["error"])
    
    # Highlighted text section (full width)
    if extract_button and input_text.strip() and health["status"] == "healthy":
        result = extract_entities(
            api_url, 
            input_text, 
            selected_entities if not select_all else None,
            threshold
        )
        if result["success"] and result["data"]["entities"]:
            st.header("🎨 Highlighted Text")
            highlighted_html = highlight_entities(input_text, result["data"]["entities"])
            st.markdown(
                f'<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; line-height: 1.8;">{highlighted_html}</div>',
                unsafe_allow_html=True
            )
            
            # Legend
            st.subheader("Legend")
            legend_cols = st.columns(4)
            legend_items = [
                ("Person", "#FF6B6B"),
                ("Organization", "#4ECDC4"),
                ("Phone", "#45B7D1"),
                ("Address", "#96CEB4"),
                ("Email", "#FFEAA7"),
                ("Credit Card", "#DDA0DD"),
                ("SSN", "#FF7F50"),
                ("DOB", "#98D8C8"),
            ]
            for i, (name, color) in enumerate(legend_items):
                with legend_cols[i % 4]:
                    st.markdown(
                        f'<span style="background-color: {color}; padding: 2px 8px; border-radius: 3px;">{name}</span>',
                        unsafe_allow_html=True
                    )
    
    # JSON output section
    if extract_button and input_text.strip() and health["status"] == "healthy":
        result = extract_entities(
            api_url, 
            input_text, 
            selected_entities if not select_all else None,
            threshold
        )
        if result["success"]:
            with st.expander("📋 Raw JSON Response"):
                st.json(result["data"])


if __name__ == "__main__":
    main()
