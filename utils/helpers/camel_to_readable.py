import re
import json

with open("C:/Users/mmudallal/Desktop/kudwa-evaluation-task/utils/config/data_config/finnhub_config.json", "r") as f:
    config = json.load(f)
    
ACRONYM_MAP = config["company_basic_financials"]["acronym_map"]

NON_ALNUM_PRESERVE = set("&%$@/+")

def camel_to_readable(name: str) -> str:
    if not name or not isinstance(name, str):
        return name

    name = name.replace("_", " ").replace("-", " ")
    name = name.replace("/", " / ")
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', name)
    name = re.sub(r'([A-Za-z])([0-9])', r'\1 \2', name)
    name = re.sub(r'([0-9])([A-Za-z])', r'\1 \2', name)
    name = re.sub(r'\s+', ' ', name).strip()

    parts = name.split(' ')
    out = []
    for p in parts:
        lp = p.lower()

        if any(ch in p for ch in NON_ALNUM_PRESERVE) or re.search(r'[^A-Za-z0-9/&%$]', p):
            out.append(p.upper())
            continue

        if lp in ACRONYM_MAP:
            out.append(ACRONYM_MAP[lp])
            continue

        if p.isupper():
            out.append(p)
            continue

        if lp.isdigit():
            out.append(p)
            continue

        out.append(p.capitalize())

    readable = ' '.join(out)
    readable = re.sub(r'\s*/\s*', ' / ', readable)
    readable = re.sub(r'\s+', ' ', readable).strip()
    return readable
