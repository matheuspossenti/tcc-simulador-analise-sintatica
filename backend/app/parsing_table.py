# Importacoes
import pandas as pd


# Obtem a tabela de analise do site: https://smlweb.cpsc.ucalgary.ca/
def get_parsing_table(grammar, analysis_type):
    try:
        if analysis_type == "ll1":
            aux_type = "ll1-table"
        elif analysis_type == "slr1":
            aux_type = "lr0"
        else:
            aux_type = analysis_type

        url = f"https://smlweb.cpsc.ucalgary.ca/{aux_type}.php?grammar={grammar}"
        url = url.replace(" ", "%20")

        parsing_table = pd.read_html(url)
        
        # Verificar se há tabelas suficientes
        if len(parsing_table) == 0:
            return {"Erro": "Nenhuma tabela encontrada. Verifique a gramática."}
            
        if analysis_type == "lr0" or analysis_type == "lr1":
            if len(parsing_table) < 3:
                return {"Erro": "Tabela de análise não gerada corretamente. Verifique a gramática."}
            return parsing_table[2]
        elif analysis_type == "ll1":
            if len(parsing_table) < 2:
                return {"Erro": "Tabela de análise não gerada corretamente. Verifique a gramática."}
            return parsing_table[1]
        elif analysis_type == "slr1" or analysis_type == "lalr1":
            if len(parsing_table) < 4:
                return {"Erro": "Tabela de análise não gerada corretamente. Verifique a gramática."}
            return parsing_table[3]
        else:
            return {"Erro": "Tipo de análise não suportado."}
    except IndexError:
        return {"Erro": "Erro ao processar a tabela. A gramática pode estar incorreta ou não ser compatível com o tipo de análise."}
    except Exception as e:
        return {"Erro": f"Erro ao gerar tabela de análise: {str(e)}"}


# Converter tabela em dicionario
def get_parsing_dict(parsing_table):
    parsing_table = parsing_table.drop([0], axis=1)
    parsing_table.columns = parsing_table.iloc[0]
    parsing_table = parsing_table[1:]
    parsing_table = parsing_table.fillna(" ")

    return parsing_table.to_dict()


# Separar terminais e nao-terminais
def sep_terminals_nonterminals(grammar):
    terminals = []
    nonterminals = []

    grammar_array = grammar.split(".")
    grammar_array.pop()

    for line in grammar_array:
        aux = line.split("->")
        nonterminals.append(aux[0])
        aux1 = aux[1].split("|")
        for i in aux1:
            aux2 = i.split(" ")
            for j in aux2:
                terminals.append(j)

    for i in nonterminals:
        for j in terminals:
            if i == j:
                terminals.remove(i)

    return {"terminals": list(set(terminals)), "nonterminals": list(set(nonterminals))}


# Separar tabela de acoes e transicoes
def get_goto_action_tables(grammar, analysis_type):
    try:
        parsing_table = get_parsing_table(grammar, analysis_type)
        
        # Verificar se houve erro na obtenção da tabela
        if isinstance(parsing_table, dict) and "Erro" in parsing_table:
            raise Exception(parsing_table["Erro"])
            
        parsing_dict = get_parsing_dict(parsing_table)
        term_nterm = sep_terminals_nonterminals(grammar)

        action = {
            key: parsing_dict[key]
            for key in parsing_dict.keys() & term_nterm["terminals"]
        }
        
        # Verificar se '$' está presente
        if '$' not in parsing_dict:
            raise Exception("Símbolo '$' não encontrado na tabela. A gramática pode estar incorreta.")
            
        action["$"] = parsing_dict["$"]

        action = replace_dict(action, " ", "ERRO!")
        action = replace_dict(action, "acc", "ACEITO")
        action = replace_functions(action)
        action = replace_functions(action)

        goto = {
            key: parsing_dict[key]
            for key in parsing_dict.keys() & term_nterm["nonterminals"]
        }

        goto = replace_functions(goto)

        return {
            "terminals_nonterminals": term_nterm,
            "action_table": action,
            "goto_table": goto,
        }
    except Exception as e:
        # Propagar o erro para ser tratado na rota
        raise Exception(f"Erro na geração das tabelas: {str(e)}")


def replace_dict(dictionary, original, final):
    for key in dictionary.keys():
        for index, value in dictionary[key].items():
            if value == original:
                dictionary[key][index] = value.replace(original, final)

    return dictionary


def replace_functions(dictionary):
    for key in dictionary.keys():
        for index, value in dictionary[key].items():
            if value[0] == "r":
                dictionary[key][index] = value.replace(
                    value, f"REDUZIR[ {value[2:-1]} ]"
                )
            elif value[0] == "s":
                # print(value[1:])
                dictionary[key][index] = value.replace(
                    value, f"EMPILHAR[ {value[1:]} ]"
                )
    return dictionary


# open_site('https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/')
# print(get_parsing_table('SOMA->A|d.A->b.A->c.', 'slr1'))
# print(get_parsing_dict(get_parsing_table('SOMA->A|d.A->b.A->c.', 'slr1')))
# print(
#    get_goto_action_tables(
#        "E->E v T.E->T.T->T and F.T->F.F->parenteses_esq E parenteses_dir.F->id.",
#        "slr1",
#    )
# )
