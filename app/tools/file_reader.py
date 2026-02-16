from pathlib import Path
from typing import Dict, List
import csv
import PyPDF2


def read_file(file_path: str, chunk_size: int = 1000) -> Dict:
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_path (str): Path to the file
        max_chars (int) : Maximum number if characters to return 

    Returns:
        Dict: {
            "status": "success" | "error",
            "file_type":str,
            "chunks": [list of text chunks] OR "message": error
        }
    """
    path = Path(file_path)

    if not path.exists():
        return {"status": "error", "message": f"File {path} does not exist."}
    
    file_type = path.suffix.lower()

    try:
        if file_type == ".txt":
            text = _read_txt(path)
        elif file_type == ".pdf":
            text = _read_pdf(path)
        elif file_type == ".csv":
            text = _read_csv(path)

        else:
            return {"status": "error", "message": "Unsupported file type"}

        chunks = _chunk_text(text, chunk_size)

        return {
            "status": "success",
            "file_type": file_type,
            "chunks": chunks
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def _read_txt(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def _read_pdf(path: Path) -> str:
    text = ""
    with open(path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def _read_csv(path: Path) -> str:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            rows.append(",".join(row))
    return "\n".join(rows)

def _chunk_text(text: str, chunk_size: int) -> List[str]:
    """
    Splits long text into smaller chunks so LLM can process safely.
    """
    text = text.strip()
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])

    return chunks