
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ==================================================
# KHSK / BBDS ORTAK DENETİM TANIMLARI
# ==================================================

PROTOKOL_VERSIYONU = "1.0"

AUDIT_STATUSES = [
    "DOĞRULANDI",
    "DÜZELTME GEREKLİ",
    "KANIT YETERSİZ",
    "UYUŞMAZLIKTA",
    "DENETİM TAMAMLANMADI"
]

EVALUATOR_DECISIONS = [
    "VAR",
    "YOK",
    "KANIT_YETERSIZ",
    "UYGULANAMAZ",
    "INCELENMEDI"
]

CONFIDENCE_LEVELS = [
    "YÜKSEK",
    "ORTA",
    "DÜŞÜK"
]


# ==================================================
# MEVCUT BBDS API KAYIT MODELİ
# main.py ile uyumlu
# ==================================================

class AuditRecord(BaseModel):

    kayit_id: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    durum: str = Field(
        ...,
        max_length=50
    )

    aciklama: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )


# ==================================================
# BAĞIMSIZ DEĞERLENDİRİCİ KARAR MODELİ
# main.py ile uyumlu
# ==================================================

class EvaluatorDecision(BaseModel):

    id: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    kayit_id: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    degerlendirici_id: str = Field(
        ...,
        min_length=1,
        max_length=1
    )

    karar: str = Field(
        ...,
        min_length=1,
        max_length=30
    )

    kanit: Optional[str] = None

    gerekce: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    guven_duzeyi: Optional[str] = Field(
        default=None,
        max_length=20
    )

    protokol_versiyonu: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    kod_kitabi_versiyonu: str = Field(
        ...,
        min_length=1,
        max_length=50
    )


# ==================================================
# ÖNCEKİ AUDIT RECORD ŞEMASININ UYUMLULUK KORUMASI
# ==================================================

class AuditRecordCreate(BaseModel):

    kayit_id: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    iddia: str = Field(
        ...,
        min_length=1
    )

    kanit: Optional[str] = None

    gerekce: Optional[str] = None

    degerlendirici_a: Optional[str] = None

    degerlendirici_b: Optional[str] = None

    durum: str = "DENETİM TAMAMLANMADI"

    protokol_versiyonu: str = PROTOKOL_VERSIYONU


class AuditRecordResponse(AuditRecordCreate):

    olusturma_tarihi: datetime


# ==================================================
# BAĞIMSIZ DEĞERLENDİRİCİ KARAR YANITI
# ==================================================

class EvaluatorDecisionResponse(EvaluatorDecision):

    karar_tarihi: datetime


# ==================================================
# PROTOKOL BİLGİSİ
# ==================================================

class ProtocolInfo(BaseModel):

    name: str = "KHSK Bilimsel Denetim Protokolü"

    version: str = PROTOKOL_VERSIYONU

    purpose: str = (
        "Veri bütünlüğü, hesaplama tutarlılığı, "
        "kanıt yeterliliği ve bağımsız değerlendirici "
        "uyumunun denetlenmesi"
    )

