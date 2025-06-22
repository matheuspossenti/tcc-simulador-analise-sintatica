# Importacoes
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Importar funcoes
from app import parsing_table
from app import parsing_algorithm
from app import utils

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:5173",
    "localhost:5173",
    "https://stunning-sunburst-01b3b4.netlify.app",
    "https://stunning-sunburst-01b3b4.netlify.app"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Testar API
@app.get("/")
async def home() -> dict:
    return {"boas-vindas": "Bem-vindo a API do SASC."}


# Testar API
@app.get("/test/")
async def read_root() -> dict:
    return {"message": "Testando api"}


"""
@app.get("/analyze/{grammar}/{input}/{analysis_type}")
async def get_table(input: str, grammar: str, analysis_type: str):
    new_grammar = utils.grammar_formatter(grammar)
    treated_grammar = utils.symbol_treat(grammar)

    goto_action_tables = parsing_table.get_goto_action_tables(
        treated_grammar, analysis_type
    )

    steps_parsing = parsing_algorithm.bottom_up_algorithm(
        utils.dict_treat(goto_action_tables["action_table"]),
        utils.dict_treat(goto_action_tables["goto_table"]),
        input,
    )

    return {
        "ERROR_CODE": 0,
        "parsingTable": goto_action_tables,
        "stepsParsing": steps_parsing,
        "grammar": new_grammar,
    }
"""


@app.get("/analyze/{analysis_type}/{grammar}/{input}")
async def get_table(input: str, grammar: str, analysis_type: str):
    try:
        valid_analysis_types = ["ll1", "slr1", "lr0", "lr1", "lalr1"]
        if analysis_type not in valid_analysis_types:
            return {
                "ERROR_CODE": 2,
                "errorMessage": f"Tipo de análise inválido. Tipos válidos: {', '.join(valid_analysis_types)}"
            }
        
        new_grammar = utils.grammar_formatter(grammar)
        
        try:
            goto_action_tables = parsing_table.get_goto_action_tables(
                grammar, analysis_type
            )
        except Exception as e:
            return {
                "ERROR_CODE": 3,
                "errorMessage": f"Erro ao gerar tabelas de análise: {str(e)}",
                "errorDetails": {
                    "errorType": "GRAMMAR_ERROR",
                    "grammar": grammar
                }
            }
        
        steps_parsing = parsing_algorithm.bottom_up_algorithm(
            goto_action_tables["action_table"],
            goto_action_tables["goto_table"],
            input,
        )
        
        has_error = False
        error_info = None
        
        if steps_parsing and len(steps_parsing) > 0:
            last_step = steps_parsing[-1]
            if "errorInfo" in last_step and last_step["errorInfo"]:
                has_error = True
                error_info = last_step["errorInfo"]
        
        if has_error:
            return {
                "ERROR_CODE": 4,
                "errorMessage": error_info["message"],
                "errorDetails": error_info,
                "stepsParsing": steps_parsing,
                "grammar": new_grammar,
                "parsingTable": goto_action_tables
            }
        
        return {
            "ERROR_CODE": 0,
            "parsingTable": goto_action_tables,
            "stepsParsing": steps_parsing,
            "grammar": new_grammar,
        }

    except Exception as e:
        return {
            "ERROR_CODE": 1,
            "errorMessage": f"Houve um erro inesperado! {str(e)}",
            "errorDetails": {
                "errorType": "UNEXPECTED_ERROR",
                "exception": str(e)
            }
        }
