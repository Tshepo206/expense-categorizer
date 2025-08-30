# src/categorize.py
from __future__ import annotations
import re
from typing import Dict, List, Optional

def normalize_text(x: str) -> str:
    if x is None:
        return ""
    return re.sub(r"\s+", " ", str(x)).strip().lower()

def build_keyword_index(rules: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Make a quick lookup: keyword -> category (first match wins).
    """
    index = {}
    for cat, words in rules.items():
        for w in words:
            w_norm = normalize_text(w)
            if w_norm:
                index[w_norm] = cat
    return index

def categorize_description(description: str,
                           rules: Dict[str, List[str]],
                           default_category: str = "Uncategorized") -> str:
    """
    Simple keyword match on normalized description.
    First keyword found determines the category.
    """
    desc = normalize_text(description)
    if not desc:
        return default_category

    idx = build_keyword_index(rules)

    # exact keyword presence (substring)
    for kw, cat in idx.items():
        if kw in desc:
            return cat

    # fallback: try token-level exact match
    tokens = set(desc.split())
    for kw, cat in idx.items():
        if kw in tokens:
            return cat

    return default_category

def try_llm_category(description: str,
                     rules_text: str,
                     default_category: str = "Uncategorized",
                     model: str = "gpt-4o-mini") -> str:
    """
    Optional: If you set OPENAI_API_KEY env var, we can ask an LLM to pick a category.
    We do NOT require this—rules-only still works.
    """
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return default_category  # LLM not configured

    # Lazy import (only if key exists)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f"""You are a financial assistant. 
Given this transaction description:
\"\"\"{description}\"\"\"

And these allowed categories and their keywords (JSON-like):
{rules_text}

Return ONLY the best category name from the list above. If no match, return "{default_category}".
"""
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        text = resp.choices[0].message.content.strip()
        return text or default_category
    except Exception:
        return default_category