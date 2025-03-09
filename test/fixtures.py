dados_cadastro_sem_empresa = {
    "nome": "vaga teste",
    "link": "https://example.com",
    "status": "candidatar-se",
    "descricao": "descrição teste",
    "nome_empresa": None,
}

dados_cadastro_sem_empresa_link_duplicado = {
    "nome": "vaga teste 2",
    "link": "https://example.com",
    "status": "em análise",
    "descricao": "descrição teste",
    "nome_empresa": None,
}

dados_cadastro_sem_empresa_link_invalido = {
    "nome": "vaga teste",
    "link": "//example.com",
    "status": "candidatar-se",
    "descricao": "descrição teste",
    "nome_empresa": None,
}

dados_cadastro_com_empresa = {
    "nome": "vaga teste",
    "link": "https://example.com",
    "status": "candidatar-se",
    "descricao": "descrição teste",
    "nome_empresa": "Amazon",
}

dados_cadastro_com_empresa2 = {
    "nome": "vaga teste",
    "link": "https://example23.com",
    "status": "candidatar-se",
    "descricao": "descrição teste",
    "nome_empresa": "Amazon",
}

dados_todas_candidaturas = [
    {
        "nome": "Desenvolvedor Backend",
        "link": "https://jobs.example.com/1",
        "status": "candidatar-se",
    },
    {
        "nome": "Engenheiro de Software",
        "link": "https://jobs.example.com/2",
        "status": "entrevista",
    },
    {
        "nome": "Analista de Dados",
        "link": "https://jobs.example.com/3",
        "status": "candidatar-se",
    },
    {
        "nome": "Desenvolvedor Mobile",
        "link": "https://jobs.example.com/4",
        "status": "candidatar-se",
    },
    {
        "nome": "DevOps Engineer",
        "link": "https://jobs.example.com/5",
        "status": "teste técnico",
    },
    {
        "nome": "Product Manager",
        "link": "https://jobs.example.com/6",
        "status": "candidatar-se",
    },
    {
        "nome": "QA Engineer",
        "link": "https://jobs.example.com/7",
        "status": "candidatar-se",
    },
    {
        "nome": "Data Scientist",
        "link": "https://jobs.example.com/8",
        "status": "entrevista",
    },
    {
        "nome": "Cloud Engineer",
        "link": "https://jobs.example.com/9",
        "status": "candidatar-se",
    },
    {
        "nome": "Software Architect",
        "link": "https://jobs.example.com/10",
        "status": "candidatar-se",
    },
]

todas_candidaturas_printadas = [
    "Selecione uma candidatura para editar (Setas para navegar,"
    " Enter para selecionar e ESC para retornar ao menu principal)",
    "> Limpar filtro",
    "> Filtrar por nome",
    "> Filtrar por link",
    "> Filtrar por status",
    "Desenvolvedor Backend - candidatar-se",
    "Engenheiro de Software - entrevista",
    "Analista de Dados - candidatar-se",
    "Desenvolvedor Mobile - candidatar-se",
    "DevOps Engineer - teste técnico",
    "Product Manager - candidatar-se",
    "QA Engineer - candidatar-se",
    "Data Scientist - entrevista",
    "Cloud Engineer - candidatar-se",
    "Software Architect - candidatar-se",
]

candidaturas_filtradas_por_nome = [
    "Selecione uma candidatura para editar (Setas para navegar,"
    " Enter para selecionar e ESC para retornar ao menu principal)",
    "> Limpar filtro",
    "> Filtrar por nome",
    "> Filtrar por link",
    "> Filtrar por status",
    "Desenvolvedor Backend - candidatar-se",
    "Desenvolvedor Mobile - candidatar-se",
]

candidaturas_filtradas_por_link = [
    "Selecione uma candidatura para editar (Setas para navegar,"
    " Enter para selecionar e ESC para retornar ao menu principal)",
    "> Limpar filtro",
    "> Filtrar por nome",
    "> Filtrar por link",
    "> Filtrar por status",
    "Desenvolvedor Backend - candidatar-se",
    "Software Architect - candidatar-se",
]

candidaturas_filtradas_por_status = [
    "Selecione uma candidatura para editar (Setas para navegar,"
    " Enter para selecionar e ESC para retornar ao menu principal)",
    "> Limpar filtro",
    "> Filtrar por nome",
    "> Filtrar por link",
    "> Filtrar por status",
    "Desenvolvedor Backend - candidatar-se",
    "Analista de Dados - candidatar-se",
    "Desenvolvedor Mobile - candidatar-se",
    "Product Manager - candidatar-se",
    "QA Engineer - candidatar-se",
    "Cloud Engineer - candidatar-se",
    "Software Architect - candidatar-se",
]

nenhum_candidatura_printada = [
    "Selecione uma candidatura para editar (Setas para navegar,"
    " Enter para selecionar e ESC para retornar ao menu principal)",
    "> Limpar filtro",
    "> Filtrar por nome",
    "> Filtrar por link",
    "> Filtrar por status",
    "Nenhuma candidatura encontrada",
]


mensagem_sucesso_status = [
    "✅ Status atualizado para: entrevista",
    "Pressione qualquer tecla para voltar ao menu principal",
]

mensagem_sucesso_edicao_nome = [
    "✅ Campo Nome atualizado com sucesso!",
    "Pressione qualquer tecla para voltar ao menu principal",
]

mensagem_sucesso_edicao_link = [
    "✅ Campo Link atualizado com sucesso!",
    "Pressione qualquer tecla para voltar ao menu principal",
]

mensagem_sucesso_edicao_data = [
    "✅ Campo Data_aplicacao atualizado com sucesso!",
    "Pressione qualquer tecla para voltar ao menu principal",
]

mensagem_sucesso_edicao_status = [
    "✅ Campo Status atualizado com sucesso!",
    "Pressione qualquer tecla para voltar ao menu principal",
]

mensagem_sucesso_edicao_descricao = [
    "✅ Campo Descricao atualizado com sucesso!",
    "Pressione qualquer tecla para voltar ao menu principal",
]
