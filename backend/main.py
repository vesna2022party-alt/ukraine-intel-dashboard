from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import spacy

VALID_TOKENS = [
    "ua-intel-demo-123",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_sm")

regions = ["Kyiv","Lviv","Kharkiv","Odesa","Dnipro"]
events = {r: [] for r in regions}


def check_token(token: str):
    if token not in VALID_TOKENS:
        raise HTTPException(status_code=403, detail="Invalid token")


def fetch_data():
    return [
        "Explosion in Kyiv center",
        "Protests in Lviv",
        "Missile strike Kharkiv",
        "Attack in Odesa port",
        "Tension rising in Dnipro"
    ]


def extract_entities(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents]


def extract_topics(texts):
    words = []
    for t in texts:
        words += t.split()
    return list(set(words))[:5]


@app.get("/")
def root():
    return {"status":"ok"}


@app.get("/regions")
def get_regions(token: str = Query(...)):
    check_token(token)

    texts = fetch_data()
    result = []

    for r in regions:
        risk = round(len(texts)/10,2)

        topics = extract_topics(texts)
        entities = []
        for t in texts:
            entities += extract_entities(t)

        events[r].append({
            "time": int(time.time()),
            "text": texts[0]
        })

        result.append({
            "region": r,
            "risk": risk,
            "topics": topics,
            "entities": entities[:5]
        })

    return result
