from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import pandas as pd
import numpy as np
from json import loads
from PIL import Image, ImageFont, ImageDraw
from rembg import remove

class Page():
    def __init__(self) -> None:
        st.set_page_config(layout="wide")
        st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
        Sidebar().view_page()

class Sidebar():
    def __init__(self):
        self.sidebar_options = ['Dashboard', 'Arquivos', 'Marca De dágua', 'Widgets']
        self.sidebar_icons = ['dashboard', 'money', 'economy', '❇']
        self.sidebar_options_style = {'navtab': {'background-color':'#111',
                                                  'color': '#818181',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                       'tabOptionsStyle': {':hover :hover': {'color': 'fafafa',
                                                                      'cursor': 'pointer'}},
                                       'iconStyle':{'position':'fixed',
                                                    'left':'7.5px',
                                                    'text-align': 'left'},
                                       'tabStyle' : {'list-style-type': 'none',
                                                     'margin-bottom': '30px',
                                                     'padding-left': '30px'}}
    
    # def text_on_image(image, text, font_size, color):
    #     img = Image.open(image)
    #     font = ImageFont.truetype('arial.ttf', font_size)
    #     draw = ImageDraw.Draw(img)

    #     iw, ih = img.size
    #     fw, fh = font.getsize(text)

    #     draw.text(
    #         ((iw - fw) / 2, (ih - fh) / 2),
    #         text,
    #         fill=color,
    #         font=font
    #     )

    #     img.save('last_image.jpg')

    def view_page(self):
        with st.sidebar:
            tabs = on_hover_tabs(tabName= self.sidebar_options, 
                                 iconName= self.sidebar_icons, 
                                 styles = self.sidebar_options_style, 
                                 key="1")
            
        if tabs =='Dashboard':
            st.title("💹 Dashboard 💹")
            st.write('Name of option is {}'.format(tabs))
            st.write("Aqui está uma tabela de dados aleatórios:")
            data = pd.DataFrame(
                np.random.randn(10, 5),
                columns=('coluna %d' % i for i in range(5))
            )
            st.write(data)
            st.bar_chart(data, width=100)
            st.line_chart(data)
            st.area_chart(data)
            st.scatter_chart(data)

        elif tabs == 'Arquivos':
            st.title("Paper")
            arquivo = st.file_uploader('Suba seu arquivo aqui!',
            type=['jpg', 'png', 'py', 'wav', 'csv', 'json', 'mp3', 'mp4'])

            if arquivo:
                print(arquivo.type)
                match arquivo.type.split('/'):
                    case 'application', 'json':
                        st.json(loads(arquivo.read()))
                    case 'image', _:
                        st.image(arquivo)   
                    case 'text', 'x-python':
                        st.code(arquivo.read().decode())
                    case 'video', 'mp4':
                        st.video(arquivo)        
                    case 'audio', _:
                        st.title(arquivo.name)
                        st.audio(arquivo)
                    case 'text', 'csv':
                        df = pd.read_csv(arquivo, sep=';', encoding='ISO-8859-1')
                        st.dataframe(df)
                
            else:
                st.error("Ainda não tem nenhum arquivo inserido!")

        elif tabs == 'Marca De dágua':
          st.title("?")
            ####################################
        elif tabs == 'Widgets':
            st.title(tabs)
            
            st.text('Slider')
            x = st.slider('x')  # 👈 this is a widget
            st.write(x, 'squared is', x * x)
            st.code(f"x = st.slider('x') \nst.write(x, 'squared is', x * x)")

            st.divider()

            st.text('input')
            st.text_input("Your name", key="name", placeholder="Seu nome")
            st.code('st.text_input("Your name", key="name")\n# You can access the value at any point with: \nst.session_state.name')

            st.divider()

            st.text('CheckBox')
            if st.checkbox('Show dataframe'):
                chart_data = pd.DataFrame(
                    np.random.randn(20, 3),
                    columns=['a', 'b', 'c'])

                chart_data
            st.code("if st.checkbox('Show dataframe'):\n    chart_data = pd.DataFrame(\n        np.random.randn(20, 3),\n        columns=['a', 'b', 'c'])\nchart_data")

            st.divider()

            st.text('selextbox')
            df = pd.DataFrame({
            'first column': [1, 2, 3, 4],
            'second column': [10, 20, 30, 40]
            })

            option = st.selectbox(
                'Which number do you like best?',
                df['second column'])

            'You selected: ', option




App = Page()
