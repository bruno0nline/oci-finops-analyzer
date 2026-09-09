# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Corrigido
- Janela de Monitoring ajustada por requisição e retentativa, com margem de retenção; suporte a 1–90 dias e resolução automática.
- Métricas ausentes classificadas como dados insuficientes; picos têm precedência sobre redução e P95 usa interpolação.
- Coleta parcial preserva CSV por instância e informa falhas em Excel, Word e JSON.

### Adicionado
- Pergunta interativa de período e geração automática de Word no coletor principal, com opções `--days` e `--outdir`.
- Testes offline de limites, retentativas e geração integrada de relatórios completos, parciais e vazios.

### Planejado
- Dashboard web interativo
- Suporte para análise de Block Volumes
- API REST para integração
- Testes automatizados
- Suporte para múltiplas tenancies simultâneas

## [1.0.0] - 2026-02-11

### Adicionado
- README profissional com badges e estrutura completa
- CONTRIBUTING.md com guia de contribuição
- INSTALLATION.md com instruções detalhadas
- CHANGELOG.md para rastreamento de versões
- Documentação melhorada em docs/

### Melhorado
- Estrutura do projeto mais organizada
- Exemplos de saída atualizados
- Badges do GitHub mais informativos

## [0.9.0] - 2026-01-XX

### Adicionado
- Análise de CPU e Memória multi-região
- Geração de relatórios em CSV, XLSX e DOCX
- Cálculo de economia em BRL
- Recomendações automáticas de FinOps
- Suporte para instâncias burstable
- Análise de percentil 95 (P95)
- Script de execução auxiliar
- Exemplos de relatórios

### Funcionalidades
- `oci_metrics_cpu_mem_media_ndays.py` - Análise histórica completa
- `oci_metrics_cpu_mem_realtime.py` - Análise em tempo real
- `oci_metrics_cpu_mem_word_report.py` - Relatório executivo
- `oci_finops_cpu_mem_collect.py` - Coleta de métricas
- `oci_burstable_report.py` - Análise de burstable
- `inventarioStartStop.py` - Inventário Start/Stop
- `logs.py` - Análise de logs

---

## Tipos de Mudanças

- `Added` - Novas funcionalidades
- `Changed` - Mudanças em funcionalidades existentes
- `Deprecated` - Funcionalidades que serão removidas
- `Removed` - Funcionalidades removidas
- `Fixed` - Correções de bugs
- `Security` - Correções de vulnerabilidades

---

[Unreleased]: https://github.com/bruno0nline/OCI_FinOps_Analyzer/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/bruno0nline/OCI_FinOps_Analyzer/releases/tag/v1.0.0
