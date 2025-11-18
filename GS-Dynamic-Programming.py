# ======================================================
# GLOBAL SOLUTION – Futuro do Trabalho
# Turma: 2ESPI
# Integrantes:
# - Guilherme da Cunha Melo - 555310
# - Paulo Akira Okama - 556840
# - Rafael Bocchi - 557603
# ======================================================
# APRESENTAÇÃO DA FORMULAÇÃO DO PROBLEMA
# ======================================================
# ENTRADA (dados que o programa recebe/usa):
#   • Base de módulos de capacitação (lista de dicionários), cada módulo com:
#       - nome (texto)
#       - duracao (horas, inteiro >= 0)
#       - ganho (pontos de valor, inteiro >= 0)
#       - prazo (data no formato ddmmyy)
#   • Orçamento total de horas T (inteiro >= 0), informado pelo usuário.
#
# SAÍDA (o que o programa entrega):
#   • Conjunto de módulos selecionados cuja soma das durações <= T
#     e cujo ganho total seja o MAIOR possível.
#   • Relatório no console contendo:
#       - Orçamento T, horas efetivamente usadas e ganho total obtido.
#       - Lista dos módulos escolhidos (ordenados por prazo ddmmyy).
#   • Arquivos CSV para abrir no Excel:
#       - relatorio_capacitacao.csv  → resumo + itens escolhidos
#       - modulos_base.csv          → base completa atual
#
# OBJETIVO (formulação de otimização – Mochila 0/1):
#   • Maximizar a soma dos ganhos dos módulos escolhidos,
#     sujeito à restrição de horas:  soma(duracao) <= T.
#   • Observação: NÃO é obrigatório usar exatamente T horas; usar menos
#     horas é válido se isso resultar em ganho total maior.
# ======================================================

# ------------------------ UTIL ------------------------

def eh_inteiro_nao_negativo(txt):
    if len(txt) == 0:
        return False
    i = 0
    while i < len(txt):
        c = txt[i]
        if c < '0' or c > '9':
            return False
        i += 1
    return True

def eh_data_ddmmyy(txt):
    # formato ddmmyy; valida dia/mês e fevereiro considerando (yy % 4 == 0)
    if len(txt) != 6:
        return False
    i = 0
    while i < 6:
        c = txt[i]
        if c < '0' or c > '9':
            return False
        i += 1

    dia = int(txt[0:2])
    mes = int(txt[2:4])
    ano = int(txt[4:6])  # 00..99

    if mes < 1 or mes > 12:
        return False
    if dia < 1:
        return False

    # 31 dias
    if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
        return dia <= 31
    # 30 dias
    if mes == 4 or mes == 6 or mes == 9 or mes == 11:
        return dia <= 30
    # fevereiro
    bissexto = (ano % 4 == 0)
    if bissexto:
        return dia <= 29
    else:
        return dia <= 28

def clonar_lista(lst):
    copia = []
    i = 0
    while i < len(lst):
        copia.append(lst[i])
        i += 1
    return copia

def data_leq_ddmmyy(a, b):
    da = int(a[0:2]); ma = int(a[2:4]); aa = int(a[4:6])
    db = int(b[0:2]); mb = int(b[2:4]); ab = int(b[4:6])
    if aa != ab: return aa < ab
    if ma != mb: return ma < mb
    return da <= db

def mostrar_um(m):
    linha = "id=" + str(m["id"]) + ", nome=" + m["nome"] \
            + ", duracao=" + str(m["duracao"]) + "h" \
            + ", ganho=" + str(m["ganho"]) \
            + ", prazo=" + m["prazo"]
    print(linha)

def mostrar_lista(lst):
    i = 0
    while i < len(lst):
        mostrar_um(lst[i])
        i += 1

# ------------------------ DADOS (>= 20) ------------------------

modulos = [
    {"id": 1,  "nome": "Python p/ Dados",        "duracao": 6, "ganho": 12, "prazo": "151225"},
    {"id": 2,  "nome": "Fund. UX/UI",            "duracao": 4, "ganho": 7,  "prazo": "101225"},
    {"id": 3,  "nome": "SQL Essencial",          "duracao": 5, "ganho": 10, "prazo": "011225"},
    {"id": 4,  "nome": "Power BI Intermediário", "duracao": 8, "ganho": 15, "prazo": "200126"},
    {"id": 5,  "nome": "QA/Testing",             "duracao": 3, "ganho": 6,  "prazo": "051225"},
    {"id": 6,  "nome": "Lógica de Programação",  "duracao": 2, "ganho": 4,  "prazo": "301125"},
    {"id": 7,  "nome": "Estatística p/ Dados",   "duracao": 6, "ganho": 11, "prazo": "101226"},
    {"id": 8,  "nome": "Git e GitHub",           "duracao": 3, "ganho": 5,  "prazo": "151125"},
    {"id": 9,  "nome": "Cloud Básico",           "duracao": 5, "ganho": 9,  "prazo": "220126"},
    {"id": 10, "nome": "Automação Excel",        "duracao": 4, "ganho": 8,  "prazo": "181225"},
    {"id": 11, "nome": "Data Viz & Story",       "duracao": 3, "ganho": 6,  "prazo": "270126"},
    {"id": 12, "nome": "Introdução a NLP",       "duracao": 6, "ganho": 13, "prazo": "150226"},
    {"id": 13, "nome": "APIs REST",              "duracao": 4, "ganho": 7,  "prazo": "090126"},
    {"id": 14, "nome": "Machine Learning Intro", "duracao": 8, "ganho": 16, "prazo": "280226"},
    {"id": 15, "nome": "BigQuery Intro",         "duracao": 5, "ganho": 9,  "prazo": "120126"},
    {"id": 16, "nome": "Scrum Prático",          "duracao": 2, "ganho": 3,  "prazo": "041225"},
    {"id": 17, "nome": "Kanban na Prática",      "duracao": 2, "ganho": 3,  "prazo": "101225"},
    {"id": 18, "nome": "Segurança da Informação","duracao": 4, "ganho": 8,  "prazo": "050126"},
    {"id": 19, "nome": "Prompt Engineering",     "duracao": 3, "ganho": 7,  "prazo": "300126"},
    {"id": 20, "nome": "Docker Básico",          "duracao": 5, "ganho": 9,  "prazo": "210226"},
]
proximo_id = 21

# ---------------- MERGE SORT (rec + memo) ----------------

def merge_sort_por_campo(tabela, campo):
    memo = {}  # (ini, fim, campo) -> lista ordenada naquele intervalo

    def merge_range(ini, fim):
        chave = (ini, fim, campo)
        if chave in memo:
            return memo[chave]

        if fim - ini <= 1:
            pedaco = []
            i = ini
            while i < fim:
                pedaco.append(tabela[i])
                i += 1
            memo[chave] = pedaco
            return pedaco

        meio = (ini + fim) // 2
        esq = merge_range(ini, meio)
        dir = merge_range(meio, fim)

        i = 0; j = 0; res = []
        while i < len(esq) and j < len(dir):
            a = esq[i][campo]
            b = dir[j][campo]
            menor_ou_igual = False
            if campo == "prazo":
                menor_ou_igual = data_leq_ddmmyy(a, b)
            else:
                menor_ou_igual = (a <= b)

            if menor_ou_igual:
                res.append(esq[i]); i += 1
            else:
                res.append(dir[j]); j += 1

        while i < len(esq):
            res.append(esq[i]); i += 1
        while j < len(dir):
            res.append(dir[j]); j += 1

        memo[chave] = res
        return res

    return merge_range(0, len(tabela))

# ---------------- MOCHILA 0/1 (rec + memo) ----------------

def mochila_otima(itens, t_total):
    memo = {}  # (i, t) -> (ganho, lista_ids)

    def decide(i, t):
        chave = (i, t)
        if chave in memo:
            return memo[chave]

        if i == len(itens) or t == 0:
            memo[chave] = (0, [])
            return memo[chave]

        atual = itens[i]
        dur = atual["duracao"]
        gan = atual["ganho"]

        ganho_pula, lista_pula = decide(i + 1, t)

        if dur <= t:
            ganho_pega, lista_pega = decide(i + 1, t - dur)
            ganho_pega = ganho_pega + gan
            lista_pega = clonar_lista(lista_pega)
            lista_pega.append(atual["id"])
        else:
            ganho_pega = -1
            lista_pega = []

        if ganho_pega > ganho_pula:
            memo[chave] = (ganho_pega, lista_pega)
        else:
            memo[chave] = (ganho_pula, lista_pula)

        return memo[chave]

    return decide(0, t_total)

# ---------------- RELATÓRIO (console) ----------------

ultimo_relatorio = None

def gerar_relatorio(tabela, t_total, ganho, ids_escolhidos):
    escolhidos = []
    horas = 0
    i = 0
    while i < len(ids_escolhidos):
        alvo = ids_escolhidos[i]
        j = 0
        while j < len(tabela):
            if tabela[j]["id"] == alvo:
                escolhidos.append(tabela[j])
                horas += tabela[j]["duracao"]
                break
            j += 1
        i += 1

    escolhidos_ordenados = merge_sort_por_campo(escolhidos, "prazo")

    print("\n=== RELATÓRIO – PLANO DE CAPACITAÇÃO ===")
    print("Orçamento de horas:", t_total, "h")
    print("Horas usadas:", horas, "h")
    print("Ganho total:", ganho)
    print("\nMódulos selecionados (ordenados por prazo):")
    if len(escolhidos_ordenados) == 0:
        print("Nenhum módulo selecionado.")
    else:
        mostrar_lista(escolhidos_ordenados)

    info = {
        "t_total": t_total,
        "horas_usadas": horas,
        "ganho_total": ganho,
        "ids": clonar_lista(ids_escolhidos),
        "lista": clonar_lista(escolhidos_ordenados)
    }
    return info

# ---------------- EXPORTAÇÃO CSV ----------------

def salvar_lista_em_csv(caminho, itens):
    # Cabeçalho fixo: id;nome;duracao;ganho;prazo
    # Usamos ; como separador para abrir bem no Excel em PT-BR.
    arq = open(caminho, "w", encoding="utf-8")
    arq.write("id;nome;duracao;ganho;prazo\n")
    i = 0
    while i < len(itens):
        r = itens[i]
        # substitui ; no nome, se houver, para evitar quebrar o CSV
        nome_limpo = ""
        k = 0
        while k < len(r["nome"]):
            ch = r["nome"][k]
            if ch == ';':
                nome_limpo = nome_limpo + ','
            else:
                nome_limpo = nome_limpo + ch
            k += 1
        linha = str(r["id"]) + ";" + nome_limpo + ";" + str(r["duracao"]) + ";" + str(r["ganho"]) + ";" + r["prazo"] + "\n"
        arq.write(linha)
        i += 1
    arq.close()

def exportar_relatorio_csv(caminho, resumo):
    # CSV com o resumo + itens escolhidos (ordenados)
    arq = open(caminho, "w", encoding="utf-8")
    arq.write("Relatorio;Plano de Capacitação\n")
    arq.write("Orcamento_horas;" + str(resumo["t_total"]) + "\n")
    arq.write("Horas_usadas;" + str(resumo["horas_usadas"]) + "\n")
    arq.write("Ganho_total;" + str(resumo["ganho_total"]) + "\n")
    arq.write("\n")
    arq.write("id;nome;duracao;ganho;prazo\n")
    i = 0
    while i < len(resumo["lista"]):
        r = resumo["lista"][i]
        nome_limpo = ""
        k = 0
        while k < len(r["nome"]):
            ch = r["nome"][k]
            if ch == ';':
                nome_limpo = nome_limpo + ','
            else:
                nome_limpo = nome_limpo + ch
            k += 1
        arq.write(str(r["id"]) + ";" + nome_limpo + ";" + str(r["duracao"]) + ";" + str(r["ganho"]) + ";" + r["prazo"] + "\n")
        i += 1
    arq.close()

# ----------------------- MENU -----------------------

while True:
    print("\n=== GLOBAL SOLUTION – Capacitação ótima (Mochila) ===")
    print("1 - Cadastrar módulo")
    print("2 - Listar módulos")
    print("3 - Ordenar por GANHO (merge + memo)")
    print("4 - Ordenar por PRAZO ddmmyy (merge + memo)")
    print("5 - Resolver MOCHILA (informar orçamento de horas)")
    print("6 - Mostrar ÚLTIMO RELATÓRIO")
    print("7 - Salvar RELATÓRIO em CSV (relatorio_capacitacao.csv)")
    print("8 - Salvar BASE COMPLETA em CSV (modulos_base.csv)")
    print("0 - Sair")

    op = input("Escolha: ")

    if op == "1":
        nome = input("Nome do módulo: ")
        dur_txt = input("Duração (horas, inteiro >= 0): ")
        gan_txt = input("Ganho (pontos, inteiro >= 0): ")
        prazo = input("Prazo (ddmmyy): ")

        if not eh_inteiro_nao_negativo(dur_txt) or not eh_inteiro_nao_negativo(gan_txt):
            print("Valores inválidos (use inteiros não negativos).")
            continue

        if not eh_data_ddmmyy(prazo):
            print("Prazo inválido. Use ddmmyy real (ex.: 151225).")
            continue

        novo = {"id": proximo_id, "nome": nome, "duracao": int(dur_txt),
                "ganho": int(gan_txt), "prazo": prazo}
        modulos.append(novo)
        proximo_id += 1
        print("OK: módulo cadastrado.")

    elif op == "2":
        if len(modulos) == 0:
            print("Sem módulos.")
        else:
            mostrar_lista(modulos)

    elif op == "3":
        print("\n--- Módulos por GANHO (crescente) ---")
        ordenada = merge_sort_por_campo(modulos, "ganho")
        mostrar_lista(ordenada)

    elif op == "4":
        print("\n--- Módulos por PRAZO (crescente, ddmmyy) ---")
        ordenada = merge_sort_por_campo(modulos, "prazo")
        mostrar_lista(ordenada)

    elif op == "5":
        t_txt = input("Orçamento de horas (inteiro >= 0): ")
        if not eh_inteiro_nao_negativo(t_txt):
            print("Inválido.")
            continue
        T = int(t_txt)

        ganho_total, ids = mochila_otima(modulos, T)
        ultimo_relatorio = gerar_relatorio(modulos, T, ganho_total, ids)

    elif op == "6":
        if ultimo_relatorio is None:
            print("Ainda não foi gerado relatório.")
        else:
            print("\n=== ÚLTIMO RELATÓRIO (resumo) ===")
            print("Orçamento:", ultimo_relatorio["t_total"], "h")
            print("Horas usadas:", ultimo_relatorio["horas_usadas"], "h")
            print("Ganho total:", ultimo_relatorio["ganho_total"])
            print("Módulos escolhidos (por prazo):")
            if len(ultimo_relatorio["lista"]) == 0:
                print("Nenhum.")
            else:
                mostrar_lista(ultimo_relatorio["lista"])

    elif op == "7":
        if ultimo_relatorio is None:
            print("Gere o relatório primeiro (opção 5).")
        else:
            exportar_relatorio_csv("relatorio_capacitacao.csv", ultimo_relatorio)
            print('OK: arquivo "relatorio_capacitacao.csv" gerado na pasta do programa.')

    elif op == "8":
        salvar_lista_em_csv("modulos_base.csv", modulos)
        print('OK: arquivo "modulos_base.csv" gerado na pasta do programa.')

    elif op == "0":
        print("Encerrando. Obrigado!")
        break

    else:
        print("Opção inválida. Tente novamente.")
