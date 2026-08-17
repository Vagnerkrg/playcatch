# ADR-002 — Recomendação baseada em sentimento

**Data:** 17/08/2026  
**Marco:** Milestone 0 — Project Foundation  
**Autor:** Vagner Ferreira  
**Projeto:** Playcatch  
**Status:** Decisão planejada — a ser implementada na Milestone 2

# ADR-002 — Recomendação baseada em sentimento

**Status:** Decisão planejada (a ser implementada na Milestone 2)
**Data:** Milestone 0
**Contexto do projeto:** Playcatch

## Contexto

O núcleo funcional do Playcatch é recomendar músicas de acordo com o estado emocional do usuário, a partir do dataset de sentimentos gerado na Milestone 1. Existem várias abordagens possíveis para essa recomendação, desde filtros simples por categoria até técnicas de recomendação mais sofisticadas (ex.: similaridade vetorial, collaborative filtering, embeddings).

## Decisão

A recomendação inicial será **simples, baseada em categorias de sentimento**: dado um sentimento/preferência informado pelo usuário, o sistema filtra músicas compatíveis no dataset estruturado e aplica um mecanismo básico de feedback (`gostei` / `pulei`) para ajustar recomendações futuras. Técnicas de ML mais complexas serão evitadas nesta fase, salvo necessidade real identificada durante o desenvolvimento.

## Alternativas ainda abertas

- Uso de similaridade vetorial/embeddings para recomendação — não descartado para uma evolução futura, mas fora do escopo inicial.
- Estratégias mais elaboradas de ajuste de recomendação a partir do feedback (ex.: ponderação por histórico) — a ser avaliado conforme o projeto evolui.

## Consequências

- Implementação mais simples e rápida de validar dentro do escopo do checkpoint.
- Menor custo computacional e de manutenção.
- Recomendações inicialmente menos refinadas do que abordagens baseadas em ML mais complexo, o que é aceitável para o escopo atual do projeto.