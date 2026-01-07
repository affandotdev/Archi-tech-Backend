import re
import pdfplumber
from pathlib import Path


PDF_PATH = Path("data/raw_documents/kpbr_rule.pdf")



def extract_raw_text(pdf_path: Path) -> str:
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def is_definition_rule(text: str) -> bool:
    lowered = text.lower()
    return (
        "means" in lowered
        or "shall mean" in lowered
        or "definitions" in lowered
    )






def clean_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        line = line.strip()

        # remove empty lines
        if not line:
            continue

        # remove page numbers
        if re.fullmatch(r"\d+", line):
            continue

        # remove repeated headers (tune if needed)
        if "Kerala Panchayat Building Rules" in line:
            continue

        lines.append(line)

    return "\n".join(lines)



def normalize_rules(text: str) -> str:
    """
    Normalize KPBR-style PDFs so every 'Rule <number>.' starts on a new line.
    This fixes cases like: 'rule 56. 61. Group I...'
    """
    return re.sub(
        r"(?i)(?<!\n)(rule\s+\d+\.)",
        r"\n\1",
        text
    )








def chunk_kpbr(text: str):
    chunks = []

    chapter = None
    rule = None
    buffer = []
    started = False  # ignore preamble

    lines = text.splitlines()

    chapter_pattern = re.compile(r"^CHAPTER\s+[IVXLC]+.*", re.IGNORECASE)
    rule_pattern = re.compile(r"^Rule\s+(\d+)\.?", re.IGNORECASE)
    subrule_pattern = re.compile(r"^\((\d+)\)")

    for line in lines:
        # detect chapter
        if chapter_pattern.match(line):
            chapter = line
            continue

        # detect new rule
        rule_match = rule_pattern.match(line)
        if rule_match:
            started = True

            # flush previous rule
            if buffer and rule:
                chunks.append(build_chunk(buffer, chapter, rule))

            rule = rule_match.group(1)
            buffer = [line]
            continue

        # ignore preamble
        if not started:
            continue

        # detect first-level sub-rule only
        subrule_match = subrule_pattern.match(line)
        if subrule_match:
            # already inside a sub-rule → continuation
            if "(" in rule:
                buffer.append(line)
                continue

            # flush parent rule
            if buffer and rule:
                chunks.append(build_chunk(buffer, chapter, rule))

            rule = f"{rule}({subrule_match.group(1)})"
            buffer = [line]
            continue

        # normal continuation line
        buffer.append(line)

    # flush last rule
    chunk = build_chunk(buffer, chapter, rule)
    if chunk:
        chunks.append(chunk)


    return chunks



def is_cost_relevant(text: str) -> bool:
    keywords = [
        "height", "floor", "storey", "parking", "fire", "safety",
        "setback", "coverage", "area", "far", "fsi",
        "road", "access", "structural", "load",
        "occupancy", "hazard"
    ]
    lowered = text.lower()
    return any(k in lowered for k in keywords)








def build_chunk(lines, chapter, rule):
    text = " ".join(lines)
    lowered = text.lower()

    # 1. HARD EXCLUSIONS (domain rules)
    if rule in {"1", "2", "3"}:
        return None  # definitions, title, applicability

    if "definitions" in lowered:
        return None

    if "words and expressions" in lowered:
        return None

    if "shall apply" in lowered and "building" in lowered:
        return None

    # 2. COST-RELEVANT FILTER
    keywords = [
        "height", "floor", "storey", "parking", "fire", "safety",
        "setback", "coverage", "far", "fsi",
        "road width", "access",
        "structural", "load",
        "occupancy", "hazard",
        "open space"
    ]

    if not any(k in lowered for k in keywords):
        return None

    return {
        "text": text,
        "metadata": {
            "document": "KPBR",
            "chapter": chapter,
            "rule": rule,
            "jurisdiction": "Kerala",
            "year": 2019,
        },
    }




def main():
    raw_text = extract_raw_text(PDF_PATH)
    cleaned_text = clean_text(raw_text)
    normalized_text = normalize_rules(cleaned_text)

    chunks = [c for c in chunk_kpbr(normalized_text) if c is not None]

    print(f"Generated {len(chunks)} chunks\n")
    return chunks




if __name__ == "__main__":
    main()

