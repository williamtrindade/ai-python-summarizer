import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
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
                summary = summarize_text_map_reduce(text)

                # Save summary to PDF
                output_pdf_path = os.path.join(output_folder, f"summary_{filename}")
                save_summary_to_pdf(summary, output_pdf_path)

                print(f"Resumo de {filename} salvo com sucesso em {output_pdf_path}")

            except Exception as e:
                print(f"ERRO ao processar {filename}: {e}")

def summarize_text_map_reduce(text):
    # Configure the generative AI model
    model = genai.GenerativeModel('models/gemini-pro-latest')

    # 1. Map Step: Summarize smaller chunks of the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
    chunks = text_splitter.split_text(text)
    
    chunk_summaries = []
    print(f"Dividindo o texto em {len(chunks)} partes para a primeira fase de resumo...")
    
    for i, chunk in enumerate(chunks):
        try:
            print(f"Resumindo parte {i+1}/{len(chunks)}...")
            response = model.generate_content(f"Resuma o seguinte texto:\n\n{chunk}")
            chunk_summaries.append(response.text)
            time.sleep(1) # Add a small delay to avoid hitting API rate limits
        except Exception as e:
            print(f"Erro ao resumir a parte {i+1}: {e}")
            # Optionally, add a placeholder or skip this chunk
            chunk_summaries.append("[Erro no resumo desta parte]")

    # 2. Reduce Step: Combine the summaries and create a final summary
    combined_summary = "\n".join(chunk_summaries)
    
    print("Criando o resumo final a partir das partes resumidas...")
    final_summary_prompt = f"Crie um resumo final e coeso a partir dos seguintes resumos parciais:\n\n{combined_summary}"
    
    final_response = model.generate_content(final_summary_prompt)
    
    return final_response.text

def save_summary_to_pdf(summary, pdf_path):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    # Replace newlines with <br/> tags for proper rendering in PDF
    formatted_summary = summary.replace('\n', '<br/>')
    story = [Paragraph(formatted_summary, styles['Normal'])]
    doc.build(story)

if __name__ == "__main__":
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