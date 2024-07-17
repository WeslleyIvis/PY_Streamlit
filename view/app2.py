import streamlit as st
from spacy import load, displacy
from st_on_hover_tabs import on_hover_tabs
from json import loads
from pandas import read_csv
from PIL import Image
from rembg import remove
import fitz  # PyMuPDF
import matplotlib.pyplot as plt

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    tabs = on_hover_tabs(tabName=['Upload de arquivos', 'Cortar Imagem', 'Extrair Dados', 'Teste'], 
                         iconName=['dashboard', 'money', 'economy', '🧔'], default_choice=0)

if tabs =='Upload de arquivos':

    st.markdown('''
    # Exibidor de arquivos

    ## Suba um arquivo e vejamos o que acontece :smile::heart:
    ''')


    arquivo = st.file_uploader(
        'Suba seu arquivo aqui!',
        type=['jpg', 'png', 'py', 'wav', 'csv', 'json']
    )

    # st.text_input('Email', max_chars=10)
    # st.text_input('Senha', type='password')

    if arquivo:
        print(arquivo.type)
        match arquivo.type.split('/'):
            case 'application', 'json':
                st.json(loads(arquivo.read()))
            case 'image', _:
                st.image(arquivo)
            case 'text', 'csv':
                df = read_csv(arquivo).transpose()
                st.dataframe(df)
                st.bar_chart(df)
            case 'text', 'x-python':
                st.code(arquivo.read().decode())
            case 'audio', _:
                st.audio(arquivo)
    else:
        st.error('Ainda não tenho arquivo!')

elif tabs == 'Cortar Imagem':
    def remove_background(image):
        # Remove background from the image
        output = remove(image)
        return output

    st.markdown('''
     # Recorte o fundo de uma imagem 

        ## Suba sua iamgem e vejamos o que acontece 😎👌  >>>  🕶🤏😳
     ''')

    uploaded_image = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Imagem Original")

        # Remover o fundo
        result_image = remove_background(image)

        st.image(result_image, caption="Imagem Sem Fundo")

        # Download da imagem resultante
        st.download_button(
            label="Baixar Imagem Sem Fundo",
            data=result_image.tobytes(),
            file_name="imagem_sem_fundo.png",
            mime="image/png"
        )

elif tabs == 'Extrair Dados':
    st.title("Extraia dados de PDF")

    uploaded_pdf = st.file_uploader("Escolha um PDF", type="pdf")

    if uploaded_pdf:
        # Abrir o PDF
        pdf_document = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        
        # Extrair texto do PDF
        extracted_text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            extracted_text += page.get_text()

        st.text_area("Texto Extraído", extracted_text)

        # Plotar gráfico de contagem de palavras
        words = extracted_text.split()
        word_count = {word: words.count(word) for word in set(words)}

        fig, ax = plt.subplots()
        ax.bar(word_count.keys(), word_count.values())
        ax.set_xlabel("Palavras")
        ax.set_ylabel("Contagem")
        ax.set_title("Contagem de Palavras no Texto Extraído")
        plt.xticks(rotation=90)

        st.pyplot(fig)

elif tabs == 'Teste':
    st.title("a")