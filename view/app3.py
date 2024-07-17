import streamlit as st
from streamlit.components import v1 as components
import spacy
from spacy import displacy

# Carregar o modelo de linguagem do spaCy
nlp = spacy.load('pt_core_news_lg')

# Barra lateral para seleção de categoria
bar = st.sidebar

escolha = bar.selectbox(
    'Escolha uma categoria',
    ['Entidades', 'Gramática']
)

# Área de texto para inserir o texto
text = st.text_area('Bote um textão aqui!')

# Processar o texto com o modelo spaCy
doc = nlp(text)

if text and escolha == 'Entidades':
    data = displacy.render(doc, style='ent')

    with st.expander('Dados do spaCy'):
        components.html(
            data, scrolling=True, height=300
        )

    # Exibir entidades reconhecidas
    a, b = st.columns(2)
    for e in doc.ents:
        a.info(e.text)
        b.warning(e.label_)

if text and escolha == 'Gramática':
    filtro = bar.multiselect(
        'Filtro',
        ['VERB', 'PROPN', 'ADV', 'AUX'],
        default=['VERB', 'PROPN']
    )
    with st.expander('Dados do spaCy'):
        st.json(doc.to_json())

    # Criar colunas para exibir tokens
    container = st.container()
    a, b, c = container.columns(3)

    a.subheader('Token')
    b.subheader('Tag')
    c.subheader('Morph')

    # Exibir tokens filtrados
    for t in doc:
        if t.pos_ in filtro:
            a, b, c = st.columns(3)
            a.info(t.text)
            b.warning(t.tag_)
            c.error(t.morph)
