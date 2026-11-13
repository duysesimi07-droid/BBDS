import os
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException

try:
    from .schemas import (
        AuditRecord,
        EvaluatorDecision,
        AUDIT_STATUSES,
        EVALUATOR_DECISIONS,
        CONFIDENCE_LEVELS,
        PROTOKOL_VERSIYONU
    )
except ImportError:
    from schemas import (
        AuditRecord,
        EvaluatorDecision,
        AUDIT_STATUSES,
        EVALUATOR_DECISIONS,
        CONFIDENCE_LEVELS,
        PROTOKOL_VERSIYONU
    )

from sqlalchemy import (
    create_engine,
    String,
    Text,
    DateTime,
    select,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker
)

from sqlalchemy.exc import IntegrityError


# --------------------------------------------------
# UYGULAMA
# --------------------------------------------------

app = FastAPI(
    title="BBDS - Bağımsız Bilimsel Denetim Sistemi",
    version="3.1"
)


# --------------------------------------------------
# VERİTABANI BAĞLANTISI
# --------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL ortam değişkeni bulunamadı."
    )

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg://",
        1
    )

elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# --------------------------------------------------
# VERİTABANI TEMEL MODELİ
# --------------------------------------------------

class Base(DeclarativeBase):
    pass


# --------------------------------------------------
# DENETİM KAYDI VERİTABANI MODELİ
# --------------------------------------------------

class AuditRecordDB(Base):

    __tablename__ = "audit_records"

    kayit_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    durum: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    aciklama: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    olusturma_tarihi: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )


# --------------------------------------------------
# BAĞIMSIZ DEĞERLENDİRİCİ VERİTABANI MODELİ
# --------------------------------------------------

class EvaluatorDecisionDB(Base):

    __tablename__ = "evaluator_decisions"

    __table_args__ = (
        UniqueConstraint(
            "kayit_id",
            "degerlendirici_id",
            name="uq_evaluator_record_evaluator"
        ),
    )

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    kayit_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("audit_records.kayit_id"),
        nullable=False
    )

    degerlendirici_id: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    karar: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    kanit: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    gerekce: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    guven_duzeyi: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    protokol_versiyonu: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    kod_kitabi_versiyonu: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    karar_tarihi: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )


# --------------------------------------------------
# UYGULAMA BAŞLANGICI
# --------------------------------------------------

@app.on_event("startup")
def startup():

    Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# ANA UÇ NOKTALAR
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "name": "BBDS",
        "version": "3.1",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# KHSK BİLİMSEL DENETİM PROTOKOLÜ
# --------------------------------------------------

@app.get("/protocol")
def protocol():

    return {
        "name": "KHSK Bilimsel Denetim Protokolü",
        "version": PROTOKOL_VERSIYONU,
        "purpose": (
            "Veri bütünlüğü, hesaplama tutarlılığı, "
            "kanıt yeterliliği ve bağımsız değerlendirici "
            "uyumunun denetlenmesi"
        ),
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


# --------------------------------------------------
# DENETİM DURUMLARI
# --------------------------------------------------

@app.get("/audit-statuses")
def audit_statuses():

    return {
        "statuses": AUDIT_STATUSES
    }


# --------------------------------------------------
# POSTGRESQL DENETİM KAYDI OLUŞTURMA
# --------------------------------------------------

@app.post("/audit-records")
def create_audit_record(record: AuditRecord):

    if record.durum not in AUDIT_STATUSES:

        raise HTTPException(
            status_code=422,
            detail="Geçersiz denetim durumu"
        )

    db = SessionLocal()

    try:

        new_record = AuditRecordDB(
            kayit_id=record.kayit_id,
            durum=record.durum,
            aciklama=record.aciklama,
            olusturma_tarihi=datetime.now(timezone.utc)
        )

        db.add(new_record)
        db.commit()
        db.refresh(new_record)

        return {
            "message": "Denetim kaydı oluşturuldu",
            "record": {
                "kayit_id": new_record.kayit_id,
                "durum": new_record.durum,
                "aciklama": new_record.aciklama,
                "olusturma_tarihi":
                    new_record.olusturma_tarihi.isoformat()
            }
        }

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Bu kayıt kimliği zaten mevcut."
        )

    finally:

        db.close()


# --------------------------------------------------
# POSTGRESQL DENETİM KAYITLARINI LİSTELEME
# --------------------------------------------------

@app.get("/audit-records")
def list_audit_records():

    db = SessionLocal()

    try:

        records = db.scalars(
            select(AuditRecordDB).order_by(
                AuditRecordDB.olusturma_tarihi.desc()
            )
        ).all()

        return {
            "records": [
                {
                    "kayit_id": record.kayit_id,
                    "durum": record.durum,
                    "aciklama": record.aciklama,
                    "olusturma_tarihi":
                        record.olusturma_tarihi.isoformat()
                }
                for record in records
            ]
        }

    finally:

        db.close()


# --------------------------------------------------
# BAĞIMSIZ DEĞERLENDİRİCİ KARARI OLUŞTURMA
# --------------------------------------------------

@app.post("/evaluator-decisions")
def create_evaluator_decision(
    decision: EvaluatorDecision
):

    # Değerlendirici kimliği kontrolü

    if decision.degerlendirici_id not in ["A", "B"]:

        raise HTTPException(
            status_code=422,
            detail="Değerlendirici kimliği A veya B olmalıdır."
        )

    # Karar türü kontrolü

    if decision.karar not in EVALUATOR_DECISIONS:

        raise HTTPException(
            status_code=422,
            detail="Geçersiz değerlendirme kararı."
        )

    # Güven düzeyi kontrolü

    if (
        decision.guven_duzeyi is not None
        and decision.guven_duzeyi not in CONFIDENCE_LEVELS
    ):

        raise HTTPException(
            status_code=422,
            detail="Geçersiz güven düzeyi."
        )

    # VAR ve YOK kararları için kanıt zorunluluğu

    if decision.karar in ["VAR", "YOK"]:

        if not decision.kanit or not decision.kanit.strip():

            raise HTTPException(
                status_code=422,
                detail="VAR ve YOK kararları için kanıt gereklidir."
            )

    db = SessionLocal()

    try:

        # Ana denetim kaydının varlığını kontrol et

        parent_record = db.get(
            AuditRecordDB,
            decision.kayit_id
        )

        if parent_record is None:

            raise HTTPException(
                status_code=404,
                detail="Ana denetim kaydı bulunamadı."
            )

        # Yeni değerlendirici kararını oluştur

        new_decision = EvaluatorDecisionDB(
            id=decision.id,
            kayit_id=decision.kayit_id,
            degerlendirici_id=decision.degerlendirici_id,
            karar=decision.karar,
            kanit=decision.kanit,
            gerekce=decision.gerekce,
            guven_duzeyi=decision.guven_duzeyi,
            protokol_versiyonu=decision.protokol_versiyonu,
            kod_kitabi_versiyonu=decision.kod_kitabi_versiyonu,
            karar_tarihi=datetime.now(timezone.utc)
        )

        db.add(new_decision)
        db.commit()
        db.refresh(new_decision)

        return {
            "message": "Bağımsız değerlendirici kararı kaydedildi",
            "decision": {
                "id": new_decision.id,
                "kayit_id": new_decision.kayit_id,
                "degerlendirici_id":
                    new_decision.degerlendirici_id,
                "karar": new_decision.karar,
                "kanit": new_decision.kanit,
                "gerekce": new_decision.gerekce,
                "guven_duzeyi": new_decision.guven_duzeyi,
                "protokol_versiyonu":
                    new_decision.protokol_versiyonu,
                "kod_kitabi_versiyonu":
                    new_decision.kod_kitabi_versiyonu,
                "karar_tarihi":
                    new_decision.karar_tarihi.isoformat()
            }
        }

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Bu kayıt için aynı değerlendiricinin "
                "ilk kararı zaten mevcut veya kayıt "
                "veritabanı kısıtlarına aykırı."
            )
        )

    finally:

        db.close()


# --------------------------------------------------
# BAĞIMSIZ DEĞERLENDİRİCİ KARARLARINI LİSTELEME
# --------------------------------------------------

@app.get("/evaluator-decisions")
def list_evaluator_decisions(
    kayit_id: str | None = None
):

    db = SessionLocal()

    try:

        query = select(EvaluatorDecisionDB)

        if kayit_id:

            query = query.where(
                EvaluatorDecisionDB.kayit_id == kayit_id
            )

        decisions = db.scalars(
            query.order_by(
                EvaluatorDecisionDB.karar_tarihi.asc()
            )
        ).all()

        return {
            "decisions": [
                {
                    "id": item.id,
                    "kayit_id": item.kayit_id,
                    "degerlendirici_id":
                        item.degerlendirici_id,
                    "karar": item.karar,
                    "kanit": item.kanit,
                    "gerekce": item.gerekce,
                    "guven_duzeyi": item.guven_duzeyi,
                    "protokol_versiyonu":
                        item.protokol_versiyonu,
                    "kod_kitabi_versiyonu":
                        item.kod_kitabi_versiyonu,
                    "karar_tarihi":
                        item.karar_tarihi.isoformat()
                }
                for item in decisions
            ]
        }

    finally:

        db.close()
