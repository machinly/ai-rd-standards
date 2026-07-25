"""Deterministic guardrails for the R&D standards rebuild."""

from .model import CheckResult, ResultStatus, combine_results

__all__ = ["CheckResult", "ResultStatus", "combine_results"]
