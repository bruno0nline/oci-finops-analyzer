"""Validação de períodos e limites relativos ao instante da consulta OCI."""
from datetime import timedelta


def validate_days(value):
    try:
        days = int(value)
    except (TypeError, ValueError):
        raise ValueError("Informe um número inteiro de 1 a 90.") from None
    if str(days) != str(value).strip() or not 1 <= days <= 90:
        raise ValueError("Informe um número inteiro de 1 a 90.")
    return days


def prompt_days():
    while True:
        try:
            return validate_days(input("Quantos dias deseja analisar? [1–90, padrão: 30]: ").strip() or "30")
        except ValueError as exc:
            print(exc)
        except EOFError:
            raise ValueError("Sem entrada interativa. Use --days N ou METRICS_DAYS=N.") from None


def metric_interval(days):
    return "5m" if validate_days(days) <= 30 else "1h"


def safe_start(start, end, interval, now):
    retention = 30 if interval == "5m" else 90
    effective = max(start, now - timedelta(days=retention) + timedelta(minutes=5))
    if effective >= end:
        raise ValueError("Janela fora do histórico disponível.")
    return effective
