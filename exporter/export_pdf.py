# -*- coding: utf-8 -*-
"""
HTML to PDF Exporter
Converts HTML file to PDF using WeasyPrint or wkhtmltopdf.
"""
import os
import sys
import subprocess
from typing import Optional


class HtmlToPdfConverter:
    """Converts HTML to PDF using available tools."""

    def __init__(self, html_path: str, pdf_path: str):
        self.html_path = html_path
        self.pdf_path = pdf_path

    def convert_with_weasyprint(self) -> bool:
        """Convert using WeasyPrint library."""
        try:
            from weasyprint import HTML, CSS
            from weasyprint.text.fonts import FontConfiguration

            print("Using WeasyPrint for PDF generation...")

            font_config = FontConfiguration()

            # Additional CSS for PDF
            pdf_css = CSS(string='''
                @page {
                    size: A4 landscape;
                    margin: 8mm;
                }
                body {
                    font-family: 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', sans-serif;
                }
            ''', font_config=font_config)

            html = HTML(filename=self.html_path)
            html.write_pdf(
                self.pdf_path,
                stylesheets=[pdf_css],
                font_config=font_config
            )

            print(f"PDF generated: {self.pdf_path}")
            return True

        except ImportError:
            print("WeasyPrint not available.")
            return False
        except OSError as e:
            if "libgobject" in str(e) or "cannot load library" in str(e):
                print("WeasyPrint requires GTK libraries (not available on Windows without setup).")
            else:
                print(f"WeasyPrint error: {e}")
            return False

    def convert_with_wkhtmltopdf(self) -> bool:
        """Convert using wkhtmltopdf command line tool."""
        try:
            # Check if wkhtmltopdf is available
            result = subprocess.run(
                ["wkhtmltopdf", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return False

            print("Using wkhtmltopdf for PDF generation...")

            # Run conversion
            cmd = [
                "wkhtmltopdf",
                "--page-size", "A4",
                "--orientation", "Landscape",
                "--margin-top", "8mm",
                "--margin-bottom", "8mm",
                "--margin-left", "10mm",
                "--margin-right", "10mm",
                "--encoding", "UTF-8",
                "--enable-local-file-access",
                self.html_path,
                self.pdf_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"PDF generated: {self.pdf_path}")
                return True
            else:
                print(f"wkhtmltopdf error: {result.stderr}")
                return False

        except FileNotFoundError:
            print("wkhtmltopdf not found in PATH.")
            return False

    def convert_with_playwright(self) -> bool:
        """Convert using Playwright (headless Chrome)."""
        try:
            from playwright.sync_api import sync_playwright

            print("Using Playwright (headless Chrome) for PDF generation...")

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()

                # Load HTML file
                file_url = f"file:///{os.path.abspath(self.html_path).replace(os.sep, '/')}"
                page.goto(file_url)

                # Wait for fonts to load
                page.wait_for_load_state("networkidle")

                # Generate PDF
                page.pdf(
                    path=self.pdf_path,
                    format="A4",
                    landscape=True,
                    margin={
                        "top": "8mm",
                        "bottom": "8mm",
                        "left": "10mm",
                        "right": "10mm"
                    },
                    print_background=True
                )

                browser.close()

            print(f"PDF generated: {self.pdf_path}")
            return True

        except ImportError:
            print("Playwright not available. Install with: pip install playwright && playwright install chromium")
            return False
        except Exception as e:
            print(f"Playwright error: {e}")
            return False

    def convert(self, method: Optional[str] = None) -> bool:
        """
        Convert HTML to PDF using available method.

        Args:
            method: Force specific method ('weasyprint', 'wkhtmltopdf', 'playwright')
                   If None, tries each method in order.
        """
        os.makedirs(os.path.dirname(self.pdf_path) if os.path.dirname(self.pdf_path) else '.', exist_ok=True)

        methods = {
            'weasyprint': self.convert_with_weasyprint,
            'wkhtmltopdf': self.convert_with_wkhtmltopdf,
            'playwright': self.convert_with_playwright,
        }

        if method:
            if method in methods:
                return methods[method]()
            else:
                print(f"Unknown method: {method}")
                return False

        # Try each method in order
        for name, func in methods.items():
            print(f"Trying {name}...")
            if func():
                return True

        print("No PDF generation method available.")
        print("Install one of:")
        print("  - WeasyPrint: pip install weasyprint (requires GTK on Windows)")
        print("  - wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
        print("  - Playwright: pip install playwright && playwright install chromium")
        return False


def main():
    """Main entry point."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, "output")

    html_path = os.path.join(output_dir, "output.html")
    pdf_path = os.path.join(output_dir, "output.pdf")
    method = None

    # Parse command line args
    if len(sys.argv) > 1:
        html_path = sys.argv[1]
    if len(sys.argv) > 2:
        pdf_path = sys.argv[2]
    if len(sys.argv) > 3:
        method = sys.argv[3]

    if not os.path.exists(html_path):
        print(f"HTML file not found: {html_path}")
        print("Run export_excel.py first to generate HTML.")
        sys.exit(1)

    print(f"Converting: {html_path}")
    print(f"Output: {pdf_path}")

    converter = HtmlToPdfConverter(html_path, pdf_path)
    success = converter.convert(method)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
