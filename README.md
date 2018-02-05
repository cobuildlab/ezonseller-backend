# Ezonseller-backend
This is an application to search for products in amazon and ebay

# System Requirements
This application connects to various apis, one of them is [Paypal SDK Github](https://github.com/paypal/PayPal-Python-SDK)

PayPal SDK depends on the following system libraries:

* libssl-dev
* libffi-dev

On Debian-based systems, run:

```sh
apt-get install libssl-dev libffi-dev
```
two global variables are located in settings.py  
* PAYPAL_MODE = 'sandbox'
* PAYPAL_CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'business
* PAYPAL_CLIENT_SECRECT = 'xxxxxxxxxxxxxxxxxxxxxxxxx'

Do you need created this variables in [Paypal](https://developer.paypal.com/) in secction rest api apps, to generate a sandbox accounts, in production is necesary create a account business change the paypal mode to **live** 

Another api that the application is consuming is Amazon Product Advertising API to search product in amazon, here is the [documentation](https://docs.aws.amazon.com/es_es/AWSECommerceService/latest/DG/Welcome.html).

The library used is [python-amazon-simple-product-api](https://pypi.python.org/pypi/python-amazon-simple-product-api)

This variables are obtained in the page [affiliate-program.amazon](https://affiliate-program.amazon.com/) in the secction tools Product Advertising API here you generate the keys, the amazon associate tag is the name of username with you create accont.

The last api that the application is consuming is [ebay](https://go.developer.ebay.com/) in page register and create a clientid.

When you create a user, you must assign the associated amazon account and ebay developer to perform the product searches

Create a virtualenv a run **pip install -r requirements.txt**
Change the database name, user and password only do you if use postgresql, in case them used another database change all values and install the library associate to them. you also need to change the email settings
