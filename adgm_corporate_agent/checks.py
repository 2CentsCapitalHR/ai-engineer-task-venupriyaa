def run_all_checks(text, doc_type):
    """Advanced static legal checks, now with law references."""
    issues = []
    t = (text or "").lower()
    
    if "abu dhabi global market" not in t:
        issues.append({
            "document": doc_type,
            "section": "N/A",
            "issue": "Jurisdiction not specified as ADGM.",
            "severity": "High",
            "law_citation": "ADGM Companies Regulations 2020, Art. 6",
            "suggestion": "Replace any other reference with 'Abu Dhabi Global Market (ADGM)'."
        })

    if "signatory" not in t and doc_type in [
        "Board Resolution", "Shareholder Resolution", "Articles of Association", "Memorandum of Association"
    ]:
        issues.append({
            "document": doc_type,
            "section": "N/A",
            "issue": "Missing signatory section at end of document.",
            "severity": "Medium",
            "law_citation": "ADGM Companies Regs, Execution of Documents",
            "suggestion": "Add a section for authorized signature(s) as per ADGM requirements."
        })
    
    if "uae federal" in t or "united arab emirates law" in t:
        issues.append({
            "document": doc_type,
            "section": "N/A",
            "issue": "Wrong jurisdiction: UAE Federal Law referenced instead of ADGM.",
            "severity": "High",
            "law_citation": "ADGM Companies Regulations",
            "suggestion": "Reference only ADGM, remove/replace UAE Federal Law references."
        })

    if "may" in t and "shall" not in t and doc_type in [
        "Articles of Association", "Employment Contract"
    ]:
        issues.append({
            "document": doc_type,
            "section": "Possible Ambiguity",
            "issue": "Uses 'may' instead of 'shall', which can be ambiguous in contracts.",
            "severity": "Low",
            "law_citation": "ADGM Guidance on Drafting",
            "suggestion": "Use 'shall' for binding obligations."
        })
    if "director" in doc_type.lower() and "director" not in t:
        issues.append({
            "document": doc_type,
            "section": "N/A",
            "issue": "Director details not found.",
            "severity": "Medium",
            "law_citation": "ADGM Companies Regulations, Registers",
            "suggestion": "List Directors as per ADGM requirements."
        })
    return issues
