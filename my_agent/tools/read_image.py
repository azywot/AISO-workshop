import os
import pathlib


def read_image(file_path: str, question: str) -> str:
    """Analyze an image file and answer a question about it.

    Use this tool whenever a question references an image file (jpg, jpeg, png, gif, webp).
    Pass the exact file path and the full question to get an answer.

    Args:
        file_path: The path to the image file to analyze.
        question: The question to answer about the image.

    Returns:
        The answer to the question based on the image content.
    """
    try:
        from google import genai
        from google.genai import types

        # Resolve relative paths from the project root (two levels up from this file)
        resolved = pathlib.Path(file_path)
        if not resolved.is_absolute():
            project_root = pathlib.Path(__file__).parent.parent.parent
            resolved = project_root / file_path

        with open(resolved, "rb") as f:
            image_data = f.read()

        ext = file_path.rsplit(".", 1)[-1].lower()
        media_type_map = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
        }
        media_type = media_type_map.get(ext, "image/jpeg")

        client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=image_data, mime_type=media_type),
                question,
            ],
        )
        return response.text or "No response from image model."
    except FileNotFoundError:
        return f"Error: File not found at '{file_path}'."
    except Exception as e:
        return f"Error reading image: {str(e)}"
