# LITUS E-Commerce Demo

LITUS, sahil temalı premium moda markası için gösterimlik (demo) bir e-ticaret web sitesidir. Flask ve SQLite kullanılarak geliştirilmiştir.

## 🎨 Özellikler

- **Premium Tasarım**: Lacivert, altın, krem ve beyaz renk paleti ile modern ve şık arayüz
- **Responsive Tasarım**: Tüm cihazlarda mükemmel görünüm
- **Ürün Yönetimi**: Kategori bazlı ürün listeleme, detay sayfaları
- **Sepet Sistemi**: Session bazlı sepet yönetimi
- **Favoriler**: Kullanıcı favori ürünleri kaydedebilir
- **Yorum Sistemi**: Ürünler için yorum ve beğeni özelliği
- **Admin Panel**: Ürün ve kategori yönetimi için admin paneli
- **Animasyonlar**: AOS ile scroll animasyonları ve parallax efektleri

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

## 🚀 Kurulum

### 1. Projeyi İndirin veya Klonlayın

```bash
cd litus-ecommerce-demo
```

### 2. Sanal Ortam Oluşturun

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Veritabanını Oluşturun ve Seed Verileri Ekleyin

```bash
python init_db.py
```

Bu komut:
- Veritabanını oluşturur (`litus.db`)
- Admin kullanıcısını oluşturur
- Örnek kategorileri ekler
- 12 örnek ürünü ekler

### 5. Uygulamayı Çalıştırın

```bash
flask run
```

veya

```bash
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

## 👤 Admin Paneli

Admin paneline erişim için:

1. Tarayıcınızda `http://localhost:5000/admin` adresine gidin
2. Giriş bilgileri:
   - **Kullanıcı adı:** `admin`
   - **Şifre:** `admin`

### Admin Panel Özellikleri

- **Kategori Yönetimi**: Yeni kategori ekleme ve silme
- **Ürün Yönetimi**: 
  - Ürün ekleme
  - Ürün düzenleme
  - Ürün silme
  - Ürün görseli yükleme

## 📁 Proje Yapısı

```
litus-ecommerce-demo/
├── app.py                 # Ana Flask uygulaması
├── config.py              # Yapılandırma dosyası
├── models.py              # Veritabanı modelleri
├── forms.py               # WTForms formları
├── init_db.py             # Veritabanı seed scripti
├── requirements.txt      # Python bağımlılıkları
├── litus.db              # SQLite veritabanı (oluşturulacak)
├── templates/            # HTML şablonları
│   ├── base.html
│   ├── index.html
│   ├── shop.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── about.html
│   ├── contact.html
│   └── admin/
│       ├── admin_login.html
│       ├── admin_dashboard.html
│       └── admin_product_form.html
└── static/               # Statik dosyalar
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
        └── products/     # Yüklenen ürün görselleri
```

## 🎯 Kullanım

### Ürün Görseli Yükleme

1. Admin paneline giriş yapın
2. "Ürün Ekle" veya mevcut bir ürünü düzenleyin
3. "Ürün Görseli" alanından görsel seçin
4. Desteklenen formatlar: PNG, JPG, JPEG, GIF, WEBP
5. Maksimum dosya boyutu: 16MB
6. Görseller `static/images/products/` klasörüne kaydedilir

### Ürün Ekleme

1. Admin paneline giriş yapın
2. "Ürün Ekle" butonuna tıklayın
3. Formu doldurun:
   - Ürün Adı
   - Slug (URL için, örn: `litus-premium-elbise`)
   - Fiyat
   - Stok
   - Kategori
   - Açıklama
   - Görsel (opsiyonel)
4. "Kaydet" butonuna tıklayın

### Kategori Ekleme

1. Admin paneline giriş yapın
2. "Kategori Ekle" butonuna tıklayın
3. Kategori adı ve slug girin
4. "Ekle" butonuna tıklayın

## 🔧 Yapılandırma

`config.py` dosyasında aşağıdaki ayarları değiştirebilirsiniz:

- `SECRET_KEY`: Flask session güvenliği için
- `UPLOAD_FOLDER`: Görsel yükleme klasörü
- `MAX_CONTENT_LENGTH`: Maksimum dosya boyutu
- `ADMIN_USERNAME` ve `ADMIN_PASSWORD`: Admin giriş bilgileri

## 📝 Notlar

- Bu bir **demo** projedir. Gerçek ödeme işlemi yapılmaz.
- Güvenlik için production ortamında:
  - `SECRET_KEY` değiştirilmeli
  - Admin şifresi güçlü olmalı
  - CSRF koruması aktif edilmeli
  - HTTPS kullanılmalı

## 🐛 Sorun Giderme

### Veritabanı Hatası

Eğer veritabanı hatası alırsanız:

```bash
python init_db.py
```

komutunu tekrar çalıştırın.

### Görsel Yükleme Hatası

`static/images/products/` klasörünün var olduğundan emin olun. Klasör otomatik oluşturulur, ancak manuel olarak da oluşturabilirsiniz.

### Port Zaten Kullanılıyor

Farklı bir port kullanmak için:

```bash
flask run --port 5001
```

## 📄 Lisans

Bu proje demo amaçlıdır ve eğitim/portfolyo için kullanılabilir.

## 👨‍💻 Geliştirici

LITUS E-Commerce Demo - Flask + SQLite ile geliştirilmiştir.

---

**LITUS** - Denizin zarafetini günlük yaşamınıza taşıyoruz.

