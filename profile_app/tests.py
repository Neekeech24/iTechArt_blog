import factory
from django.test import TestCase, Client
from .models import UserModel
from .forms import RegisterUserForm


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(lambda a: '{}{}'.format(a.first_name, a.last_name))
    email = factory.LazyAttribute(lambda a: '{}.{}@example.com'.format(a.first_name, a.last_name).lower())

    class Meta:
        model = UserModel
        django_get_or_create = ('username',)


class RegisterFormTest(TestCase):

    def test_register_empty_form(self):
        form = RegisterUserForm(data={})
        if form.is_valid():
            pass
        else:
            expected_errors = {
                'username':['Обязательное поле.'],
                'password':['Обязательное поле.'],
                'password2':['Обязательное поле.']
            }
            received_errors = dict(zip(form.errors.keys(), form.errors.values()))
            self.assertEqual(expected_errors, received_errors)


    def test_register_wo_password(self):
        form = RegisterUserForm(data={'username': 'Username'})
        if form.is_valid():
            pass
        else:
            expected_errors = {
                'password': ['Обязательное поле.'],
                'password2': ['Обязательное поле.']
            }
            received_errors = dict(zip(form.errors.keys(), form.errors.values()))
            self.assertEqual(expected_errors, received_errors)

    def test_register_wo_username(self):
        form = RegisterUserForm(data={'password': 'testingForm123', 'password2': 'testingForm123'})
        if form.is_valid():
            pass
        else:
            expected_errors = {
                'username': ['Обязательное поле.']
            }
            received_errors = dict(zip(form.errors.keys(), form.errors.values()))
            self.assertEqual(expected_errors, received_errors)

    def test_register_unequal_passwords(self):
        form = RegisterUserForm(data={'username': 'Username', 'password': 'testingForm123', 'password2': 'testingForm'})
        if form.is_valid():
            pass
        else:
            expected_errors = {
                'password': ['Введенные пароли не совпадают.']
            }
            received_errors = dict(zip(form.errors.keys(), form.errors.values()))
            self.assertEqual(expected_errors, received_errors)

    def test_non_unique_username(self):
        user = UserFactory.create(username='Username')
        form = RegisterUserForm(data={'username': 'Username', 'password': 'testingForm123', 'password2': 'testingForm123'})
        if form.is_valid():
            pass
        else:
            expected_errors = {
                'username': ['Пользователь с таким именем уже существует.']
            }
            received_errors = dict(zip(form.errors.keys(), form.errors.values()))
            self.assertEqual(expected_errors, received_errors)

    def test_correct_register_form(self):
        form = RegisterUserForm(data={'username': 'Username', 'password': 'testingForm123', 'password2': 'testingForm123'})
        self.assertTrue(form.is_valid())


class ClientRegisterTest(TestCase):

    def test_register_empty_form(self):
        response = self.client.post('/accounts/registration', data={})
        self.assertEqual(response.status_code, 400)
        expected_errors = {
            'username': ['Обязательное поле.'],
            'password': ['Обязательное поле.'],
            'password2': ['Обязательное поле.']
        }
        received_errors = dict(zip(response.context['form'].errors.keys(), response.context['form'].errors.values()))
        self.assertEqual(expected_errors, received_errors)

    def test_unequal_password(self):
        response = self.client.post('/accounts/registration',
                                    data={'username':'Username',
                                          'password': 'testingForm123',
                                          'password2': 'testingForm'})
        self.assertEqual(response.status_code, 400)
        expected_errors = {
            'password': ['Введенные пароли не совпадают.']
        }
        received_errors = dict(zip(response.context['form'].errors.keys(), response.context['form'].errors.values()))
        self.assertEqual(expected_errors, received_errors)

    def test_correct_register_form(self):
        response = self.client.post('/accounts/registration',
                                    data={'username': 'Username',
                                          'password': 'testingForm123',
                                          'password2': 'testingForm123'})
        user = User.objects.get()
        self.assertEqual(user.username, 'Username')
        self.assertRedirects(response, '/')

    def test_non_unique_username(self):
        user = UserFactory.create(username='Username')
        response = self.client.post('/accounts/registration',
                                    data={'username': 'Username',
                                          'password': 'testingForm123',
                                          'password2': 'testingForm123'})
        self.assertEqual(response.status_code, 400)
        expected_errors = {
            'username': ['Пользователь с таким именем уже существует.']
        }
        received_errors = dict(zip(response.context['form'].errors.keys(), response.context['form'].errors.values()))
        self.assertEqual(expected_errors, received_errors)


