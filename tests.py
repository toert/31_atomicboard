import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CREATE_USER_URL = 'http://atomicboard.devman.org/create_test_user/'
MAIN_PAGE_URL = 'http://atomicboard.devman.org/'
JQUERY_URL = "http://code.jquery.com/jquery-1.11.2.min.js"
TIMEOUT = 20
TEST_STRING = 'test-test-test'


class AtomicTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get(CREATE_USER_URL)
        self.driver.find_element_by_xpath('/html/body/form/button').click()
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/p[2]')))
        self.driver.get(MAIN_PAGE_URL)
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'tickets-column')))

    def test_actual_tasks(self):
        self.assertTrue(self.driver.find_element_by_class_name('js-tickets-column'))

    def test_editing_task(self):
        self.driver.find_element_by_class_name('js-ticket_description_text').click()
        task_description = self.driver.find_element_by_class_name('editable-has-buttons')
        task_description.send_keys(TEST_STRING)
        task_description.send_keys(Keys.RETURN)
        self.assertTrue((task_description.get_attribute('value')).startswith(TEST_STRING))

    def test_closing_task(self):
        status = self.driver.find_element_by_class_name('ticket_status')
        status.click()
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'change-status-form__button')))
        self.driver.find_elements_by_class_name('change-status-form__button')[2].click()
        self.assertEqual(status.text, 'closed')

    def test_add_task(self):
        self.driver.find_element_by_class_name('add-ticket-block_button').click()
        new_task_name = self.driver.find_element_by_class_name('editable-has-buttons')
        new_task_name.send_keys(TEST_STRING)
        new_task_name.send_keys(Keys.RETURN)
        self.assertTrue(self.driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(TEST_STRING)))

    def test_drag_and_drop_task(self):
        columns = self.driver.find_elements_by_class_name('tickets-column')
        draggable = columns[0].find_element_by_class_name('js-ticket')
        draggable_text = draggable.find_element_by_class_name('panel-heading_text').text
        with open("jquery_load_helper.js") as jquery_file:
            load_jquery_js = jquery_file.read()
        with open("drag_and_drop_helper.js") as drag_and_drop_file:
            drag_and_drop_js = drag_and_drop_file.read()
        self.driver.execute_async_script(load_jquery_js, JQUERY_URL)
        self.driver.execute_script(drag_and_drop_js
            + "$('div.js-ticket:eq(0)').simulateDragDrop({ dropTarget: 'span.tickets-column:eq(1)'});")

        droppable_text = columns[1].find_element_by_xpath(".//*[contains(text(), '{}')]".format(draggable_text)).text
        self.assertEqual(droppable_text, draggable_text)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()