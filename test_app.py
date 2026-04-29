import unittest
from app import app
from models import db, User, Computer

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Šī funkcija izpildās pirms katra testa. Tā izveido testa vidi."""
        # Konfigurējam lietotni testēšanas režīmam
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Izmanto operatīvo atmiņu, nevis reālo failu
        self.app = app.test_client()

        with app.app_context():
            db.create_all()
            # Pievienojam testa datus
            test_admin = User(username='test_admin', password='123', is_admin=True)
            test_comp = Computer(name='Testa Dators', serial_number='SN-TEST-01')
            db.session.add(test_admin)
            db.session.add(test_comp)
            db.session.commit()

    def tearDown(self):
        """Šī funkcija izpildās pēc katra testa, lai notīrītu datubāzi."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # --- 1. TESTS: Vai ielādējas pieteikšanās lapa? ---
    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pieteikties', response.data) # Pārbauda, vai lapā ir vārds "Pieteikties"

    # --- 2. TESTS: Vai datubāzē pareizi izveidojas lietotājs? ---
    def test_user_creation(self):
        with app.app_context():
            user = User.query.filter_by(username='test_admin').first()
            self.assertIsNotNone(user)
            self.assertTrue(user.is_admin)
            self.assertEqual(user.password, '123')

    # --- 3. TESTS: Vai datubāzē pareizi reģistrējas dators ar S/N? ---
    def test_computer_creation(self):
        with app.app_context():
            comp = Computer.query.filter_by(serial_number='SN-TEST-01').first()
            self.assertIsNotNone(comp)
            self.assertEqual(comp.name, 'Testa Dators')
            self.assertEqual(comp.status, 'Pieejams')

    # --- 4. TESTS: Piekļuve aizliegta (401), ja nav ielogojies ---
    def test_dashboard_access_without_login(self):
        response = self.app.get('/')
        # Ja nav ielogojies, Flask-Login novirza (status 302) uz login lapu
        self.assertEqual(response.status_code, 302) 
        self.assertTrue('/login' in response.location)

if __name__ == '__main__':
    unittest.main()
