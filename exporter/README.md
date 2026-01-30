# Excel to HTML/PDF Exporter

情報処理技術者経歴書 (IT Engineer Skill Sheet) を Excel から HTML/PDF に変換するツール。

## Features

- Excel ファイルのレイアウトを保持したまま HTML に変換
- 結合セル対応
- 列幅・行高さの維持
- 日本語フォント対応 (Noto Sans JP)
- A4 横向き印刷対応
- 複数の PDF 生成方法をサポート

## Directory Structure

```
exporter/
├── export_excel.py          # Excel → HTML 変換
├── export_pdf.py            # HTML → PDF 変換
├── main.py                  # メインスクリプト
├── templates/
│   └── excel_to_html.html   # Jinja2 HTML テンプレート
└── README.md

output/
├── output.html              # 生成された HTML
└── output.pdf               # 生成された PDF
```

## Installation

### Required Dependencies

```bash
pip install jinja2 openpyxl
```

### PDF Generation (choose one)

#### Option 1: WeasyPrint (Recommended for Linux/macOS)
```bash
pip install weasyprint
```
> **Note:** Windows requires GTK libraries. See: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows

#### Option 2: wkhtmltopdf (Cross-platform)
Download from: https://wkhtmltopdf.org/downloads.html

```bash
# Windows: Add to PATH after installation
# macOS:
brew install wkhtmltopdf
# Ubuntu:
sudo apt install wkhtmltopdf
```

#### Option 3: Playwright (Cross-platform, uses Chrome)
```bash
pip install playwright
playwright install chromium
```

## Usage

### Basic Usage

```bash
cd exporter
python main.py
```

This will:
1. Read `../Skill_Sheet_Pham_The_Son_ja.xlsx`
2. Generate `../output/output.html`
3. Generate `../output/output.pdf`

### Custom Excel File

```bash
python main.py path/to/your/skillsheet.xlsx
```

### HTML Preview Only

```bash
python main.py --html-only
```

### Specify PDF Method

```bash
python main.py --pdf-method playwright
python main.py --pdf-method wkhtmltopdf
python main.py --pdf-method weasyprint
```

### Custom Output Directory

```bash
python main.py --output-dir ./my-output
```

### All Options

```bash
python main.py --help
```

## API Usage

```python
from exporter import ExcelToHtmlConverter, HtmlToPdfConverter

# Excel to HTML
converter = ExcelToHtmlConverter("skillsheet.xlsx")
sheets = converter.parse()
converter.to_html("output.html")

# HTML to PDF
pdf_converter = HtmlToPdfConverter("output.html", "output.pdf")
pdf_converter.convert()
```

## Customizing the Template

Edit `templates/excel_to_html.html` to customize:

- Page size (`@page { size: A4 landscape; }`)
- Fonts (`font-family`)
- Colors (`--header-bg`, `--category-bg`, etc.)
- Cell padding and borders
- Section styling

## Layout Limitations vs Excel

| Feature | Support |
|---------|---------|
| Cell values | ✅ Full |
| Merged cells | ✅ Full |
| Column widths | ⚠️ Approximate |
| Row heights | ⚠️ Approximate |
| Cell borders | ✅ Uniform style |
| Font styles | ⚠️ Limited |
| Cell colors | ⚠️ Not preserved |
| Formulas | ✅ Values only |
| Images | ❌ Not supported |
| Charts | ❌ Not supported |
| Comments | ❌ Not supported |

## Troubleshooting

### "WeasyPrint requires GTK libraries"

On Windows, either:
1. Install GTK3: https://github.com/nicman23/gtk3-installer-msvc
2. Use wkhtmltopdf or Playwright instead

### Japanese text not displaying correctly

Ensure you have Japanese fonts installed:
- Windows: MS Gothic, Meiryo (usually pre-installed)
- macOS: Hiragino (pre-installed)
- Linux: `sudo apt install fonts-noto-cjk`

### PDF is blank

Check that HTML was generated correctly:
```bash
# Generate HTML only first
python main.py --html-only

# Open output/output.html in browser to verify
```

## License

MIT
