schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


AUDIT_STATUSES = [
    "DOĞRULANDI",
    "DÜZELTME GEREKLİ",
    "KANIT YETERSİZ",
    "UYUŞMAZLIKTA",
    "DENETİM TAMAMLANMADI"
]


class AuditRecordCreate(BaseModel):
    kayit_id: str = Field(min_length=1, max_length=100)
    iddia: str = Field(min_length=1)
    kanit: Optional[str] = None
    gerekce: Optional[str] = None
    degerlendirici_a: Optional[str] = None
    degerlendirici_b: Optional[str] = None
    durum: str = "DENETİM TAMAMLANMADI"
    protokol_versiyonu: str = "1.0"


class AuditRecordResponse(AuditRecordCreate):
    olusturma_tarihi: datetime
