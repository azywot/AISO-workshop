import pathlib

import fitz  # PyMuPDF


def read_pdf(file_path: str) -> str:
    """Read and extract all text content from a PDF file.

    Use this tool whenever a question references a PDF file or when file paths
    ending in .pdf are provided. Pass the exact file path given in the question.

    Args:
        file_path: The path to the PDF file to read.

    Returns:
        The full text content extracted from all pages of the PDF, with page markers.
    """
    try:
        # Resolve relative paths from the project root (two levels up from this file)
        resolved = pathlib.Path(file_path)
        if not resolved.is_absolute():
            project_root = pathlib.Path(__file__).parent.parent.parent
            resolved = project_root / file_path

        doc = fitz.open(str(resolved))
        text_parts = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            if page_text.strip():
                text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")
        doc.close()
        full_text = "\n".join(text_parts)
        if not full_text.strip():
            return "The PDF appears to contain no extractable text (it may be image-based)."
        return full_text
    except FileNotFoundError:
        return f"Error: File not found at '{file_path}'. Resolved to: '{resolved}'."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
