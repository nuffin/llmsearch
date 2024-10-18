"""
Document file types support
"""

from . import docx
from . import pdf
from . import pptx
from . import xlsx
from . import csv
from . import text
from . import image
from . import video

from .mimetype import detect

parsers = {
    "application/pdf": pdf.PdfFileParser,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": docx.DocxFileParser,
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": pptx.PptxFileParser,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": xlsx.XlsxFileParser,
    "text/csv": csv.CsvFileParser,
    "text/plain": text.TextFileParser,
    "image/gif": image.ImageFileParser,
    "image/jpeg": image.ImageFileParser,
    "image/png": image.ImageFileParser,
    "image/svg+xml": image.ImageFileParser,
    "video/mp4": video.VideoFileParser,
    "video/quicktime": video.VideoFileParser,
    "video/x-msvideo": video.VideoFileParser,
}


def tokenize(filepath: str):
    mimetype = detect(filepath)
    if mimetype in parsers:
        parser = parsers[mimetype](filepath)
        parser.tokenize()
    else:
        print(f"Unsupported file type: {mimetype}")
