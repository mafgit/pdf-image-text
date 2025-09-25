# Extract Text & Diagrams from PDFs

> Extracts complete text from PDF, even from images inside it, and saves images/diagrams separately.

#### Why did I make it?

When using tools like ChatGPT or NotebookLM for summarizing or explaining university lectures (PDFs) provided by universities, there is often an issue that all the content that is in the form of images (diagrams, etc) gets ignored by these tools unless you manually take screenshot of the page and use an online OCR which would have limits. So, this program will simplify your task by helping you extract complete text and all diagrams from PDFs.

## Usage

### 1. Convert Single PDF
```py
def convert(filepath: str, min_chars=512, save_images=False) -> str
```

Args:
- `filename (str)`: Path to PDF file
- `min_chars (int)`: If no. of characters in a page that are directly extractable are less than min_chars, it would be processed using OCR, otherwise it would just be extracted simply. Use 0 if you want to force OCR for all page.
- `save_images (bool)`: If true, every image (e.g. diagram) found inside each page will be saved in output folder in the format <page_num>_<img_no>.<img_text>

### 4. Convert Multiple PDFs
```py
def convert_multi(filepaths: List[str], **kwargs)
```

## Requirements

- `Tesseract`: You can download it from https://github.com/tesseract-ocr/tesseract/releases
- `Python>=3.9`