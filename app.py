"""Interface Streamlit do PDF Study Assistant."""
import hashlib

import pymupdf
import streamlit as st

from pdf_study import analisar_documento, extrair_texto_pdf, validar_topicos

st.set_page_config(page_title="PDF Study Assistant", page_icon="📚", layout="centered")
st.title("📚 PDF Study Assistant")
st.write("Envie um PDF com texto selecionável e receba um guia de estudos para iniciantes.")

arquivo = st.file_uploader("Selecione um arquivo PDF", type=["pdf"])

if arquivo is not None:
    conteudo_pdf = arquivo.getvalue()
    id_arquivo = hashlib.sha256(conteudo_pdf).hexdigest()
    st.caption(f"Arquivo: {arquivo.name}")
    if st.button("Gerar guia de estudos", type="primary"):
        try:
            with st.spinner("Lendo o PDF..."):
                document, total_paginas = extrair_texto_pdf(conteudo_pdf)
                if not document:
                    st.error("Este PDF não possui texto extraível. PDFs digitalizados ainda não são suportados.")
                    st.stop()
                if sum(len(p["texto"]) for p in document) > 300_000:
                    st.error("PDF muito extenso para esta versão. Use um PDF com até 300 mil caracteres extraídos.")
                    st.stop()

            with st.spinner("Gerando o guia com Gemini..."):
                resultado = analisar_documento(document)
                topicos = validar_topicos(resultado, document, total_paginas)

            st.session_state["resultado_pdf"] = {
                "id_arquivo": id_arquivo,
                "total_paginas": total_paginas,
                "topicos": topicos,
            }
        except (ValueError, RuntimeError, pymupdf.FileDataError) as erro:
            st.error(f"Não foi possível processar o PDF: {erro}")

    resultado_pdf = st.session_state.get("resultado_pdf")
    if resultado_pdf and resultado_pdf["id_arquivo"] == id_arquivo:
        st.success("Guia de estudos gerado!")
        st.caption(f"{resultado_pdf['total_paginas']} páginas no PDF")
        for numero, topico in enumerate(resultado_pdf["topicos"], start=1):
            st.subheader(f"{numero}. {topico['nome']}")
            st.write(topico["explicacao"])
            st.markdown(f"**Por que estudar?** {topico['importancia']}")
            st.caption(f"Página física: {topico['pagina']}")
            if topico["status"] == "pagina_invalida":
                st.warning("Referência inválida: página fora do PDF.")
            elif topico["status"] == "sem_texto":
                st.warning("Página existe, mas não possui texto extraído.")
            else:
                st.caption("Página existente e com texto; conteúdo não verificado semanticamente.")
            st.divider()

st.caption("MVP: PDFs com texto selecionável. As explicações e referências da IA devem ser conferidas.")
