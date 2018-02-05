from . import utils


def query(receipt_number):
    '''Query USCIS with a receipt number and fetch the message.

    Args:
        receipt_number (str):   SRC1890055883

    Returns:
        status (dict):  {title: title, message: message}
    '''

    url = 'https://egov.uscis.gov/casestatus/landing.do'

    driver = utils.start_driver('chrome', verbose=True)
    status = {'receipt': receipt_number, 'title': None, 'message': None}

    try:
        utils.open_url(driver, url)
        driver.find_element_by_id('receipt_number').send_keys(receipt_number)
        driver.find_element_by_xpath('//*[@type="submit"]').click()
        utils.wait(3)

        title = driver.find_element_by_xpath('//h1')
        message = title.find_element_by_xpath('../p').text
        title = title.text
        status = {'receipt': receipt_number, 'title': title, 'message': message}

    finally:
        utils.wait(3)
        utils.close_driver(driver, verbose=True)

    return status
