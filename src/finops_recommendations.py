"""Motor offline: configura??o candidata; n?o executa altera??es na OCI."""
import math
from datetime import datetime

RULE_VERSION = "2.0"
# Limites conservadores do cat?logo padr?o; extended memory exige revis?o.
# https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm
LIMITS = {"VM.Standard.E3.Flex": (64, 1024), "VM.Standard.E4.Flex": (64, 1024),
          "VM.Standard.E5.Flex": (126, 1024), "VM.Standard.A1.Flex": (76, 472)}


def number(value):
    try:
        value = float(value)
        return value if math.isfinite(value) else None
    except (TypeError, ValueError):
        return None


def coverage(row, metric):
    try:
        start = datetime.fromisoformat(row[f"{metric}_start_utc"])
        end = datetime.fromisoformat(row["end_utc"])
        seconds = {"5m": 300, "1h": 3600}[row["metric_interval"]]
        expected = max(1, math.ceil((end - start).total_seconds() / seconds))
        if end <= start:
            return None
        samples = number(row.get(f"{metric}_samples"))
        return min(100, 100 * samples / expected) if samples is not None and samples >= 0 else None
    except (KeyError, TypeError, ValueError):
        return None


def recommend(row, min_coverage=90, target_utilization=75):
    result = dict(rule_version=RULE_VERSION, min_coverage_percent=min_coverage,
                  target_utilization_percent=target_utilization,
                  cpu_coverage_percent=coverage(row, "cpu"), mem_coverage_percent=coverage(row, "mem"),
                  proposed_ocpus=None, proposed_memory_gb=None,
                  projected_cpu_p95_percent=None, projected_mem_p95_percent=None,
                  finops_recommendation="INSUFFICIENT_DATA", recommendation_reason="")
    def stop(status, reason):
        result.update(finops_recommendation=status, recommendation_reason=reason)
        return result
    cpu, mem = number(row.get("ocpus")), number(row.get("memory_gb"))
    cp, mp = number(row.get("cpu_p95_percent")), number(row.get("mem_p95_percent"))
    if row.get("collection_error") or any(v is None for v in (cpu, mem, cp, mp)):
        return stop("INSUFFICIENT_DATA", "Configura??o ou m?tricas ausentes/falha de coleta.")
    if cpu <= 0 or mem <= 0 or not (0 <= cp <= 100 and 0 <= mp <= 100):
        return stop("INSUFFICIENT_DATA", "Configura??o ou percentuais inv?lidos.")
    if any(result[f"{m}_coverage_percent"] is None or result[f"{m}_coverage_percent"] < min_coverage for m in ("cpu", "mem")):
        return stop("INSUFFICIENT_DATA", "Cobertura insuficiente da janela; verificar agenda, cria??o e agente. N?o equivale a ociosidade.")
    shape = row.get("shape")
    if shape not in LIMITS:
        return stop("REVIEW", "Shape fixa ou fora do cat?logo validado; avaliar migra??o/limites manualmente.")
    if row.get("burstable_enabled") == "YES" or row.get("baseline_raw") not in (None, "", "BASELINE_1_1"):
        return stop("REVIEW", "Baseline burstable/desconhecida exige an?lise espec?fica.")
    max_cpu, max_mem = LIMITS[shape]
    if cpu > max_cpu or mem > max_mem or mem < cpu or mem > 64 * cpu:
        return stop("REVIEW", "Configura??o fora dos limites padr?o; avaliar extended memory/shape.")
    # Aumento somente na dimens?o pressionada; n?o reduzir outra dimens?o no mesmo cen?rio.
    upscale = cp > 80 or mp > 85
    nc, nm = cpu, mem
    if upscale:
        if cp > 80:
            nc = max(cpu, math.ceil(cpu * cp / target_utilization))
        if mp > 85:
            nm = max(mem, math.ceil(mem * mp / target_utilization))
    else:
        nc = min(cpu, max(1, math.ceil(cpu * cp / target_utilization)))
        nm = min(mem, max(1, math.ceil(mem * mp / target_utilization)))
    # Rela??o mem?ria/OCPU: preservar capacidade necess?ria, jamais truncar demanda.
    nc = max(nc, math.ceil(nm / 64))
    nm = max(nm, nc)
    if nc > max_cpu or nm > max_mem:
        return stop("REVIEW", "Demanda calculada excede o cat?logo padr?o; avaliar alternativa de capacidade.")
    status = "UPSCALE" if upscale else ("DOWNSIZE" if nc < cpu or nm < mem else "KEEP")
    if status == "DOWNSIZE" and nc == cpu:
        status = "DOWNSIZE-MEM"
    result.update(proposed_ocpus=nc, proposed_memory_gb=nm,
                  projected_cpu_p95_percent=cp * cpu / nc, projected_mem_p95_percent=mp * mem / nm)
    return stop(status, "Candidato baseado no P95 agregado e margem; validar picos, aplica??o, rede, I/O, HA e capacidade regional antes da mudan?a.")
