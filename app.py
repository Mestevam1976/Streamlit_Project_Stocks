# 1. Importação das bibliotecas:
import yfinance as yf
import datetime as dt
import streamlit as st

# 2. Variáveis de tempo:
end_date = dt.datetime.today()
start_date = dt.datetime(end_date.year-1,end_date.month,end_date.day)

# 2.1 Lista de Ativos da Bolsa Brasileira - acompanhados do .SA:
ativos = sorted(['PETR4.SA','VALE3.SA', 'MGLU3.SA','ITSA4.SA','ITUB4.SA',
                'TRPL4.SA', 'BBDC4.SA', 'ABEV3.SA', 'BOVA11.SA',
                'BBAS3.SA', 'KLBN4.SA', 'LEVE3.SA','MRVE3.SA',
                'CIEL3.SA', 'BBSE3.SA', 'STBP3.SA', 'GGBR4.SA',
                'AZUL4.SA', 'RENT3.SA', 'PRIO3.SA', 'LREN3.SA',
                'HAPV3.SA', 'VBBR3.SA', 'ELET3.SA', 'ELET6.SA',
                'WEGE3.SA', 'RADL3.SA', 'JBSS3.SA', 'EMBR3.SA',
                'RAIL3.SA', 'TIMS3.SA', 'ODPV3.SA', 'CSNA3.SA',
                'KLBN11.SA', 'UGPA3.SA', 'SUZB3.SA'])

# 3. Exibindo as informações:
st.set_page_config('Dashboard - Ativos na Bolsa de Valores', page_icon='stock.png', layout='wide')

#st.sidebar.header('Teste') # Sidebar

st.title('Dashboard - Ativos na Bolsa de Valores')

with st.container():
    st.header('Insira as informações solicitadas abaixo:')

    col1,col2,col3 = st.columns(3)

    with col1:
        ativo = st.selectbox('Selecione o ativo desejado: ',options=ativos)
    with col2:
        data_inicial = st.date_input('Selecione a data inicial: ',start_date)
    with col3:
        data_final = st.date_input('Selecione a data final: ', end_date)

# 4. Coletando as informações com a API do Yahoo Finance:
df = yf.download(ativo,data_inicial,data_final)

# 5. Definição das Métricas:
ult_atualizacao = df.index.max() # Data da última atualização
ult_cotacao = round(df.loc[df.index.max(),'Close'],2) # Última cotação encontrada
menor_cotacao = round(df['Close'].min(),2) # Menor cotação no período escolhido
maior_cotacao = round(df['Close'].max(),2) # Maior cotação no período escolhido
prim_cotacao = round(df.loc[df.index.min(),'Close'],2) # Primeira cotação encontrada
delta = round(((ult_cotacao - prim_cotacao)/prim_cotacao)*100,2) # A variação % da cotação no período escolhido

# 6. Acrescentando as métricas no container das 3 colunas:
with st.container():
    with col1:
        real_ult_cotacao =str("R$ {:,.2f}").format(ult_cotacao).replace('.', ',')
        st.metric(f"Última atualização (D-1) em: {ult_atualizacao:%d/%m/%Y}", real_ult_cotacao,f"{delta} %")
    with col2:
        real_menor_cotacao = str("R$ {:,.2f}").format(menor_cotacao).replace('.', ',')
        st.metric("Menor cotação no período: ", real_menor_cotacao)
    with col3:
        real_maior_cotacao = str("R$ {:,.2f}").format(maior_cotacao).replace('.',',')
        st.metric("Maior cotação no período: ", real_maior_cotacao)

# 7. Criando o Gráfico do Ativo Escolhido:
with st.container():
   st.area_chart(round(df[['Close']],2),use_container_width=True) # Gráfico de Área
   st.line_chart(round(df[['Low','Close','High']], 2),color= ["#ffaa00","#ff0000","#00bbcc"]) # Gráf. linha
   #st.bar_chart(round(df[['Low', 'Close', 'High']], 2), color=["#ffaa00", "#ff0000", "#00bbcc"])