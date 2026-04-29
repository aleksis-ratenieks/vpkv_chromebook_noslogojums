import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash # JAUNUMS: Šifrēšana
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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Jūs esat izrakstījies.')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    weather = get_weather_data()
    computers = Computer.query.all()
    reservations = Reservation.query.filter(Reservation.end_time >= datetime.datetime.now()).all()
    return render_template('dashboard.html', computers=computers, weather=weather, reservations=reservations)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        # JAUNUMS: Pārbauda šifrēto paroli datubāzē pret ievadīto tekstu
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Nepareizs lietotājvārds vai parole!')
    return render_template('login.html')

@app.route('/reserve', methods=['POST'])
@login_required
def reserve():
    comp_id = request.form.get('computer_id')
    date_str = request.form.get('date')
    start_str = request.form.get('start_time')
    end_str = request.form.get('end_time')
    
    try:
        start_dt = datetime.datetime.strptime(f"{date_str} {start_str}", '%Y-%m-%d %H:%M')
        end_dt = datetime.datetime.strptime(f"{date_str} {end_str}", '%Y-%m-%d %H:%M')
        
        new_res = Reservation(user_id=current_user.id, computer_id=comp_id, start_time=start_dt, end_time=end_dt)
        db.session.add(new_res)
        db.session.commit()
        flash('Rezervācija veiksmīga!')
    except Exception as e:
        flash('Kļūda! Lūdzu, pārliecinieties, ka ievadījāt pareizu datumu un laiku.', 'error')
        
    return redirect(url_for('dashboard'))

@app.route('/cancel_reservation/<int:id>')
@login_required
def cancel_reservation(id):
    res = Reservation.query.get(id)
    if res and (res.user_id == current_user.id or current_user.is_admin):
        db.session.delete(res)
        db.session.commit()
        flash('Rezervācija atcelta.')
    return redirect(url_for('dashboard'))

@app.route('/report_damage/<int:id>')
@login_required
def report_damage(id):
    comp = Computer.query.get(id)
    comp.status = "Bojāts"
    db.session.commit()
    flash(f'Ziņots par {comp.name} bojājumu.')
    return redirect(url_for('dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        return "Piekļuve liegta", 403
        
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_user':
            username = request.form.get('username')
            # JAUNUMS: Paroles šifrēšana pirms saglabāšanas datubāzē
            hashed_password = generate_password_hash(request.form.get('password'))
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            flash(f'Lietotājs {username} pievienots!')
            
        elif action == 'add_computer':
            name = request.form.get('comp_name')
            sn = request.form.get('serial_number')
            new_comp = Computer(name=name, serial_number=sn)
            db.session.add(new_comp)
            flash(f'Dators {name} pievienots!')
            
        db.session.commit()
        
    users = User.query.all()
    computers = Computer.query.all()
    return render_template('admin.html', users=users, computers=computers)

@app.route('/fix/<int:id>')
@login_required
def fix_computer(id):
    if current_user.is_admin:
        comp = Computer.query.get(id)
        comp.status = "Pieejams"
        db.session.commit()
        flash(f'Dators {comp.name} atzīmēts kā saremontēts.')
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # JAUNUMS: Sākotnējo lietotāju paroles tiek nošifrētas
        if not User.query.first():
            admin = User(username='admin', password=generate_password_hash('123'), is_admin=True)
            u1 = User(username='skolotajs1', password=generate_password_hash('123'))
            u2 = User(username='skolotajs2', password=generate_password_hash('123'))
            c1 = Computer(name='Chromebook #1', serial_number='SN-001-ABC')
            c2 = Computer(name='Chromebook #2', serial_number='SN-002-XYZ')
            db.session.add_all([admin, u1, u2, c1, c2])
            db.session.commit()
    app.run(debug=True)
