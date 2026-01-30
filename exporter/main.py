# -*- coding: utf-8 -*-
"""
Main Exporter Script
Converts Excel skill sheet to HTML and PDF.

Usage:
    python main.py                          # Use default paths
    python main.py path/to/excel.xlsx       # Specify Excel file
    python main.py excel.xlsx --pdf-only    # Generate PDF only (requires HTML)
    python main.py excel.xlsx --html-only   # Generate HTML only
"""
import os
import sys
import argparse

from export_excel import ExcelToHtmlConverter
from export_pdf import HtmlToPdfConverter


def main():
    parser = argparse.ArgumentParser(
        description='Convert Excel skill sheet to HTML and PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py
  python main.py ../Skill_Sheet_Pham_The_Son_ja.xlsx
  python main.py skillsheet.xlsx --html-only
  python main.py skillsheet.xlsx --pdf-method playwright
        '''
    )

    parser.add_argument(
        'excel_file',
        nargs='?',
        default=None,
        help='Path to Excel file (default: ../Skill_Sheet_Pham_The_Son_ja.xlsx)'
    )

    parser.add_argument(
        '--output-dir',
        default=None,
        help='Output directory (default: ../output)'
    )

    parser.add_argument(
        '--html-only',
        action='store_true',
        help='Generate HTML only, skip PDF'
    )

    parser.add_argument(
        '--pdf-only',
        action='store_true',
        help='Generate PDF only (requires existing HTML)'
    )

    parser.add_argument(
        '--pdf-method',
        choices=['weasyprint', 'wkhtmltopdf', 'playwright', 'auto'],
        default='auto',
        help='PDF generation method (default: auto)'
    )

    parser.add_argument(
        '--template',
        default=None,
        help='Custom HTML template path'
    )

    args = parser.parse_args()

    # Determine paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    excel_path = args.excel_file or os.path.join(base_dir, "Skill_Sheet_Pham_The_Son_ja.xlsx")
    output_dir = args.output_dir or os.path.join(base_dir, "output")
    html_path = os.path.join(output_dir, "output.html")
    pdf_path = os.path.join(output_dir, "output.pdf")
    template_path = args.template or os.path.join(os.path.dirname(__file__), "templates", "excel_to_html.html")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("Excel to HTML/PDF Exporter")
    print("=" * 60)
    print(f"Excel file: {excel_path}")
    print(f"Output dir: {output_dir}")
    print()

    # Step 1: Generate HTML
    if not args.pdf_only:
        if not os.path.exists(excel_path):
            print(f"Error: Excel file not found: {excel_path}")
            sys.exit(1)

        print("[1/2] Converting Excel to HTML...")
        converter = ExcelToHtmlConverter(excel_path)
        sheets = converter.parse()
        print(f"     Parsed {len(sheets)} sheet(s)")

        if os.path.exists(template_path):
            print(f"     Using template: {template_path}")
            converter.to_html(html_path, template_path)
        else:
            print("     Using embedded template")
            converter.to_html(html_path)

        print(f"     HTML saved: {html_path}")
        print()

    # Step 2: Generate PDF
    if not args.html_only:
        if not os.path.exists(html_path):
            print(f"Error: HTML file not found: {html_path}")
            print("Run without --pdf-only first to generate HTML.")
            sys.exit(1)

        print("[2/2] Converting HTML to PDF...")
        pdf_converter = HtmlToPdfConverter(html_path, pdf_path)

        method = None if args.pdf_method == 'auto' else args.pdf_method
        success = pdf_converter.convert(method)

        if not success:
            print()
            print("PDF generation failed. HTML preview is still available.")
            print(f"Open in browser: {html_path}")
            sys.exit(1)

        print()

    print("=" * 60)
    print("Export Complete!")
    print("=" * 60)

    if not args.pdf_only:
        print(f"HTML Preview: {html_path}")
    if not args.html_only and os.path.exists(pdf_path):
        print(f"PDF Document: {pdf_path}")

    print()
    print("Open HTML in browser for preview, or use PDF for printing.")


if __name__ == "__main__":
    main()
