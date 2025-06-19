import React from "react";
import { Link } from "react-router-dom";

const ErrorDiagnostic = ({ errorInfo, input }) => {
  if (!errorInfo) return null;

  const renderErrorDetails = () => {
    switch (errorInfo.errorType) {
      case "LEXICAL_ERROR":
        return (
          <>
            <h5>Erro Léxico</h5>
            <p>
              O token <code>'{errorInfo.found}'</code> na posição {errorInfo.position + 1} não é reconhecido pela gramática.
            </p>
            {errorInfo.expected && errorInfo.expected.length > 0 && (
              <p>
                Tokens esperados: <code>{errorInfo.expected.slice(0, 5).join("', '")}{errorInfo.expected.length > 5 ? "..." : ""}</code>
              </p>
            )}
            <p className="text-muted">
              Erros léxicos ocorrem quando um token não pertence ao vocabulário da linguagem.
            </p>
          </>
        );
      
      case "SYNTAX_ERROR":
        return (
          <>
            <h5>Erro Sintático</h5>
            <p>
              Token inesperado <code>'{errorInfo.found}'</code> na posição {errorInfo.position + 1}.
            </p>
            {errorInfo.expected && errorInfo.expected.length > 0 && (
              <p>
                Tokens esperados: <code>{errorInfo.expected.join("', '")}</code>
              </p>
            )}
            <p>
              Estado atual: <code>{errorInfo.state}</code>
            </p>
            <p className="text-muted">
              Erros sintáticos ocorrem quando a estrutura da entrada não segue as regras da gramática.
            </p>
          </>
        );
      
      case "LOOP_LIMIT":
        return (
          <>
            <h5>Limite de Iterações Excedido</h5>
            <p>
              A análise foi interrompida após muitas iterações, indicando um possível loop infinito.
            </p>
            <p className="text-muted">
              Isso geralmente ocorre quando há problemas na definição da gramática ou quando a entrada é muito complexa.
            </p>
          </>
        );
      
      case "TABLE_ACCESS_ERROR":
        return (
          <>
            <h5>Erro na Tabela de Análise</h5>
            <p>
              Não foi possível encontrar uma ação para o estado e símbolo atual.
            </p>
            <p className="text-muted">
              Isso pode indicar um problema na geração da tabela de análise ou uma incompatibilidade entre a gramática e o tipo de análise escolhido.
            </p>
          </>
        );
      
      default:
        return (
          <>
            <h5>Erro Desconhecido</h5>
            <p>{errorInfo.message || "Ocorreu um erro durante a análise."}</p>
          </>
        );
    }
  };

  const highlightError = () => {
    if (!input || !errorInfo.position) return null;
    
    const tokens = input.split(" ");
    return (
      <div className="error-highlight mt-3">
        <h6>Visualização do erro:</h6>
        <div className="d-flex flex-wrap">
          {tokens.map((token, index) => (
            <span 
              key={index} 
              className={`tape-element m-1 p-2 ${index === errorInfo.position ? 'bg-danger text-white' : ''}`}
            >
              {token}
            </span>
          ))}
        </div>
        {errorInfo.position < tokens.length && (
          <div className="mt-2">
            <span className="text-danger">↑</span>
            <span className="ms-2">Erro encontrado aqui</span>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="card border-danger mb-4">
      <div className="card-header bg-danger text-white">
        Diagnóstico de Erro
      </div>
      <div className="card-body">
        {renderErrorDetails()}
        {highlightError()}
        
        <div className="mt-3">
          <h6>Sugestões:</h6>
          <ul>
            <li>Verifique se a gramática está corretamente definida</li>
            <li>Certifique-se de que a entrada segue as regras da gramática</li>
            <li>Tente um tipo diferente de análise (LL(1), SLR(1), etc.)</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ErrorDiagnostic;