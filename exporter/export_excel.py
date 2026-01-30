# -*- coding: utf-8 -*-
"""
Excel to HTML Exporter
Converts Excel file to HTML while preserving layout, merged cells, and structure.
"""
import os
import re
import zipfile
from io import BytesIO
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from jinja2 import Environment, FileSystemLoader
import xml.etree.ElementTree as ET


@dataclass
class CellData:
    """Represents a single cell in the Excel sheet."""
    value: str = ""
    row: int = 0
    col: int = 0
    rowspan: int = 1
    colspan: int = 1
    is_merged: bool = False
    is_merged_hidden: bool = False
    width: float = 64.0
    height: float = 20.0
    font_bold: bool = False
    font_size: float = 11.0
    align: str = "left"
    valign: str = "top"
    border_top: bool = False
    border_bottom: bool = False
    border_left: bool = False
    border_right: bool = False
    bg_color: str = ""


@dataclass
class SheetData:
    """Represents a single Excel sheet."""
    name: str
    cells: List[List[CellData]] = field(default_factory=list)
    col_widths: List[float] = field(default_factory=list)
    row_heights: List[float] = field(default_factory=list)
    max_row: int = 0
    max_col: int = 0


class ExcelToHtmlConverter:
    """Converts Excel file to HTML preserving layout."""

    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.sheets: List[SheetData] = []
        self.shared_strings: List[str] = []
        self.styles: Dict[int, Dict[str, Any]] = {}

    def _fix_xlsx_xml(self, xml_content: bytes) -> bytes:
        """Fix problematic empty attributes in Excel XML."""
        content = xml_content.decode('utf-8')
        # Fix empty float values
        content = re.sub(r'left=""', 'left="0.7"', content)
        content = re.sub(r'right=""', 'right="0.7"', content)
        content = re.sub(r'top=""', 'top="0.75"', content)
        content = re.sub(r'bottom=""', 'bottom="0.75"', content)
        content = re.sub(r'header=""', 'header="0.3"', content)
        content = re.sub(r'footer=""', 'footer="0.3"', content)
        content = re.sub(r'paperSize=""', 'paperSize="9"', content)
        content = re.sub(r'scale=""', 'scale="100"', content)
        content = re.sub(r'orientation=""', 'orientation="portrait"', content)
        return content.encode('utf-8')

    def _load_shared_strings(self, zf: zipfile.ZipFile) -> List[str]:
        """Load shared strings from xlsx."""
        strings = []
        try:
            with zf.open('xl/sharedStrings.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for si in root.findall('.//main:si', ns):
                    text_parts = []
                    for t in si.findall('.//main:t', ns):
                        if t.text:
                            text_parts.append(t.text)
                    strings.append(''.join(text_parts))
        except KeyError:
            pass
        return strings

    def _col_letter_to_index(self, col: str) -> int:
        """Convert column letter to index (A=0, B=1, etc)."""
        result = 0
        for char in col:
            result = result * 26 + (ord(char.upper()) - ord('A') + 1)
        return result - 1

    def _parse_cell_ref(self, ref: str) -> Tuple[int, int]:
        """Parse cell reference like 'A1' to (row, col)."""
        match = re.match(r'([A-Z]+)(\d+)', ref)
        if match:
            col = self._col_letter_to_index(match.group(1))
            row = int(match.group(2)) - 1
            return row, col
        return 0, 0

    def _load_sheet(self, zf: zipfile.ZipFile, sheet_path: str, sheet_name: str) -> SheetData:
        """Load a single sheet from xlsx."""
        sheet = SheetData(name=sheet_name)
        ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

        # Read and fix XML
        with zf.open(sheet_path) as f:
            xml_content = self._fix_xlsx_xml(f.read())
            tree = ET.parse(BytesIO(xml_content))
            root = tree.getroot()

        # Get dimensions
        dimension = root.find('.//main:dimension', ns)
        if dimension is not None:
            dim_ref = dimension.get('ref', 'A1:A1')
            if ':' in dim_ref:
                end_ref = dim_ref.split(':')[1]
                sheet.max_row, sheet.max_col = self._parse_cell_ref(end_ref)
                sheet.max_row += 1
                sheet.max_col += 1

        # Get column widths
        cols = root.findall('.//main:col', ns)
        col_widths = {}
        for col in cols:
            min_col = int(col.get('min', 1)) - 1
            max_col = int(col.get('max', 1)) - 1
            width = float(col.get('width', 8.43)) * 7  # Approximate pixel width
            for c in range(min_col, max_col + 1):
                col_widths[c] = width

        # Get row heights
        rows = root.findall('.//main:row', ns)
        row_heights = {}
        for row in rows:
            row_num = int(row.get('r', 1)) - 1
            height = float(row.get('ht', 15))
            row_heights[row_num] = height

        # Get merged cells
        merged_cells = {}
        merge_cells = root.findall('.//main:mergeCell', ns)
        for merge in merge_cells:
            ref = merge.get('ref', '')
            if ':' in ref:
                start, end = ref.split(':')
                start_row, start_col = self._parse_cell_ref(start)
                end_row, end_col = self._parse_cell_ref(end)
                rowspan = end_row - start_row + 1
                colspan = end_col - start_col + 1
                merged_cells[(start_row, start_col)] = (rowspan, colspan)
                # Mark hidden cells
                for r in range(start_row, end_row + 1):
                    for c in range(start_col, end_col + 1):
                        if r != start_row or c != start_col:
                            merged_cells[(r, c)] = (0, 0)  # Hidden

        # Initialize cells grid
        max_row = max(sheet.max_row, max(row_heights.keys(), default=0) + 1, 60)
        max_col = max(sheet.max_col, max(col_widths.keys(), default=0) + 1, 20)

        sheet.col_widths = [col_widths.get(c, 64) for c in range(max_col)]
        sheet.row_heights = [row_heights.get(r, 20) for r in range(max_row)]

        # Create empty grid
        sheet.cells = []
        for r in range(max_row):
            row_cells = []
            for c in range(max_col):
                cell = CellData(row=r, col=c)
                cell.width = sheet.col_widths[c] if c < len(sheet.col_widths) else 64
                cell.height = sheet.row_heights[r] if r < len(sheet.row_heights) else 20

                # Check if merged
                if (r, c) in merged_cells:
                    rowspan, colspan = merged_cells[(r, c)]
                    if rowspan == 0 and colspan == 0:
                        cell.is_merged_hidden = True
                    else:
                        cell.is_merged = True
                        cell.rowspan = rowspan
                        cell.colspan = colspan

                row_cells.append(cell)
            sheet.cells.append(row_cells)

        # Fill in cell values
        for row in rows:
            row_num = int(row.get('r', 1)) - 1
            for c in row.findall('main:c', ns):
                ref = c.get('r', '')
                cell_row, cell_col = self._parse_cell_ref(ref)
                cell_type = c.get('t', '')

                v = c.find('main:v', ns)
                value = ""
                if v is not None and v.text:
                    if cell_type == 's':
                        idx = int(v.text)
                        if idx < len(self.shared_strings):
                            value = self.shared_strings[idx]
                    else:
                        value = v.text

                # Also check for inline string
                is_elem = c.find('main:is', ns)
                if is_elem is not None:
                    t_elem = is_elem.find('main:t', ns)
                    if t_elem is not None and t_elem.text:
                        value = t_elem.text

                if cell_row < len(sheet.cells) and cell_col < len(sheet.cells[cell_row]):
                    sheet.cells[cell_row][cell_col].value = value

        # Trim empty rows/cols from the end
        sheet.max_row = max_row
        sheet.max_col = max_col

        return sheet

    def parse(self) -> List[SheetData]:
        """Parse the Excel file and return sheet data."""
        with zipfile.ZipFile(self.excel_path, 'r') as zf:
            # Load shared strings first
            self.shared_strings = self._load_shared_strings(zf)

            # Get sheet names from workbook.xml
            with zf.open('xl/workbook.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                sheets_elem = root.findall('.//main:sheet', ns)
                sheet_names = [s.get('name', f'Sheet{i+1}') for i, s in enumerate(sheets_elem)]

            # Load each sheet
            for i, name in enumerate(sheet_names):
                sheet_path = f'xl/worksheets/sheet{i+1}.xml'
                try:
                    sheet = self._load_sheet(zf, sheet_path, name)
                    self.sheets.append(sheet)
                except KeyError:
                    continue

        return self.sheets

    def to_html(self, output_path: str, template_path: Optional[str] = None) -> str:
        """Convert parsed Excel to HTML."""
        if not self.sheets:
            self.parse()

        # Use Jinja2 template
        if template_path and os.path.exists(template_path):
            template_dir = os.path.dirname(template_path)
            template_name = os.path.basename(template_path)
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template(template_name)
        else:
            # Use embedded template
            template_str = self._get_default_template()
            env = Environment()
            template = env.from_string(template_str)

        html = template.render(sheets=self.sheets)

        # Write output
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return html

    def _get_default_template(self) -> str:
        """Return the default HTML template."""
        return '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skill Sheet</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
            font-size: 10px;
            line-height: 1.4;
            background: #f5f5f5;
            color: #333;
        }

        .page {
            width: 297mm;
            min-height: 210mm;
            margin: 10mm auto;
            background: white;
            padding: 10mm;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        @media print {
            body {
                background: white;
            }
            .page {
                width: 100%;
                margin: 0;
                padding: 5mm;
                box-shadow: none;
                page-break-after: always;
            }
        }

        .sheet-title {
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 10px;
            color: #1a1a1a;
        }

        .excel-table {
            border-collapse: collapse;
            width: 100%;
            table-layout: fixed;
            font-size: 9px;
        }

        .excel-table td {
            border: 1px solid #ccc;
            padding: 2px 4px;
            vertical-align: top;
            word-wrap: break-word;
            overflow: hidden;
            white-space: pre-wrap;
            background: white;
        }

        .excel-table td.header-cell {
            background: #f0f0f0;
            font-weight: 500;
        }

        .excel-table td.category-cell {
            background: #e8f4f8;
            font-weight: 500;
        }

        .excel-table td.highlight-cell {
            background: #fff3cd;
        }

        .excel-table tr:first-child td {
            border-top: 2px solid #666;
        }

        .level-marker {
            text-align: center;
            font-weight: bold;
        }

        .section-break {
            height: 5mm;
        }

        @page {
            size: A4 landscape;
            margin: 10mm;
        }
    </style>
</head>
<body>
{% for sheet in sheets %}
<div class="page">
    <table class="excel-table">
        {% for row in sheet.cells[:60] %}
        {% set has_content = row | selectattr('value') | list | length > 0 %}
        {% if has_content %}
        <tr style="height: {{ sheet.row_heights[loop.index0] if loop.index0 < sheet.row_heights|length else 20 }}px;">
            {% for cell in row[:20] %}
            {% if not cell.is_merged_hidden %}
            <td
                {% if cell.rowspan > 1 %}rowspan="{{ cell.rowspan }}"{% endif %}
                {% if cell.colspan > 1 %}colspan="{{ cell.colspan }}"{% endif %}
                style="width: {{ cell.width }}px; min-width: {{ cell.width }}px;"
                {% if cell.value and ('プログラミング' in cell.value or 'フレームワーク' in cell.value or 'クラウド' in cell.value or 'データベース' in cell.value or 'ドメイン' in cell.value) %}class="category-cell"{% endif %}
                {% if cell.value and ('序数' in cell.value or '業務内容' in cell.value or '役割' in cell.value or 'ランキング' in cell.value) %}class="header-cell"{% endif %}
            >{{ cell.value | replace('\n', '<br>') | safe }}</td>
            {% endif %}
            {% endfor %}
        </tr>
        {% endif %}
        {% endfor %}
    </table>
</div>
{% endfor %}
</body>
</html>'''


def main():
    """Main entry point."""
    import sys

    # Default paths
    excel_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "Skill_Sheet_Pham_The_Son_ja.xlsx"
    )
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    output_html = os.path.join(output_dir, "output.html")

    # Allow command line override
    if len(sys.argv) > 1:
        excel_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_html = sys.argv[2]

    print(f"Converting: {excel_path}")
    print(f"Output: {output_html}")

    converter = ExcelToHtmlConverter(excel_path)
    converter.parse()
    converter.to_html(output_html)

    print(f"HTML generated: {output_html}")


if __name__ == "__main__":
    main()
