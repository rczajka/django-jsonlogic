import django
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class JSONWidgetTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(JSONWidgetTest, cls).setUpClass()
        user = User.objects.create(
            username='user', is_staff=True, is_superuser=True
        )
        user.set_password('secret')
        user.save()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(JSONWidgetTest, cls).tearDownClass()

    def test_operator_not(self):
        """Try to login to admin, go to the editor and use an operator."""
        # Login to admin.
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('user')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        self.selenium.get('%s%s' % (
            self.live_server_url,
            '/admin/example_app/examplemodel/add/'
        ))

        expected_fields = 3
        if django.VERSION >= (1, 9):
            self.selenium.find_element_by_class_name(
                "add-row").find_element_by_tag_name("a").click()
            expected_fields += 1

        fields = self.selenium.find_elements_by_class_name("jsonlogic-field")
        # There should be 4 editors now: one for ExampleModel, one
        # for initial inline, one in added inline (in Django >= 1.9),
        # and one hidden for adding more inlines, which we'll ignore.
        self.assertEqual(len(fields), expected_fields)
        for field in fields[:-1]:
            textarea = field.find_element_by_tag_name("textarea")
            self.assertEqual(textarea.text, '')
            container = field.find_element_by_class_name("jsonlogic-container")
            container.click()
            button = field.find_element_by_xpath('.//span[text()="!"]')
            button.click()
            self.assertEqual(
                textarea.get_attribute('textContent'),
                '{"!":[null]}'
            )
