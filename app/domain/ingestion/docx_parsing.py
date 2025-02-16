# app/utils/docx_parsing.py

import re
from typing import List, Tuple, Any

# from docx.document import Document as DocxDocument
from docx import Document as DocxDocument


def read_docx(file_path: str) -> Tuple[str, str, List[str]]:
    """
    Đọc file .docx và trích xuất văn bản và bảng, kết hợp chúng thành một chuỗi Markdown
    theo đúng thứ tự xuất hiện trong file.

    Args:
        file_path (str): Đường dẫn đến file .docx.

    Returns:
        Tuple[str, str, str]: Markdown content, text content, table content
    """
    doc: DocxDocument = DocxDocument(file_path)
    markdown_content = ""
    paragraph_index = 0
    table_index = 0
    text_content = ""
    table_content: List[str] = []

    for element in doc.element.body:
        if element.tag.endswith('p'):
            if paragraph_index < len(doc.paragraphs):
                paragraph = doc.paragraphs[paragraph_index]
                text = paragraph.text.strip()
                if text:
                    is_bold = any(run.bold for run in paragraph.runs)

                    # Header 1: In đậm + CHỮ HOA
                    if is_bold and text.isupper():
                        markdown_content += f"# {text}\n\n"
                        text_content += "f{text}\n\n"

                    # Header 2: In đậm + Bắt đầu bằng số Latin
                    elif is_bold and re.match(r"^\d+\.", text):
                        markdown_content += f"## {text}\n\n"
                        text_content += "f{text}\n\n"

                    # Văn bản thường
                    else:
                        markdown_content += f"{text}\n\n"
                        text_content += "f{text}\n\n"

                paragraph_index += 1

        elif element.tag.endswith('tbl'):
            if table_index < len(doc.tables):
                table = doc.tables[table_index]
                table_data = []
                for row in table.rows:
                    row_data = [cell.text.strip().replace("\n", " ") for cell in row.cells]
                    table_data.append(row_data)

                markdown_table = "| " + " | ".join(table_data[0]) + " |\n"
                markdown_table += "| " + " | ".join(["---"] * len(table_data[0])) + " |\n"
                for row in table_data[1:]:
                    markdown_table += "| " + " | ".join(row) + " |\n"

                markdown_content += markdown_table + "\n"
                table_index += 1
                table_content.append(markdown_table)

    return markdown_content, text_content, table_content


def detect_markdown_tables(md_text):
    # Regex tìm bảng Markdown
    table_pattern = re.compile(r"(?:\|.*?\|\n)+\|[-:| ]+\|\n(?:\|.*?\|\n)+"
                               r"|(?:\S+\s*\|\s*\S+.*\n)(?:[-:]+[\| ]+[-:]+\n)(?:\S+\s*\|\s*\S+.*\n)+")

    tables = table_pattern.findall(md_text)
    return tables


if __name__ == '__main__':
    mardown_content, text_content, table_content = read_docx(
        file_path=r"C:\Users\Vitus\Downloads\Telegram Desktop\QD342 De an tuyen sinh dai hoc 2024 (web)A.docx")

    # with open("table.md", "w", encoding="utf-8") as file:
    #     for table in hola:
    #         file.write(table)

    # Phát hiện bảng
    tables = detect_markdown_tables(table_content)

    res: List[Any] = []
    # In kết quả

    for chunk in table_chunking(table_content):
        res.append(LangchainDocument(page_content=chunk, metadata={"heading": "table"}))

    for chunk in title_chunking(mardown_content):
        res.append(chunk)

    print(res)
