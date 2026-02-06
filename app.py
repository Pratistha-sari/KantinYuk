from flask import Flask, session, redirect, url_for, request
import os
from login import login_bp
from keranjang import keranjang_bp
from checkout import checkout_bp

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(keranjang_bp)
app.register_blueprint(checkout_bp)

menu_css = '''
    <style>
        :root{--accent:#00796b;--accent-2:#00bfa5;--muted:#6b7280}
        .site-header{background:var(--surface);border-bottom:1px solid #eef6f4}
        .site-header .container{max-width:980px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:12px 20px}
        .header-left{display:flex;align-items:center;gap:16px}
        .site-nav{display:flex;gap:10px;align-items:center}
        .site-nav .nav-item{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:8px;color:#064b44;text-decoration:none;font-weight:700}
        .site-nav .nav-item .icon{font-size:1.05rem}
        .site-nav .nav-item:hover{background:#f1fffb}
        .site-nav .nav-item.logout-link{background:#fff1f1;color:#b91c1c;border:1px solid #ffdede}
        html,body{height:100%;margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;background:linear-gradient(135deg,#f0fcfb 0%,#f3e8ff 100%);color:#0b2f2a}
        .menu-box{max-width:900px;margin:40px auto;background:rgba(255,255,255,0.95);padding:34px;border-radius:14px;box-shadow:0 12px 30px rgba(5,38,34,0.08);border:1px solid rgba(255,255,255,0.6);backdrop-filter:blur(6px)}
        h1{color:var(--accent);text-align:center;margin:0 0 10px 0;letter-spacing:0.6px}
        .categories{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:18px}
        .category-card{background:linear-gradient(180deg,#fff,#f7fffd);padding:18px;border-radius:10px;box-shadow:0 6px 18px rgba(0,0,0,0.04);border-left:6px solid var(--accent);display:flex;align-items:center;justify-content:space-between}
        .category-link{display:block;text-decoration:none;color:#043c35;font-weight:800;font-size:1.25rem}
        .cat-icon{display:inline-block;margin-right:10px;font-size:1.3rem}
        .category-meta{color:var(--muted);font-size:0.9rem}
        .menu-list,.category-list{list-style:none;padding:0;margin:0}
        .menu-list li{display:flex;align-items:center;justify-content:space-between;padding:12px 10px;border-radius:8px;background:#fff;margin-bottom:10px;border:1px solid #eef6f4;box-shadow:0 4px 10px rgba(14,52,45,0.03)}
        .menu-item-name{font-weight:600;color:#07423b}
        .menu-item-price{color:#1f6f61;font-weight:700}
        input[type=number]{width:70px;padding:6px 8px;border-radius:6px;border:1px solid #d1eaea}
        button{background:linear-gradient(90deg,var(--accent),var(--accent-2));color:#fff;border:none;padding:8px 14px;border-radius:8px;cursor:pointer;font-weight:700}
        button:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,191,165,0.18)}
        .nav-link,.logout-btn{display:inline-block;margin-top:18px;text-decoration:none;padding:8px 12px;border-radius:8px}
        .nav-link{color:var(--accent);background:transparent;border:1px solid rgba(0,121,107,0.08);margin-right:8px}
        .logout-btn{background:#ff6b6b;color:#fff;border:none}
        .flash-list{margin-top:10px;color:#0b5}
        .category-link:hover{background:#e9fffb;border-radius:8px}
        .back-link{display:inline-block;margin-top:10px;color:var(--accent);text-decoration:none;font-weight:700}
        @media (max-width:600px){.menu-box{padding:20px}.categories{grid-template-columns:1fr}input[type=number]{width:60px}.category-link{font-size:1.05rem}.cat-icon{font-size:1.1rem}}
    </style>
'''

menu_data = {
    'Makanan Berat': [
        {'nama': 'Mie Ayam', 'harga': 5000},
        {'nama': 'Bakso', 'harga': 7000},
        {'nama': 'Nasi Pecel', 'harga': 8000},
        {'nama': 'Mie Instan', 'harga': 5000},
        {'nama': 'Nasi Rames', 'harga': 8000}
    ],
    'Makanan Ringan': [
        {'nama': 'Risol Mayo', 'harga': 2000},
        {'nama': 'Donat Gula', 'harga': 2000},
        {'nama': 'Tahu Walik', 'harga': 2000},
        {'nama': 'Tahu Bakso', 'harga': 5000},
        {'nama': 'Dimsum Goreng', 'harga': 5000},
        {'nama': 'Cihu', 'harga': 5000},
        {'nama': 'Sempol', 'harga': 5000},
        {'nama': 'Kebab', 'harga': 6000},
        {'nama': 'Kimbab', 'harga': 6000},
        {'nama': 'Salad Buah', 'harga': 5000}
    ],
    'Minuman': [
        {'nama': 'Pop Ice', 'harga': 3000, 'rasa': ['Coklat', 'Strawberry', 'Anggur']},
        {'nama': 'Jus Buah', 'harga': 3000, 'rasa': ['Alpukat', 'Jambu', 'Melon']},
        {'nama': 'Es Teh', 'harga': 3000},
        {'nama': 'Es Jeruk', 'harga': 3000},
        {'nama': 'Kopi Susu', 'harga': 3000},
        {'nama': 'Thai Tea', 'harga': 3000},
        {'nama': 'Green Tea', 'harga': 3000} 
    ],
}

# Ikon untuk kategori (menggunakan emoji kecil)
category_icons = {
    'makanan-berat': '🍜',
    'makanan-ringan': '🍿',
    'minuman': '🥤',
}


@app.route('/')
def root():
    # Jika belum login, redirect ke login
    if 'user' not in session:
        return redirect(url_for('login_bp.login'))
    return redirect(url_for('menu'))

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'user' not in session:
        return redirect(url_for('login_bp.login'))
    from flask import request, render_template_string, flash
    if request.method == 'POST':
        nama = request.form['nama']
        harga = int(request.form['harga'])
        quantity = int(request.form['quantity'])
        keranjang = session.get('keranjang', [])
        found = False
        for item in keranjang:
            if item['nama'] == nama:
                item['quantity'] += quantity
                found = True
                break
        if not found:
            keranjang.append({'nama': nama, 'harga': harga, 'quantity': quantity})
        session['keranjang'] = keranjang
        session.modified = True
        flash(f"{nama} ditambahkan ke keranjang.")
    # Tampilkan indeks kategori (klik salah satu untuk melihat detil menu)
    categories = []
    for name, items in menu_data.items():
        slug = name.lower().replace(' ', '-')
        categories.append({'name': name, 'slug': slug, 'count': len(items), 'icon': category_icons.get(slug, '')})
    
    template = '''
        ''' + menu_css + '''
        <header class="site-header">
            <div class="container">
                <div class="header-left">
                    <div class="logo"><span class="logo-mark">🍽</span><span class="logo-text">KantinYuk</span></div>
                    <nav class="site-nav">
                        <a class="nav-item" href="/menu"><span class="icon">📋</span><span>Menu</span></a>
                        <a class="nav-item" href="/keranjang"><span class="icon">🛒</span><span>Keranjang</span></a>
                        <a class="nav-item logout-link" href="/logout"><span class="icon">🚪</span><span>Logout</span></a>
                    </nav>
                </div>
                <div class="header-right"></div>
            </div>
        </header>
        <main class="content">
            <div class="menu-box">
                <h1>Menu Pemesanan</h1>
                <div class="categories">
                {% for cat in categories %}
                    <div class="category-card">
                        <a class="category-link" href="{{ url_for('menu_category', category_slug=cat['slug']) }}"><span class="cat-icon">{{ cat['icon'] }}</span> {{ cat['name'] }}</a>
                        <div class="category-meta">{{ cat['count'] }} items</div>
                    </div>
                {% endfor %}
                </div>
                <div style="margin-top:18px;">
                    {% with messages = get_flashed_messages() %}
                        {% if messages %}
                            <ul class="flash-list">
                                {% for message in messages %}
                                    <li>{{ message }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    {% endwith %}
                </div>
            </div>
        </main>
        <footer class="site-footer">© 2026 KantinYuk — Semua hak dilindungi.</footer>
    '''
    return render_template_string(template, categories=categories) 

# Halaman detail kategori: menampilkan menu saat pengguna mengklik kategori
@app.route('/menu/<category_slug>', methods=['GET', 'POST'])
def menu_category(category_slug):
    if 'user' not in session:
        return redirect(url_for('login_bp.login'))
    from flask import request, render_template_string, flash, abort
    slug_map = {name.lower().replace(' ', '-'): name for name in menu_data.keys()}
    if category_slug not in slug_map:
        abort(404)
    category_name = slug_map[category_slug]
    items = menu_data[category_name]
    if request.method == 'POST':
        nama = request.form['nama']
        harga = int(request.form['harga'])
        quantity = int(request.form['quantity'])
        rasa = request.form.get('rasa', '')  # Ambil pilihan rasa jika ada
        keranjang = session.get('keranjang', [])
        found = False
        for item in keranjang:
            # Cek kecocokan berdasarkan nama dan rasa (jika ada)
            if item['nama'] == nama and item.get('rasa') == rasa:
                item['quantity'] += quantity
                found = True
                break
        if not found:
            item_data = {'nama': nama, 'harga': harga, 'quantity': quantity, 'kategori': category_name}
            if rasa:
                item_data['rasa'] = rasa
            keranjang.append(item_data)
        session['keranjang'] = keranjang
        session.modified = True
        rasa_text = f" ({rasa})" if rasa else ""
        flash(f"{nama}{rasa_text} ditambahkan ke keranjang.")
        return redirect(url_for('menu_category', category_slug=category_slug))
    
    template = '''
        ''' + menu_css + '''
        <header class="site-header">
            <div class="container">
                <div class="header-left">
                    <div class="logo"><span class="logo-mark">🍽</span><span class="logo-text">KantinYuk</span></div>
                    <nav class="site-nav">
                        <a class="nav-item" href="/menu"><span class="icon">📋</span><span>Menu</span></a>
                        <a class="nav-item" href="/keranjang"><span class="icon">🛒</span><span>Keranjang</span></a>
                        <a class="nav-item logout-link" href="/logout"><span class="icon">🚪</span><span>Logout</span></a>
                    </nav>
                </div>
                <div class="header-right"></div>
            </div>
        </header>
        <main class="content">
            <div class="menu-box">
                <h1>{{ category_name }}</h1>
                <ul class="menu-list">
                {% for item in items %}
                    <li>
                        <div>
                            <div class="menu-item-name">{{ item.nama }}</div>
                            <div class="menu-item-price">Rp {{ item.harga }}</div>
                        </div>
                        <form method="post" style="display:inline;">
                            <input type="hidden" name="nama" value="{{ item.nama }}">
                            <input type="hidden" name="harga" value="{{ item.harga }}">
                            {% if item.get('rasa') %}
                                <select name="rasa" style="padding:6px 8px;border-radius:6px;border:1px solid #d1eaea;margin-right:8px;" required>
                                    <option value="">Pilih Rasa</option>
                                    {% for r in item['rasa'] %}
                                        <option value="{{ r }}">{{ r }}</option>
                                    {% endfor %}
                                </select>
                            {% endif %}
                            <input type="number" name="quantity" value="1" min="1">
                            <button type="submit">Pesan</button>
                        </form>
                    </li>
                {% endfor %}
                </ul>
                <div style="margin-top:12px;">
                    <a class="back-link" href="/menu">Kembali ke Kategori</a>
                    <a class="nav-link" href="/keranjang">Lihat Keranjang</a>
                </div>
            </div>
        </main>
        <footer class="site-footer">© 2026 KantinYuk — Semua hak dilindungi.</footer>
    '''
    return render_template_string(template, category_name=category_name, items=items) 

# Pastikan checkout dan keranjang hanya bisa diakses jika sudah login
@app.before_request
def protect_pages():
    allowed = {'login_bp.login', 'login_bp.logout', 'static'}
    endpoint = request.endpoint
    if endpoint is None or endpoint in allowed:
        return None
    if 'user' not in session:
        return redirect(url_for('login_bp.login'))

if __name__ == '__main__':
    app.run(debug=True)
