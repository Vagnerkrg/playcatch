# ADR-001 — Arquitetura incremental

**Data:** 17/08/2026  
**Marco:** Milestone 0 — Project Foundation  
**Autor:** Vagner Ferreira  
**Projeto:** Playcatch  
**Status:** Decisão já tomada


# ADR-001 — Arquitetura incremental

**Status:** Decisão já tomada
**Data:** Milestone 0
**Contexto do projeto:** Playcatch

## Contexto

O Playcatch envolve múltiplos componentes de IA (análise de sentimento, recomendação, chatbot) e uma interface de usuário, integrados em um único fluxo ponta a ponta. Construir todos os componentes simultaneamente aumentaria o risco de retrabalho e dificultaria a validação isolada de cada parte.

## Decisão

O sistema será construído de forma **incremental**, seguindo um roadmap de 6 milestones (M0 a M5). Cada componente — dados/análise de sentimento, recomendação, chatbot — será desenvolvido e testado isoladamente antes de ser integrado aos demais na Milestone 4.

## Consequências

- Cada milestone tem um entregável testável e independente, reduzindo risco de integração.
- A integração completa (Milestone 4) só ocorre depois que cada componente já foi validado isoladamente.
- Como contrapartida, algumas decisões de interface entre componentes (ex.: formato exato de entrada/saída entre recomendação e chatbot) podem precisar de pequenos ajustes no momento da integração.