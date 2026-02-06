from flask import Blueprint, render_template_string, request, redirect, url_for, session, flash

keranjang_bp = Blueprint('keranjang_bp', __name__)

keranjang_css = '''
    <style>
        :root{--accent:#0b6b63;--danger:#d32f2f}
        html,body{margin:0;font-family:Inter, system-ui, -apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;background:linear-gradient(180deg,#f6fdfd 0%,#f3e8ff 100%);color:#072b28}
        .site-header{background:#fff;border-bottom:1px solid #eef6f4}
        .site-header .container{max-width:980px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:12px 20px}
        .header-left{display:flex;align-items:center;gap:16px}
        .logo{display:flex;align-items:center;gap:10px;font-weight:800;color:var(--accent);font-size:1.05rem}
        .site-nav{display:flex;gap:10px;align-items:center}
        .site-nav .nav-item{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:8px;color:#064b44;text-decoration:none;font-weight:700}
        .site-nav .nav-item .icon{font-size:1.05rem}
        .site-nav .nav-item:hover{background:#f1fffb}
        .site-nav .nav-item.logout-link{background:#fff1f1;color:#b91c1c;border:1px solid #ffdede} 
        .keranjang-box{max-width:780px;margin:28px auto;background:linear-gradient(180deg,#fff,#fbfffe);padding:28px;border-radius:12px;box-shadow:0 12px 30px rgba(3,38,33,0.06);border:1px solid rgba(0,0,0,0.04)}
        h1{color:var(--accent);text-align:center;margin:0 0 10px 0}
        ul{list-style:none;padding:0;margin:0}
        li{display:flex;align-items:center;justify-content:space-between;padding:12px;border-radius:10px;background:#fff;margin:8px 0;border:1px solid #eef6f4}
        .item-info{display:flex;align-items:center;gap:12px}
        .item-name{font-weight:700;color:#053a36}
        .item-price{color:#1f6f61;font-weight:700}
        input[type=number]{width:80px;padding:8px;border-radius:8px;border:1px solid #e3f2ef}
        button{background:linear-gradient(90deg,var(--accent),#00bfa5);color:#fff;border:none;padding:8px 12px;border-radius:8px;cursor:pointer}
        .btn-red{background:var(--danger);color:#fff;border:none;padding:8px 12px;border-radius:8px}
        .nav-link{color:var(--accent);text-decoration:none;font-weight:700}
        .total{font-size:1.1rem;font-weight:800;color:#053a36;margin-top:12px}
        .item-icon{display:inline-block;width:34px;height:34px;border-radius:8px;background:#f4fffb;display:flex;align-items:center;justify-content:center;margin-right:10px;font-size:1.1rem}
        footer.site-footer{max-width:980px;margin:22px auto;text-align:center;color:#6b7280;font-size:0.9rem;padding:16px 20px}
        @media (max-width:600px){.keranjang-box{padding:18px}input[type=number]{width:64px}}
    </style>
''' 

# Ikon kategori (mencocokkan slug)
category_icons = {
    'makanan-berat': '🍜',
    'makanan-ringan': '🍿',
    'minuman': '🥤',
} 


@keranjang_bp.route('/keranjang', methods=['GET', 'POST'])
def keranjang():
    if 'user' not in session:
        return redirect(url_for('login_bp.login'))
    keranjang = session.get('keranjang', [])
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update':
            for i, item in enumerate(keranjang):
                # Create unique key for each item including rasa if exists
                rasa = item.get('rasa', '')
                key_suffix = f"_{rasa}" if rasa else ""
                key = f"quantity_{item['nama']}{key_suffix}"
                q = request.form.get(key)
                if q is not None:
                    try:
                        item['quantity'] = max(1, int(q))
                    except ValueError:
                        pass
            session['keranjang'] = keranjang
            session.modified = True
            flash('Keranjang diperbarui.')
        elif action == 'clear':
            session.pop('keranjang', None)
            flash('Keranjang dikosongkan.')
        return redirect(url_for('keranjang_bp.keranjang'))

    # Buat versi tampilan dengan ikon untuk setiap item
    display_items = []
    for item in keranjang:
        slug = item.get('kategori', '').lower().replace(' ', '-')
        icon = category_icons.get(slug, '')
        display_items.append({**item, 'icon': icon})

    total = sum(item['harga'] * item['quantity'] for item in keranjang)
    template = '''
        ''' + keranjang_css + '''
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
            <div class="keranjang-box">
                <h1>Keranjang Anda</h1>
                {% if not keranjang %}
                    <p>Keranjang kosong.</p>
                    <a class="nav-link" href="/menu">Kembali ke Menu</a>
                {% else %}
                    <form method="post">
                        <ul>
                        {% for item in keranjang %}
                            {% set rasa = item.get('rasa', '') %}
                            {% set key_suffix = ('_' + rasa) if rasa else '' %}
                            <li>
                                <div class="item-info"><span class="item-icon">{{ item.icon }}</span> <div><div class="item-name">{{ item.nama }}{% if rasa %} - {{ rasa }}{% endif %}</div><div class="item-price">Rp {{ item.harga }}</div></div></div>
                                <input type="number" name="quantity_{{ item.nama }}{{ key_suffix }}" value="{{ item.quantity }}" min="1">
                            </li>
                        {% endfor %}
                        </ul>
                        <p class="total"><b>Total: Rp {{ total }}</b></p>
                        <input type="hidden" name="action" value="update">
                        <button type="submit">Perbarui Keranjang</button>
                    </form>
                    <form method="post" style="display:inline; margin-top:10px;">
                        <input type="hidden" name="action" value="clear">
                        <button type="submit" class="btn-red">Kosongkan Keranjang</button>
                    </form>
                    <a class="nav-link" href="/checkout">Lanjut ke Checkout</a>
                {% endif %}
            </div>
        </main>
        <footer class="site-footer">© 2026 KantinYuk — Semua hak dilindungi.</footer>
    '''
    return render_template_string(template, keranjang=display_items, total=total) 
 