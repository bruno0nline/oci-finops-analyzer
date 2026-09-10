> **Atualiza??o 10/09/2026:** o fluxo principal consulta somente S?o Paulo e Vinhedo por padr?o. Dimensionamento por P95 com margem, cobertura m?nima de 90% e propostas ?nicas no CSV/Excel/Word. Valores financeiros ainda s?o cen?rios ilustrativos USD. Consulte as regras e o comando de valida??o em [Execu??o autom?tica](docs/EXECUCAO_AUTOMATICA.md#corre??es-de-dimensionamento--10092026); exemplos antigos abaixo n?o representam todas as regras atuais.

# 🚀 Guia de Início Rápido

> **Fluxo atualizado:** após clonar o projeto e entrar na pasta, execute apenas `bash scripts/run_finops.sh`. Responda quantos dias deseja (1–90); CSV, Excel e Word são gerados automaticamente. Não é necessário executar o gerador Word separadamente. Veja [execução automática](docs/EXECUCAO_AUTOMATICA.md).

**Comece a otimizar seus custos OCI em 5 minutos!**

---

## ⚡ Início Rápido (Cloud Shell OCI)

```bash
# 1. Clone o repositório
git clone https://github.com/bruno0nline/oci-finops-analyzer.git
cd oci-finops-analyzer

# 2. Configure o ambiente
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Execute a análise
export METRICS_DAYS=30
python3 src/oci_metrics_cpu_mem_media_ndays.py

# 4. Gere o relatório executivo
python3 src/oci_metrics_cpu_mem_word_report.py
```

**Pronto!** Seus relatórios estão em `~/`

---

## 📊 Seus Relatórios

Após a execução, você terá:

```
~/Relatorio_CPU_Memoria_media_30d_multi_region.csv   # Dados detalhados
~/Relatorio_CPU_Memoria_media_30d_multi_region.xlsx  # Planilha colorida
~/Relatorio_FinOps_CPU_Mem_30d_multi_region.docx     # Relatório executivo
```

---

## 🎯 Próximos Passos

### 1. Revise o Relatório Excel

Abra o arquivo `.xlsx` e procure por:
- 🟥 Linhas vermelhas = **DOWNSIZE** (economia imediata)
- 🟨 Linhas amarelas = **UPSCALE** (atenção necessária)
- 🔁 Linhas azuis = **BURSTABLE** (grande economia)

### 2. Priorize Ações

**Alta Prioridade:**
- DOWNSIZE-STRONG (economia > 50%)
- BURSTABLE (economia > 40%)

**Média Prioridade:**
- DOWNSIZE (economia 30-50%)

**Baixa Prioridade:**
- UPSCALE (investimento necessário)

### 3. Implemente Mudanças

```bash
# Exemplo: Redimensionar instância
oci compute instance update \
  --instance-id <instance-ocid> \
  --shape <new-shape>
```

### 4. Monitore Resultados

Aguarde 7 dias e execute novamente:

```bash
export METRICS_DAYS=7
python3 src/oci_metrics_cpu_mem_media_ndays.py
```

---

## 📖 Documentação Completa

- [README.md](README.md) - Visão geral completa
- [INSTALLATION.md](INSTALLATION.md) - Instalação detalhada
- [TIPS.md](TIPS.md) - Dicas e melhores práticas
- [CONTRIBUTING.md](CONTRIBUTING.md) - Como contribuir

---

## 🆘 Precisa de Ajuda?

### Problemas Comuns

**Erro de autenticação?**
```bash
oci setup config
```

**Módulo não encontrado?**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Sem dados?**
- Aguarde 1 hora após criar instâncias
- Verifique permissões OCI
- Reduza METRICS_DAYS para 7

### Suporte

- 📝 [Abra uma Issue](https://github.com/bruno0nline/OCI_FinOps_Analyzer/issues)
- 💬 [Discussões](https://github.com/bruno0nline/OCI_FinOps_Analyzer/discussions)
- 📧 Email: brunomendesaugusto@gmail.com

---

## 🎓 Aprenda Mais

### Entendendo as Recomendações

| Recomendação | CPU | Memória | Ação |
|--------------|-----|---------|------|
| KEEP | 30-70% | 40-80% | ✅ Nada |
| DOWNSIZE | <30% | <40% | 📉 Reduzir |
| DOWNSIZE-STRONG | <15% | <30% | 📉📉 Reduzir muito |
| UPSCALE | >70% | >80% | 📈 Aumentar |
| BURSTABLE | <10% | - | 🔄 Converter |

### Calculando Economia

```
Economia Mensal = (Shape Atual - Shape Recomendado) × 730h × Preço/hora
```

Exemplo:
```
VM.Standard.E4.Flex (4 OCPUs) → VM.Standard.E4.Flex (2 OCPUs)
Economia = (4 - 2) × 730 × R$ 0,06 = R$ 87,60/mês
```

---

## 🎯 Metas Recomendadas

### Primeira Análise
- [ ] Executar análise completa (30 dias)
- [ ] Revisar relatório Excel
- [ ] Identificar top 10 economias
- [ ] Apresentar para gestão

### Primeiro Mês
- [ ] Implementar DOWNSIZE-STRONG em DEV/QA
- [ ] Converter instâncias para BURSTABLE
- [ ] Monitorar resultados
- [ ] Documentar economia

### Segundo Mês
- [ ] Implementar DOWNSIZE em produção
- [ ] Executar UPSCALE onde necessário
- [ ] Automatizar análises mensais
- [ ] Criar dashboard de acompanhamento

### Terceiro Mês
- [ ] Revisar todas as mudanças
- [ ] Calcular ROI total
- [ ] Ajustar limites de recomendação
- [ ] Expandir para outros recursos (Block Volumes, etc)

---

## 💡 Dica Pro

**Automatize análises mensais:**

```bash
# Adicione ao crontab
crontab -e

# Execute todo dia 1º às 2h
0 2 1 * * cd ~/oci-finops-analyzer && source .venv/bin/activate && export METRICS_DAYS=30 && python3 src/oci_metrics_cpu_mem_media_ndays.py && python3 src/oci_metrics_cpu_mem_word_report.py
```

---

## 🌟 Casos de Sucesso

### Empresa A
- **Instâncias analisadas:** 150
- **Economia mensal:** R$ 18.500
- **ROI:** 6 meses
- **Tempo de implementação:** 2 meses

### Empresa B
- **Instâncias analisadas:** 80
- **Economia mensal:** R$ 12.300
- **ROI:** 4 meses
- **Tempo de implementação:** 1 mês

---

**Pronto para começar? Execute o primeiro comando e comece a economizar! 🚀**

```bash
git clone https://github.com/bruno0nline/oci-finops-analyzer.git && cd oci-finops-analyzer
```
