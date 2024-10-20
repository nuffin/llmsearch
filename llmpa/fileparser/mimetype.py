import os
import magic

mime = magic.Magic(mime=True)

mimetypes_names = {
    "text/plain": "Plain Text",
    "text/csv": "CSV (Comma Separated Values)",
    "text/html": "HTML",
    "text/xml": "XML",
    "text/x-c": "C Source Code",  # c, go  # XXX: Add file extension checking
    "text/x-c++": "C++ Source Code",  # cpp
    "text/x-java-source": "Java Source Code",  # java
    "text/x-go": "Go Source Code",  # FAKE: Not supported by python-magic, but checking file extension
    "text/x-ini": "INI Configuration",  # FAKE: Not detected by python-magic, but checking file extension
    "text/x-matlab": "MATLAB Source Code",  # matlab
    "text/x-perl": "Perl Source Code",  # perl
    "text/x-php": "PHP Source Code",  # php
    "text/x-python": "Python Source Code",  # python, /etc/mime.types
    "text/x-script.python": "Python Script",  # python, by magic
    "application/javascript": "JavaScript",  # js
    "application/json": "JSON",
    # "application/x-python-code": "Compiled Python Code",  # python, /etc/mime.types, pyc pyo
    "application/pdf": "PDF",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "PPTX Presentation",  # pptx
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "XLSX Spreadsheet",  # xlsx
    "audio/mpeg": "MPEG Audio",  # mp3
    "audio/x-wav": "WAVE Audio",  # wav
    "image/gif": "GIF Image",  # gif
    "image/jpeg": "JPEG Image",  # jpg
    "image/png": "PNG Image",  # png
    "image/svg+xml": "SVG Image",  # svg
    "video/mp4": "MP4 Video",  # mp4
    "video/quicktime": "QuickTime Video",  # mov
    "video/x-msvideo": "AVI Video",  # avi
    "font/woff": "Web Open Font Format",  # woff
}

supported_mimetypes = mimetypes_names.keys()


def _detect(filepath: str, follow_symlinks: bool = True) -> str:
    resolved_filepath = follow_symlinks and os.path.realpath(filepath) or filepath
    mimetype = mime.from_file(resolved_filepath) if os.path.isfile(filepath) else None
    if mimetype == "text/x-c" and filepath.endswith(".go"):
        return "text/x-go"
    if mimetype == "text/plain" and filepath.endswith(".ini"):
        return "text/x-ini"
    return mimetype


def detect(filepath: str, follow_symlinks: bool = True) -> str:
    mimetype = _detect(filepath, follow_symlinks)
    return mimetype if mimetype in supported_mimetypes else None


def main():
    import os
    import sys

    if len(sys.argv) < 2:
        print(f"Usage: {os.path.basename(__file__)} <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    meme_type_real = _detect(filepath)
    meme_type = detect(filepath)
    print(f"{filepath}: {meme_type_real}, {meme_type}")


if __name__ == "__main__":
    main()
