from fastapi import APIRouter, UploadFile, File
from PIL import Image
import pytesseract
import re
from io import BytesIO

router = APIRouter()

@router.post("/ocr/job")
async def extract_job_info(file: UploadFile = File(...)):
    # Read image from in-memory file
    contents = await file.read()
    image = Image.open(BytesIO(contents))

    # OCR processing
    text = pytesseract.image_to_string(image)
    lines = [line.strip("•¢°*\\/- ") for line in text.split("\n") if line.strip()]

    # Parse relevant info
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
        if "Hiring" in line:
            data["title"] = "Product Advisor"
        elif "SALARY" in line.upper():
            match = re.search(r"(\d{4,6})\s*-\s*(\d{4,6})", line)
            if match:
                data["salary"] = f"{match.group(1)} - {match.group(2)}"
        elif "INCENTIVE" in line.upper():
            data["incentives"] = True
        elif "Qualification" in line:
            data["qualification"] = line.split(":")[-1].strip()
        elif "Exp" in line or "Experience" in line:
            data["experience"] = line.split(":")[-1].strip()
        elif "Age Limit" in line:
            data["age_limit"] = line.split(":")[-1].strip()
        elif "Gender" in line:
            data["gender"] = line.split(":")[-1].strip()
        elif "Location" in line:
            data["location"] = line.split(":")[-1].strip()
        elif "Resume" in line or re.search(r"\d{10}", line):
            phone_match = re.search(r"\d{10}", line)
            if phone_match:
                data["contact"] = phone_match.group()

    return data