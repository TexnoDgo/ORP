from fpdf import FPDF, HTMLMixin


class HTML2PDF(FPDF, HTMLMixin):
    pass


def html2pdf():
    html = '''
    <div>

    </div>
    '''
    pdf = HTML2PDF()
    pdf.add_page()
    pdf.write_html(html)
    pdf.output('html2pdf.pdf')


if __name__ == '__main__':
    html2pdf()
