from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth

# Membuat aplikasi flask
app = Flask(__name__)

# konfigurasi secret key
app.secret_key = 'aodjwopdj'

# konfigurasi google client id dan client secret
app.config['GOOGLE_ID'] = '988410444924-5197ls8h7c77sirvlrhplqd8mp3la48a.apps.googleusercontent.com'
app.config['GOOGLE_SECRET'] = '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'

# inisialisasi OAuth
oauth = OAuth(app)

# Remote app untuk google
google = oauth.remote_app(
    # Penyedia OAuth
    'google',
    consumer_key = app.config.get('GOOGLE_ID'),
    consumer_secret = app.config.get('GOOGLE_SECRET'),
    # ruang lingkup akses yang diminta
    request_token_params = {
        'scope': 'email',
    },
    # URL base buat sumber daya OAuth dari google
    base_url = 'https://www.googleapis.com/oauth2/v1/',
    # URL buat alur OAuth untuk mendapatkan token akses
    request_token_url = None,
    access_token_methods = 'POST',
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
)

# Rute utama di halaman utama
@app.route('/')
# Memeriksa apakah ada token akses Google yang tersimpan dalam sesi user
def index():
    # kalo ada, berarti user sudah login
    if 'google_token' in session:
        # mendapat user info
        me = google.get('userinfo')
        return 'Logged in as: ' + me.data['email']
    # kalo gaada disuruh login
    return 'You are not logged in! <a href = "/login">Login with Google</a>'

# Rute login
@app.route('/login')
# Manggil method 'authorize' dari objek 'google' buat user login akun google atau ngasih izin
def login():
    # Mengatur callback URL yang akan dipanggil Google abis berhasil atau gagal login. Abis login ke rute '/login/authorized'
    return google.authorize(callback = url_for('authorized', _external = True))

# Rute logout
@app.route('/logout')
# Menghapus token akses Google dari user
def logout():
    # Buat ngapus token
    session.pop('google_token', None)
    # balik ke rute utama '/'
    return redirect(url_for('index'))

# Rute callback abis user berhasil atau gagal login
app.route('/login/authorized')
# Memeriksa tanggapan dari Google
def authorized():
    resp = google.authorized_response()
    # login gagal
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason = {} error = {}'.format(
            request.arges['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return 'Logged in as: ' + me.data['email']

# Aplikasi dijalankan
if __name__ == '__main__':
    app.run()