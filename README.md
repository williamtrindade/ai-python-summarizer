# AI Python Summarizer

Este projeto é um poderoso resumidor de documentos PDF que utiliza a API do Google Gemini para criar resumos detalhados e aprofundados. Ele é capaz de processar livros inteiros ou grandes documentos, gerando um novo PDF formatado com o conteúdo sumarizado.

## Funcionalidades

- **Processamento em Lote:** Processa automaticamente todos os arquivos PDF localizados na pasta `res`.
- **Resumos Detalhados:** Utiliza uma estratégia de MapReduce, dividindo o texto em partes e resumindo cada uma individualmente para garantir um resultado extenso e de alta qualidade.
- **Formatação Avançada:** Gera um PDF de saída com formatação limpa, incluindo títulos centralizados, parágrafos e listas.
- **Modelo de IA Rápido e Eficiente:** Utiliza o modelo `gemini-flash-latest` para um bom equilíbrio entre velocidade e qualidade do resumo.

## Pré-requisitos

- Python 3.x

## Instalação

1. Clone este repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd ai-python-summarizer
   ```

2. Instale as dependências a partir do `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Crie um arquivo de ambiente a partir do exemplo. Este arquivo guardará sua chave de API de forma segura.
   ```bash
   cp env.example .env
   ```

4. Abra o arquivo `.env` com um editor de texto e adicione sua chave da API do Google:
   ```
   GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
   ```

## Como Usar

1. **Adicione seus PDFs:** Coloque os arquivos PDF que você deseja resumir na pasta `res`. Se a pasta não existir, o script a criará para você.

2. **Execute o Script:** Abra seu terminal e execute o seguinte comando:
   ```bash
   python3 summarizer.py
   ```

3. **Verifique os Resultados:** O script processará cada PDF, exibindo o progresso no terminal. Os resumos finalizados, em formato PDF, serão salvos na pasta `output`.

## Como Funciona

O script segue os seguintes passos para cada arquivo encontrado:
1. **Extração de Texto:** O texto completo do PDF é extraído usando a biblioteca `PyPDF2`.
2. **Divisão (Chunking):** O texto extraído é dividido em segmentos menores e sobrepostos para garantir que o contexto não seja perdido.
3. **Resumo por Partes (Map):** Cada segmento de texto é enviado individualmente para a API do Gemini Pro com um prompt para gerar um resumo detalhado daquela parte específica.
4. **Combinação (Reduce):** Todos os resumos parciais são concatenados para formar um único documento de texto em HTML.
5. **Geração do PDF:** O HTML final é processado pela biblioteca `ReportLab` para criar um arquivo PDF bem formatado, com títulos centralizados e estrutura de parágrafos preservada.

## Tecnologias Utilizadas

- [Google Generative AI](https://ai.google.dev/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [ReportLab](https://www.reportlab.com/)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)
