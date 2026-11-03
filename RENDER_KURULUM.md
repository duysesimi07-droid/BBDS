# BBDS 3.0 — Android tablet üzerinden ücretsiz pilot yayınlama

Bu paket Render (ücretsiz web servisi) + Neon (ücretsiz PostgreSQL) üzerinde pilot denemeye göre hazırlanmıştır. Ücretsiz servis uykuya geçebilir; Neon ücretsiz planı kota sınırlarına tabidir. Üretim/kurumsal/hassas veri için uygun değildir.

## 1) GitHub deposu
- GitHub'da yeni ve **Private** bir repository oluşturun.
- ZIP'i Android Dosyalar uygulamasında çıkarın.
- Çıkan klasörün içindeki dosya ve klasörleri (backend, frontend, README.md, vb.) deponun köküne yükleyin. `.env` dosyasını yüklemeyin; gizli anahtarları GitHub'a koymayın.

## 2) Neon veritabanı
- Neon'da ücretsiz PostgreSQL projesi oluşturun.
- Connection string'i kopyalayın; kullanıcı/parola içerir, kimseyle paylaşmayın.
- Render backend ortam değişkeni için URL şemasını `postgresql+psycopg://` olarak kullanın. Neon URL'si `postgresql://` ile başlıyorsa yalnızca başını `postgresql+psycopg://` olarak değiştirin. Geri kalan parametreleri koruyun.

## 3) Render API servisi
- Render > New > Web Service > GitHub deposunu bağlayın.
- Root Directory: `backend`
- Runtime: Docker
- Plan: Free
- Advanced > Health Check Path: `/health`
- Start Command alanını boş bırakın (Dockerfile komutu kullanılır). Servis portu için Environment Variables bölümüne `PORT` = `8000` ekleyin.
- Environment Variables ekleyin:
  - `DATABASE_URL` = Neon bağlantı adresi (`postgresql+psycopg://...`)
  - `SECRET_KEY` = en az 32 karakterlik rastgele, benzersiz değer
  - `ADMIN_USERNAME` = tahmin edilmesi zor olmayan ama size özel kullanıcı adı
  - `ADMIN_PASSWORD` = uzun ve benzersiz parola
- Deploy edin. Servis URL'sini not edin (ör. `https://bbds-api-....onrender.com`). API sağlık kontrolü `https://.../health` adresinde `{"status":"ok"}` döndürmelidir.

## 4) Render arayüzü (Static Site)
- Render > New > Static Site > aynı GitHub deposu.
- Build Command: `cd frontend && npm install && npm run build`
- Publish Directory: `frontend/dist`
- Environment Variable: `VITE_API_URL` = API servisinin tam URL'si (sonunda `/` olmadan).
- Deploy edin. Statik sitenin verdiği URL'yi Android Chrome'da açın.

## 5) İlk giriş
`ADMIN_USERNAME` ve `ADMIN_PASSWORD` ile giriş yapın. İlk testte gerçek kişisel/kurumsal veri kullanmayın.

## Önemli
- Render ücretsiz web servisi 15 dakika trafik almazsa uykuya geçer ve ilk açılışta yaklaşık bir dakika bekletebilir.
- Neon ücretsiz planının kota ve depolama sınırları vardır.
- Bu BBDS 3.0 pilotunda kurumsal tenant izolasyonu, tam kullanıcı yönetimi, MFA/SSO ve üretim düzeyinde güvenlik henüz tamamlanmış değildir. Hassas veri yüklemeyin; internete açık kullanımı sadece kontrollü demo olarak değerlendirin.
- İlk admin kullanıcısı veritabanı ilk kez oluşturulurken oluşturulur. İlk deploy sonrasında parola değiştirme/yenileme mekanizması olmadığı için admin parolasını baştan güçlü seçin.
