# PDF Study Assistant 📚

Aplicação educacional que transforma documentos PDF
em guias de estudo utilizando Inteligência Artificial.

## Funcionalidades
- Upload de PDFs
- Extração de texto com PyMuPDF
- Identificação e explicação de tópicos com Gemini
- Respostas estruturadas com Pydantic
- Validação básica de referências de páginas
- Interface desenvolvida com Streamlit

## Tecnologias
Python, Streamlit, Google Gemini, PyMuPDF e Pydantic.

## Como executar

1. Crie e ative um ambiente virtual.
2. Instale as dependências:
   pip install -r requirements.txt
3. Configure GEMINI_API_KEY no arquivo .env.
4. Execute:
   streamlit run app.py

## Limitações
- Não suporta PDFs digitalizados sem texto selecionável.
- As referências de páginas não são verificadas semanticamente.
- O uso da API Gemini pode estar sujeito a limites.