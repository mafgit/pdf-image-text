# pdf-image-text — Extract Text & Diagrams from PDFs

> Extracts complete text from PDF, even from images inside it, and saves images/diagrams separately.

#### Why did I make it?

Ever tried summarizing university lecture PDFs with **ChatGPT**, **NotebookLM**, or other AI tools, only to find they completely miss the text inside images, scanned pages, or diagrams? Online OCR tools exist, but they’re either limited, slow, or too much hassle.

## Usage

### 1. Installation
```bash
pip install git+https://github.com/mafgit/pdf-image-text
```

### 2. Import & Example
```py
from pdf_image_text import convert, convert_multi

text = convert_multi(
    ['IS_Week # 2.pdf', 'IS_Week # 3.pdf', 'IS_Week # 3.pdf'],
     min_chars=0 # FORCE OCR FOR EVERY PAGE
     save_images=True,
)
```

### 3. Convert Single PDF
```py
def convert(
    filepath: str, 
    min_chars=512, 
    save_images=False, 
    save_text_file=True, 
    langs=['eng']
) -> str
```

Args:
- **filepath (str)**: Path to PDF file
- **min_chars (int)**: If no. of characters in a page that are directly extractable are less than min_chars, it would be processed using OCR, otherwise it would just be extracted simply. Use 0 if you want to force OCR for all page.
- **save_images (bool)**: If true, every image (e.g. diagram) found inside each page will be saved in output folder in the format <page_num>_<img_no>.<img_text>
- **langs (List[str])**: List of languages used in PDF in order of importance for OCR (you should have language packs installed if you add other languages)
- **save_text_file (bool)**

### 4. Convert Multiple PDFs
```py
def convert_multi(
    filepaths: List[str], single_text_file=True,
    **kwargs
) -> str
```

- **filepath (str)**: Path to PDF file
- **single_text_file (bool)**: If true, all textual content will be stored in a single .txt file instead of separate files 
- **min_chars (int)**: If no. of characters in a page that are directly extractable are less than min_chars, it would be processed using OCR, otherwise it would just be extracted simply. Use 0 if you want to force OCR for all page.
- **save_images (bool)**: If true, every image (e.g. diagram) found inside each page will be saved in output folder in the format <page_num>_<img_no>.<img_text>
- **langs (List[str])**: List of languages used in PDF in order of importance for OCR (you should have language packs installed if you add other languages)
- **save_text_file** (bool)

## Requirements

- `Tesseract`: You can download it from https://github.com/tesseract-ocr/tesseract/releases. Add it to system's PATH environment variables as well.
- `Python>=3.9`