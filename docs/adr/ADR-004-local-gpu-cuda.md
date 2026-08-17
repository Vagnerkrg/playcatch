# ADR-004 — GPU/CUDA local

**Data:** 17/08/2026  
**Marco:** Milestone 0 — Project Foundation  
**Autor:** Vagner Ferreira  
**Projeto:** Playcatch  
**Status:** Decisão já tomada

# ADR-004 — GPU/CUDA local

**Status:** Decisão já tomada
**Data:** Milestone 0
**Contexto do projeto:** Playcatch

## Contexto

Os modelos de análise de sentimento (Milestone 1) e, possivelmente, componentes do chatbot (Milestone 3) dependem de modelos do Hugging Face que podem se beneficiar de aceleração por GPU. O ambiente de desenvolvimento conta com uma GPU NVIDIA GeForce RTX 4060 disponível localmente.

## Decisão

O projeto utilizará **PyTorch com suporte a CUDA** para aproveitar a GPU RTX 4060 disponível durante o processamento dos modelos de sentimento e, se aplicável, do chatbot. A disponibilidade de CUDA já foi validada no ambiente (`CUDA disponível: True`, PyTorch 2.12.0+cu132, CUDA 13.2).

## Consequências

- Processamento de modelos mais rápido durante desenvolvimento e testes locais.
- O projeto passa a depender de uma GPU compatível com CUDA para obter esse ganho de performance; em ambientes sem GPU, o código deve continuar funcional em CPU (ainda que mais lento), sem que a GPU seja um requisito obrigatório de execução.