from pathlib import Path
from dataclasses import dataclass
from collections import Counter
from math import sqrt
from pypdf import PdfReader
import re

PDF_DIR = Path('data/pdfs')

@dataclass
class Chunk:
    source: str
    page: int
    text: str

_chunks: list[Chunk] = []
_vectors: list[Counter] = []

def _tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 2]

def _cosine(a: Counter, b: Counter) -> float:
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    na = sqrt(sum(v*v for v in a.values())) or 1.0
    nb = sqrt(sum(v*v for v in b.values())) or 1.0
    return dot / (na * nb)

def load_pdfs(pdf_dir: Path = PDF_DIR) -> list[Chunk]:
    chunks: list[Chunk] = []
    for pdf in sorted(pdf_dir.glob('*.pdf')):
        reader = PdfReader(str(pdf))
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ''
            words = text.split()
            for start in range(0, len(words), 120):
                piece = ' '.join(words[start:start+160])
                if len(piece) > 50:
                    chunks.append(Chunk(source=pdf.name, page=i, text=piece))
    return chunks

def build_index(force: bool = False):
    global _chunks, _vectors
    if _vectors and not force:
        return
    _chunks = load_pdfs()
    _vectors = [Counter(_tokens(c.text)) for c in _chunks]

def search_docs(query: str, k: int = 4) -> list[dict]:
    build_index()
    qv = Counter(_tokens(query))
    scored = sorted(enumerate(_vectors), key=lambda iv: _cosine(qv, iv[1]), reverse=True)[:k]
    results = []
    for idx, vec in scored:
        score = _cosine(qv, vec)
        if score <= 0:
            continue
        c = _chunks[idx]
        results.append({'source': c.source, 'page': c.page, 'text': c.text, 'score': float(round(score, 3))})
    return results
