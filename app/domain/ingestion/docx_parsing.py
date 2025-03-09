# app/utils/docx_parsing.py
"""
This module contains functions for parsing files.
"""
import io
from typing import List

import pandas as pd
from fastapi import UploadFile, File
from langchain_core.documents.base import Document as LangchainDocument

from api.logging_theme import setup_logger


class DocxParser:
    """
    Define Docx Parser
    """

    def __init__(self):
        self.results: List[LangchainDocument] = []
        self.logger = setup_logger(__name__)

    async def faq_parsing(self, upload_file: UploadFile = File(...), question_column_name: str = "CÂU HỎI",
                          answer_column_name: str = "CÂU TRẢ LỜI ", header: int = 1) -> List[LangchainDocument]:
        """
        Reads a CSV file containing FAQ data and returns a list of LangchainDocument objects.

        Args:
            upload_file (UploadFile): The list of uploaded CSV files containing FAQ data.
            question_column_name (str): The column name for questions in the CSV file.
            answer_column_name (str): The column name for answers in the CSV file.

        Returns:
            List[LangchainDocument]: A list of LangchainDocument objects with page content set to the question
                                     and metadata containing the answer.
        """
        try:
            content = await upload_file.read()
            faq = pd.read_csv(io.BytesIO(content), header=header)
            self.logger.debug(faq)
            for item in faq.to_dict(orient="records"):
                self.results.append(LangchainDocument(page_content=item[question_column_name],
                                                      metadata={"answer": item[answer_column_name]}))
            self.logger.info(f"Successfully parsed {len(self.results)} FAQ data")
            return self.results
        except Exception as e:
            self.logger.error(f"Error parsing FAQ data: {str(e)}")
            raise ValueError(f"Error parsing FAQ data: {str(e)}")
