import unittest
from app import create_app
from bs4 import BeautifulSoup

class AddUserUnitTest(unittest.TestCase):

    def test_add_user_elements(self):
        """Test if elements are displayed on the Add User page."""

        app = create_app()
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SERVER_NAME'] = 'localhost.localdomain'

        with app.app_context():
            client = app.test_client()

            response = client.get('/add_user')

            self.assertEqual(response.status_code, 200)

            soup = BeautifulSoup(response.data, 'html.parser')

            name_field = soup.find('input', {'name': 'name'})
            self.assertIsNotNone(name_field)

            email_field = soup.find('input', {'name': 'email'})
            self.assertIsNotNone(email_field)

            phone_field = soup.find('input', {'name': 'phone_number'})
            self.assertIsNotNone(phone_field)

            birthdate_field = soup.find('input', {'name': 'birthdate'})
            self.assertIsNotNone(birthdate_field)

            submit_button = soup.find('button', {'type': 'submit'})
            self.assertIsNotNone(submit_button)
            self.assertEqual(submit_button.text.strip(), 'Add User')

            back_button = soup.find('a', {'href': '/users'})
            self.assertIsNotNone(back_button)
            self.assertEqual(back_button.text.strip(), 'User Catalog')

if __name__ == '__main__':
    unittest.main()