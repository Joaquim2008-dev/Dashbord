import pandas as pd
import plotly.express as px
import streamlit as st
from matplotlib.ticker import FuncFormatter

# Cache para leitura dos dados

st.set_page_config(layout='wide')


@st.cache_data
def carregar_dados():
    df = pd.read_csv('Relatorio (1).csv', sep=';')
    df['Valor Transferência'] = df['Valor Transferência'] / 100
    df['Mês / Ano'] = pd.to_datetime(df['Mês / Ano'],
                                     format='%Y%m')
    df['Ano'] = df['Mês / Ano'].dt.year
    df['Mês'] = df['Mês / Ano'].dt.month

    for coluna in df.columns:
        if len(df[df[coluna].notnull()].index) == 0:
            df.drop(coluna, axis=1, inplace=True)
    df.dropna(inplace=True)
    return df


df = carregar_dados()

todos_meses = pd.date_range(
    start=df['Mês / Ano'].min(),
    end=df['Mês / Ano'].max(),
    freq='MS'  # 'MS' = Month Start
)


# Função para formatar valores em reais


def formatar_reais(valor, pos):
    return f'R${valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# Função para gráfico de barras empilhadas


def grafico_barra_stacked(df, index, columns, values):
    grupo = df.groupby([index, columns])[values].sum().reset_index()
    tabela_pivot = pd.pivot(
        grupo, index=index, columns=columns, values=values).fillna(0)
    fig = px.bar(tabela_pivot, x=tabela_pivot.index, y=[col for col in tabela_pivot.columns if
                                                        col != 'Ano'], text_auto=True)
    st.plotly_chart(fig, use_container_width=True)


def grafico_linha_meses(df, index, columns, values):
    grupo = df.groupby([index, columns])[values].sum().reset_index()
    tabela_pivot = pd.pivot(
        grupo, index=index, columns=columns, values=values).fillna(0)
    fig = px.line(tabela_pivot, x=tabela_pivot.index, y=tabela_pivot.columns)
    fig.update_xaxes(
        tickformat="%b/%Y"
    )
    st.plotly_chart(fig)


# Layout do app
dados_totais = df['Valor Transferência'].sum()
total_anos = df.groupby('Ano')['Valor Transferência'].sum()

st.title('📈Dashbord dos recursos transferidos entre 2020 a 2025📊')
st.metric('Total transferido do período:', f'R${dados_totais:,.2f}'.replace(
    ',', 'X').replace('.', ',').replace('X', '.'))

co2, co3, co4, co5, co6, co7 = st.columns(6)

with co2:
    st.metric('Total transferido em 2020:', f'R${total_anos[2020]:,.2f}'.replace(
        ',', 'X').replace('.', ',').replace('X', '.'))
with co3:
    st.metric('Total transferido em 2021:', f'R${total_anos[2021]:,.2f}'.replace(
        ',', 'X').replace('.', ',').replace('X', '.'))
with co4:
    st.metric('Total transferido em 2022:', f'R${total_anos[2022]:,.2f}'.replace(
        ',', 'X').replace('.', ',').replace('X', '.'))
with co5:
    st.metric('Total transferido em 2023:', f'R${total_anos[2023]:,.2f}'.replace(
        ',', 'X').replace('.', ',').replace('X', '.'))
with co6:
    st.metric('Total transferido em 2024:', f'R${total_anos[2024]:,.2f}'.replace(
        ',', 'X').replace('.', ',').replace('X', '.'))
with co7:
    st.metric('Total transferido em 2025:', f'R${total_anos[2025]:,.2f}'.replace(
        ',', 'X').replace('.', ',').replace('X', '.'))

aba1, aba2, aba3 = st.tabs(['Comparação dos recursos por ano e por Mês',
                            'Proporção Tipo Favorecido e Modalidade Despesa',
                            'Análise de alguns recursos transferidos por mês no período analisado'])


with aba1:
    opcao = st.selectbox('Escolha uma categoria',
                         ('Tipo Transferência', 'Tipo Favorecido',
                          'Linguagem Cidadã', 'Nome Grupo Despesa',
                          'Nome Modalidade Aplicação Despesa', 'Nome Elemento Despesa', 'Nome Ação'))

    grafico_barra_stacked(df, 'Ano', opcao,
                              'Valor Transferência')

    grafico_linha_meses(df, 'Mês / Ano', opcao, 'Valor Transferência')

with aba2:
    st.subheader('Proporção dos recursos por Tipo Favorecido')
    grupo = df.groupby(['Ano', 'Tipo Favorecido'])['Valor Transferência'].sum()
    con = grupo.groupby(level=0).sum()
    new = (grupo/con)*100
    new = new.round(1)
    tabela_pivot = new.reset_index().pivot(index='Ano', columns='Tipo Favorecido',
                                           values='Valor Transferência')
    tabela_long = tabela_pivot.reset_index().melt(
        id_vars='Ano', var_name='Categoria', value_name='Proporção')
    fig = px.bar(
        tabela_long,
        x='Ano',
        y='Proporção',
        color='Categoria',
        text='Proporção',
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textfont_size=18)
    fig.update_yaxes(ticksuffix='%')
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader(
        'Proporção dos recursos por Nome Modalidade Aplicação Despesa')
    grupo = df.groupby(['Ano', 'Nome Modalidade Aplicação Despesa'])[
        'Valor Transferência'].sum()
    con = grupo.groupby(level=0).sum()
    new = (grupo/con)*100
    new = new.round(1)
    tabela_pivot = new.reset_index().pivot(index='Ano', columns='Nome Modalidade Aplicação Despesa',
                                           values='Valor Transferência').fillna(0)
    tabela_long = tabela_pivot.reset_index().melt(
        id_vars='Ano', var_name='Categoria', value_name='Proporção')
    fig = px.bar(
        tabela_long,
        x='Ano',
        y='Proporção',
        color='Categoria',
        text='Proporção',
    )
    fig.update_traces(texttemplate='%{text:.1f}%')
    fig.update_yaxes(ticksuffix='%')
    st.plotly_chart(fig, use_container_width=True)

with aba3:
    lista_recursos = ['Tipo Favorecido',
                      'Tipo Transferência',
                      'Nome Ação',
                      'Nome Modalidade Aplicação Despesa', 'Todos']
    print(lista_recursos[0:4])

    lista_datas = [2020, 2021, 2022, 2023, 2024, 2025, 'Todos']

    ano = st.selectbox('Escolha um ano',
                       lista_datas,
                       index=6
                       )

    recurso = st.selectbox('Escolha uma categoria',
                           lista_recursos,
                           index=4

                           )

    if recurso == 'Todos':
        opcao = ''

    elif recurso != 'Todos':
        opcao = st.multiselect('Escolha seu objeto de análise',
                               df[recurso].unique())

    if recurso == ano == 'Todos':

        grupo = df.groupby(
            ['Ano', 'Mês / Ano', 'Tipo Favorecido', 'Tipo Transferência',
             'Nome Ação', 'Nome Modalidade Aplicação Despesa'])['Valor Transferência'].sum().reset_index()

        long = grupo.melt(id_vars=['Ano', 'Mês / Ano',
                                   'Valor Transferência'], value_vars=lista_recursos[0:4], value_name='Categoria')

        fig = px.bar(long, x='Mês / Ano',
                     y='Valor Transferência', color='Categoria', text='Valor Transferência')

        fig.update_traces(
            texttemplate='%{text:,.1f}',
            textangle=0,                # texto horizontal
            textposition='outside',     # texto fora da barra
            cliponaxis=False,           # texto não é cortado
            textfont_size=14
        )

        st.plotly_chart(fig)

    if ano == 'Todos' and recurso != 'Todos':

        filtro_ano = df[df[recurso].isin(opcao)]

        grupo = filtro_ano.groupby(
            ['Ano', 'Mês / Ano', recurso])['Valor Transferência'].sum().reset_index()

        long = grupo.melt(id_vars=['Ano', 'Mês / Ano',
                                   'Valor Transferência'], value_vars=recurso, value_name='Categoria')

        fig = px.bar(long, x='Mês / Ano',
                     y='Valor Transferência', color='Categoria', text='Valor Transferência')

        fig.update_traces(
            texttemplate='%{text:,.1f}',
            textangle=0,                # texto horizontal
            textposition='outside',     # texto fora da barra
            cliponaxis=False,           # texto não é cortado
            textfont_size=14
        )

        st.plotly_chart(fig)

    if recurso == 'Todos' and ano != 'Todos':
        filtro_ano = df[df['Ano'] == ano]

        grupo = filtro_ano.groupby(
            ['Ano', 'Mês / Ano', 'Tipo Favorecido', 'Tipo Transferência',
             'Nome Ação', 'Nome Modalidade Aplicação Despesa'])['Valor Transferência'].sum().reset_index()

        long = grupo.melt(id_vars=['Ano', 'Mês / Ano',
                                   'Valor Transferência'], value_vars=lista_recursos[0:4], value_name='Categoria')

        fig = px.bar(long, x='Mês / Ano',
                     y='Valor Transferência', color='Categoria', text='Valor Transferência')

        fig.update_traces(
            texttemplate='%{text:,.1f}',
            textangle=0,                # texto horizontal
            textposition='outside',     # texto fora da barra
            cliponaxis=False,           # texto não é cortado
            textfont_size=14
        )

        st.plotly_chart(fig)

    if recurso != 'Todos' and ano != 'Todos':

        filtro_ano = df[df['Ano'] == ano][df[recurso].isin(opcao)]

        grupo = filtro_ano.groupby(
            ['Ano', 'Mês / Ano', recurso])['Valor Transferência'].sum().reset_index()

        long = grupo.melt(id_vars=['Ano', 'Mês / Ano',
                                   'Valor Transferência'], value_vars=recurso, value_name='Categoria')

        fig = px.bar(long, x='Mês / Ano',
                     y='Valor Transferência', color='Categoria', text='Valor Transferência')

        fig.update_traces(
            texttemplate='%{text:,.2f}',
            textangle=0,                # texto horizontal
            textposition='outside',     # texto fora da barra
            cliponaxis=False,           # texto não é cortado
            textfont_size=14
        )

        st.plotly_chart(fig)

