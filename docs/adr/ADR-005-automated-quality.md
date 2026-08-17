# ADR-005 — Qualidade automatizada

**Data:** 17/08/2026  
**Marco:** Milestone 0 — Project Foundation  
**Autor:** Vagner Ferreira  
**Projeto:** Playcatch  
**Status:** Decisão já tomada

# ADR-005 — Qualidade automatizada

**Status:** Decisão já tomada
**Data:** Milestone 0
**Contexto do projeto:** Playcatch

## Contexto

Como projeto de portfólio profissional, o Playcatch precisa manter um padrão mínimo de qualidade de código e confiabilidade ao longo de todas as milestones, mesmo sendo desenvolvido de forma incremental por diferentes assistentes de IA.

## Decisão

Foi adotado como baseline de qualidade:

- **Ruff** para lint e formatação de código, configurado em `pyproject.toml` (`target-version = "py312"`, `line-length = 88`, regras `E`/`F`, formatação com aspas duplas);
- **Pytest** para testes automatizados, com teste smoke inicial já validado;
- **GitHub Actions** como pipeline de CI, executando checkout, setup do Python 3.12.3, instalação de dependências, Ruff (lint e format) e Pytest a cada alteração.

A primeira execução do CI já foi concluída com sucesso.

## Consequências

- Garante um padrão mínimo de qualidade e consistência de código desde a Milestone 0, antes da implementação dos componentes funcionais.
- Cada nova milestone deve manter os testes e o lint passando no CI antes de ser considerada concluída.
- Adiciona uma pequena sobrecarga de manutenção (manter testes e lint atualizados), considerada aceitável dado o benefício de confiabilidade para um projeto de portfólio.