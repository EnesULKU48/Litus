from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
import uuid
from datetime import datetime
from functools import wraps

from config import *
from models import db, User, Category, Product, Comment, CartItem
from forms import ProductForm, CategoryForm, CommentForm, ContactForm

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

db.init_app(app)

# Upload klasörünü oluştur
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Dosya uzantısı kontrolü"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_or_create_session_id():
    """Session ID oluştur veya mevcut olanı al"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']


def admin_required(f):
    """Admin yetkisi kontrolü decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ANA SAYFALAR ====================

@app.route('/')
def index():
    """Ana sayfa"""
    # Öne çıkan ürünler
    featured_products = Product.query.order_by(Product.likes.desc()).limit(6).all()
    new_products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    categories = Category.query.all()
    
    return render_template('index.html', 
                         featured_products=featured_products,
                         new_products=new_products,
                         categories=categories)


@app.route('/shop')
def shop():
    """Ürün listeleme sayfası"""
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    
    query = Product.query
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.all()
    categories = Category.query.all()
    
    return render_template('shop.html', 
                         products=products,
                         categories=categories,
                         selected_category=category_id,
                         search=search)


@app.route('/product/<slug>')
def product_detail(slug):
    """Ürün detay sayfası"""
    product = Product.query.filter_by(slug=slug).first_or_404()
    comments = Comment.query.filter_by(product_id=product.id).order_by(Comment.created_at.desc()).all()
    form = CommentForm()
    
    return render_template('product_detail.html', 
                         product=product,
                         comments=comments,
                         form=form)


@app.route('/cart')
def cart():
    """Sepet sayfası"""
    session_id = get_or_create_session_id()
    cart_items = CartItem.query.filter_by(session_id=session_id).all()
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/about')
def about():
    """Hakkımızda sayfası"""
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """İletişim sayfası"""
    form = ContactForm()
    if form.validate_on_submit():
        # Form verilerini logla (gerçek e-posta gönderme yok)
        print(f"İletişim Formu - {datetime.now()}")
        print(f"Ad: {form.name.data}")
        print(f"E-posta: {form.email.data}")
        print(f"Konu: {form.subject.data}")
        print(f"Mesaj: {form.message.data}")
        flash('Mesajınız alındı! En kısa sürede size dönüş yapacağız.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)


# ==================== API ENDPOINTS ====================

@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    """Sepete ürün ekle"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    product = Product.query.get_or_404(product_id)
    session_id = get_or_create_session_id()
    
    # Mevcut sepet öğesini kontrol et
    cart_item = CartItem.query.filter_by(
        session_id=session_id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            session_id=session_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    # Sepet toplamını hesapla
    cart_count = CartItem.query.filter_by(session_id=session_id).count()
    
    return jsonify({
        'success': True,
        'message': 'Ürün sepete eklendi',
        'cart_count': cart_count
    })


@app.route('/api/update-cart', methods=['POST'])
def update_cart():
    """Sepet öğesi güncelle"""
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    
    cart_item = CartItem.query.get_or_404(item_id)
    session_id = get_or_create_session_id()
    
    if cart_item.session_id != session_id:
        return jsonify({'success': False, 'message': 'Yetkisiz işlem'}), 403
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    
    # Yeni toplamı hesapla
    cart_items = CartItem.query.filter_by(session_id=session_id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return jsonify({
        'success': True,
        'total': float(total),
        'item_total': float(cart_item.product.price * cart_item.quantity) if quantity > 0 else 0
    })


@app.route('/api/remove-from-cart', methods=['POST'])
def remove_from_cart():
    """Sepetten ürün sil"""
    data = request.get_json()
    item_id = data.get('item_id')
    
    cart_item = CartItem.query.get_or_404(item_id)
    session_id = get_or_create_session_id()
    
    if cart_item.session_id != session_id:
        return jsonify({'success': False, 'message': 'Yetkisiz işlem'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    
    cart_count = CartItem.query.filter_by(session_id=session_id).count()
    cart_items = CartItem.query.filter_by(session_id=session_id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return jsonify({
        'success': True,
        'cart_count': cart_count,
        'total': float(total)
    })


@app.route('/api/toggle-favorite', methods=['POST'])
def toggle_favorite():
    """Favori ekle/çıkar"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    if 'favorites' not in session:
        session['favorites'] = []
    
    favorites = session['favorites']
    
    if product_id in favorites:
        favorites.remove(product_id)
        is_favorite = False
    else:
        favorites.append(product_id)
        is_favorite = True
    
    session['favorites'] = favorites
    
    return jsonify({
        'success': True,
        'is_favorite': is_favorite
    })


@app.route('/api/like-product', methods=['POST'])
def like_product():
    """Ürün beğen"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    product = Product.query.get_or_404(product_id)
    product.likes += 1
    db.session.commit()
    
    return jsonify({
        'success': True,
        'likes': product.likes
    })


@app.route('/api/add-comment', methods=['POST'])
def add_comment():
    """Yorum ekle"""
    data = request.get_json()
    product_id = data.get('product_id')
    author_name = data.get('author_name')
    content = data.get('content')
    
    if not author_name or not content:
        return jsonify({'success': False, 'message': 'Ad ve yorum gereklidir'}), 400
    
    comment = Comment(
        product_id=product_id,
        author_name=author_name,
        content=content
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'comment': {
            'id': comment.id,
            'author_name': comment.author_name,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M')
        }
    })


# ==================== ADMIN PANEL ====================

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    """Admin giriş"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!', 'error')
    
    return render_template('admin/admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin çıkış"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin panel ana sayfa"""
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('admin/admin_dashboard.html', 
                         products=products,
                         categories=categories)


@app.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Ürün ekle"""
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        # Görsel yükleme
        image_filename = None
        if form.image.data:
            file = form.image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Benzersiz isim oluştur
                unique_filename = f"{uuid.uuid4()}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                image_filename = unique_filename
        
        product = Product(
            name=form.name.data,
            slug=form.slug.data,
            price=form.price.data,
            description=form.description.data,
            stock=form.stock.data,
            category_id=form.category_id.data,
            image_filename=image_filename
        )
        
        db.session.add(product)
        db.session.commit()
        flash('Ürün başarıyla eklendi!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/admin_product_form.html', form=form, title='Ürün Ekle')


@app.route('/admin/product/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(id):
    """Ürün düzenle"""
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.slug = form.slug.data
        product.price = form.price.data
        product.description = form.description.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        
        # Yeni görsel yüklendiyse
        if form.image.data:
            file = form.image.data
            if file and allowed_file(file.filename):
                # Eski görseli sil
                if product.image_filename:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                product.image_filename = unique_filename
        
        db.session.commit()
        flash('Ürün başarıyla güncellendi!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/admin_product_form.html', form=form, product=product, title='Ürün Düzenle')


@app.route('/admin/product/delete/<int:id>', methods=['POST'])
@admin_required
def admin_delete_product(id):
    """Ürün sil"""
    product = Product.query.get_or_404(id)
    
    # Görseli sil
    if product.image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    flash('Ürün başarıyla silindi!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/category/add', methods=['POST'])
@admin_required
def admin_add_category():
    """Kategori ekle"""
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            slug=form.slug.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Kategori başarıyla eklendi!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/category/delete/<int:id>', methods=['POST'])
@admin_required
def admin_delete_category(id):
    """Kategori sil"""
    category = Category.query.get_or_404(id)
    
    # Kategoriye ait ürünler varsa silinemez
    if category.products:
        flash('Bu kategoriye ait ürünler olduğu için silinemez!', 'error')
        return redirect(url_for('admin_dashboard'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Kategori başarıyla silindi!', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

