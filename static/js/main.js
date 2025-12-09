// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initParallax();
    initScrollAnimations();
    initFlashMessages();
    initSmoothScroll();
    initCartAndFavorites();
    initDropdowns();
    initMobileMenu();
    updateCartCount();
});

// ==================== NAVBAR ====================
function initNavbar() {
    const navbar = document.getElementById('navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
    
    // Logo hover glow effect
    const logoImg = document.querySelector('.logo-img');
    if (logoImg) {
        logoImg.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    }
}

// ==================== PARALLAX EFFECTS ====================
function initParallax() {
    const hero = document.getElementById('hero');
    const storySection = document.querySelector('.story-section');
    
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * 0.5;
            
            if (scrolled < window.innerHeight) {
                hero.style.transform = `translateY(${rate}px)`;
            }
        });
    }
    
    if (storySection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const storyOffset = storySection.offsetTop;
            const windowHeight = window.innerHeight;
            
            if (scrolled + windowHeight > storyOffset && scrolled < storyOffset + storySection.offsetHeight) {
                const parallaxRate = (scrolled - storyOffset + windowHeight) * 0.3;
                const background = storySection.querySelector('.story-background');
                if (background) {
                    background.style.transform = `translateY(${parallaxRate}px)`;
                }
            }
        });
    }
}

// ==================== SCROLL ANIMATIONS ====================
function initScrollAnimations() {
    // AOS (Animate On Scroll) benzeri basit implementasyon
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Tüm animasyonlu elementleri bul
    const animatedElements = document.querySelectorAll('[data-aos]');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        
        const delay = el.getAttribute('data-aos-delay') || 0;
        el.style.transitionDelay = `${delay}ms`;
        
        observer.observe(el);
    });
    
    // Product cards için özel animasyon
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        card.style.transitionDelay = `${index * 100}ms`;
        
        observer.observe(card);
    });
}

// ==================== SMOOTH SCROLL ====================
function initSmoothScroll() {
    // Hero scroll button
    const heroScroll = document.querySelector('.hero-scroll');
    if (heroScroll) {
        heroScroll.addEventListener('click', function() {
            const productsSection = document.getElementById('products');
            if (productsSection) {
                productsSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }
    
    // Tüm anchor linkler için smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// ==================== FLASH MESSAGES ====================
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        const closeBtn = message.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (message.parentNode) {
                message.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }
        }, 5000);
    });
}

// Slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ==================== PRODUCT CARD HOVER EFFECTS ====================
document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
    });
});

// ==================== PARALLAX ON MOUSE MOVE ====================
document.addEventListener('mousemove', function(e) {
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    // Hero section subtle parallax
    const hero = document.getElementById('hero');
    if (hero && window.pageYOffset < window.innerHeight) {
        const heroContent = hero.querySelector('.hero-content');
        if (heroContent) {
            const moveX = (mouseX - 0.5) * 20;
            const moveY = (mouseY - 0.5) * 20;
            heroContent.style.transform = `translate(${moveX}px, ${moveY}px)`;
        }
    }
});

// ==================== LAZY LOADING IMAGES ====================
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ==================== SCROLL PROGRESS INDICATOR ====================
function createScrollProgress() {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 2px;
        background: linear-gradient(90deg, #D4AF37, #F4D03F);
        z-index: 9999;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', function() {
        const windowHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrolled = (window.pageYOffset / windowHeight) * 100;
        progressBar.style.width = scrolled + '%';
    });
}

createScrollProgress();

// ==================== CURSOR EFFECT (OPTIONAL - Premium feel) ====================
function initCustomCursor() {
    if (window.innerWidth > 768) {
        const cursor = document.createElement('div');
        cursor.className = 'custom-cursor';
        cursor.style.cssText = `
            width: 20px;
            height: 20px;
            border: 2px solid #D4AF37;
            border-radius: 50%;
            position: fixed;
            pointer-events: none;
            z-index: 9999;
            transition: transform 0.2s ease;
            display: none;
        `;
        document.body.appendChild(cursor);
        
        document.addEventListener('mousemove', function(e) {
            cursor.style.left = e.clientX - 10 + 'px';
            cursor.style.top = e.clientY - 10 + 'px';
            cursor.style.display = 'block';
        });
        
        document.querySelectorAll('a, button, .product-card').forEach(el => {
            el.addEventListener('mouseenter', function() {
                cursor.style.transform = 'scale(1.5)';
                cursor.style.borderColor = '#F4D03F';
            });
            el.addEventListener('mouseleave', function() {
                cursor.style.transform = 'scale(1)';
                cursor.style.borderColor = '#D4AF37';
            });
        });
    }
}

// Uncomment to enable custom cursor
// initCustomCursor();

// ==================== DROPDOWN MENUS ====================
function initDropdowns() {
    const dropdowns = document.querySelectorAll('.nav-dropdown');
    
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (toggle && menu) {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Diğer dropdown'ları kapat
                dropdowns.forEach(other => {
                    if (other !== dropdown) {
                        other.classList.remove('active');
                    }
                });
                
                // Bu dropdown'ı toggle et
                dropdown.classList.toggle('active');
            });
        }
    });
    
    // Dışarı tıklanınca kapat
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.nav-dropdown')) {
            dropdowns.forEach(dropdown => dropdown.classList.remove('active'));
        }
    });
}

// ==================== CART & FAVORITES ====================
function initCartAndFavorites() {
    // Sepete ekle butonları
    document.querySelectorAll('.btn-add-cart, #addToCartBtn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const productId = this.getAttribute('data-product-id');
            if (productId) {
                addToCart(productId, 1);
            }
        });
    });
    
    // Favori butonları
    document.querySelectorAll('.btn-favorite, #toggleFavoriteBtn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const productId = this.getAttribute('data-product-id');
            if (productId) {
                toggleFavorite(productId);
            }
        });
    });
    
    // Sepet sayfası butonları
    document.querySelectorAll('.increase-qty').forEach(btn => {
        btn.addEventListener('click', function() {
            const cartId = this.getAttribute('data-cart-id');
            const item = this.closest('.cart-item');
            const quantityEl = item.querySelector('.quantity-value');
            const currentQty = parseInt(quantityEl.textContent);
            updateCartQuantity(cartId, currentQty + 1);
        });
    });
    
    document.querySelectorAll('.decrease-qty').forEach(btn => {
        btn.addEventListener('click', function() {
            const cartId = this.getAttribute('data-cart-id');
            const item = this.closest('.cart-item');
            const quantityEl = item.querySelector('.quantity-value');
            const currentQty = parseInt(quantityEl.textContent);
            if (currentQty > 1) {
                updateCartQuantity(cartId, currentQty - 1);
            }
        });
    });
    
    document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', function() {
            const cartId = this.getAttribute('data-cart-id');
            if (confirm('Bu ürünü sepetten çıkarmak istediğinize emin misiniz?')) {
                removeFromCart(cartId);
            }
        });
    });
}

function addToCart(productId, quantity) {
    fetch('/api/add-to-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: parseInt(productId),
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Ürün sepete eklendi!', 'success');
            updateCartCount();
            
            // Buton görünümünü güncelle
            const btn = document.querySelector(`[data-product-id="${productId}"].btn-add-cart, #addToCartBtn`);
            if (btn) {
                const originalHTML = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Eklendi';
                btn.style.backgroundColor = '#28a745';
                setTimeout(() => {
                    btn.innerHTML = originalHTML;
                    btn.style.backgroundColor = '';
                }, 2000);
            }
        } else {
            if (data.message && data.message.includes('giriş')) {
                window.location.href = '/login';
            } else {
                showNotification(data.message || 'Bir hata oluştu!', 'error');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Bir hata oluştu!', 'error');
    });
}

function toggleFavorite(productId) {
    fetch('/api/toggle-favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: parseInt(productId)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const btn = document.querySelector(`[data-product-id="${productId}"].btn-favorite, #toggleFavoriteBtn`);
            const icon = btn ? btn.querySelector('i') : null;
            const text = btn ? btn.querySelector('#favoriteText') : null;
            
            if (data.is_favorite) {
                showNotification('Favorilere eklendi!', 'success');
                if (icon) {
                    icon.classList.remove('far', 'fa-heart-o');
                    icon.classList.add('fas', 'fa-heart');
                }
                if (text) text.textContent = 'Favorilerden Çıkar';
                if (btn) btn.classList.add('active');
            } else {
                showNotification('Favorilerden çıkarıldı!', 'success');
                if (icon) {
                    icon.classList.remove('fas', 'fa-heart');
                    icon.classList.add('far', 'fa-heart-o');
                }
                if (text) text.textContent = 'Favorilere Ekle';
                if (btn) btn.classList.remove('active');
                
                // Eğer favoriler sayfasındaysak, ürünü listeden kaldır
                if (window.location.pathname === '/favorites') {
                    const productCard = btn ? btn.closest('.product-card') : null;
                    if (productCard) {
                        productCard.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                        productCard.style.opacity = '0';
                        productCard.style.transform = 'scale(0.9)';
                        setTimeout(() => {
                            productCard.remove();
                            // Eğer favori kalmadıysa sayfayı yenile
                            const remainingFavorites = document.querySelectorAll('.product-card');
                            if (remainingFavorites.length === 0) {
                                setTimeout(() => location.reload(), 500);
                            }
                        }, 300);
                    }
                }
            }
        } else {
            if (data.message && data.message.includes('giriş')) {
                window.location.href = '/login';
            } else {
                showNotification(data.message || 'Bir hata oluştu!', 'error');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Bir hata oluştu!', 'error');
    });
}

function updateCartQuantity(cartId, quantity) {
    fetch('/api/update-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            cart_id: parseInt(cartId),
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const item = document.querySelector(`[data-cart-id="${cartId}"]`);
            if (item) {
                const quantityEl = item.querySelector('.quantity-value');
                const priceEl = item.querySelector('.cart-item-price');
                
                if (quantityEl) quantityEl.textContent = quantity;
                
                // Toplamı güncelle
                if (data.total !== undefined) {
                    document.getElementById('subtotal').textContent = data.total.toFixed(2) + ' ₺';
                    document.getElementById('total').textContent = data.total.toFixed(2) + ' ₺';
                }
                
                if (quantity === 0) {
                    item.style.opacity = '0';
                    setTimeout(() => item.remove(), 300);
                    updateCartCount();
                }
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Bir hata oluştu!', 'error');
    });
}

function removeFromCart(cartId) {
    fetch('/api/remove-from-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            cart_id: parseInt(cartId)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const item = document.querySelector(`[data-cart-id="${cartId}"]`);
            if (item) {
                // Fiyatı al
                const priceText = item.querySelector('.cart-item-price');
                const price = priceText ? parseFloat(priceText.textContent.replace(' ₺', '').replace(',', '.')) : 0;
                
                item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                item.style.opacity = '0';
                item.style.transform = 'translateX(-20px)';
                
                setTimeout(() => {
                    item.remove();
                    updateCartCount();
                    
                    // Toplamı güncelle
                    const subtotalEl = document.getElementById('subtotal');
                    const totalEl = document.getElementById('total');
                    if (subtotalEl && totalEl) {
                        const currentTotal = parseFloat(subtotalEl.textContent.replace(' ₺', '').replace(',', '.'));
                        const newTotal = Math.max(0, currentTotal - price);
                        subtotalEl.textContent = newTotal.toFixed(2) + ' ₺';
                        totalEl.textContent = newTotal.toFixed(2) + ' ₺';
                    }
                    
                    // Eğer sepet boşsa sayfayı yenile
                    const remainingItems = document.querySelectorAll('.cart-item');
                    if (remainingItems.length === 0) {
                        setTimeout(() => location.reload(), 500);
                    }
                }, 300);
            }
            showNotification('Ürün sepetten çıkarıldı!', 'success');
        } else {
            showNotification('Bir hata oluştu!', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Bir hata oluştu!', 'error');
    });
}

function updateCartCount() {
    fetch('/cart')
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const cartItems = doc.querySelectorAll('.cart-item');
            const count = cartItems.length;
            
            const cartCountEl = document.getElementById('navCartCount');
            if (cartCountEl) {
                cartCountEl.textContent = count;
                cartCountEl.style.display = count > 0 ? 'inline-block' : 'none';
            }
        })
        .catch(error => {
            console.error('Error updating cart count:', error);
        });
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `flash-message flash-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 9999;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        animation: slideInRight 0.3s ease-out;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ==================== MOBILE MENU ====================
function initMobileMenu() {
    const toggle = document.getElementById('mobileMenuToggle');
    const menu = document.querySelector('.nav-menu');
    
    if (toggle && menu) {
        toggle.addEventListener('click', function() {
            menu.classList.toggle('active');
        });
        
        // Dışarı tıklanınca kapat
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.navbar')) {
                menu.classList.remove('active');
            }
        });
    }
}
