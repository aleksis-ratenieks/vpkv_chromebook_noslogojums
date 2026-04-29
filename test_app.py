import unittest
from app import app
from models import db, User, Computer
from werkzeug.security import generate_password_hash, check_password_hash

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        self.app = app.test_client()

        with app.app_context():
            db.create_all()
            # JAUNUMS: Testa paroli arī atjauninām uz drošu
            hashed_pw = generate_password_hash('Admin123!')
            test_admin = User(username='test_admin', password=hashed_pw, is_admin=True)
            test_comp = Computer(name='Testa Dators', serial_number='SN-TEST-01')
            db.session.add(test_admin)
            db.session.add(test_comp)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pieteikties', response.data)

    def test_user_creation(self):
        with app.app_context():
            user = User.query.filter_by(username='test_admin').first()
            self.assertIsNotNone(user)
            self.assertTrue(user.is_admin)
            # JAUNUMS: Pārbauda atjaunoto testa paroli
            self.assertTrue(check_password_hash(user.password, 'Admin123!'))

    def test_computer_creation(self):
        with app.app_context():
            comp = Computer.query.filter_by(serial_number='SN-TEST-01').first()
            self.assertIsNotNone(comp)
            self.assertEqual(comp.name, 'Testa Dators')
            self.assertEqual(comp.status, 'Pieejams')

    def test_dashboard_access_without_login(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302) 
        self.assertTrue('/login' in response.location)

if __name__ == '__main__':
    unittest.main()
