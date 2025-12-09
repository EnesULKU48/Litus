# LITUS Store - Ultra Premium Fashion E-Commerce Demo

Ultra-premium fashion brand demo website built with Flask and SQLite. Inspired by Gucci, Louis Vuitton, and Prada design aesthetics.

## 🎨 Features

- **Ultra-Premium Design**: Black & gold luxury theme
- **Full-Screen Hero Section**: Massive hero banner with smooth animations
- **Parallax Effects**: Smooth parallax scrolling throughout
- **Product Showcase**: Beautiful product grid with hover effects
- **Category Pages**: Dedicated category browsing
- **Product Details**: Large product images with comment system
- **Admin Panel**: Simple product management
- **Responsive Design**: Works on all devices

## 📋 Requirements

- Python 3.8 or higher
- pip

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
cd litus-ecommerce-demo
```

### 2. Create Virtual Environment (Optional but Recommended)

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The application will automatically:
- Create the SQLite database (`database.db`)
- Create necessary tables (categories, products, comments)
- Add sample categories
- Create the `static/uploads/` folder for product images

### 5. Access the Website

Open your browser and go to: `http://localhost:5000`

## 📁 Project Structure

```
litus-ecommerce-demo/
├── app.py                      # Main Flask application
├── database.db                 # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── static/
│   ├── css/
│   │   └── style.css          # Ultra-premium styling
│   ├── js/
│   │   └── main.js            # Animations & interactions
│   ├── images/
│   │   └── Litus_amblem.jpeg  # Logo
│   └── uploads/               # Product images (auto-created)
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Homepage
    ├── category.html          # Category page
    ├── product_detail.html    # Product detail page
    └── admin_add_product.html # Admin panel
```

## 🎯 Usage

### Adding Products (Admin Panel)

1. Navigate to: `http://localhost:5000/admin/add-product`
2. Fill in the form:
   - Product Name (required)
   - Price (required)
   - Category (required)
   - Description (optional)
   - Product Image (optional - PNG, JPG, JPEG, GIF, WEBP)
3. Click "Ürünü Kaydet" (Save Product)

### Viewing Products

- **Homepage**: Shows featured products (latest 8 products)
- **Categories**: Click on any category card to view products in that category
- **Product Detail**: Click on any product to see full details and comments

### Adding Comments

1. Go to any product detail page
2. Fill in your name and comment
3. Click "Yorum Yap" (Add Comment)

## 🎨 Design Features

- **Color Scheme**: Black (#000000) and Gold (#D4AF37)
- **Typography**: Playfair Display (headings) + Montserrat (body)
- **Animations**: Smooth fade-in, parallax, and hover effects
- **Layout**: Ultra-wide hero, grid-based product display
- **Effects**: Gold glow on logo hover, smooth scroll, progress indicator

## 📝 Database Schema

### Categories Table
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT)

### Products Table
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT)
- `price` (REAL)
- `description` (TEXT)
- `image` (TEXT - filename)
- `category_id` (INTEGER - foreign key)

### Comments Table
- `id` (INTEGER PRIMARY KEY)
- `product_id` (INTEGER - foreign key)
- `username` (TEXT)
- `comment` (TEXT)
- `created_at` (TIMESTAMP)

## 🔧 Configuration

Edit `app.py` to modify:
- Upload folder location
- Maximum file size
- Allowed file extensions
- Secret key

## 📱 Responsive Breakpoints

- Desktop: 1400px+
- Tablet: 768px - 968px
- Mobile: < 768px

## 🐛 Troubleshooting

### Database Errors
If you encounter database errors, delete `database.db` and restart the app. It will recreate the database automatically.

### Image Upload Issues
- Ensure `static/uploads/` folder exists (created automatically)
- Check file size (max 16MB)
- Verify file format (PNG, JPG, JPEG, GIF, WEBP)

### Port Already in Use
Run on a different port:
```bash
flask run --port 5001
```

## 📄 License

This is a demo project for portfolio/educational purposes.

## 👨‍💻 Developer Notes

- This is a **visual showcase** project, not a full e-commerce solution
- No payment processing
- No user authentication (admin panel is open)
- Simple SQLite database (suitable for demo purposes)
- All images are stored locally in `static/uploads/`

---

**LITUS** - Ultra Premium Fashion
