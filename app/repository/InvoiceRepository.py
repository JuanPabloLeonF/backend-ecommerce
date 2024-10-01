from flask import make_response
import json
import jinja2

class InvoiceRepository:

    @classmethod
    def createHtml(cls, dataRequest):
        data = json.loads(dataRequest)
        htmlGenerated = cls.createDataHtml(
            urlTemplate=r"C:/Users/USUARIO/Desktop/ecommerce-backend/app/templates/invoice.html",
            data=data
        )

        response = make_response(htmlGenerated)
        response.headers['Content-Type'] = 'text/html'
        response.headers['Content-Disposition'] = 'inline; filename=invoice.html'
        return response

    @staticmethod
    def createDataHtml(urlTemplate: str, data: dict) -> str:
        nameTemplate = urlTemplate.split("/")[-1]
        pathTemplate = urlTemplate.replace(nameTemplate, "")

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(pathTemplate))
        template = env.get_template(nameTemplate)

        html = template.render(data)
        return html
