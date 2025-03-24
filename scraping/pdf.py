import fitz  # PyMuPDF
import requests
import app_base.write_log as wr
from io import BytesIO
import gc, sys


sys.stdout.reconfigure(encoding="utf-8")
def limpiar_texto(texto):
    return texto #''.join(c for c in unicodedata.normalize('NFKD', texto) if ord(c) < 128)
def sraper_pdf(url):

    #url = "https://www.rae.es/sites/default/files/Discurso_Ingreso_Pedro_Alvarez.pdf"
    response = requests.get(url)
    if response.status_code == 200:
        pdf_file = BytesIO(response.content)
        # Abrir el PDF con PyMuPDF
        doc = fitz.open(stream=pdf_file, filetype="pdf")
        # Extraer texto de cada página
        page_num = 1
        for page_num, page in enumerate(doc, start=1):
            texto = page.get_text("text")
            texto_limpio = limpiar_texto(texto)
            texto += texto_limpio
            page_num += 1
            print(f"Página {page_num}:\n{texto_limpio}\n{'-'*40}")
        
        return texto
         

