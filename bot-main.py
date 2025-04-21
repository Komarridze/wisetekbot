import urllib, json
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
start = time.time()



##
# User Information 
##

#!

CCNumber="1456 1771 2992 0022"
CCExpiry="11/25"
CCVerification="123"

EXPIRY = 1767225105

POOL = 100000
USDTOUAH = 41.3825

FIRSTNAME='John';
LASTNAME='Doe';
COMPANY = '' #opitional
EMAIL = '' #optional
ADDRESS = '12345 Some Street';
SUITE = '' #optional
CITY = 'Mermaid Beach';
STATE = 'IA';
ZIP = '50317';
PHONE = '(319) 337-3024';



DOMAIN = "https://www.wisetekmarket.com"
HANDLE = 'iphone-8-plus-2'
URL = DOMAIN + "/products/" + HANDLE;

QUANTITY = 'max'

CONDITION = 'Fair' # Very Good / Fair
MEMSPACE1 = '64'
MEMSPACE2 = '128'
#!


options = webdriver.ChromeOptions()


options.add_argument("--incognito")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
# options.add_argument("--headless") # Comment that line to see script running in Chrome.
driver = webdriver.Chrome(options=options)

with open('./cookie.json', 'r') as ck:
    cookie_data = json.loads(ck.read());
    ck.close();

# print(cookie_data)



response = urllib.request.urlopen(URL)
data = response.read()

STOLEN = json.loads(str(data).split('<script type="application/json">')[2].split('</script>')[0].replace(' ', '').replace(r'\n', ''))

response_comparison = urllib.request.urlopen(URL + '.json');
data_comparison = json.loads(response_comparison.read())

#? print(data_comparison)

#! ЕСЛИ ЗАХОЧЕШЬ ВРУЧНУЮ ПРОЧЕКАТЬ РЕКВЕСТ
# with open('response.json', 'w') as res:
#     # res.write(str(response.read()).split('<script type="application/json">')[2].split('</script>')[0].replace(' ', '').replace(r'\n', ''));
#     res.write(str(STOLEN))
#     res.close();

#? print(STOLEN)

#! option1 is CONDITION
#! option2 is MEMSPACE

#? json -> product -> variants[] -> option1 / option2


driver.get(DOMAIN + '/account/login')
for cookie in cookie_data:
    driver.add_cookie(cookie_dict={"name":cookie['name'],"value":cookie['value'],"path":cookie['path'],"domain":cookie['domain'],"secure":cookie['secure'],"httpOnly":cookie['httpOnly'], "expiry":EXPIRY});
time.sleep(1);

# driver.get(DOMAIN + '/account/login')

# time.sleep(1);
# driver.find_element(By.ID, 'customer-email').send_keys(EMAIL);
# time.sleep(2);
# driver.find_element(By.ID, 'customer-password').send_keys(PASSWORD);
# time.sleep(1.4);
# driver.find_element(By.XPATH, '//button[text()="Sign in"]').click();


# time.sleep(8);
while True:
    for i in data_comparison['product']['variants']: 
        # print(i['option1'])
        # print(i['option2']);

        CONDKEY = 'option1'
        MEMKEY = 'option2'
                    


        if ((i[CONDKEY] == CONDITION) and ((i[MEMKEY] == MEMSPACE1 + ' GB') or i[MEMKEY] == MEMSPACE2 + ' GB')):
            # print(CONDITION);
            # print(i[MEMKEY]);
            for final in STOLEN:
                # print(final['id'])
                # print(i['id'])
                # print(final['inventory_quantity'])
                if ((final['id'] == i['id']) and (final['inventory_quantity'] > 0)):
                    print('[DEBUG] ' + str(final))
                    print("[INFO] Цена артикула: " + i['price'])

                    MAXQUANTITY = (POOL / USDTOUAH) // float(i['price']);
                    print("[INFO] Макс. количество таких артикулов: " + str(MAXQUANTITY))



                    link = DOMAIN + '/cart/' + str(final['id']) + ':' + (QUANTITY if (QUANTITY != 'max' and int(QUANTITY) <= MAXQUANTITY) else (str(final['inventory_quantity']) if final['inventory_quantity'] <= MAXQUANTITY else str(int(MAXQUANTITY)))) + '?';
                    driver.get(link);

                    print('[COLLECT] Артикул ' + str(final['id']) + ' добавлен в корзину в количестве ' + str(final['inventory_quantity']) + '.')
                    
                    # with open('source.html', 'w', encoding='utf-8') as src:
                    #     src.write(driver.page_source)
                    #     src.close();                


                    print('[DEBUG] ' + driver.current_url)

                    time.sleep(2);

                    #! SHIPPING PART 1

                    # SECRET = int((driver.page_source.split('input id="')[1].split('"')[0])[9::])
                    # SECRET2 = int((driver.page_source.split('select id="')[3].split('"')[0])[6::])
                    # print(Fore.GREEN + f'[COLLECT] Сессионные ключи элементов: {SECRET} и {SECRET2}.' + Fore.RESET)





                    #! ЕСЛИ ХОЧЕШЬ ЧИСТОЕ АВТОЗАПОЛНЕНИЕ ОТКОММЕНТИРУЙ

                    # FIELDS = driver.find_elements(By.XPATH, '//input[contains(@id, "TextField")]')
                    # SELECT = driver.find_elements(By.XPATH, '//select[contains(@id, "Select")]')[2]
                    # shippingAddr = driver.find_element(By.ID, 'shipping-address1');


                    # FIELDS[0].clear()
                    # FIELDS[1].clear()
                    # FIELDS[2].clear()
                    # FIELDS[3].clear()
                    # FIELDS[4].clear()
                    # FIELDS[5].clear()
                    # FIELDS[6].clear()
                    # shippingAddr.clear();



                    # FIELDS[0].send_keys(FIRSTNAME);
                    # time.sleep(0.5);
                    # FIELDS[1].send_keys(LASTNAME);
                    # time.sleep(0.5);
                    # FIELDS[2].send_keys(COMPANY);
                    # time.sleep(0.5);
                    # shippingAddr.send_keys(ADDRESS);
                    # time.sleep(0.5);
                    # FIELDS[3].send_keys(SUITE);
                    # time.sleep(0.5);
                    # FIELDS[4].send_keys(CITY);
                    # time.sleep(0.5);
                    # SELECT.click();
                    # time.sleep(0.5);
                    # driver.execute_script(f'arguments[0].value="{ADDRESS}"', shippingAddr)
                    # time.sleep(0.5);
                    # FIELDS[5].send_keys(ZIP);
                    # time.sleep(0.5);
                    # FIELDS[6].send_keys(PHONE);
                    # time.sleep(0.5);

                    #!

                    
                    driver.find_element(By.XPATH, '//button[contains(@type, "submit")]').click()

                    time.sleep(2)
                    print('[DEBUG] ' + driver.current_url)

                    driver.find_element(By.XPATH, '//button[contains(@type, "submit")]').click()

                    time.sleep(2)
                    print('[DEBUG] ' + driver.current_url)

                    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[contains(@id, 'card-fields-number-')]"))
                    driver.find_element(By.ID, 'number').clear()
                    driver.find_element(By.ID, 'number').send_keys(CCNumber);
                    driver.switch_to.parent_frame();
                    time.sleep(0.5);

                    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[contains(@id, 'card-fields-expiry-')]"))
                    driver.find_element(By.ID, 'expiry').clear();
                    driver.find_element(By.ID, 'expiry').send_keys(CCExpiry.split('/')[0]);
                    driver.find_element(By.ID, 'expiry').send_keys(CCExpiry.split('/')[1]);
                    driver.switch_to.parent_frame();
                    time.sleep(0.5);

                    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[contains(@id, 'card-fields-verification_value-')]"))
                    driver.find_element(By.ID, 'verification_value').clear();
                    driver.find_element(By.ID, 'verification_value').send_keys(CCVerification);
                    driver.switch_to.parent_frame();
                    time.sleep(0.5);

                    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[contains(@id, 'card-fields-name-')]"))
                    driver.find_element(By.ID, 'name').clear();
                    driver.find_element(By.ID, 'name').send_keys(FIRSTNAME+' '+LASTNAME);
                    driver.switch_to.parent_frame();

                    driver.find_element(By.ID, 'billing_address_selector-shipping').click();
                    time.sleep(0.5);


                    #! PAYMENT
                    print('[PAYMENT] Оформляю покупку...')
                    driver.find_element(By.XPATH, '//button[contains(@type, "submit")]').click()

                    time.sleep(3)
                else:
                    time.sleep(10);

