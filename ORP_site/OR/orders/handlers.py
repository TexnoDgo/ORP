'''import ghostscript
import locale


def pdf2jpeg(pdf_input_path, jpeg_output_path):
    args = ["pef2jpeg",  # actual value doesn't matter
            "-dNOPAUSE",
            "-sDEVICE=jpeg",
            "-r144",
            "-sOutputFile=" + jpeg_output_path,
            pdf_input_path]

    encoding = locale.getpreferredencoding()
    args = [a.encode(encoding) for a in args]

    ghostscript.Ghostscript(*args)


pdf2jpeg(
    'Invoice3.pdf',
    'Invoice3.jpg'
)'''

import fitz

'''pdf_file = "111.PDF"
doc = fitz.open(pdf_file)
page = doc.loadPage(0) #number of page
pix = page.getPixmap()
output = "outfile.png"
pix.writePNG(output)'''


# Конвертор файлов
def convert_pdf_to_bnp(infile, outfile):
    doc = fitz.open(infile)
    page = doc.loadPage(0)
    pix = page.getPixmap()
    output = outfile
    pix.writePNG(output)

