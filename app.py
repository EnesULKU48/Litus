from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'litus-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Upload klasörünü oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Veritabanı bağlantısı
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Veritabanını başlat
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Categories tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    # Products tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image TEXT,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    
    # Comments tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_id INTEGER,
            username TEXT NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Users tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cart tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    # Favorites tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id),
            UNIQUE(user_id, product_id)
        )
    ''')
    
    # Admin kullanıcısı oluştur
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
    if cursor.fetchone()[0] == 0:
        admin_password = generate_password_hash('admin')
        cursor.execute('INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)',
                      ('admin', 'admin@litus.com', admin_password, 1))
    
    # Veritabanı migration - eksik kolonları ekle
    try:
        # Comments tablosuna user_id kolonu ekle (eğer yoksa)
        cursor.execute("PRAGMA table_info(comments)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'user_id' not in columns:
            cursor.execute('ALTER TABLE comments ADD COLUMN user_id INTEGER')
            conn.commit()
    except Exception as e:
        print(f"Migration hatası: {e}")
    
    # Örnek kategoriler ekle
    cursor.execute('SELECT COUNT(*) FROM categories')
    if cursor.fetchone()[0] == 0:
        categories = ['Kadın', 'Erkek', 'Çocuk', 'Aksesuar', 'Koleksiyon']
        for cat in categories:
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (cat,))
    
    conn.commit()
    conn.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bu sayfaya erişmek için giriş yapmalısınız!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bu sayfaya erişmek için giriş yapmalısınız!', 'error')
            return redirect(url_for('login'))
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT is_admin FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        conn.close()
        if not user or user['is_admin'] != 1:
            flash('Bu sayfaya erişim yetkiniz yok!', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor - tüm template'lere categories ve user bilgisi ekle
@app.context_processor
def inject_categories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    
    user = None
    if 'user_id' in session:
        cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
    
    conn.close()
    return dict(categories=categories, current_user=user)

# ==================== AUTH ROUTES ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not username or not email or not password:
            flash('Lütfen tüm alanları doldurun!', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Şifreler eşleşmiyor!', 'error')
            return redirect(url_for('register'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Kullanıcı adı kontrolü
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            flash('Bu kullanıcı adı zaten kullanılıyor!', 'error')
            conn.close()
            return redirect(url_for('register'))
        
        # Email kontrolü
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            flash('Bu e-posta adresi zaten kullanılıyor!', 'error')
            conn.close()
            return redirect(url_for('register'))
        
        # Kullanıcı oluştur
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                      (username, email, hashed_password))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        session['user_id'] = user_id
        session['username'] = username
        flash('Kayıt başarılı! Hoş geldiniz!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Lütfen kullanıcı adı ve şifre girin!', 'error')
            return redirect(url_for('login'))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            
            if user['is_admin'] == 1:
                flash('Admin paneline hoş geldiniz!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Giriş başarılı! Hoş geldiniz!', 'success')
                return redirect(url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Çıkış yapıldı!', 'success')
    return redirect(url_for('index'))

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    # Kategorileri al
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    
    # Öne çıkan ürünler (ilk 8 ürün)
    cursor.execute('SELECT * FROM products ORDER BY id DESC LIMIT 8')
    featured_products = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', categories=categories, featured_products=featured_products)

@app.route('/category/<int:category_id>')
def category(category_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Kategori bilgisi
    cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
    category = cursor.fetchone()
    
    if not category:
        flash('Kategori bulunamadı!', 'error')
        return redirect(url_for('index'))
    
    # Kategoriye ait ürünler
    cursor.execute('SELECT * FROM products WHERE category_id = ?', (category_id,))
    products = cursor.fetchall()
    
    conn.close()
    return render_template('category.html', category=category, products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Ürün bilgisi
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        flash('Ürün bulunamadı!', 'error')
        return redirect(url_for('index'))
    
    # Ürün yorumları
    # user_id kolonu varsa JOIN yap, yoksa sadece username kullan
    try:
        cursor.execute("PRAGMA table_info(comments)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'user_id' in columns:
            cursor.execute('SELECT c.*, u.username as user_username FROM comments c LEFT JOIN users u ON c.user_id = u.id WHERE c.product_id = ? ORDER BY c.created_at DESC', (product_id,))
        else:
            cursor.execute('SELECT * FROM comments WHERE product_id = ? ORDER BY created_at DESC', (product_id,))
    except Exception as e:
        # Hata durumunda basit sorgu
        print(f"Yorum sorgusu hatası: {e}")
        cursor.execute('SELECT * FROM comments WHERE product_id = ? ORDER BY created_at DESC', (product_id,))
    comments = cursor.fetchall()
    
    # Favori kontrolü
    is_favorite = False
    if 'user_id' in session:
        cursor.execute('SELECT id FROM favorites WHERE user_id = ? AND product_id = ?', 
                     (session['user_id'], product_id))
        is_favorite = cursor.fetchone() is not None
    
    conn.close()
    return render_template('product_detail.html', product=product, comments=comments, is_favorite=is_favorite)

@app.route('/product/<int:product_id>/comment', methods=['POST'])
@login_required
def add_comment(product_id):
    comment = request.form.get('comment', '').strip()
    
    if not comment:
        flash('Lütfen yorum yazın!', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # user_id kolonu varsa ekle, yoksa sadece username kullan
    try:
        cursor.execute("PRAGMA table_info(comments)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'user_id' in columns:
            cursor.execute('INSERT INTO comments (product_id, user_id, username, comment) VALUES (?, ?, ?, ?)',
                          (product_id, session['user_id'], session['username'], comment))
        else:
            cursor.execute('INSERT INTO comments (product_id, username, comment) VALUES (?, ?, ?)',
                          (product_id, session['username'], comment))
    except Exception as e:
        print(f"Yorum ekleme hatası: {e}")
        # Fallback - sadece username ile ekle
        cursor.execute('INSERT INTO comments (product_id, username, comment) VALUES (?, ?, ?)',
                      (product_id, session['username'], comment))
    
    conn.commit()
    conn.close()
    
    flash('Yorumunuz eklendi!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

# ==================== CART & FAVORITES API ====================

@app.route('/api/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Mevcut sepet öğesini kontrol et
    cursor.execute('SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?',
                  (session['user_id'], product_id))
    existing = cursor.fetchone()
    
    if existing:
        new_quantity = existing['quantity'] + quantity
        cursor.execute('UPDATE cart SET quantity = ? WHERE id = ?', (new_quantity, existing['id']))
    else:
        cursor.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)',
                      (session['user_id'], product_id, quantity))
    
    conn.commit()
    
    # Sepet sayısını al
    cursor.execute('SELECT COUNT(*) as count FROM cart WHERE user_id = ?', (session['user_id'],))
    cart_count = cursor.fetchone()['count']
    
    conn.close()
    return jsonify({'success': True, 'message': 'Ürün sepete eklendi', 'cart_count': cart_count})

@app.route('/api/toggle-favorite', methods=['POST'])
@login_required
def toggle_favorite():
    data = request.get_json()
    product_id = data.get('product_id')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Favori kontrolü
    cursor.execute('SELECT id FROM favorites WHERE user_id = ? AND product_id = ?',
                  (session['user_id'], product_id))
    favorite = cursor.fetchone()
    
    if favorite:
        cursor.execute('DELETE FROM favorites WHERE id = ?', (favorite['id'],))
        is_favorite = False
    else:
        cursor.execute('INSERT INTO favorites (user_id, product_id) VALUES (?, ?)',
                      (session['user_id'], product_id))
        is_favorite = True
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'is_favorite': is_favorite})

@app.route('/cart')
@login_required
def cart():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.*, p.name, p.price, p.image 
        FROM cart c 
        JOIN products p ON c.product_id = p.id 
        WHERE c.user_id = ?
    ''', (session['user_id'],))
    cart_items = cursor.fetchall()
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    conn.close()
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/api/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    data = request.get_json()
    cart_id = data.get('cart_id')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart WHERE id = ? AND user_id = ?', (cart_id, session['user_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/update-cart', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json()
    cart_id = data.get('cart_id')
    quantity = int(data.get('quantity', 1))
    
    conn = get_db()
    cursor = conn.cursor()
    
    if quantity <= 0:
        cursor.execute('DELETE FROM cart WHERE id = ? AND user_id = ?', (cart_id, session['user_id']))
    else:
        cursor.execute('UPDATE cart SET quantity = ? WHERE id = ? AND user_id = ?',
                      (quantity, cart_id, session['user_id']))
    
    conn.commit()
    
    # Yeni toplamı hesapla
    cursor.execute('''
        SELECT SUM(p.price * c.quantity) as total 
        FROM cart c 
        JOIN products p ON c.product_id = p.id 
        WHERE c.user_id = ?
    ''', (session['user_id'],))
    total = cursor.fetchone()['total'] or 0
    
    conn.close()
    return jsonify({'success': True, 'total': total})

@app.route('/favorites')
@login_required
def favorites():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, f.id as favorite_id
        FROM favorites f
        JOIN products p ON f.product_id = p.id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC
    ''', (session['user_id'],))
    favorite_products = cursor.fetchall()
    
    conn.close()
    return render_template('favorites.html', favorite_products=favorite_products)

# ==================== ADMIN PANEL ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username == 'admin' and password == 'admin':
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['is_admin'] = 1
                flash('Admin paneline hoş geldiniz!', 'success')
                return redirect(url_for('admin_dashboard'))
        
        flash('Kullanıcı adı veya şifre hatalı!', 'error')
        return redirect(url_for('admin_login'))
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM products ORDER BY id DESC')
    products = cursor.fetchall()
    
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    
    conn.close()
    return render_template('admin_dashboard.html', products=products, categories=categories)

@app.route('/admin/add-product', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = request.form.get('price', '').strip()
        description = request.form.get('description', '').strip()
        category_id = request.form.get('category_id', '').strip()
        file = request.files.get('image')
        
        if not name or not price or not category_id:
            flash('Lütfen zorunlu alanları doldurun!', 'error')
            return redirect(url_for('admin_add_product'))
        
        try:
            price = float(price)
        except ValueError:
            flash('Geçerli bir fiyat girin!', 'error')
            return redirect(url_for('admin_add_product'))
        
        # Görsel yükleme
        image_filename = None
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            file.save(filepath)
        
        # Veritabanına kaydet
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, price, description, image, category_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, price, description, image_filename, category_id))
        conn.commit()
        conn.close()
        
        flash('Ürün başarıyla eklendi!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    # GET request - formu göster
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    conn.close()
    
    return render_template('admin_add_product.html', categories=categories)

@app.route('/admin/delete-product/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Ürün bilgisini al (görsel dosyasını silmek için)
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        flash('Ürün bulunamadı!', 'error')
        conn.close()
        return redirect(url_for('admin_dashboard'))
    
    # İlgili yorumları sil
    cursor.execute('DELETE FROM comments WHERE product_id = ?', (product_id,))
    
    # Sepetten sil
    cursor.execute('DELETE FROM cart WHERE product_id = ?', (product_id,))
    
    # Favorilerden sil
    cursor.execute('DELETE FROM favorites WHERE product_id = ?', (product_id,))
    
    # Ürünü sil
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    
    conn.commit()
    conn.close()
    
    # Görsel dosyasını sil (varsa)
    if product['image']:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product['image'])
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"Görsel silme hatası: {e}")
    
    flash('Ürün başarıyla silindi!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
