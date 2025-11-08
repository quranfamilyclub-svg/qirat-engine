
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Issue(BaseModel):
    severity: str
    type: str
    word: str | None = None
    start: float | None = None
    detect: str
    fix: str

class EvalResponse(BaseModel):
    is_quran: bool
    scores: dict
    bench: dict
    words: list
    issues: list[Issue]
    ustad_text_en: str | None = None
    ustad_text_ur: str | None = None
    ustad_text_ar: str | None = None

@app.post("/eval_ayah")
async def eval_ayah(
    file: UploadFile = File(...),
    verse_key: str = Form(...),
    lang: str = Form("en")
):
    """
    TEMP STUB:
    Always returns a fixed but *real-format* response.
    Replace internal logic later with real tajweed / ASR engine.
    """
    # Basic sanity check: ensure it's some audio bytes
    content = await file.read()
    if not content or len(content) < 4000:
        return JSONResponse(
            {
                "ok": False,
                "error": "Audio too short or invalid for evaluation."
            },
            status_code=400,
        )

    # Example: simple mocked logic based only on verse_key
    # This avoids irrelevant letters like ض for Al-Fatihah 2.
    surah, ayah = verse_key.split(":")
    issues = []

    if verse_key == "1:2":
        # Only Madd on آخره, no fake ض
        issues.append({
            "severity": "major",
            "type": "Madd",
            "word": "الْعَالَمِينَ",
            "start": 2.30,
            "detect": "Short Madd on ending.",
            "fix": "Extend the Madd at the end to 4–5 counts with stability."
        })
    else:
        issues.append({
            "severity": "minor",
            "type": "Makharij",
            "word": "",
            "start": 1.10,
            "detect": "Some letters slightly unclear.",
            "fix": "Slow down and hit each makhraj precisely."
        })

    data = {
        "is_quran": True,
        "scores": {"total": 84},
        "bench": {"speed": 78, "waqf": 70},
        "words": [
            {"text": "sample", "score": 82},
            {"text": "sample", "score": 86},
        ],
        "issues": issues,
        "ustad_text_en": "Clear recitation. Focus on Madd length and makharij stability.",
        "ustad_text_ur": "تلاوت واضح ہے، مد کی مقدار اور مخارج کی پختگی پر توجہ دیں۔",
        "ustad_text_ar": "تلاوة واضحة؛ راقب مقدار المد وثبات المخارج.",
    }

    return {"ok": True, "data": data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
