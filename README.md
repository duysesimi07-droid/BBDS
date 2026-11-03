# BBDS 3.0 — Kurumsal Bilimsel Denetim Sistemi

Çalıştırılabilir başlangıç projesi: React (mobil uyumlu web arayüzü) + FastAPI + PostgreSQL + Docker Compose.

## Gereksinimler
- Docker Desktop / Docker Engine ve Docker Compose
- İnternet erişimi (ilk imaj ve paket indirmeleri için)

## Başlatma
```bash
cp .env.example .env
docker compose up --build
```
- Arayüz: http://localhost:8080
- API dokümantasyonu: http://localhost:8000/docs
- Sağlık kontrolü: http://localhost:8000/health

İlk kurulumda `admin / ChangeThis-Immediately-2026!` hesabı oluşturulur.
`.env` içindeki `ADMIN_PASSWORD` değerini dağıtımdan önce değiştirin.

## Bu sürümde bulunanlar
- Kurum/proje kaydı oluşturma ve listeleme
- İddia/araştırma bulgusu kaydı
- Kaynak ve kanıt bağlantısı
- Bağımsız değerlendirici notları
- Değerlendirme durumları: pending, verified, partially_verified, unverified, contradictory
- Rol temeli: admin, project_manager, researcher, reviewer, statistician, viewer
- API üzerinden kayıt oluşturma/listeleme
- PostgreSQL kalıcılığı
- Mobil uyumlu React arayüzü
- Docker Compose ile tek komutla yerel kurulum

## Güvenlik ve kurumsal dağıtım öncesi
Bu paket bir geliştirme/pilot başlangıç sürümüdür; üretim ortamına doğrudan açılmamalıdır.
1. `SECRET_KEY`, `ADMIN_PASSWORD` ve DB parolasını güçlü, benzersiz değerlerle değiştirin.
2. HTTPS/TLS ters proxy arkasında yayınlayın.
3. Kurumun OIDC/SSO kimlik sağlayıcısını entegre edin.
4. MFA, parola politikası, hız sınırlama ve oturum iptali ekleyin.
5. Yedekleme, geri yükleme tatbikatı, izleme ve olay müdahale prosedürü kurun.
6. Denetim kayıtlarını ayrı, erişimi kısıtlı ve değiştirilemez depoya aktarın.
7. KVKK, veri saklama, erişim ve silme politikalarını kurum hukuk/bilgi güvenliği birimleriyle belirleyin.
8. Bağımsız sızma testi ve güvenlik incelemesi yaptırın.

## Bilimsel sınırlama
Otomatik kontroller veri alanlarının ve iş akışının tutarlılığını kontrol eder; bilimsel doğruluğu kendiliğinden kanıtlamaz. Sonuçlar gerekçe ve kanıtla uzmanlarca değerlendirilmelidir. Güvenilirlik istatistikleri yeterli sayıda uygun değerlendirme olmadan hesaplanmamalıdır.

## Proje yapısı
- `backend/` FastAPI servisi
- `frontend/` React/Vite arayüzü
- `docker-compose.yml` PostgreSQL + API + web
