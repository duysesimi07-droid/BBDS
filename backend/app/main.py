

from fastapi import FastAPI

app = FastAPI(
    title="BBDS - Bağımsız Bilimsel Denetim Sistemi",
    version="3.0"
)

AUDIT_STATUSES = [
    "DOĞRULANDI",
    "DÜZELTME GEREKLİ",
    "KANIT YETERSİZ",
    "UYUŞMAZLIKTA",
    "DENETİM TAMAMLANMADI"
]

@app.get("/")
def home():
    return {
        "name": "BBDS",
        "version": "3.0",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/protocol")
def protocol():
    return {
        "name": "KHSK Bilimsel Denetim Protokolü",
        "version": "1.0",
        "purpose": "Veri bütünlüğü, hesaplama tutarlılığı, kanıt yeterliliği ve bağımsız değerlendirici uyumunun denetlenmesi",
        "principles": [
            "Kanıt önceliği",
            "Önceden tanımlı ölçüt",
            "Bağımsız değerlendirme",
            "Uyuşmazlığın korunması",
            "İzlenebilirlik",
            "Belirsizliğin dürüstçe bildirilmesi",
            "Yeniden üretilebilirlik"
        ]
    }

@app.get("/audit-statuses")
def audit_statuses():
    return {"statuses": AUDIT_STATUSES}
