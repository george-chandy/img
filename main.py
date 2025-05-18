# from PIL import Image
# import pytesseract
# import re

# def extract_text(image_path):
#     img = Image.open(image_path)
#     text = pytesseract.image_to_string(img)
#     return text

# def parse_fields(text):
#     # Very basic regex-based parsing
#     job_title = re.search(r"(?:Job|Role|Position):?\s*(.*)", text, re.IGNORECASE)
#     company = re.search(r"(?:Company|Organization):?\s*(.*)", text, re.IGNORECASE)
#     location = re.search(r"(?:Location):?\s*(.*)", text, re.IGNORECASE)

#     return {
#         "Job Title": job_title.group(1).strip() if job_title else "Not found",
#         "Company": company.group(1).strip() if company else "Not found",
#         "Location": location.group(1).strip() if location else "Not found",
#         "Full Text": text[:300] + "..." if len(text) > 300 else text  # preview
#     }

# if __name__ == "__main__":
#     path = "sample_images/job_post.png"  # change this path to your image
#     raw_text = extract_text(path)
#     fields = parse_fields(raw_text)

#     print("\n--- Extracted Fields ---")
#     for key, value in fields.items():
#         print(f"{key}: {value}")


from fastapi import FastAPI
from ocr.router import router as ocr_router

app = FastAPI()

app.include_router(ocr_router, prefix="/api")