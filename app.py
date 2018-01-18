import io

from wand.image import Image, Color
from PyPDF2 import PdfFileReader, PdfFileWriter

mem = {}


def get_pdf_data(filename):
    reader = mem.get(filename, None)
    if reader is None:
        reader = PdfFileReader(filename, strict=True)
        mem[filename] = reader
    return reader


def convert(filename, res=120):
    pdfile = get_pdf_data(filename)
    pages = pdfile.getNumPages()
    for page in range(pages):
        pobj = pdfile.getPage(page)
        dst_pdf = PdfFileWriter()
        dst_pdf.addPage(pobj)

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)

        img = Image(file=pdf_bytes, resolution=res)
        img.format = 'png'
        img.compression_quality = 60
        img.background_color = Color('white')
        img_path = "%s-%d.png" % (filename[:filename.rindex('.')], page)
        img.save(filename=img_path)
        img.destroy()


if __name__ == "__main__":
    convert('demo.pdf')
