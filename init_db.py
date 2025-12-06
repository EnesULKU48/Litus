"""
Veritabanı oluşturma ve seed veri ekleme scripti
"""
from app import app, db
from models import User, Category, Product
from datetime import datetime

def init_db():
    """Veritabanını oluştur ve seed verileri ekle"""
    with app.app_context():
        # Veritabanını oluştur
        db.create_all()
        
        # Admin kullanıcı oluştur
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', is_admin=True)
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin kullanıcı oluşturuldu")
        
        # Kategorileri oluştur
        categories_data = [
            {'name': 'Kadın', 'slug': 'kadin'},
            {'name': 'Erkek', 'slug': 'erkek'},
            {'name': 'Çocuk', 'slug': 'cocuk'},
            {'name': 'Home & Aksesuar', 'slug': 'home-aksesuar'},
            {'name': 'Koleksiyonlar', 'slug': 'koleksiyonlar'}
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = Category.query.filter_by(slug=cat_data['slug']).first()
            if not category:
                category = Category(**cat_data)
                db.session.add(category)
                db.session.commit()
            categories[cat_data['slug']] = category
            print(f"✓ Kategori oluşturuldu: {cat_data['name']}")
        
        # Ürünleri oluştur
        products_data = [
            {
                'name': 'Litus Premium Deniz Mavisi Elbise',
                'slug': 'litus-premium-deniz-mavisi-elbise',
                'price': 1299.00,
                'description': 'Denizin derin mavisi tonlarında, premium kumaştan üretilmiş şık elbise. Sahil temalı zarif tasarım.',
                'stock': 15,
                'category_id': categories['kadin'].id,
                'likes': 42
            },
            {
                'name': 'Litus Klasik Erkek Gömlek',
                'slug': 'litus-klasik-erkek-gomlek',
                'price': 599.00,
                'description': 'Klasik kesim, yumuşak pamuklu kumaş. Günlük kullanım için ideal, şık ve rahat.',
                'stock': 25,
                'category_id': categories['erkek'].id,
                'likes': 38
            },
            {
                'name': 'Litus Çocuk Deniz Kıyısı Tişört',
                'slug': 'litus-cocuk-deniz-kiyisi-tisort',
                'price': 299.00,
                'description': 'Çocuklar için eğlenceli deniz temalı tişört. Yumuşak ve nefes alabilir kumaş.',
                'stock': 30,
                'category_id': categories['cocuk'].id,
                'likes': 25
            },
            {
                'name': 'Litus Premium Altın Aksesuar Seti',
                'slug': 'litus-premium-altin-aksesuar-seti',
                'price': 899.00,
                'description': 'Altın tonlarında zarif aksesuar seti. Sahil temalı özel tasarım.',
                'stock': 12,
                'category_id': categories['home-aksesuar'].id,
                'likes': 35
            },
            {
                'name': 'Litus Özel Koleksiyon Ceket',
                'slug': 'litus-ozel-koleksiyon-ceket',
                'price': 1899.00,
                'description': 'Özel koleksiyon parçası. Premium malzeme, özenli işçilik. Sınırlı sayıda.',
                'stock': 8,
                'category_id': categories['koleksiyonlar'].id,
                'likes': 55
            },
            {
                'name': 'Litus Kadın Sahil Şortu',
                'slug': 'litus-kadin-sahil-sortu',
                'price': 449.00,
                'description': 'Rahat ve şık sahil şortu. Yüksek kalite kumaş, modern kesim.',
                'stock': 20,
                'category_id': categories['kadin'].id,
                'likes': 28
            },
            {
                'name': 'Litus Erkek Denizci Pantolon',
                'slug': 'litus-erkek-denizci-pantolon',
                'price': 799.00,
                'description': 'Klasik denizci tarzı pantolon. Dayanıklı ve şık.',
                'stock': 18,
                'category_id': categories['erkek'].id,
                'likes': 32
            },
            {
                'name': 'Litus Çocuk Deniz Yıldızı Şapka',
                'slug': 'litus-cocuk-deniz-yildizi-sapka',
                'price': 199.00,
                'description': 'Eğlenceli deniz yıldızı desenli şapka. UV korumalı.',
                'stock': 35,
                'category_id': categories['cocuk'].id,
                'likes': 20
            },
            {
                'name': 'Litus Premium Ev Tekstili Seti',
                'slug': 'litus-premium-ev-tekstili-seti',
                'price': 1299.00,
                'description': 'Ev dekorasyonu için premium tekstil seti. Sahil temalı zarif desenler.',
                'stock': 10,
                'category_id': categories['home-aksesuar'].id,
                'likes': 40
            },
            {
                'name': 'Litus Limited Edition Çanta',
                'slug': 'litus-limited-edition-canta',
                'price': 1599.00,
                'description': 'Sınırlı sayıda üretilmiş özel tasarım çanta. Premium deri ve altın detaylar.',
                'stock': 5,
                'category_id': categories['koleksiyonlar'].id,
                'likes': 48
            },
            {
                'name': 'Litus Kadın Özel Tasarım Etek',
                'slug': 'litus-kadin-ozel-tasarim-etek',
                'price': 699.00,
                'description': 'Özel tasarım, sahil temalı zarif etek. Yüksek kalite kumaş.',
                'stock': 15,
                'category_id': categories['kadin'].id,
                'likes': 30
            },
            {
                'name': 'Litus Erkek Premium Polo',
                'slug': 'litus-erkek-premium-polo',
                'price': 549.00,
                'description': 'Premium polo yaka tişört. Klasik ve şık tasarım.',
                'stock': 22,
                'category_id': categories['erkek'].id,
                'likes': 27
            }
        ]
        
        for prod_data in products_data:
            product = Product.query.filter_by(slug=prod_data['slug']).first()
            if not product:
                # Placeholder görsel dosya adı (gerçek görsel yoksa)
                prod_data['image_filename'] = None
                product = Product(**prod_data)
                db.session.add(product)
                db.session.commit()
                print(f"✓ Ürün oluşturuldu: {prod_data['name']}")
        
        print("\n✓ Veritabanı başarıyla oluşturuldu ve seed veriler eklendi!")
        print(f"✓ Toplam {len(categories_data)} kategori")
        print(f"✓ Toplam {len(products_data)} ürün")
        print("\nAdmin giriş bilgileri:")
        print("  Kullanıcı adı: admin")
        print("  Şifre: admin")

if __name__ == '__main__':
    init_db()

