# AI-Powered ADGM Corporate Agent – Automated Legal Compliance Review

**An intelligent legal assistant that automatically checks, annotates, and verifies business process documents for compliance with Abu Dhabi Global Market (ADGM) regulations.**

Using AI + rule-based logic, it not only detects the legal process and verifies required documents against official checklists, but also flags potential compliance issues with law citations, and delivers fully-annotated `.docx` files alongside a structured JSON report.

This project showcases my ability to combine document parsing, compliance automation, and AI-assisted analysis into a production-ready solution.

---

## ADGM Corporate Agent – AI-Powered Compliance Assistant

An **AI-driven legal assistant** designed to automate **document review, checklist verification, and compliance analysis** for the Abu Dhabi Global Market (ADGM) jurisdiction.

Built as part of an **AI Engineer Intern Take-Home Assignment**, it meets **all core requirements**: process detection, completeness check, red-flag detection, annotated outputs, and structured reports.

---

## Key Features

- **Document Intake:** Upload multiple `.docx` (or PDF) files for analysis (via Gradio UI)
- **Process Auto-Detection:** Recognizes the target legal process (*e.g.*, Company Incorporation, Licensing, Employment HR)
- **Checklist Verification:** Compares uploaded docs against **official ADGM document checklists** for that process and **notifies missing mandatory docs** in plain language
- **Red-Flag Detection:** Highlights missing clauses, wrong jurisdiction references, ambiguous language, and formatting issues
- **Legal Citations:** Suggests fixes with references to relevant ADGM regulations (RAG-ready)
- **Inline Annotations:** Adds red highlighted issue notes directly inside `.docx` content & appends a Compliance Review Summary
- **Structured Output:** Generates both a reviewed `.docx` file and a summary `.json` report, packaged into a downloadable ZIP

---

## 📂 Folder Structure

```
adgm_corporate_agent/
│
├── app.py                    # Main application – Gradio UI, process orchestration
├── checklist.py             # Process & doc type detection + checklist comparison
├── checks.py                # Rule-based compliance & red-flag detection
├── annotate_docx.py         # Inline annotations + summary section in reviewed docx
├── text_utils.py            # .docx text extraction helpers
├── outputs.py               # JSON writing + ZIP packaging utilities
├── extract_download.py      # Downloads & extracts ADGM reference docs (pre-run)
│
├── data/                    # Reference docs, checklists, sample documents
├── outputs/                 # Auto-generated reviewed docs & summary reports
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## How It Works (Logic Flow)

1. **Upload & Save** – User uploads `.docx` files via Gradio; app saves them into a temp folder
2. **Extract & Classify** – Text read with `python-docx` → `checklist.py` detects document type
3. **Process Recognition** – Keywords from all docs identify the intended ADGM process
4. **Checklist Verification** – Compares detected doc types to the required checklist for that process; records missing docs
5. **Compliance Checks** – `checks.py` flags:
   - Missing jurisdiction references to ADGM
   - Missing signatories
   - Wrong jurisdiction mentions (UAE Federal Law instead of ADGM)
   - Ambiguous terms like *may* instead of *shall*
6. **Annotations** – `annotate_docx.py` adds inline red issue tags + final "Compliance Review Summary" page to each `.docx`
7. **Outputs** – Writes a structured JSON summary of all findings + bundles reviewed files into a ZIP for download

---

## 🔧 Tech Stack

- **Backend:** Python 3.9+
- **UI Framework:** Gradio
---

##  Installation & Setup

### 1. Clone Repository
```bash
git clone <https://github.com/2CentsCapitalHR/ai-engineer-task-venupriyaa>
cd adgm_corporate_agent
```

### 2. Create & Activate Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```
---

## ▶️ Running the App

```bash
python app.py
```

- Open the **local URL** shown in terminal (e.g., `http://127.0.0.1:7860`)
- Upload `.docx` files for a single process
- Click **Submit** to:
  - View missing document checklist
  - Download reviewed `.docx` with inline comments
  - Get JSON summary + ZIP of results

---

##  Example Outputs

- **Reviewed.docx** – Original doc + inline red issue notes + compliance summary page
- **output_summary.json** – All process/checklist results and issues in structured form
- **results.zip** – Packaged reviewed docs & summary for delivery

---
