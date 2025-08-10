import os
import glob
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from text_utils import file_to_text

MODEL_NAME = "all-MiniLM-L6-v2"
REF_DIR = "reference_docs"
EMB_OUT = "embeddings.npy"
METAS_OUT = "metas.json"

def collect_docs(ref_dir=REF_DIR, max_len=20000):
    docs = []
    metas = []
    for fp in sorted(glob.glob(os.path.join(ref_dir, "*"))):
        try:
            text = file_to_text(fp)
            if not text or len(text.strip()) == 0:
                continue
            text = text[:max_len]
            docs.append(text)
            metas.append({"source": fp})
        except Exception as e:
            print("Skipping", fp, e)
    return docs, metas

def build_and_save(docs, metas, model_name=MODEL_NAME):
    if not docs:
        print("No reference docs found to index.")
        return
    model = SentenceTransformer(model_name)
    embeddings = model.encode(docs, convert_to_numpy=True, show_progress_bar=True)
    np.save(EMB_OUT, embeddings)
    with open(METAS_OUT, "w") as f:
        json.dump(metas, f, indent=2)
    print(f"Saved embeddings -> {EMB_OUT}, metas -> {METAS_OUT}")

def main():
    docs, metas = collect_docs()
    build_and_save(docs, metas)

if __name__ == "__main__":
    main()
