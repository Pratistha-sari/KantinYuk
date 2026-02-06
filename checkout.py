from flask import Blueprint, render_template_string, request, redirect, url_for, session, flash

checkout_bp = Blueprint('checkout_bp', __name__)

checkout_css = '''
    <style>
        :root{--accent:#0b6b63;--accent-2:#00bfa5;--muted:#6b7280}
        html,body{height:100%;margin:0;font-family:Inter, system-ui, -apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;background:linear-gradient(135deg,#f0f9f8 0%,#f7eefb 100%);color:#052e2b}
        .site-header{background:#fff;border-bottom:1px solid #eef6f4}
        .site-header .container{max-width:980px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:12px 20px}
        .header-left{display:flex;align-items:center;gap:16px}
        .logo{display:flex;align-items:center;gap:10px;font-weight:800;color:var(--accent);font-size:1.05rem}
        .site-nav{display:flex;gap:10px;align-items:center}
        .site-nav .nav-item{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:8px;color:#064b44;text-decoration:none;font-weight:700}
        .site-nav .nav-item .icon{font-size:1.05rem}
        .site-nav .nav-item:hover{background:#f1fffb}
        .site-nav .nav-item.logout-link{background:#fff1f1;color:#b91c1c;border:1px solid #ffdede}
        h2{color:var(--accent);text-align:center;margin-top:0}
        form{max-width:480px;margin:36px auto;background:linear-gradient(180deg,#ffffff,#fbfffe);padding:22px;border-radius:12px;box-shadow:0 12px 30px rgba(3,38,33,0.06);border:1px solid rgba(0,0,0,0.04)}
        input,select{width:100%;padding:10px;margin:8px 0;border:1px solid #e6f3f0;border-radius:8px;background:#fbfffe}
        /* Tombol di dalam .btn-group dibuat seragam (ukuran dan layout) */
        .btn-group{margin-top:18px;display:flex;gap:10px}
        .btn-group .back-btn, .btn-group .next-btn {
            flex: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 46px;
            padding: 10px 14px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 700;
            cursor: pointer;
        }
        /* Gaya tombol kembali (terlihat netral) */
        .btn-group .back-btn { background: #f3f4f6; color: #053a36; border: 1px solid #e6f3f0; }
        /* Gaya tombol selanjutnya (accent) */
        .btn-group .next-btn { background: linear-gradient(90deg,var(--accent),var(--accent-2)); color:#fff; }
        .btn-group .back-btn:hover, .btn-group .next-btn:hover { transform: translateY(-3px); box-shadow:0 10px 20px rgba(0,191,165,0.12); }
        .qris-box{text-align:center;margin-top:24px}
        .qris-box img{border:6px solid var(--accent);border-radius:14px;box-shadow:0 8px 30px rgba(0,0,0,0.08)}
        .back-link{display:inline-block;margin-top:12px;color:var(--accent);text-decoration:none;font-weight:700}
        .success-box{max-width:520px;margin:24px auto;background:linear-gradient(180deg,#fff,#fbfff5);padding:26px;border-radius:12px;box-shadow:0 12px 30px rgba(0,0,0,0.06);text-align:center}
        .btn-group{margin-top:18px;display:flex;gap:10px}
        footer.site-footer{max-width:980px;margin:22px auto;text-align:center;color:#6b7280;font-size:0.9rem;padding:16px 20px}
        @media (max-width:520px){form{margin:20px;padding:18px}}
    </style>
''' 

@checkout_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user' not in session:
        return redirect(url_for('login_bp.login'))
    if request.method == 'POST':
        nama = request.form.get('nama')
        kelas = request.form.get('kelas')
        metode = request.form.get('metode')
        # After checkout is performed, clear the cart because items are paid
        session['keranjang'] = []
        session.modified = True
        flash('Pembayaran diproses — keranjang dikosongkan.', 'checkout')

        if metode == 'qris':
            return render_template_string(f'''
                {checkout_css}
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
                    <div class="qris-box">
                        <h2>Pembayaran QRIS</h2>
                        <p>Silakan scan QR berikut untuk membayar:</p>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=KantinYuk-ContohQRIS" alt="QRIS">
                        <br><a class="back-link" href="/checkout">Kembali</a>
                    </div>
                </main>
                <footer class="site-footer">© 2026 KantinYuk — Semua hak dilindungi.</footer>
            ''')
        return render_template_string(f'''
            {checkout_css}
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
                <div class="success-box">
                    <h2>Terima kasih, {nama}!</h2>
                    <p>Kelas: <b>{kelas}</b></p>
                    <p>Metode Pembayaran: <b>{metode.upper()}</b></p>
                    <a class="back-link" href="/">Kembali ke Menu</a>
                </div>
            </main>
            <footer class="site-footer">© 2026 KantinYuk — Semua hak dilindungi.</footer>
        ''') 
    return render_template_string(f'''
        {checkout_css}
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
            <form method="post">
                <h2>Checkout</h2>
                Nama Siswa: <input type="text" name="nama" required><br>
                Kelas: <input type="text" name="kelas" required><br>
                Metode Pembayaran:<br>
                <select name="metode">
                    <option value="tunai">Tunai</option>
                    <option value="qris">QRIS</option>
                </select><br>
                <div class="btn-group">
                    <a class="back-btn" href="/keranjang">Kembali</a>
                    <input class="next-btn" type="submit" value="Selanjutnya">
                </div>
            </form>
        </main>
        <footer class="site-footer">© 2026 KantinYuk — Semua hak dilindungi.</footer>
    ''')
