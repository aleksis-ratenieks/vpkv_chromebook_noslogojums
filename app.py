import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Computer, Reservation
from utils import get_weather_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'superslepens_atslega_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skolas_datori.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Maršruti (Routes) ---

@app.route('/')
@login_required
def dashboard():
    """Galvenais skats: datori, statusi un laikapstākļi."""
    weather = get_weather_data() # API izsaukums 
    computers = Computer.query.all()
    reservations = Reservation.query.filter(Reservation.end_time >= datetime.datetime.now()).all()
    return render_template('dashboard.html', computers=computers, weather=weather, reservations=reservations)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Nepareizs lietotājvārds vai parole!')
    return render_template('login.html')

@app.route('/reserve', methods=['POST'])
@login_required
def reserve():
    """Datora rezervācija ar laika posmu."""
    comp_id = request.form.get('computer_id')
    date_str = request.form.get('date')
    start_str = request.form.get('start_time')
    end_str = request.form.get('end_time')
    
    # Loģika: Pārvēršam tekstus par datetime objektiem
    start_dt = datetime.datetime.strptime(f"{date_str} {start_str}", '%Y-%m-%d %H:%M')
    end_dt = datetime.datetime.strptime(f"{date_str} {end_str}", '%Y-%m-%d %H:%M')
    
    new_res = Reservation(user_id=current_user.id, computer_id=comp_id, start_time=start_dt, end_time=end_dt)
    db.session.add(new_res)
    db.session.commit()
    flash('Rezervācija veiksmīga!')
    return redirect(url_for('dashboard'))

@app.route('/report_damage/<int:id>')
@login_required
def report_damage(id):
    """Jebkurš lietotājs var atzīmēt kā bojātu."""
    comp = Computer.query.get(id)
    comp.status = "Bojāts"
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    """Admina panelis jaunu lietotāju reģistrācijai un statusu maiņai."""
    if not current_user.is_admin:
        return "Piekļuve liegta", 403
        
    if request.method == 'POST':
        # Jauna lietotāja izveide
        username = request.form.get('username')
        password = request.form.get('password')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Lietotājs {username} pievienots!')
        
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/fix/<int:id>')
@login_required
def fix_computer(id):
    """Tikai admin var noņemt 'Bojāts' statusu."""
    if current_user.is_admin:
        comp = Computer.query.get(id)
        comp.status = "Pieejams"
        db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Sākotnējo datu izveide (Vismaz 3 lietotāji) [cite: 16]
        if not User.query.first():
            admin = User(username='admin', password='123', is_admin=True)
            u1 = User(username='skolotajs1', password='123')
            u2 = User(username='skolotajs2', password='123')
            c1 = Computer(name='Chromebook #1')
            c2 = Computer(name='Chromebook #2')
            db.session.add_all([admin, u1, u2, c1, c2])
            db.session.commit()
    app.run(debug=True)
