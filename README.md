# GLOBAL SOLUTION – Futuro do Trabalho (Dynamic Programming)

> **Turma:** 2ESPI  
> **Integrantes:**  
> - Guilherme da Cunha Melo – 555310  
> - Paulo Akira Okama – 556840  
> - Rafael Bocchi – 557603  

---

## 1. Visão Geral do Projeto

Este projeto implementa, em **Python puro**, uma solução de **Programação Dinâmica (problema da Mochila 0/1)** aplicada a um cenário de **capacitação para o futuro do trabalho**.

A ideia é ajudar uma pessoa (ou empresa) a montar um **plano ótimo de cursos/treinamentos**, escolhendo, dentre vários **módulos de capacitação**:

- Quais módulos **valem mais a pena fazer** dentro de um **orçamento de horas** disponível;
- **Maximizando o ganho total** (em pontos) desses módulos;
- Respeitando o limite de **tempo** (horas) que o profissional pode investir.

Além da escolha ótima de módulos, o programa também:

- Permite **cadastrar novos módulos de capacitação**;
- **Lista** todos os módulos cadastrados;
- Ordena módulos por **ganho** ou por **prazo** usando **Merge Sort com memoização**;
- Resolve a **Mochila 0/1 com recursão + memoização (Programação Dinâmica)**;
- Gera **relatórios em console**;
- Exporta dados em **CSV** para análise em planilhas (por exemplo, Excel).

> 🔹 Não foram usadas classes nem bibliotecas externas.  
> 🔹 Todo o código utiliza apenas estruturas ensinadas em aula: listas, dicionários, funções, laços, condicionais e recursão.

---

## 2. Formulação do Problema (Mochila 0/1)

### 2.1. Entradas do Problema

O programa trabalha com:

- Uma **lista de módulos de capacitação**, onde cada módulo é um dicionário com:
  - `id` – identificador numérico único (`int`);
  - `nome` – nome do módulo (`str`);
  - `duracao` – carga horária do módulo em horas (`int >= 0`);
  - `ganho` – pontuação/valor daquele módulo para o futuro do trabalho (`int >= 0`);
  - `prazo` – limite de prazo no formato `ddmmyy` (string com 6 dígitos, ex.: `151225`).

- Um **orçamento total de horas `T`** (inteiro ≥ 0), informado pelo usuário na opção de resolver a mochila.

### 2.2. Saídas do Problema

A solução gerada pelo programa inclui:

- **Conjunto de módulos selecionados**, tal que:
  - A **soma das durações** seja ≤ `T`;
  - O **ganho total** (soma dos `ganho`) seja **maximizado**.

- Exibição em console:
  - Orçamento de horas (`T`);
  - Horas efetivamente utilizadas;
  - Ganho total obtido;
  - Lista de módulos selecionados **ordenados por prazo** (`ddmmyy`).

- Exportação para arquivos CSV:
  - `relatorio_capacitacao.csv` → resumo do plano ótimo + módulos selecionados;
  - `modulos_base.csv` → lista completa de todos os módulos cadastrados.

### 2.3. Objetivo de Otimização

O problema é equivalente à **Mochila 0/1**, com a seguinte formulação:

- **Objetivo:** maximizar  
  \[
  \sum ganho(módulo_i)
  \]

- **Sujeito a:**  
  \[
  \sum duracao(módulo_i) \le T
  \]

- Cada módulo pode ser:
  - **Selecionado (1)**;
  - **Não selecionado (0)**;
  - Nunca fracionado.

> ✅ O programa **não obriga** a usar exatamente `T` horas. Às vezes, a melhor solução usa menos horas com ganho maior.

---

## 3. Estrutura Geral do Código

O projeto consiste em um único arquivo Python (`GS-Dynamic-Programming.py`) com as seguintes partes principais:

- **Funções utilitárias**:
  - Validação de números inteiros não negativos;
  - Validação de datas `ddmmyy`;
  - Clonagem de listas;
  - Impressão de módulos.

- **Base de dados**:
  - Lista inicial de **módulos de capacitação** (pelo menos 20 módulos);
  - Controle de `proximo_id` para novos cadastros.

- **Algoritmo de ordenação**:
  - `merge_sort_por_campo` → **Merge Sort recursivo com memoização**, ordenando por `ganho` ou `prazo`.

- **Algoritmo de Programação Dinâmica (Mochila)**:
  - `mochila_otima` → resolve a **Mochila 0/1** via recursão + memoização, retornando ganho máximo e IDs escolhidos.

- **Relatórios e exportação**:
  - `gerar_relatorio` → monta e imprime o relatório em console;
  - `salvar_lista_em_csv` → exporta listas em CSV;
  - `exportar_relatorio_csv` → exporta o último relatório em formato CSV.

- **Menu interativo (loop principal)**:
  - Opções para cadastrar, listar, ordenar, resolver a mochila e exportar resultados.

---

## 4. Estruturas de Dados Principais

### 4.1. Lista de Módulos (`modulos`)

```python
modulos = [
    {"id": 1,  "nome": "Python p/ Dados",       "duracao": 6, "ganho": 12, "prazo": "151225"},
    {"id": 2,  "nome": "Fund. UX/UI",           "duracao": 4, "ganho": 7,  "prazo": "101225"},
    # ...
    {"id": 20, "nome": "Docker Básico",         "duracao": 5, "ganho": 9,  "prazo": "210226"},
]
proximo_id = 21
```

- **Tipo:** lista de dicionários (`list[dict]`);
- Cada dicionário representa **um módulo/capacitação**;
- `proximo_id` guarda o **id a ser atribuído** ao próximo módulo cadastrado via menu.

### 4.2. Estrutura de Relatório (`ultimo_relatorio`)

```python
ultimo_relatorio = None
```

Após resolver a mochila, o programa guarda o resultado em um dicionário com a seguinte estrutura:

```python
info = {
    "t_total": t_total,           # orçamento de horas informado pelo usuário
    "horas_usadas": horas,        # horas realmente utilizadas
    "ganho_total": ganho,         # ganho total máximo encontrado
    "ids": [...],                 # lista de IDs dos módulos escolhidos
    "lista": [...],               # lista de dicionários dos módulos escolhidos, ordenados por prazo
}
```

Esse dicionário é armazenado em `ultimo_relatorio` para:

- Ser reexibido em console (opção 6 do menu);
- Ser exportado em CSV (opção 7 do menu).

---

## 5. Explicação Função por Função (Estrutura por Estrutura)

A seguir, cada função e estrutura desenvolvida no projeto é explicada em detalhes, conforme solicitado pelo professor.

---

### 5.1. `eh_inteiro_nao_negativo(txt)`

```python
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
```

**Função:** `eh_inteiro_nao_negativo`  
**Objetivo:** verificar se uma **string** contém apenas dígitos (`0` a `9`) e, portanto, representa um **inteiro não negativo**.

**Como funciona:**

1. Se a string estiver vazia, retorna `False`.
2. Percorre caractere por caractere com um `while`:
   - Se encontrar algo que não seja dígito (`'0'` a `'9'`), retorna `False`.
3. Se passar por todos os caracteres sem erro, retorna `True`.

**Uso no programa:**

- Validação de:
  - `duracao` ao cadastrar um módulo;
  - `ganho` ao cadastrar um módulo;
  - Orçamento de horas (`T`) informado para resolver a mochila.

> 🔸 Evita que o programa tente fazer `int()` em valores inválidos, prevenindo erros em tempo de execução.

---

### 5.2. `eh_data_ddmmyy(txt)`

```python
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
```

**Função:** `eh_data_ddmmyy`  
**Objetivo:** validar se uma string representa uma **data válida no formato `ddmmyy`**.

**Validações realizadas:**

- Tamanho exato = 6 caracteres;
- Todos os caracteres são dígitos;
- Mês entre 1 e 12;
- Dia ≥ 1;
- Dias máximos por mês (31, 30 ou fevereiro);
- Fevereiro considera anos bissextos (`ano % 4 == 0`).

**Uso no programa:**

- Validação do campo `prazo` ao cadastrar novos módulos.

> 🔸 Garante que os prazos utilizados para ordenação e relatórios sejam coerentes e válidos.

---

### 5.3. `clonar_lista(lst)`

```python
def clonar_lista(lst):
    copia = []
    i = 0
    while i < len(lst):
        copia.append(lst[i])
        i += 1
    return copia
```

**Função:** `clonar_lista`  
**Objetivo:** criar uma **cópia independente** de uma lista.

**Por que é importante:**

- Evita que listas retornadas pela Programação Dinâmica sejam alteradas sem querer em outros pontos do código.
- Garante que `ids` e listas de módulos usados em relatórios sejam estáveis.

**Uso no programa:**

- Dentro de `mochila_otima`:
  - Clona a lista de IDs antes de adicionar o ID atual.
- Dentro de `gerar_relatorio`:
  - Clona `ids` e `lista` antes de guardar na estrutura `info`.

---

### 5.4. `data_leq_ddmmyy(a, b)`

```python
def data_leq_ddmmyy(a, b):
    da = int(a[0:2]); ma = int(a[2:4]); aa = int(a[4:6])
    db = int(b[0:2]); mb = int(b[2:4]); ab = int(b[4:6])
    if aa != ab: return aa < ab
    if ma != mb: return ma < mb
    return da <= db
```

**Função:** `data_leq_ddmmyy`  
**Objetivo:** comparar duas datas `a` e `b` no formato `ddmmyy` e retornar se **`a` é menor ou igual a `b`**.

**Lógica de comparação:**

1. Converte dia, mês e ano para inteiros;
2. Compara ano → mês → dia, nessa ordem;
3. Retorna `True` se `a` é **antes ou igual** a `b`.

**Uso no programa:**

- É utilizada dentro de `merge_sort_por_campo` quando o campo de ordenação é `"prazo"`.

---

### 5.5. `mostrar_um(m)` e `mostrar_lista(lst)`

```python
def mostrar_um(m):
    linha = "id=" + str(m["id"]) + ", nome=" + m["nome"]             + ", duracao=" + str(m["duracao"]) + "h"             + ", ganho=" + str(m["ganho"])             + ", prazo=" + m["prazo"]
    print(linha)

def mostrar_lista(lst):
    i = 0
    while i < len(lst):
        mostrar_um(lst[i])
        i += 1
```

**Funções:** `mostrar_um` e `mostrar_lista`  
**Objetivos:**

- `mostrar_um(m)`:
  - Imprimir um módulo em uma linha padronizada, com todos os campos: id, nome, duração, ganho e prazo.

- `mostrar_lista(lst)`:
  - Percorrer uma lista de módulos e chamar `mostrar_um` para cada elemento.

**Uso no programa:**

- Opção 2 do menu (listar todos os módulos);
- Após ordenar por ganho (opção 3);
- Após ordenar por prazo (opção 4);
- Exibição dos módulos selecionados no relatório;
- Exibição do último relatório (opção 6).

---

### 5.6. `merge_sort_por_campo(tabela, campo)`

```python
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
```

**Função:** `merge_sort_por_campo`  
**Objetivo:** ordenar uma lista de módulos (`tabela`) considerando um campo específico (`ganho` ou `prazo`), usando **Merge Sort recursivo com memoização**.

**Detalhes importantes:**

- Usa um dicionário `memo` para memorizar subintervalos já ordenados:
  - Chave: `(ini, fim, campo)`;
  - Valor: lista de módulos ordenados naquele intervalo.

- A função interna `merge_range(ini, fim)`:
  - Caso base: intervalo com 0 ou 1 elemento → retorna cópia simples;
  - Caso geral: divide o intervalo ao meio, ordena recursivamente as duas metades e faz o **merge**.

- Comparação:
  - Se `campo == "prazo"`, usa `data_leq_ddmmyy` para comparar datas;
  - Caso contrário (campo numérico, como `ganho`), usa comparação simples `<=`.

**Uso no programa:**

- Opção 3 do menu → ordenação por **ganho**;
- Opção 4 do menu → ordenação por **prazo**;
- Dentro de `gerar_relatorio` → ordenação dos módulos selecionados por `prazo`.

---

### 5.7. `mochila_otima(itens, t_total)`

```python
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
```

**Função:** `mochila_otima`  
**Objetivo:** resolver o problema da **Mochila 0/1** usando **recursão + memoização**.

**Parâmetros:**

- `itens`: lista de módulos (cada item com `duracao`, `ganho`, `id`, etc.);
- `t_total`: capacidade total de horas (orçamento máximo).

**Retorno:**

- Tupla `(ganho_maximo, lista_ids_escolhidos)`.

**Função interna:** `decide(i, t)`  
Significa:

- Considerando apenas os itens a partir do índice `i`;
- E tendo ainda `t` horas disponíveis;
- Qual o **ganho máximo** possível?
- Quais **IDs de módulos** preciso escolher?

**Casos base:**

- Quando `i == len(itens)` (sem itens restantes) ou `t == 0` (sem horas restantes):
  - Retorna `(0, [])`.

**Passos principais:**

1. **Opção 1 – Pular o item atual:**
   - Chama `decide(i + 1, t)` → obtém `ganho_pula` e `lista_pula`.

2. **Opção 2 – Pegar o item atual (se couber):**
   - Se `dur <= t`:
     - Chama `decide(i + 1, t - dur)` para o restante da capacidade;
     - Soma `gan` ao ganho obtido;
     - Clona a lista de IDs retornada e adiciona o `id` do item atual.
   - Caso contrário (`dur > t`), não é possível pegar o item → ganho da opção é definido como `-1`.

3. **Escolha da melhor opção:**
   - Compara `ganho_pega` e `ganho_pula`;
   - Guarda em `memo[(i, t)]` a opção com maior ganho.

4. **Memoização:**
   - Antes de computar `decide(i, t)`, verifica se `(i, t)` já existe em `memo`;
   - Se sim, reutiliza o resultado, otimizando o desempenho.

**Uso no programa:**

- Opção 5 do menu:
  - Ao informar o orçamento de horas, o programa chama `mochila_otima` para descobrir:
    - O **ganho total máximo**;
    - A **lista de IDs** dos módulos selecionados.

---

### 5.8. `gerar_relatorio(tabela, t_total, ganho, ids_escolhidos)`

```python
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

    print("
=== RELATÓRIO – PLANO DE CAPACITAÇÃO ===")
    print("Orçamento de horas:", t_total, "h")
    print("Horas usadas:", horas, "h")
    print("Ganho total:", ganho)
    print("
Módulos selecionados (ordenados por prazo):")
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
```

**Função:** `gerar_relatorio`  
**Objetivo:** montar o **relatório do plano ótimo de capacitação**, exibir em console e retornar uma estrutura organizada.

**Passos:**

1. Para cada `id` em `ids_escolhidos`:
   - Procura o módulo correspondente na `tabela`;
   - Adiciona o módulo na lista `escolhidos`;
   - Soma sua duração em `horas`.

2. Ordena `escolhidos` por `prazo` usando `merge_sort_por_campo`.

3. Exibe no console:
   - Orçamento total de horas (`t_total`);
   - Horas efetivamente usadas (`horas`);
   - Ganho total (`ganho`);
   - Lista de módulos selecionados (ou mensagem se estiver vazia).

4. Cria o dicionário `info` com:
   - `t_total`, `horas_usadas`, `ganho_total`;
   - Cópia da lista de IDs (campo `ids`);
   - Cópia da lista de módulos ordenados (campo `lista`).

5. Retorna `info`, que é armazenado em `ultimo_relatorio`.

---

### 5.9. `salvar_lista_em_csv(caminho, itens)`

```python
def salvar_lista_em_csv(caminho, itens):
    # Cabeçalho fixo: id;nome;duracao;ganho;prazo
    # Usamos ; como separador para abrir bem no Excel em PT-BR.
    arq = open(caminho, "w", encoding="utf-8")
    arq.write("id;nome;duracao;ganho;prazo
")
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
        linha = str(r["id"]) + ";" + nome_limpo + ";" + str(r["duracao"]) + ";" + str(r["ganho"]) + ";" + r["prazo"] + "
"
        arq.write(linha)
        i += 1
    arq.close()
```

**Função:** `salvar_lista_em_csv`  
**Objetivo:** exportar qualquer **lista de módulos** para um arquivo CSV.

**Características:**

- Usa `;` como separador, compatível com o padrão do Excel em PT-BR;
- Escreve cabeçalho fixo:
  - `id;nome;duracao;ganho;prazo`;
- Substitui `;` no nome do módulo por `,` para não quebrar a estrutura do CSV.

**Uso no programa:**

- Opção 8 do menu:
  - Exporta a **base completa** de módulos para `modulos_base.csv`.

---

### 5.10. `exportar_relatorio_csv(caminho, resumo)`

```python
def exportar_relatorio_csv(caminho, resumo):
    # CSV com o resumo + itens escolhidos (ordenados)
    arq = open(caminho, "w", encoding="utf-8")
    arq.write("Relatorio;Plano de Capacitação
")
    arq.write("Orcamento_horas;" + str(resumo["t_total"]) + "
")
    arq.write("Horas_usadas;" + str(resumo["horas_usadas"]) + "
")
    arq.write("Ganho_total;" + str(resumo["ganho_total"]) + "
")
    arq.write("
")
    arq.write("id;nome;duracao;ganho;prazo
")
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
        arq.write(str(r["id"]) + ";" + nome_limpo + ";" + str(r["duracao"]) + ";" + str(r["ganho"]) + ";" + r["prazo"] + "
")
        i += 1
    arq.close()
```

**Função:** `exportar_relatorio_csv`  
**Objetivo:** exportar o **último relatório gerado** (resumo + módulos escolhidos) em formato CSV para análise externa.

**Formato do arquivo:**

- Cabeçalho inicial com:
  - Nome do relatório;
  - Orçamento de horas;
  - Horas usadas;
  - Ganho total.
- Linha em branco;
- Tabela com:
  - `id;nome;duracao;ganho;prazo` dos módulos escolhidos.

**Uso no programa:**

- Opção 7 do menu:
  - Gera o arquivo `relatorio_capacitacao.csv`.

---

## 6. Menu Principal e Fluxo do Programa

O fluxo principal do programa é um loop `while True` que exibe um **menu interativo**:

```python
while True:
    print("
=== GLOBAL SOLUTION – Capacitação ótima (Mochila) ===")
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
    # ... tratamento de cada opção ...
```

### 6.1. Opção 1 – Cadastrar Módulo

- Lê do usuário:
  - `nome`;
  - `dur_txt` (duração em horas, texto);
  - `gan_txt` (ganho em pontos, texto);
  - `prazo` (data no formato `ddmmyy`).

- Valida:
  - `dur_txt` e `gan_txt` com `eh_inteiro_nao_negativo`;
  - `prazo` com `eh_data_ddmmyy`.

- Se houver erro de validação:
  - Mostra mensagem e **não cadastra** o módulo.

- Se estiver tudo correto:
  - Converte para inteiros (`duracao` e `ganho`);
  - Cria um dicionário com:
    - `id = proximo_id`;
    - `nome`, `duracao`, `ganho`, `prazo`;
  - Insere na lista `modulos`;
  - Incrementa `proximo_id`.

---

### 6.2. Opção 2 – Listar Módulos

- Usa `mostrar_lista(modulos)` para exibir todos os módulos cadastrados, com:
  - `id`, `nome`, `duracao`, `ganho`, `prazo`.

---

### 6.3. Opção 3 – Ordenar por GANHO (Merge Sort + Memoização)

- Chama:

  ```python
  ordenada = merge_sort_por_campo(modulos, "ganho")
  ```

- Exibe a lista ordenada por ganho (crescente) com `mostrar_lista(ordenada)`.

> 🔸 A lista original `modulos` não é modificada; é criada uma nova lista ordenada.

---

### 6.4. Opção 4 – Ordenar por PRAZO (Merge Sort + Memoização)

- Chama:

  ```python
  ordenada = merge_sort_por_campo(modulos, "prazo")
  ```

- Exibe os módulos ordenados por `prazo` (`ddmmyy`) usando `data_leq_ddmmyy` para comparação de datas.

---

### 6.5. Opção 5 – Resolver MOCHILA

Fluxo:

1. Lê o texto `t_txt` (orçamento de horas);
2. Valida com `eh_inteiro_nao_negativo`;
3. Converte para inteiro `T`;
4. Chama:

   ```python
   ganho_total, ids = mochila_otima(modulos, T)
   ultimo_relatorio = gerar_relatorio(modulos, T, ganho_total, ids)
   ```

5. A função `gerar_relatorio`:
   - Exibe o relatório completo no console;
   - Retorna um dicionário com todos os dados, armazenado em `ultimo_relatorio`.

---

### 6.6. Opção 6 – Mostrar ÚLTIMO RELATÓRIO

- Se `ultimo_relatorio` for `None`:
  - Informa que ainda não foi gerado relatório.
- Senão:
  - Reexibe:
    - Orçamento;
    - Horas usadas;
    - Ganho total;
    - Lista de módulos selecionados, usando `mostrar_lista`.

---

### 6.7. Opção 7 – Salvar RELATÓRIO em CSV

- Se `ultimo_relatorio` for `None`:
  - Pede para primeiro gerar o relatório (opção 5).
- Se existir:
  - Chama `exportar_relatorio_csv("relatorio_capacitacao.csv", ultimo_relatorio)`;
  - Informa o usuário que o arquivo foi salvo.

---

### 6.8. Opção 8 – Salvar BASE COMPLETA em CSV

- Chama:

  ```python
  salvar_lista_em_csv("modulos_base.csv", modulos)
  ```

- Gera um CSV com **todos os módulos** cadastrados (inicial + novos).

---

### 6.9. Opção 0 – Sair

- Exibe uma mensagem de encerramento (ex.: `"Encerrando. Obrigado!"`);
- Dá `break` no loop principal;
- Encerra o programa.

---

## 7. Como Executar o Programa

1. Certificar-se de que o **Python** está instalado na máquina;
2. Salvar o arquivo como, por exemplo, `GS-Dynamic-Programming.py`;
3. Abrir um terminal/Prompt de comando na pasta do arquivo;
4. Executar:

   ```bash
   python GS-Dynamic-Programming.py
   ```

5. Navegar pelo menu utilizando as opções de `0` a `8`.

---

## 8. Resumo Final das Funções e Estruturas Criadas

Para reforçar o atendimento ao requisito do professor (“**explicar cada função/estrutura criada**”), segue um resumo direto:

### 8.1. Estruturas de Dados

- **`modulos`** → lista de dicionários com os módulos de capacitação;
- **`proximo_id`** → inteiro que guarda o próximo ID a ser utilizado;
- **`ultimo_relatorio`** → dicionário com o resultado mais recente da mochila (ou `None` se ainda não houver relatório).

### 8.2. Funções Utilitárias

- **`eh_inteiro_nao_negativo(txt)`** → valida se uma string representa um inteiro não negativo;
- **`eh_data_ddmmyy(txt)`** → valida datas no formato `ddmmyy`;
- **`clonar_lista(lst)`** → retorna uma cópia independente de uma lista;
- **`data_leq_ddmmyy(a, b)`** → compara duas datas no formato `ddmmyy`;
- **`mostrar_um(m)`** → imprime um módulo formatado;
- **`mostrar_lista(lst)`** → imprime uma lista de módulos.

### 8.3. Algoritmos Principais

- **`merge_sort_por_campo(tabela, campo)`** → ordena módulos por um campo (`ganho` ou `prazo`) usando Merge Sort recursivo com memoização;
- **`mochila_otima(itens, t_total)`** → resolve o problema da Mochila 0/1 com Programação Dinâmica (recursão + memoização), retornando ganho máximo e lista de IDs.

### 8.4. Relatórios e Exportação

- **`gerar_relatorio(tabela, t_total, ganho, ids_escolhidos)`** → monta e exibe o relatório em console, calculando horas usadas, ordenando módulos por prazo e retornando um dicionário com todas as informações;
- **`salvar_lista_em_csv(caminho, itens)`** → exporta qualquer lista de módulos para CSV;
- **`exportar_relatorio_csv(caminho, resumo)`** → exporta o último relatório (resumo + módulos escolhidos) para CSV.

---
