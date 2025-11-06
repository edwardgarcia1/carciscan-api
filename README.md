# Carciscan API

A FastAPI-based web service that analyzes product ingredient labels to identify potential carcinogenic hazards and routes of exposure.

It uses OCR to extract text from an image, parses the ingredients, and then uses machine learning models to predict the carcinogenicity group and exposure routes for each chemical.

## Quick Start

### 1. Prerequisites

-   Python 3.8+
-   `pip`, or another dependency manager.
-   [DuckDB](https://duckdb.org/) database file (`carciscan.db`).

### 2. Installation

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd carciscan-api
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**
    -   Copy the example environment file (if provided) and fill in your values:
        ```bash
        cp .env.example .env
        ```
    -   Ensure the `DATABASE_URL` in your `.env` file points to the correct location of `carciscan.db`.

### 3. Running the Application

1.  **Start the Uvicorn server**
    ```bash
    uvicorn app.main:app --reload
    ```
    The `--reload` flag enables auto-reloading when code changes, which is great for development.

2.  **Access the API**
    -   **Interactive Docs**: Open your browser and navigate to `http://127.0.0.1:8000/docs`.
    -   **Root Endpoint**: `http://127.0.0.1:8000/`

## API Usage

### Endpoint: `POST /api/v1/predict`

Analyzes an image of an ingredient label.

-   **URL**: `/api/v1/predict`
-   **Method**: `POST`
-   **Content-Type**: `multipart/form-data`
-   **Body**: A file with the form field name `file`.

#### Example Request (using cURL)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predict" -F "file=@/path/to/your/image.png"
```

#### Example Response

```json
{
  "success": true,
  "message": "Analysis complete.",
  "ocr_result": {
    "text": "INGREDIENTS: WATER, GLYCERIN, FRAGRANCE",
    "ingredients": [
      "WATER",
      "GLYCERIN",
      "FRAGRANCE"
    ]
  },
  "ingredients": [
    {
      "name": "WATER",
      "prediction_details": {
        "carcinogenicity_group": "Group 3",
        "evidence": "Not classifiable as to its carcinogenicity to humans.",
        "confidence": 78.50,
        "route_of_exposure": ["Oral"]
      },
      "matched_name": "Water",
      "pubchem_url": "https://pubchem.ncbi.nlm.nih.gov/compound/962",
      "status": "Success"
    }
  ],
  "processing_time": 2.15,
  "practical_advice": [
    "Avoid ingestion. Wash hands thoroughly after handling."
  ]
}
```