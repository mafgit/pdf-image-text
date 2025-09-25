# pip install pytesseract PyMuPDF pillow
import pytesseract
from PIL import Image
import fitz
import io
import os
import shutil
from typing import List

def convert(filepath: str, min_chars=512, save_images=False) -> str:
    """Extracts complete text from PDF and saves images/diagrams separately
    
    Args:
        filename (str): Path to PDF file
        min_chars (int): If no. of characters in a page that are directly extractable are less than min_chars, it would be processed using OCR, otherwise it would just be extracted simply. Use 0 if you want to force OCR for all page.
        save_images (bool): If true, every image (e.g. diagram) found inside each page will be saved in output folder in the format <page_num>_<img_no>.<img_text>
    """
    pdf = fitz.open(filepath)

    title = os.path.splitext(os.path.basename(filepath))[0]
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

                text += pytesseract.image_to_string(pil_img)

        full_text += text
    
    with open(f'{title}/full_text.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
        
    return full_text


def convert_multi(filepaths: List[str], **kwargs):
    """Extracts complete text from PDFs and saves images/diagrams separately
    
    Args:
        filename (str): Path to PDF file
        min_chars (int): If no. of characters in a page that are directly extractable are less than min_chars, it would be processed using OCR, otherwise it would just be extracted simply. Use 0 if you want to force OCR for all page.
        save_images (bool): If true, every image (e.g. diagram) found inside each page will be saved in output folder in the format <page_num>_<img_no>.<img_text>
    """
    for filepath in filepaths:
        print(f'Processing {filepath}')
        convert(filepath, **kwargs)


convert_multi(['IS_Week # 2.pdf', 'IS_Week # 3.pdf', 'Week # 4.pdf'])