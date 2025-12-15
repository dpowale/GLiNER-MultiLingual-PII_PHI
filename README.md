# GLiNER MultiLingual PII/PHI Extraction Service

A FastAPI service for extracting Personally Identifiable Information (PII) and Protected Health Information (PHI) from text using the [GLiNER Multi-PII Model](https://huggingface.co/urchade/gliner_multi_pii-v1).

## Features

- 🌍 **Multilingual Support** - English, French, German, Spanish, and more
- 🔍 **50+ Entity Types** - Person, email, phone, SSN, address, medical conditions, etc.
- ⚡ **Fast API** - RESTful endpoints with automatic documentation
- 🎯 **Configurable Threshold** - Adjust confidence levels for entity detection
- 🖥️ **Cross-Platform** - Works on Windows, Linux, and macOS
- 🎨 **Streamlit UI** - Interactive web interface for testing and visualization

## Supported Entity Types

| Category | Entity Types |
|----------|-------------|
| **Personal** | person, date of birth, nationality |
| **Contact** | email, phone number, mobile phone number, address |
| **Financial** | credit card number, bank account number, iban, cvv |
| **Government IDs** | social security number, passport number, driver's license number, tax identification number, national id number |
| **Medical** | medical condition, medication, health insurance id number, medical record number |

## Quick Start

### Step 1: Clone the Repository

```bash
git clone <repository-url> GLiNER_MultiLingual_PII_PHI
cd GLiNER_MultiLingual_PII_PHI
```

### Step 2: Install uv (if not installed)

**Windows (PowerShell):**
```powershell
pip install uv
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or with pip:
```bash
pip install uv
```

### Step 3: Create Virtual Environment

**Windows:**
```powershell
uv venv
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
uv venv
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
uv pip install -r requirements.txt
```

### Step 5: Start the Service

```bash
python main_service.py
```

Or with uvicorn directly:

```bash
uvicorn main_service:app --host 127.0.0.1 --port 8000 --reload
```

You should see:

```
INFO:     Loading GLiNER PII model...
INFO:     Model loaded successfully
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 6: Test the Service

**Option A: Open API Docs in Browser**

http://127.0.0.1:8000/docs

**Option B: Test with curl (Linux/macOS/Windows)**

```bash
# Health check
curl http://127.0.0.1:8000/health

# Extract PII
curl -X POST "http://127.0.0.1:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{"text":"John Smith email is john@test.com and phone is 555-123-4567"}'
```

**Option C: Test with PowerShell (Windows)**

```powershell
# Health check
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"

# Extract PII
$body = '{"text":"John Smith email is john@test.com and phone is 555-123-4567"}'
Invoke-RestMethod -Uri "http://127.0.0.1:8000/extract" -Method Post -Body $body -ContentType "application/json"
```

**Option D: Streamlit Web UI**

For an interactive web interface, run the Streamlit app:

```bash
# Make sure the FastAPI service is running first, then:
streamlit run streamlit_app.py
```

Open http://localhost:8501 in your browser.

## Streamlit UI

The Streamlit app provides an interactive interface for testing the PII extraction service:

### Features

- **Service Health Check** - Real-time connection status to the FastAPI backend
- **Configurable Threshold** - Slider to adjust detection sensitivity (0.0-1.0)
- **Entity Type Selection** - Choose specific PII/PHI types or select all
- **Sample Texts** - Pre-loaded examples (Medical Record, Financial Document, Business Contact, International Document)
- **Results Display** - Summary metrics, entity breakdown, and detailed entity list with confidence scores
- **Highlighted Text View** - Visual color-coded highlighting of detected entities
- **Raw JSON Output** - Expandable section with the full API response

### Running the Streamlit App

**Windows:**
```powershell
# Terminal 1: Start FastAPI service
.venv\Scripts\python.exe -m uvicorn main_service:app --reload

# Terminal 2: Start Streamlit app
.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

**Linux/macOS:**
```bash
# Terminal 1: Start FastAPI service
source .venv/bin/activate
uvicorn main_service:app --reload

# Terminal 2: Start Streamlit app
source .venv/bin/activate
streamlit run streamlit_app.py
```

### Screenshot

The UI includes:
- Left panel: Input text area with sample text selector
- Right panel: Extraction results with entity details
- Bottom: Highlighted text with color-coded entities and legend

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/entities` | List supported entity types |
| GET | `/docs` | Swagger UI documentation |
| POST | `/extract` | Extract PII entities from text |

## Example Request/Response

**Request:**

```json
{
  "text": "Contact John Smith at john.smith@email.com or call 555-123-4567",
  "threshold": 0.5
}
```

**Response:**

```json
{
  "entities": [
    {"text": "John Smith", "label": "person", "start": 8, "end": 18, "score": 0.98},
    {"text": "john.smith@email.com", "label": "email", "start": 22, "end": 42, "score": 0.99},
    {"text": "555-123-4567", "label": "phone number", "start": 51, "end": 63, "score": 0.96}
  ],
  "text": "Contact John Smith at john.smith@email.com or call 555-123-4567",
  "entity_count": 3,
  "entity_types": {"person": 1, "email": 1, "phone number": 1}
}
```

## Running Tests

```bash
# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Run all tests
pytest test_extraction.py -v

# Run specific test class
pytest test_extraction.py::TestPersonExtraction -v

# Run multilingual tests
pytest test_extraction.py::TestMultilingualParagraphs -v

# Run with short traceback
pytest test_extraction.py -v --tb=short
```

## Project Structure

```
GLiNER_MultiLingual_PII_PHI/
├── main_service.py      # FastAPI service
├── streamlit_app.py     # Streamlit web UI for testing
├── test_extraction.py   # Pytest test cases
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── .venv/               # Virtual environment
```

## Model Information

- **Model**: [urchade/gliner_multi_pii-v1](https://huggingface.co/urchade/gliner_multi_pii-v1)
- **Size**: ~1.16 GB
- **Base Model**: microsoft/mdeberta-v3-base

**Cache Location:**

| OS | Path |
|----|------|
| Windows | `C:\Users\<username>\.cache\huggingface\hub\models--urchade--gliner_multi_pii-v1` |
| Linux | `~/.cache/huggingface/hub/models--urchade--gliner_multi_pii-v1` |
| macOS | `~/.cache/huggingface/hub/models--urchade--gliner_multi_pii-v1` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Model not loaded` | Wait for startup to complete or check disk space |
| `Connection refused` | Ensure service is running on port 8000 |
| `Import error` | Run `uv pip install -r requirements.txt` |
| `CUDA out of memory` | Model runs on CPU by default |
| `Permission denied (Linux)` | Run `chmod +x` or check file permissions |
| `uv not found` | Restart terminal after installing uv |

## Environment Variables (Optional)

```bash
# Set custom Hugging Face cache directory
export HF_HOME=/path/to/cache  # Linux/macOS
set HF_HOME=C:\path\to\cache   # Windows

# Disable symlinks (Windows - fixes download errors)
set HF_HUB_DISABLE_SYMLINKS_WARNING=1
```

## Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install uv && uv pip install --system -r requirements.txt

COPY main_service.py .
EXPOSE 8000

CMD ["uvicorn", "main_service:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t gliner-pii .
docker run -p 8000:8000 gliner-pii
```

## License

MIT License

## References

- [GLiNER GitHub](https://github.com/urchade/GLiNER)
- [GLiNER Multi-PII Model](https://huggingface.co/urchade/gliner_multi_pii-v1)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [uv Documentation](https://github.com/astral-sh/uv)
