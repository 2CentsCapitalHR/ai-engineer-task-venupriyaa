
import os
import tempfile
import shutil
import json
import gradio as gr

from text_utils import file_to_text
from checklist import detect_doc_type_from_text, compare_checklist
from checks import run_all_checks
from annotate_docx import annotate_docx
from outputs import write_summary_json, create_zip


def process_upload(files):
   
    if not files:
        return None, "No files uploaded.", None

    uploaded_types = []
    issues_all = []
    reviewed_files = []

    tmpdir = tempfile.mkdtemp(prefix="adgm_")
    paths = []

    
    for src_path in files:
        if not os.path.exists(src_path):
            return None, f"Uploaded file path not found: {src_path}", None
        dst_path = os.path.join(tmpdir, os.path.basename(src_path))
        shutil.copyfile(src_path, dst_path)
        paths.append(dst_path)


    for p in paths:
        txt = file_to_text(p)
        dtype = detect_doc_type_from_text(txt)
        uploaded_types.append(dtype)

        issues = run_all_checks(txt, dtype)
        issues_all.extend(issues)

 
        if p.lower().endswith(".docx"):
            reviewed_path = p.replace(".docx", "_reviewed.docx")
            annotate_docx(p, issues, reviewed_path)
            reviewed_files.append(reviewed_path)


    checklist_res = compare_checklist(uploaded_types)
    summary = {**checklist_res, "issues_found": issues_all}

   
    summary_json_path = write_summary_json(summary, os.path.join(tmpdir, "summary.json"))


    zip_path = create_zip(reviewed_files + [summary_json_path], os.path.join(tmpdir, "results.zip"))

    json_display = json.dumps(summary, indent=4)

    first_reviewed_doc = reviewed_files[0] if reviewed_files else None

    return zip_path, json_display, first_reviewed_doc


def serve():
    demo = gr.Interface(
        fn=process_upload,
        inputs=gr.File(file_count="multiple", file_types=[".docx", ".pdf"], type="filepath"),
        outputs=[
            gr.File(label="Download Results ZIP"),
            gr.Textbox(label="Summary JSON Output", interactive=False, lines=20),
            gr.File(label="Download First Reviewed DOCX (After)")
        ],
        title="ADGM Corporate Agent (MVP)"
    )
    demo.launch(share=False)


if __name__ == "__main__":
    serve()
