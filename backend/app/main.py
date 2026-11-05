

from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
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

audit_records = []

@app.post("/audit-records")
def create_audit_record(record: dict):
    if record.get("durum") not in AUDIT_STATUSES:
        raise HTTPException(
            status_code=422,
            detail="Geçersiz denetim durumu"
        )

    new_record = record.copy()
    new_record["olusturma_tarihi"] = datetime.now(timezone.utc).isoformat()
    audit_records.append(new_record)

    return {
        "message": "Denetim kaydı oluşturuldu",
        "record": new_record
    }


@app.get("/audit-records")
def list_audit_records():
    return {"records": audit_records}
