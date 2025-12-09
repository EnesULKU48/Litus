"""
Veritabanı migration scripti
Mevcut veritabanına eksik kolonları ekler
"""
import sqlite3
import os

def migrate_database():
    db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print("Veritabanı bulunamadı. Lütfen önce uygulamayı çalıştırın.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Comments tablosundaki kolonları kontrol et
        cursor.execute("PRAGMA table_info(comments)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("user_id kolonu ekleniyor...")
            cursor.execute('ALTER TABLE comments ADD COLUMN user_id INTEGER')
            conn.commit()
            print("✓ user_id kolonu eklendi!")
        else:
            print("✓ user_id kolonu zaten mevcut.")
        
        # Users tablosunu kontrol et
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("Users tablosu oluşturuluyor...")
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    is_admin INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("✓ Users tablosu oluşturuldu!")
        
        # Cart tablosunu kontrol et
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cart'")
        if not cursor.fetchone():
            print("Cart tablosu oluşturuluyor...")
            cursor.execute('''
                CREATE TABLE cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            ''')
            conn.commit()
            print("✓ Cart tablosu oluşturuldu!")
        
        # Favorites tablosunu kontrol et
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='favorites'")
        if not cursor.fetchone():
            print("Favorites tablosu oluşturuluyor...")
            cursor.execute('''
                CREATE TABLE favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    UNIQUE(user_id, product_id)
                )
            ''')
            conn.commit()
            print("✓ Favorites tablosu oluşturuldu!")
        
        print("\n✓ Migration tamamlandı!")
        
    except Exception as e:
        print(f"Migration hatası: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()

