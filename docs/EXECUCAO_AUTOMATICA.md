# Execução automática no Cloud Shell

Na raiz da cópia atualizada do projeto, execute:

```bash
bash scripts/run_finops.sh
```

O comando prepara as dependências, pergunta quantos dias analisar e executa a coleta seguida da geração automática de CSV, Excel e Word. Enter seleciona 30 dias. Valores inválidos são perguntados novamente. Em terminal interativo, uma variável `METRICS_DAYS` antiga não substitui a pergunta.

Também é possível executar diretamente no ambiente virtual já preparado:

```bash
python3 src/oci_metrics_cpu_mem_media_ndays.py
```

Para execução sem pergunta:

```bash
bash scripts/run_finops.sh --days 90 --outdir ~/finops_reports
```

Sem terminal interativo, `METRICS_DAYS` continua aceito; `--days` tem precedência. Sem período informado e sem entrada disponível, a execução termina com uma mensagem de orientação.

## Período e resolução

| Dias solicitados | Agregação |
|---|---|
| 1 a 30 | Média a cada 5 minutos |
| 31 a 90 | Média a cada 1 hora |

O máximo é 90 dias para as métricas históricas de Monitoring consultadas. A retenção é calculada em relação ao momento de cada requisição, não ao fim fixado da janela. Por isso, nas fronteiras de 30/90 dias, o início é ajustado a cada tentativa para permanecer dentro da retenção, com margem de 5 minutos. O período efetivamente consultado pode ser um pouco menor que o solicitado, conforme a duração da coleta. [Documentação Oracle](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/query-metric-resolution.htm).

As colunas `requested_start_utc`, `end_utc`, `cpu_start_utc`, `mem_start_utc`, `metric_interval`, `cpu_samples` e `mem_samples` tornam essa diferença verificável. Datas são UTC. São janelas de consulta; não comprovam cobertura contínua de telemetria. P95 é calculado por interpolação sobre as médias agregadas, não sobre amostras brutas. Resultados de 5 minutos e 1 hora não têm a mesma sensibilidade a picos.

## Resultados e falhas

Por padrão, os arquivos ficam no diretório pessoal (`~/`):

```text
Relatorio_CPU_Memoria_media_Nd_multi_region.csv
Relatorio_CPU_Memoria_media_Nd_multi_region.xlsx
Relatorio_FinOps_CPU_Mem_Nd_multi_region.docx
Relatorio_FinOps_Coleta_Nd.json
```

O Word automático utiliza o gerador detalhado `oci_metrics_cpu_mem_word_report.py`, o mesmo usado na execução manual analisada. Ele mantém as estimativas simplificadas em USD e agora recebe diretamente os dados desta execução. A revisão da precificação BRL continua no backlog. O shell deixa de chamar os dois geradores alternativos de Top 5, cujo contrato financeiro era incompatível com o CSV.

O CSV é salvo por instância. Falhas de inventário, detalhes ou métricas são registradas; a coleta continua e os relatórios mostram `PARCIAL`. Métricas ausentes não viram zero: recebem `INSUFFICIENT_DATA` e não entram nas estimativas de economia. P95 alto tem precedência sobre regras de redução. A redução de memória no Word preserva a CPU quando a recomendação é `DOWNSIZE-MEM`.

O JSON e a aba `Coleta` do Excel listam falhas. Código de saída 0 indica coleta finalizada sem erros registrados; 2 indica coleta parcial, com relatórios produzidos. Ausência de métricas pode ocorrer mesmo sem erro de API e aparece separadamente como dados insuficientes. Um escopo sem instâncias produz relatórios vazios explícitos, sem reutilizar um CSV anterior.

Falhas fatais antes da coleta, como autenticação, impedem a geração de novos relatórios. Interrupção do processo durante a coleta preserva o CSV já escrito, mas pode impedir Excel/Word finais. Arquivos com o mesmo período/destino são sobrescritos; use `--outdir` diferente para preservar execuções e não rode simultaneamente no mesmo destino.

## Verificação local

```bash
python3 -m unittest discover -s tests -v
```

Os testes usam APIs simuladas e geram arquivos Office reais em diretórios temporários. A validação de autenticação, rede, permissões e dados reais requer execução no Cloud Shell.
