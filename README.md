# 📊 OCI FinOps Analyzer

> **Execução automática:** rode `bash scripts/run_finops.sh`. O script pergunta o período (1–90 dias) e gera CSV, Excel e Word automaticamente. Consulte o [guia atualizado](docs/EXECUCAO_AUTOMATICA.md) para resolução, falhas parciais e execução sem interação. O Word detalhado atual usa estimativas USD; a descrição BRL abaixo se refere ao gerador alternativo e está pendente de consolidação.

<div align="center">

![OCI FinOps Analyzer](https://img.shields.io/badge/OCI-FinOps_Analyzer-red?style=for-the-badge&logo=oracle)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![OCI](https://img.shields.io/badge/Cloud-Oracle_Cloud-F80000?logo=oracle&logoColor=white)](https://www.oracle.com/cloud/)
[![FinOps](https://img.shields.io/badge/Focus-FinOps-blueviolet)](https://www.finops.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Reports](https://img.shields.io/badge/Reports-CSV%20%7C%20XLSX%20%7C%20DOCX-success)

**Ferramenta para análise de CPU, Memória e Burstable Baseline em instâncias OCI Compute**

[Funcionalidades](#-funcionalidades) • [Instalação](#-instalação-rápida) • [Como Usar](#-como-usar) • [Exemplos](#-exemplos) • [Documentação](#-documentação)

</div>

---

## 🎯 Sobre o Projeto

Ferramenta **open-source**, simples e poderosa, para analisar o uso de **CPU**, **Memória** e **baseline expansível (burstable)** das instâncias OCI Compute e gerar recomendações automáticas de **FinOps** – incluindo **estimativa de economia/aumento de custo em real (BRL)**.

### 💡 Por que usar?

- ✅ Identifica instâncias subutilizadas ou sobrecarregadas
- ✅ Gera recomendações automáticas de rightsizing
- ✅ Calcula economia potencial em BRL
- ✅ Relatórios prontos para apresentação executiva
- ✅ Suporte a múltiplas regiões e compartments
- ✅ Análise de instâncias burstable

---

## ✨ Funcionalidades

### 🔍 Análise Completa
- Varredura automática de **todas as regiões** da tenancy
- Suporte a **todos os compartments** (raiz + filhos)
- Análise histórica dos últimos **N dias** (padrão: 30)

### 📈 Métricas Calculadas
- Média de CPU / Memória
- Percentil 95 (P95) de CPU / Memória
- Identificação de baseline burstable (12.5% e 50%)

### 🤖 Recomendações Automáticas FinOps
- 🟩 **KEEP** - Instância bem dimensionada
- 🟥 **DOWNSIZE** - Redução recomendada
- 🟥 **DOWNSIZE-STRONG** - Redução fortemente recomendada
- 🟥 **DOWNSIZE-MEM** - Redução por memória
- 🟨 **UPSCALE** - Aumento recomendado
- 🔁 **BURSTABLE-12.5** / **BURSTABLE-50** - Conversão para instância burstable

### 📤 Relatórios Gerados
- **CSV** - Dados detalhados para análise
- **Excel (.xlsx)** - Planilha com cores por recomendação
- **Word (.docx)** - Relatório executivo com:
  - Lista de recomendações detalhadas
  - Estimativa de economia/aumento em BRL/mês
  - Resumo financeiro consolidado
  - Gráficos e tabelas formatadas

> ⚠️ **Nota sobre Preços:** As estimativas financeiras são calculadas em **real (BRL)** usando uma matriz simplificada de preços por família de forma (E3/E4/E5/E6/A1/A2/X9), baseada na tabela pública da Oracle. Para clientes com contratos específicos, ajuste o dicionário `PRICE_MATRIX` no script `oci_metrics_cpu_mem_word_report.py`.

---

## 📁 Estrutura do Projeto

```
oci-finops-analyzer/
├── src/                                      # Código fonte
│   ├── oci_metrics_cpu_mem_media_ndays.py   # Script principal FinOps (CSV/XLSX)
│   ├── oci_metrics_cpu_mem_realtime.py      # Relatório rápido (30 min)
│   ├── oci_metrics_cpu_mem_word_report.py   # Relatório executivo DOCX com BRL
│   ├── oci_finops_cpu_mem_collect.py        # Coleta de métricas
│   ├── oci_cpu_mem_report.py                # Geração de relatórios
│   ├── oci_burstable_report.py              # Análise de instâncias burstable
│   ├── inventarioStartStop.py               # Inventário Start/Stop
│   └── logs.py                              # Análise de logs
├── docs/                                     # Documentação
│   ├── README_WIKI.md                       # Guia para Wiki corporativa
│   └── PRESENTACAO_GESTAO.md                # Estrutura para apresentação
├── examples/                                 # Exemplos de saída
│   ├── sample_output.csv
│   ├── sample_output.xlsx
│   ├── Relatorio_FinOps_CPU_MEM_30d.xlsx
│   └── Relatorio_FinOps_Downsizes_Strong_30d.docx
├── scripts/                                  # Scripts auxiliares
│   └── run_finops.sh                        # Script de execução
├── requirements.txt                          # Dependências Python
├── .gitignore
└── README.md
```

---

## 🚀 Instalação Rápida

### Pré-requisitos

- Python 3.9+
- OCI CLI configurado
- Acesso à tenancy OCI com permissões de leitura

### 1. Clonar o repositório

```bash
git clone https://github.com/bruno0nline/oci-finops-analyzer.git
cd oci-finops-analyzer
```

### 2. Criar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar OCI CLI (se ainda não configurado)

```bash
oci setup config
```

---

## 💻 Como Usar

### Análise Completa (30 dias)

```bash
# Definir período de análise
export METRICS_DAYS=30

# Executar análise principal
python3 src/oci_metrics_cpu_mem_media_ndays.py
```

**Saídas geradas:**
```
~/Relatorio_CPU_Memoria_media_30d_multi_region.csv
~/Relatorio_CPU_Memoria_media_30d_multi_region.xlsx
```

### Relatório Executivo em Word

```bash
python3 src/oci_metrics_cpu_mem_word_report.py
```

**Saída:**
```
~/Relatorio_FinOps_CPU_Mem_30d_multi_region.docx
```

### Análise em Tempo Real (30 minutos)

```bash
python3 src/oci_metrics_cpu_mem_realtime.py
```

### Usando o Script Auxiliar

```bash
bash scripts/run_finops.sh
```

---

## 📊 Exemplos

### Exemplo de Recomendações

| Instância | CPU Média | Mem Média | P95 CPU | P95 Mem | Burstable | Recomendação      | Economia (BRL/mês) |
|-----------|-----------|-----------|---------|---------|-----------|-------------------|--------------------|
| vm-app01  | 9%        | 22%       | 15%     | 28%     | NO        | 🟥 DOWNSIZE       | R$ 450,00          |
| vm-db02   | 65%       | 88%       | 82%     | 95%     | NO        | 🟨 UPSCALE        | -R$ 300,00         |
| vm-web03  | 43%       | 31%       | 58%     | 45%     | NO        | 🟩 KEEP           | R$ 0,00            |
| vm-scan   | 4%        | 18%       | 8%      | 22%     | NO        | 🔁 BURSTABLE-12.5 | R$ 600,00          |

### Resumo Financeiro Consolidado

```
💰 Economia Total com Downsizing:    R$ 12.450,00/mês
💸 Custo com Upscale:                -R$ 2.300,00/mês
🔄 Economia com Burstable:           R$ 3.800,00/mês
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ECONOMIA LÍQUIDA POTENCIAL:       R$ 13.950,00/mês
                                     R$ 167.400,00/ano
```

---

## 🔧 Scripts Disponíveis

| Script | Descrição | Saída |
|--------|-----------|-------|
| `oci_metrics_cpu_mem_media_ndays.py` | Análise histórica completa | CSV + XLSX |
| `oci_metrics_cpu_mem_realtime.py` | Análise rápida (30 min) | Console |
| `oci_metrics_cpu_mem_word_report.py` | Relatório executivo | DOCX |
| `oci_finops_cpu_mem_collect.py` | Coleta de métricas | Dados brutos |
| `oci_burstable_report.py` | Análise de burstable | Relatório |
| `inventarioStartStop.py` | Inventário Start/Stop | XLSX |
| `logs.py` | Análise de logs OCI | XLSX |

---

## 📚 Documentação

### Configuração Avançada

Para ajustar os limites de recomendação, edite as constantes no script principal:

```python
# Limites para recomendações
CPU_DOWNSIZE_THRESHOLD = 30  # CPU média < 30% = DOWNSIZE
CPU_UPSCALE_THRESHOLD = 70   # CPU média > 70% = UPSCALE
MEM_DOWNSIZE_THRESHOLD = 40  # Memória média < 40% = DOWNSIZE
MEM_UPSCALE_THRESHOLD = 80   # Memória média > 80% = UPSCALE
```

### Ajuste de Preços

Edite o dicionário `PRICE_MATRIX` em `oci_metrics_cpu_mem_word_report.py`:

```python
PRICE_MATRIX = {
    'E3': 0.05,  # Preço por OCPU/hora em BRL
    'E4': 0.06,
    'E5': 0.07,
    # ... adicione suas famílias
}
```

### Documentação Adicional

- [Wiki Corporativa](docs/README_WIKI.md) - Guia para documentação interna
- [Apresentação para Gestão](docs/PRESENTACAO_GESTAO.md) - Template de apresentação

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja como você pode ajudar:

1. 🍴 Fork o projeto
2. 🔨 Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. ✅ Commit suas mudanças (`git commit -m 'feat: adiciona MinhaFeature'`)
4. 📤 Push para a branch (`git push origin feature/MinhaFeature`)
5. 🎉 Abra um Pull Request

### Padrões de Commit

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `refactor:` Refatoração
- `test:` Testes

---

## 📝 Licença

Distribuído sob a licença **MIT**. Veja [LICENSE](LICENSE) para mais informações.

Você pode usar este código em ambientes pessoais ou corporativos.

---

## 👤 Autor

**Bruno Mendes Augusto**

- GitHub: [@bruno0nline](https://github.com/bruno0nline)
- Email: brunomendesaugusto@gmail.com

---

## 🙏 Agradecimentos

- Oracle Cloud Infrastructure pela plataforma
- Comunidade FinOps pela inspiração
- Todos os contribuidores do projeto

---

## 📞 Suporte

Encontrou um bug ou tem uma sugestão?

- 🐛 [Abra uma Issue](https://github.com/bruno0nline/OCI_FinOps_Analyzer/issues)
- 💬 [Discussões](https://github.com/bruno0nline/OCI_FinOps_Analyzer/discussions)

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Made with ❤️ by [Bruno Mendes Augusto](https://github.com/bruno0nline)

</div>
