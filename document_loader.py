import os

import tempfile

import pandas as pd

from pypdf import PdfReader

from docx import Document


def extract_text(
    uploaded_file
):

    file_name = uploaded_file.name.lower()

    file_extension = os.path.splitext(
        file_name
    )[1]


    # =====================================================
    # TXT / MARKDOWN
    # =====================================================

    if file_extension in [

        ".txt",

        ".md"

    ]:

        return uploaded_file.getvalue().decode(

            "utf-8",

            errors="ignore"

        )


    # =====================================================
    # PDF
    # =====================================================

    elif file_extension == ".pdf":

        temporary_path = None

        try:

            with tempfile.NamedTemporaryFile(

                delete=False,

                suffix=".pdf"

            ) as temporary_file:

                temporary_file.write(
                    uploaded_file.getbuffer()
                )

                temporary_path = (
                    temporary_file.name
                )

            text = ""

            reader = PdfReader(
                temporary_path
            )

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:

                    text += (
                        page_text
                        + "\n"
                    )

            return text

        finally:

            if (

                temporary_path

                and os.path.exists(
                    temporary_path
                )

            ):

                os.remove(
                    temporary_path
                )


    # =====================================================
    # DOCX
    # =====================================================

    elif file_extension == ".docx":

        temporary_path = None

        try:

            with tempfile.NamedTemporaryFile(

                delete=False,

                suffix=".docx"

            ) as temporary_file:

                temporary_file.write(
                    uploaded_file.getbuffer()
                )

                temporary_path = (
                    temporary_file.name
                )

            document = Document(
                temporary_path
            )

            text = "\n".join(

                paragraph.text

                for paragraph in document.paragraphs

                if paragraph.text.strip()

            )

            return text

        finally:

            if (

                temporary_path

                and os.path.exists(
                    temporary_path
                )

            ):

                os.remove(
                    temporary_path
                )


    # =====================================================
    # CSV
    # =====================================================

    elif file_extension == ".csv":

        dataframe = pd.read_csv(
            uploaded_file
        )

        return dataframe.to_string(
            index=False
        )


    # =====================================================
    # EXCEL
    # =====================================================

    elif file_extension in [

        ".xlsx",

        ".xls"

    ]:

        excel_file = pd.ExcelFile(
            uploaded_file
        )

        text = ""

        for sheet_name in excel_file.sheet_names:

            dataframe = pd.read_excel(

                excel_file,

                sheet_name=sheet_name

            )

            text += (

                f"\n\n===== SHEET: "

                f"{sheet_name}"

                f" =====\n\n"

            )

            text += dataframe.to_string(
                index=False
            )

        return text


    # =====================================================
    # JSON
    # =====================================================

    elif file_extension == ".json":

        return uploaded_file.getvalue().decode(

            "utf-8",

            errors="ignore"

        )


    # =====================================================
    # XML
    # =====================================================

    elif file_extension == ".xml":

        return uploaded_file.getvalue().decode(

            "utf-8",

            errors="ignore"

        )


    # =====================================================
    # RTF
    # =====================================================

    elif file_extension == ".rtf":

        return uploaded_file.getvalue().decode(

            "utf-8",

            errors="ignore"

        )


    return ""