from fastapi import APIRouter, UploadFile, File
from io import BytesIO
import pytesseract
import re
from PIL import Image  # Required by pytesseract

router = APIRouter()

@router.post("/ocr/job")
async def extract_job_info(file: UploadFile = File(...)):
    # Read image directly into memory and run OCR
    image = Image.open(BytesIO(await file.read()))
    text = pytesseract.image_to_string(image)
    
    # Clean and split lines
    lines = [line.strip("•¢°*\\/- ").strip() for line in text.splitlines() if line.strip()]
    result = parse_job_info(lines)
    return {"data": result}


def parse_job_info(lines: list[str]) -> dict:
    data = {
        "title": None,
        "salary": None,
        "incentives": None,
        "qualification": None,
        "experience": None,
        "age_limit": None,
        "gender": None,
        "location": None,
        "contact": None,
    }

    for line in lines:
        l = line.lower()

        if "hiring" in l:
            data["title"] = data["title"] or "Product Advisor"
        elif "salary" in l:
            match = re.search(r"(\d{4,6})\s*[-to]\s*(\d{4,6})", line)
            if match:
                data["salary"] = f"{match.group(1)} - {match.group(2)}"
        elif "incentive" in l:
            data["incentives"] = True
        elif "qualification" in l:
            data["qualification"] = line.split(":")[-1].strip()
        elif "exp" in l or "experience" in l:
            data["experience"] = line.split(":")[-1].strip()
        elif "age limit" in l:
            data["age_limit"] = line.split(":")[-1].strip()
        elif "gender" in l:
            data["gender"] = line.split(":")[-1].strip()
        elif "location" in l:
            data["location"] = line.split(":")[-1].strip()
        elif "resume" in l or re.search(r"\d{10}", line):
            phone_match = re.search(r"\d{10}", line)
            if phone_match:
                data["contact"] = phone_match.group()

    return data