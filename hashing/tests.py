from django.test import TestCase
from selenium import webdriver
from .forms import HashForm
import hashlib
from .models import Hash
from django.core.exceptions import ValidationError
import time


class FunctionTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_home_page_content(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Enter text here:', self.browser.page_source)

    # def test_hash_of_hello(self):
    #     self.browser.get('http://localhost:8000')
    #     text = self.browser.find_element_by_id("id_text")
    #     text.send_keys("hello")
    #     self.browser.find_element_by_name("submit").click()
    #     self.assertIn(
    #         '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', self.browser.page_source)

    def test_ajax(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id("id_text")
        text.send_keys("hello")
        time.sleep(5)
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',
                      self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTest(TestCase):
    def test_home_page_success(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_home_page_uses_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, template_name='hashing/home.html')

    def test_form_is_valid(self):
        response = self.client.get('/')
        form = HashForm(data={"text": "hello"})
        self.assertTrue(form.is_valid())

    def test_hash_function(self):
        text = "hello"
        hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        hash_res = hashlib.sha256(text.encode('utf-8')).hexdigest()
        self.assertEquals(hash_res, hash)

    def test_viewing_hash(self):
        text = "hello world"
        hash = 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
        hash_obj = Hash.objects.create(text=text, hash=hash)
        hash_obj.save()
        response = self.client.get(
            '/hash/b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9')
        self.assertContains(response, 'hello world')

    def test_bad_data(self):
        def bad_hash():
            hash = Hash()
            hash.hash = 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9wwwwwwwwwww'
            hash.full_clean()
        self.assertRaises(ValidationError, bad_hash)
