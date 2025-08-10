

CHECKLISTS = {
    "company_incorporation": [
        "Articles of Association",
        "Memorandum of Association",
        "Board Resolution",
        "Shareholder Resolution",
        "Incorporation Application",
        "UBO Declaration Form",
        "Register of Members and Directors",
        "Change of Registered Address Notice"
    ],
    "employment_hr": [
        "Employment Contract",
        "Offer Letter",
        "Non-Disclosure Agreement"
    ],
    "licensing": [
        "Licence Application Form",
        "Business Plan",
        "Supporting Regulatory Forms"
    ]
}

PROCESS_KEYWORDS = {
    "company_incorporation": [
        "articles of association", "memorandum of association", "board resolution", "shareholder",
        "incorporation", "ubo", "register of members", "registered address"
    ],
    "employment_hr": [
        "employment contract", "offer letter", "employee", "hr", "non-disclosure"
    ],
    "licensing": [
        "licence application", "license application", "business plan", "regulatory", "permit"
    ]
}

def detect_doc_type_from_text(text):
    t = (text or "").lower()
    for dtype in CHECKLISTS["company_incorporation"]:
        if dtype.lower().split(" ")[0] in t:
            return dtype
    for dtype in CHECKLISTS["employment_hr"]:
        if dtype.lower().split(" ")[0] in t:
            return dtype
    for dtype in CHECKLISTS["licensing"]:
        if dtype.lower().split(" ")[0] in t:
            return dtype
    
    if "employment" in t:
        return "Employment Contract"
    if "licence" in t or "license" in t:
        return "Licence Application Form"
    return "Unknown"

def detect_process_from_docs(texts):
    lower_all = " ".join([t.lower() for t in texts])
    for proc, keywords in PROCESS_KEYWORDS.items():
        if any(k in lower_all for k in keywords):
            return proc
    return "company_incorporation"  

def compare_checklist(uploaded_types, process="company_incorporation"):
    required = CHECKLISTS.get(process, [])
    missing = [r for r in required if r not in uploaded_types]
    result = {
        "process": process.replace("_", " ").title(),
        "documents_uploaded": len(uploaded_types),
        "required_documents": len(required),
        "missing_documents": missing
    }
    return result
