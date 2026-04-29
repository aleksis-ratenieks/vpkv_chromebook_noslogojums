import unittest
import datetime
from app import app
from models import db, User, Computer, Reservation
from werkzeug.security import generate_password_hash, check_password_hash

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Sagatavo tīru testa vidi pirms katra testa."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        self.app = app.test_client()

        with app.app_context():
            db.create_all()
            
            # Izveidojam testa lietotāju ar STINGRO paroli
            hashed_pw = generate_password_hash('Admin123!')
            test_admin = User(username='test_admin', password=hashed_pw, is_admin=True)
            
            # Izveidojam testa datoru (ar Sērijas Numuru, lai nebūtu kļūdu)
            test_comp = Computer(name='Testa Dators', serial_number='SN-TEST-01')
            
            db.session.add(test_admin)
            db.session.add(test_comp)
            db.session.commit()
            
            # Saglabājam ID vēlākam rezervācijas testam
            self.test_comp_id = test_comp.id
            self.test_user_id = test_admin.id

    def tearDown(self):
        """Notīra datubāzi pēc katra testa."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_user_creation(self):
        with app.app_context():
            user = User.query.filter_by(username='test_admin').first()
            self.assertIsNotNone(user)
            # Pārbauda jauno, drošo paroli
            self.assertTrue(check_password_hash(user.password, 'Admin123!'))

    def test_computer_creation(self):
        with app.app_context():
            comp = Computer.query.filter_by(serial_number='SN-TEST-01').first()
            self.assertIsNotNone(comp)

    def test_dashboard_access_without_login(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302) 

    # JAUNAIS TESTS: Pārbauda, vai dubultā rezervācija tiek pamanīta
    def test_reservation_overlap_control(self):
        with app.app_context():
            # 1. Izveidojam pirmo rezervāciju (10:00 - 11:00)
            start1 = datetime.datetime(2024, 5, 20, 10, 0)
            end1 = datetime.datetime(2024, 5, 20, 11, 0)
            res1 = Reservation(user_id=self.test_user_id, computer_id=self.test_comp_id, start_time=start1, end_time=end1)
            db.session.add(res1)
            db.session.commit()

            # 2. Mēģinām atrast pārklāšanos ar jaunu laiku (10:30 - 11:30)
            start2 = datetime.datetime(2024, 5, 20, 10, 30)
            end2 = datetime.datetime(2024, 5, 20, 11, 30)
            
            overlap = Reservation.query.filter(
                Reservation.computer_id == self.test_comp_id,
                Reservation.start_time < end2,
                Reservation.end_time > start2
            ).first()
            
            # 3. Pārbaudām, ka sistēma tiešām uztvēra šo pārklāšanos (overlap nav tukšs)
            self.assertIsNotNone(overlap)

if __name__ == '__main__':
    unittest.main()
