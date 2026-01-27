"""Safe util package init.

Avoid importing submodules at package import time to prevent optional
dependency import errors (e.g. pdf2image). Import submodules explicitly
where needed, e.g. `from util import pdf_utils` or `from util import ollama`.
"""

__all__ = []