from fastapi import HTTPException, APIRouter, File, UploadFile
from utils.excel_import import extract_from_file
import tempfile
import shutil
import os 

upload_router = APIRouter(prefix="/upload", tags=["upload"])


@upload_router.post("/file")
async def uploads(
    file: UploadFile = File(...),
):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=400, detail="Only .xlsx Excel files are supported."
        )

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path = tmp.name
    except Exception as e:
        print(f"error, {e}")

    try:
        await extract_from_file(temp_path)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process Excel file: {e}"
        )
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
