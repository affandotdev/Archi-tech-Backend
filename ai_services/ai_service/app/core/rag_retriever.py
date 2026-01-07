import chromadb
from chromadb.config import Settings


def retrieve_relevant_rules(query: str, k: int = 3):
    client = chromadb.Client(
        Settings(
            persist_directory="vector_store/kpbr",
            anonymized_telemetry=False,
        )
    )

    collection = client.get_or_create_collection(
        name="kpbr_rules"
    )

    results = collection.query(
        query_texts=[query],
        n_results=k,
    )

    rules = []

    for doc, meta in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        rules.append({
            "text": doc,
            "rule": meta.get("rule"),
            "chapter": meta.get("chapter"),
        })

    return rules


def build_rag_context(rules):
    lines = []

    for r in rules:
        lines.append(
            f"Rule {r['rule']}: {r['text']}"
        )

    return "\n\n".join(lines)


def format_rules_for_client(rules):
    formatted = []

    for r in rules:
        formatted.append({
            "rule": r.get("rule"),
            "summary": (
                r.get("text")[:250] + "..."
                if r.get("text") and len(r.get("text")) > 250
                else r.get("text")
            ),
            "source": "Kerala Panchayat Building Rules"
        })

    return formatted

