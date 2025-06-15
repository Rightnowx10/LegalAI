import re

def route_query_type(query: str) -> str:
    """
    Determines the appropriate prompt type for a legal query based on keywords.
    Returns one of the predefined prompt types used in the system.
    """
    q = re.sub(r"[^\w\s]", "", query.lower())  # Remove punctuation

    if any(kw in q for kw in ["brief", "summarize", "summary", "case overview", "case summary", "explain the case"]):
        return "case_brief"
    elif any(kw in q for kw in ["facts", "factual background", "incident", "sequence of events", "what happened"]):
        return "facts_extraction"
    elif any(kw in q for kw in ["why", "reason", "logic", "basis for decision", "rationale", "court reasoning"]):
        return "reasoning"
    elif any(kw in q for kw in [
        "bail", "acquitted", "convicted", "relief", "decision", "allowed", "dismissed",
        "held", "outcome", "verdict", "granted", "denied"
    ]):
        return "decision_check"
    elif any(kw in q for kw in ["list citations", "cited cases", "references", "cited acts", "what did the court refer to"]):
        return "citations_list"
    elif any(kw in q for kw in [
        "extract sections", "extract acts", "extract provisions", "legal provisions referenced",
        "ipc", "crpc", "article", "section", "constitution"
    ]):
        return "extraction"
    elif any(kw in q for kw in ["procedural history", "stages of case", "court journey", "appeals", "remand"]):
        return "procedural_history"
    elif any(kw in q for kw in ["define", "meaning of", "what is", "legal term", "concept of", "explain the term"]):
        return "legal_definition"
    elif any(kw in q for kw in ["interpret", "interpretation of", "meaning of section", "how is", "how is x applied"]):
        return "statutory_interpretation"
    elif any(kw in q for kw in ["dissenting opinion", "concurring opinion", "dissent", "differing view", "judge disagreed"]):
        return "dissenting_opinion_summary"
    elif any(kw in q for kw in ["implications", "impact", "effect on future", "precedent set", "consequences"]):
        return "case_implications"
    else:
        return "general"
