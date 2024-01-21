from django.template.loader import render_to_string
from weasyprint import HTML


def convert_to_pdf(context):

    rendered = render_to_string("report/caratula.html", context)

    HTML(string=rendered).write_pdf(target='caratula.pdf', )
