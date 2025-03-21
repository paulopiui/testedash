from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Simulando base de dados
dados = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "nome_projeto": ["Obra A", "Obra B", "Obra C", "Obra D"],
    "contrato": ["CT-01", "CT-01", "CT-02", "CT-03"],
    "valor_orcamento": [100000, 150000, 120000, 180000]
})

# Inicializa o app
app = Dash(__name__)
app.title = "Dashboard de Projetos"

# Layout
app.layout = html.Div([
    html.H2("📊 Visualização de Projetos"),

    html.Label("Contrato"),
    dcc.Dropdown(
        options=[{"label": c, "value": c} for c in sorted(dados["contrato"].unique())],
        id="filtro_contrato",
        placeholder="Selecione um contrato",
        clearable=True
    ),

    dcc.Graph(id="grafico_valores"),

    html.H4("📋 Tabela de Projetos"),
    html.Div(id="tabela_projetos")
])

# Callback: atualiza gráfico e tabela
@app.callback(
    Output("grafico_valores", "figure"),
    Output("tabela_projetos", "children"),
    Input("filtro_contrato", "value")
)
def atualizar_visao(contrato_selecionado):
    if contrato_selecionado:
        df_filtrado = dados[dados["contrato"] == contrato_selecionado]
    else:
        df_filtrado = dados

    # Gráfico
    fig = px.bar(df_filtrado, x="nome_projeto", y="valor_orcamento",
                 title="Valor por Projeto", labels={"valor_orcamento": "Valor (R$)"})

    # Tabela em HTML
    tabela_html = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df_filtrado.columns])),
        html.Tbody([
            html.Tr([html.Td(df_filtrado.iloc[i][col]) for col in df_filtrado.columns])
            for i in range(len(df_filtrado))
        ])
    ])

    return fig, tabela_html

# Rodar
if __name__ == "__main__":
    app.run_server(debug=True)
