import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { Steps } from "intro.js-react";
import Cookies from "js-cookie";

import { getAllData } from "../services/ParsingService";

import TableBottomUp from "../components/bottomUpAnalisys/TableBottomUp";
import Stack from "../components/bottomUpAnalisys/Stack";
import InputTape from "../components/bottomUpAnalisys/InputTape";
import CardStepByStep from "../components/bottomUpAnalisys/CardStepByStep";
import CardGrammar from "../components/bottomUpAnalisys/CardGrammar";
import LoadingCard from "../components/common/LoadingCard";
import ErrorDiagnostic from "../components/common/ErrorDiagnostic";

const BottomUpAnalisys = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const [stepCont, setStepCont] = useState(0);
  const [loading, setLoading] = useState(true);
  const [parsingTable, setParsingTable] = useState({});
  const [steps, setSteps] = useState([]);
  const [grammar, setGrammar] = useState([]);

  const stepsTutorial = [
    {
      element: "#inputTape",
      title: "Fita de entrada",
      intro:
        "Na fita de entrada está a sequência de tokens que está sendo analisada. Os tokens são colocados na fita de entrada na ordem em que aparecem na entrada.",
    },
    {
      element: "#stack",
      title: "Pilha",
      intro:
        "A pilha armazena símbolos da gramática intercalados com estados do analisador. O símbolo da base da pilha é o estado inicial do analisador.",
    },
    {
      element: "#actionTable",
      title: "Tabela de ações",
      intro:
        "A tabela de ações contém as ações que devem ser tomadas em cada estado do analisador. As ações podem ser: empilhar, reduzir, aceitar e erro.",
    },
    {
      element: "#gotoTable",
      title: "Tabela de transições",
      intro:
        "A tabela de transições contém as transições de estado com relação aos símbolos não terminais.",
    },
    {
      element: "#stepByStep",
      title: "Passo a passo",
      intro:
        "No passo a passo está descrito os passos de como foi feito a análise sintática.",
    },
    {
      element: "#accordionStep",
      title: "Descrição dos passos",
      intro:
        "Para ver mais detalhes sobre um passo da análise clique sobre ele.",
    },
    {
      element: "#stepButtons",
      title: "Botões de navegações",
      intro:
        "Esses botões são utilizados para navegar no passo a passo da análise sintática.",
    },
  ];

  useEffect(() => {
    console.log(
      "Gramatica: " +
        location.state["grammar"] +
        "==Tipo: " +
        location.state["parsingType"] +
        "==Fita: " +
        location.state["inputTape"]
    );
    getAllData(
      location.state["grammar"],
      location.state["inputTape"],
      location.state["parsingType"]
    )
      .then((response) => {
        if (response.data["ERROR_CODE"] == 0) {
          console.log(response.data);
          setLoading(false);
          setGrammar(response.data["grammar"]);
          setSteps(response.data["stepsParsing"]);
          setParsingTable(response.data["parsingTable"]);
        } else {
          navigate("/error", {
            state: {
              message: response.data["errorMessage"],
            },
          });
        }
      })
      .catch((error) => console.error(error));
  }, []);

  return (
    <div className="container">
      {loading ? (
        <div></div>
      ) : (
        <Steps
          enabled={Cookies.get("BottomUpViewed") == undefined ? true : false}
          steps={stepsTutorial}
          initialStep={0}
          onExit={BottomUpAnalisys}
        />
      )}
      {loading ? (
        <LoadingCard message={"Carregando dados para analise."} />
      ) : (
        <div className="row">
          <div className="col-md-6">
            <div className="row">
              <div className="col-md-9">
                <InputTape
                  inputTape={steps[0]["input"]}
                  pointer={steps[stepCont]["pointer"]}
                />
                <CardStepByStep
                  stepCont={stepCont}
                  setStepCont={setStepCont}
                  stepByStep={steps[stepCont]["stepByStep"]}
                  stepByStepDetailed={steps[stepCont]["stepByStepDetailed"]}
                  qtSteps={steps.length - 1}
                />
              </div>
              <div className="col-md-3">
                <Stack stack={steps[stepCont]["stack"]} />
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <TableBottomUp
              parsingTable={parsingTable}
              stepMarker={steps[stepCont]["stepMarker"]}
            />
            <CardGrammar grammar={grammar} />
          </div>
        </div>
      )}
      {steps && steps.length > 0 && steps[steps.length - 1].errorInfo && (
        <ErrorDiagnostic 
          errorInfo={steps[steps.length - 1].errorInfo} 
          input={location.state["inputTape"]}
        />
      )}
    </div>
  );
};

export default BottomUpAnalisys;
