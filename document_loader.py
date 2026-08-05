import os
import pandas as pd
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from docx import Document

# Path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(uploaded_file):
    file_name = uploaded_file.name.lower()
    file_extension = os.path.splitext(file_name)[1]

    # =====================================================
    # TXT / MARKDOWN
    # =====================================================
    if file_extension in [".txt", ".md"]:
        return uploaded_file.getvalue().decode(
            "utf-8",
            errors="ignore"
        )

    # =====================================================
    # PDF (PyMuPDF + OCR fallback)
    # =====================================================
    elif file_extension == ".pdf":

        pdf_bytes = uploaded_file.getvalue()

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        text = ""

        for page in document:

            page_text = page.get_text().strip()

            if page_text:
                text += page_text + "\n"

            else:
                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2)
                )

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                ocr_text = pytesseract.image_to_string(image)

                text += ocr_text + "\n"

        document.close()

        return text

    # =====================================================
    # DOCX
    # =====================================================
    elif file_extension == ".docx":

        document = Document(uploaded_file)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )

        return text

    # =====================================================
    # CSV
    # =====================================================
    elif file_extension == ".csv":

        dataframe = pd.read_csv(uploaded_file)

        return dataframe.to_string(index=False)

    # =====================================================
    # EXCEL
    # =====================================================
    elif file_extension in [".xlsx", ".xls"]:

        excel_file = pd.ExcelFile(uploaded_file)

        text = ""

        for sheet_name in excel_file.sheet_names:

            dataframe = pd.read_excel(
                excel_file,
                sheet_name=sheet_name
            )

            text += (
                f"\n\n===== SHEET: {sheet_name} =====\n\n"
            )

            text += dataframe.to_string(index=False)

        return text

    # =====================================================
    # JSON / XML / RTF
    # =====================================================
    elif file_extension in [".json", ".xml", ".rtf"]:

        return uploaded_file.getvalue().decode(
            "utf-8",
            errors="ignore"
        )

    # =====================================================
    # Unsupported
    # =====================================================
    return ""