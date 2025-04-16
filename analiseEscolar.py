import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html

# Gerar Dados Fictícios para análise
np.random.seed(42)
n_alunos = 500

dados = {
    "Aluno": [f"Aluno{i+1}" for i in range(n_alunos)],
    "Nota_Matematica": np.random.randint(50, 100, n_alunos),
    "Nota_Portugues": np.random.randint(50, 100, n_alunos),
    "Nota_Ciencia": np.random.randint(50, 100, n_alunos),
    "Nota_Historia": np.random.randint(50, 100, n_alunos),
    "Nota_Geografia": np.random.randint(50, 100, n_alunos),
    "Nota_Ingles": np.random.randint(50, 100, n_alunos),
    "Frequencia": np.random.randint(15, 25, n_alunos),
    "Atividade_Extra": np.random.choice(["Sim", "Não"], n_alunos)
}

df = pd.DataFrame(dados)

# Cálculo de média geral
df["Media_Geral"] = df[["Nota_Matematica", "Nota_Portugues", "Nota_Ciencia", "Nota_Historia", "Nota_Geografia", "Nota_Ingles"]].mean(axis=1)

# Dash app
app = dash.Dash(__name__)
app.title = "Dashboard Escolar"

# Gráfico de distribuição de notas
fig_disciplinas = px.box(
    df,
    y=["Nota_Matematica", "Nota_Portugues", "Nota_Ciencia", "Nota_Historia", "Nota_Geografia", "Nota_Ingles"],
    points="all",
    title="Distribuição das Notas por Disciplina"
)

# Gráfico de média por atividade extra
media_por_atividade = df.groupby("Atividade_Extra")[["Nota_Matematica", "Nota_Portugues", "Nota_Ciencia", "Nota_Historia", "Nota_Geografia", "Nota_Ingles"]].mean().reset_index()
fig_atividade = px.bar(
    media_por_atividade.melt(id_vars="Atividade_Extra", var_name="Disciplina", value_name="Nota Média"),
    x="Disciplina",
    y="Nota Média",
    color="Atividade_Extra",
    barmode="group",
    title="Média das Notas por Participação em Atividades Extracurriculares"
)

# Top 10 alunos por média geral
top_alunos = df.sort_values(by="Media_Geral", ascending=False).head(10)

# Comparação de alunos com mais e menos faltas
aluno_mais_faltas = df.sort_values(by="Frequencia").iloc[0]
aluno_menos_faltas = df.sort_values(by="Frequencia", ascending=False).iloc[0]

# Gráfico comparativo de notas por aluno
disciplinas = ["Nota_Matematica", "Nota_Portugues", "Nota_Ciencia", "Nota_Historia", "Nota_Geografia", "Nota_Ingles"]

fig_comparativo = go.Figure()
fig_comparativo.add_trace(go.Bar(
    x=disciplinas,
    y=[aluno_mais_faltas[disc] for disc in disciplinas],
    name=f"{aluno_mais_faltas['Aluno']} (Mais Faltas)"
))
fig_comparativo.add_trace(go.Bar(
    x=disciplinas,
    y=[aluno_menos_faltas[disc] for disc in disciplinas],
    name=f"{aluno_menos_faltas['Aluno']} (Menos Faltas)"
))
fig_comparativo.update_layout(
    barmode='group',
    title="Comparação de Desempenho: Aluno com Mais e Menos Faltas",
    yaxis_title="Nota",
    xaxis_title="Disciplina"
)

# Layout do app
app.layout = html.Div([
    html.H1("Análise de Desempenho Escolar", style={"textAlign": "center"}),

    html.H2("Distribuição das Notas"),
    dcc.Graph(figure=fig_disciplinas),

    html.H2("Média por Participação em Atividades Extracurriculares"),
    dcc.Graph(figure=fig_atividade),

    html.H2("Top 10 Alunos por Média Geral"),
    html.Ul([
        html.Li(f"{row['Aluno']}: {row['Media_Geral']:.2f}")
        for i, row in top_alunos.iterrows()
    ]),

    html.H2("Aluno com MAIS faltas"),
    html.P(f"{aluno_mais_faltas['Aluno']} - Frequência: {aluno_mais_faltas['Frequencia']}"),
    html.Ul([
        html.Li(f"{disciplina}: {aluno_mais_faltas[disciplina]}") for disciplina in disciplinas
    ]),

    html.H2("Aluno com MENOS faltas"),
    html.P(f"{aluno_menos_faltas['Aluno']} - Frequência: {aluno_menos_faltas['Frequencia']}"),
    html.Ul([
        html.Li(f"{disciplina}: {aluno_menos_faltas[disciplina]}") for disciplina in disciplinas
    ]),

    html.H2("Comparação Gráfica entre os dois alunos"),
    dcc.Graph(figure=fig_comparativo)
])

if __name__ == '__main__':
    app.run(debug=True)