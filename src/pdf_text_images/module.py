# pip install pytesseract PyMuPDF pillow
import pytesseract
from PIL import Image
import fitz
import io
import os
import shutil
from typing import List

__all__ = ['convert', 'convert_multi']
__version__ = "0.1.0"

def convert(filepath: str, min_chars=512, save_images=False, save_text_file=True, langs=['eng']) -> str:
    """Extracts complete text from PDF and saves images/diagrams separately
    
    Args:
        - **filepath (str)**: Path to PDF file
        - **min_chars (int)**: If **no. of characters in a page that are directly extractable are less than min_chars, it would be processed using OCR, otherwise it would just be extracted simply. Use 0 if you want to force OCR for all page.
        - **save_images (bool)**: If true, every image (e.g. diagram) found inside each page will be saved in output folder in the format <page_num>_<img_no>.<img_text>
        - **langs (List[str])**: List of languages used in PDF in order of importance for OCR (you should have language packs installed if you add other languages)
        - **save_text_file (bool)**
    """
    pdf = fitz.open(filepath)

    title = os.path.splitext(os.path.basename(filepath))[0]
    if save_images:
        if os.path.exists(title):
            shutil.rmtree(title)
        os.mkdir(title)

    full_text = ""
    for page_idx in range(pdf.page_count):
        print(f'\n> Page {page_idx + 1}/{pdf.page_count}...')

        page = pdf.load_page(page_idx)
        text = ""

        if min_chars:
            text = page.get_text().strip() # pyright: ignore[reportAttributeAccessIssue]

        if not min_chars or len(text) < min_chars:
            print('Using OCR for this page...')
            imgs = page.get_images(full=True)
            if not imgs:
                continue

            text = ""
            for img_no, img in enumerate(imgs, start=1):
                xref = img[0]
                base_img = pdf.extract_image(xref)
                img_bytes = base_img['image']
                img_ext = base_img['ext']

                pil_img = Image.open(io.BytesIO(img_bytes))

                if save_images:
                    pil_img.save(f'{title}/{page_idx + 1}_{img_no}.{img_ext}')

                try:
                    text += pytesseract.image_to_string(pil_img, lang="+".join(langs))
                except pytesseract.TesseractNotFoundError:
                    raise RuntimeError("Error: Tesseract OCR is not installed on your system.\nInstall it first from https://github.com/tesseract-ocr/tesseract/releases")

        full_text += f"----------- Page {page_idx + 1} -----------\n{text.strip()}\n"
    
    if save_text_file:
        with open(f'{title}.txt', 'w', encoding='utf-8') as f:
            f.write(full_text)
        
    return full_text


def convert_multi(filepaths: List[str], single_text_file=True, **kwargs) -> str:
    """Extracts complete text from PDFs and saves images/diagrams separately
    
    Args:
        - **filepath (str)**: Path to PDF file
        - **single_text_file (bool)**: If true, all textual content will be stored in a single .txt file instead of separate files 
        - **min_chars (int)**: If no. of characters in a page that are directly extractable are less than min_chars, it would be processed using OCR, otherwise it would just be extracted simply. Use 0 if you want to force OCR for all page.
        - **save_images (bool)**: If true, every image (e.g. diagram) found inside each page will be saved in output folder in the format <page_num>_<img_no>.<img_text>
        - **langs (List[str])**: List of languages used in PDF in order of importance for OCR (you should have language packs installed if you add other languages)
        - **save_text_file (bool)**
    """
    full_text = ""
    for filepath in filepaths:
        print(f'Processing {filepath}')
        text = convert(filepath, save_text_file=not single_text_file, **kwargs)
        full_text += f"=========== File: {os.path.basename(filepath)} ===========\n{text.strip()}\n"

    if single_text_file:
        with open(f'full_text.txt', 'w', encoding='utf-8', errors="replace") as f:
            f.write(full_text)

    return full_text