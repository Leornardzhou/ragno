from . import utils
from pyvirtualdisplay import Display


def query(receipt_number_list):
    '''Query USCIS with a receipt number and fetch the message.

    Args:
        receipt_number_list (list):  a list of receipt numbers (str)

    Returns:
        status (dict):
            {rc_number: {title: title (str), message: message (str)}}
    '''

    url = 'https://egov.uscis.gov/casestatus/landing.do'

    # start virtual display
    display = Display(visible=0, size=(1024,768))
    display.start()

    driver = utils.start_driver('chrome', verbose=True)
    status = {}

    try:
        for receipt_number in receipt_number_list:
            utils.print_message('querying receipt number: {}'
                                .format(receipt_number))
            status[receipt_number] = {'title': None, 'message': None}

            utils.open_url(driver, url, reopen=True)
            driver.find_element_by_id('receipt_number')\
                  .send_keys(receipt_number)
            driver.find_element_by_xpath('//*[@type="submit"]').click()
            utils.wait(3)

            title = driver.find_element_by_xpath('//h1')
            status[receipt_number]['message'] \
                = title.find_element_by_xpath('../p').text
            status[receipt_number]['title'] = title.text

    finally:
        utils.close_driver(driver, verbose=True)
        display.stop()

    return status
