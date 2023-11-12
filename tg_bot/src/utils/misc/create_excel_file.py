import io

import openpyxl
from openpyxl.styles import Font


def create_bytes_excel_file(data: list, headers: list) -> bytes:
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    bold_font = Font(bold=True)

    for i, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=i)
        cell.value = header
        cell.font = bold_font

    # Add data rows
    for row_num, row_data in enumerate(data, 2):
        for col_num, cell_data in enumerate(row_data.values(), 1):
            sheet.cell(row=row_num, column=col_num).value = cell_data

    with io.BytesIO() as file_stream:
        workbook.save(file_stream)
        return file_stream.getvalue()
