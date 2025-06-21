from fastapi import HTTPException, APIRouter, File, UploadFile, status
from utils.excel_import import extract_from_file
from utils.upload_google import upload_to_bucket
from utils.inserting_multi_images import insert_data
import tempfile
import shutil
import os

upload_router = APIRouter(prefix="/upload", tags=["upload"])


@upload_router.post("/file", status_code=status.HTTP_200_OK)
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
        run = await extract_from_file(temp_path)
        if not run:
            raise HTTPException(
                status_code=500, detail=f"cannot find the image in the xlsx file"
            )
        else:
            return {"detail": "uploaded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process Excel file: {e}"
        )
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


@upload_router.post("/images", status_code=status.HTTP_200_OK)
async def uploads_images(
    event_id: int,
    files: list[UploadFile] = File(...)):
    saved_files = []
    for image in files:
        image_name = image.filename
        saved_files.append(image_name)
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, detail=f"{image.filename} is not a valid image"
            )
        output_directory = "/home/kevin/projects/tread-events-python/images/"
        file_path = os.path.join(output_directory, image.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to process images: {e}"
            )
        try:
            await insert_data(event_id, image_name)
        except:
            raise HTTPException(
                status_code=500, detail=f"Failed to insert image to db"
            )
        try:
            complete_path_image = os.path.join(output_directory, image_name)
            upload_to_bucket(complete_path_image, image_name)
        except:
            raise HTTPException(
                status_code=500, detail=f"Failed to load images to bucket: {e}"
            )
    return {"uploaded_files": saved_files}
