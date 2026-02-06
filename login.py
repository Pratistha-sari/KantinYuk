from flask import Blueprint, render_template_string, request, redirect, url_for, session, flash, current_app, get_flashed_messages

login_bp = Blueprint('login_bp', __name__)

login_css = '''
    <style>
        :root{--accent:#0b6b63;--accent-2:#00bfa5}
        html,body{height:100%;margin:0;font-family:Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;background:linear-gradient(180deg,#f6fbfa 0%,#f7eefb 100%);}
        .site-header{background:#fff;border-bottom:1px solid #eef6f4}
        .site-header .container{max-width:980px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:12px 20px}
        .header-left{display:flex;align-items:center;gap:14px}
        .logo{display:flex;align-items:center;gap:10px;font-weight:800;color:var(--accent);font-size:1.05rem}
        .logo-mark{font-size:1.25rem}
        .logo-text{font-size:1rem}
        /* Compact, neat nav */
        .site-nav{display:flex;gap:8px;align-items:center}
        .site-nav .nav-item{display:inline-flex;align-items:center;gap:8px;padding:6px 10px;border-radius:10px;color:#064b44;text-decoration:none;font-weight:700;background:transparent;border:1px solid transparent}
        .site-nav .nav-item .icon{font-size:1.05rem}
        .site-nav .nav-item:hover{background:#f1fffb;transform:translateY(-2px)}
        .site-nav .nav-item.logout-link{background:#fff1f1;color:#b91c1c;border:1px solid #ffdede}
        .site-nav .nav-item .label{font-size:0.95rem}
        h2{color:var(--accent);text-align:center;margin-top:6px}
        form{max-width:420px;margin:40px auto;background:linear-gradient(180deg,#ffffff,#f7fffdf2);padding:24px;border-radius:12px;box-shadow:0 12px 30px rgba(3,38,33,0.06);border:1px solid rgba(0,0,0,0.04)}
        label{display:block;margin:8px 0 4px;color:#254b45;font-weight:600}
        input{width:100%;padding:10px;margin:6px 0;border:1px solid #e6f3f0;border-radius:8px;background:#fbfffe}
        input[type=submit],.next-btn,.back-btn{background:linear-gradient(90deg,var(--accent),var(--accent-2));color:#fff;border:none;cursor:pointer;font-weight:700;border-radius:8px;padding:10px;width:100%;text-align:center;text-decoration:none}
        input[type=submit]:hover,.next-btn:hover,.back-btn:hover{transform:translateY(-3px);box-shadow:0 10px 20px rgba(0,191,165,0.12)}
        ul{color:#d32f2f;margin-top:10px}
        .btn-group{margin-top:18px;display:flex;gap:10px}
        .link-muted{display:block;margin-top:8px;text-align:center;color:#00796b;text-decoration:none}
        footer.site-footer{max-width:980px;margin:22px auto;text-align:center;color:#6b7280;font-size:0.9rem;padding:16px 20px}
        @media (max-width:480px){form{margin:30px 18px;padding:18px}}
    </style>
'''  

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        flash('Anda sudah login!')
        return redirect(url_for('menu'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['user'] = username
            flash('Login berhasil!')
            return redirect(url_for('menu'))
        else:
            flash('Username atau password salah!')
    # collect flashed messages and filter out checkout-related ones
    raw_msgs = get_flashed_messages(with_categories=True)
    filtered_msgs = []
    exclude_keywords = ['checkout', 'pembayaran', 'terima kasih']
    for cat, msg in raw_msgs:
        if cat == 'checkout':
            continue
        if msg and any(k in msg.lower() for k in exclude_keywords):
            continue
        filtered_msgs.append(msg)

    return render_template_string(f'''
    {login_css}
    <header class="site-header">
        <div class="container">
            <div class="header-left">
                <div class="logo"><span class="logo-mark">🍽</span><span class="logo-text">KantinYuk</span></div>
                <nav class="site-nav">
                    <a class="nav-item" href="/menu"><span class="icon" aria-hidden>📋</span><span class="label">Menu</span></a>
                    <a class="nav-item" href="/keranjang"><span class="icon" aria-hidden>🛒</span><span class="label">Keranjang</span></a>
                    {{% if session.get('user') %}}
                        <a class="nav-item logout-link" href="/logout"><span class="icon" aria-hidden>🚪</span><span class="label">Logout</span></a>
                    {{% endif %}}
                </nav>
            </div>
            <div class="header-right"></div>
        </div>
    </header>
    <main class="content">
        <form method="post">
            <h2>Login</h2>
            Username: <input type="text" name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <input type="submit" value="Login">
            {{% if messages %}}
                <ul>
                {{% for message in messages %}}
                    <li>{{{{ message }}}}</li>
                {{% endfor %}}
                </ul>
            {{% endif %}}
        </form>
    </main>
    <footer class="site-footer">© 2026 KantinYuk — Semua hak dilindungi.</footer>
    ''', messages=filtered_msgs) 

@login_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Anda telah logout.')
    return redirect(url_for('login_bp.login'))
