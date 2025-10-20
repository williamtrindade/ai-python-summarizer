import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph
import google.generativeai as genai
import time

def summarize_pdfs_from_folder(folder_path, output_folder):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            try:
                print(f"Iniciando o processamento de: {filename}...")
                # Extract text from PDF
                reader = PdfReader(pdf_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()

                if not text.strip():
                    print(f"AVISO: Nenhum texto extraído de {filename}. Pulando.")
                    continue

                # Summarize the text
                summary = summarize_text(text)

                # Save summary to PDF
                output_pdf_path = os.path.join(output_folder, f"summary_{filename}")
                save_summary_to_pdf(summary, output_pdf_path)

                print(f"Resumo de {filename} salvo com sucesso em {output_pdf_path}")

            except Exception as e:
                print(f"ERRO ao processar {filename}: {e}")

def summarize_text(text):
    # Configure the generative AI model for its large context window
    model = genai.GenerativeModel('models/gemini-flash-latest')

    print("Enviando o texto completo para o resumo com o modelo Flash...")
    
    # Generate the summary in a single request
    try:
        # Add a more detailed prompt for better results
        prompt = f"""Por favor, elabore um resumo **extremamente detalhado e aprofundado** do seguinte texto, com o objetivo de criar um documento de várias páginas. Faça um fichamento completo, explorando cada seção ou capítulo do texto original.

**Instruções de Conteúdo:**
- Identifique e detalhe os conceitos centrais, os argumentos principais e as conclusões de cada parte do texto.
- Use múltiplos parágrafos para explicar ideias complexas.
- Crie várias seções distintas para organizar o conteúdo de forma lógica e clara.

**Instruções de Formatação OBRIGATÓRIAS:**
- Use **exclusivamente** tags HTML simples.
- Use `<h2>` para os títulos de cada seção.
- Use `<p>` para parágrafos.
- Use `<ul>` e `<li>` para listas.
- Use `<b>` para texto em negrito.
- **É PROIBIDO usar qualquer sintaxe Markdown.**

Texto a ser resumido:
{text}
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao gerar o resumo: {e}")
        return "[Erro ao gerar o resumo]"

def save_summary_to_pdf(summary, pdf_path):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create a new style for centered H2 titles
    h2_style = ParagraphStyle(
        name='H2',
        parent=styles['h2'],
        alignment=TA_CENTER,
        fontSize=14,
        leading=18
    )

    story = []
    paragraphs = summary.split('\n')
    for para_text in paragraphs:
        if para_text.strip():
            # Check if the paragraph is a title
            if para_text.startswith('<h2>') and para_text.endswith('</h2>'):
                # Remove the h2 tags and apply the centered style
                title_text = para_text.replace('<h2>', '').replace('</h2>', '')
                p = Paragraph(title_text, h2_style)
            else:
                # Apply the normal style for other paragraphs
                p = Paragraph(para_text, styles['Normal'])
            story.append(p)
    doc.build(story)

from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Por favor, defina a variável de ambiente GOOGLE_API_KEY.")
    else:
        genai.configure(api_key=api_key)
        
        res_folder = "res"
        output_folder = "output"

        if not os.path.exists(res_folder):
            os.makedirs(res_folder)
            print(f"Pasta '{res_folder}' criada. Por favor, adicione seus livros em PDF aqui.")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        summarize_pdfs_from_folder(res_folder, output_folder)