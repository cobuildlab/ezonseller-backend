# Documentation of services app Payment
## Term and Conditions

* Url

   http://127.0.0.1:8080/terms

* Method

   **GET**

* Url Params

   **None**

* Data Params
  
  **None**

* Success Response:
   * code : 200
   ```javascript
   {
    "description": "Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica a la imprenta) desconocido usó una galería de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. No sólo sobrevivió 500 años, sino que tambien ingresó como texto de relleno en documentos electrónicos, quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas \"Letraset\", las cuales contenian pasajes de Lorem Ipsum, y más recientemente con software de autoedición, como por ejemplo Aldus PageMaker, el cual incluye versiones de Lorem Ipsum."
   }
   ```

* Error Response:
   * code: 400
   ```javascript
   {
        "message":"error"
   } 
   ```
* Notes: 

   **None**
   
## Plan subcription
The token of user is required to call this service

* Url

   http://127.0.0.1:8080/payment/plans

* Method

   **GET**

* Url Params

   **None**

* Data Params
  
   **None**

* Success Response:
   * code : 200
   ```javascript
   [
           {
            "cost": 100,
            "duration": "1 mounth",
            "terms": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "list": [
                "lorem impsu 1",
                "lorem impsu 2"
            ],
            "title": "plan vip",
            "type_plan": "vip",
            "id": 1,
            "image": "https://ezonsellerbackend.herokuapp.com/media/VIP.png"
        }
    ] 
   ```

* Error Response:
   * code: 400
   ```javascript
   {
      "message": "error"
   } 
   ```
* Notes: 

   **None**

## Payment history
The token of user is required to call this service

* Url

   http://127.0.0.1:8080/payment/history

* Method

   **GET**

* Url Params

   **None**

* Data Params
  
   **None**

* Success Response:
   * code : 200
   ```javascript
    {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "date_start": "2018-01-16T01:44:13Z",
            "user": "solrac",
            "date_finish": "2018-02-15T01:44:13Z",
            "cost": 100,
            "title": "plan vip",
            "id": 1
        },
        {
            "date_start": "2018-01-16T02:06:08Z",
            "user": "solrac",
            "date_finish": "2018-02-15T02:06:08Z",
            "cost": 200,
            "title": "plan suprime",
            "id": 2
        }
    ]
  } 
   ```

* Error Response:
   * code: 400
   ```javascript
   {
      "message":"error" 
   } 
   ```
* Notes: 

This service activates paging when the user has more than 10 payment records in his account
  
## Purchase Plan subcription
The token of user is required to call this service

* Url

   http://127.0.0.1:8080/payment/purchase/

* Method

   **POST**

* Url Params

   **None**

* Data Params
  ```javascript
  {
      "id_plan":1,
      "id_card":6,
      "accept": "True",
      "automatic": "False"
  } 
  ```

* Success Response:
   * code : 200
   ```javascript
   {
      "message": "the purchase of the plan has been successful",
      "title": "plan vip",
      "date_finish": "2018-03-08T02:43:58.167673",
      "user": "solrac",
      "cost": 100,
      "id": 4,
      "date_start": "2018-02-06T02:43:58.167829"
    }
   ```

* Error Response:
   * code: 400
   this service have multiple error message 
   
   ```javascript
   {
      'message': 'the plan id cant be empty'
      'message': 'the credit card id cant be empty'
      'message': 'the accept term and coditions cant be empty'
      'message': 'the payment automatic cant be empty'
      'message': 'You must accept the terms and conditions'
      'message': 'this field only contains true or false'
      'message': 'the plan does not exist'
      'message': 'the credit card with you buy this plan dont belong a your account, or not exist'
      'message': 'payment could not be made, please notify your bank distributor'
   } 
   ```
   
   all message this activated in different situations check the code in the app payment service PurchasePlanView line 72
   
* Notes: 
to user call this service is necesary be have a credit card associate to account, to realize the payment correspondent to acquired the plan, the data params have a field called automatic this is true the payment has realize automatic for the credit card if not only has realize a one payment

## Cancel subcription
The token of user is required to call this service

* Url

   http://127.0.0.1:8080/payment/cancel-subscription/

* Method

   **POST**

* Url Params

   **None**

* Data Params
  ```javascript
    {
      "id_plan":2,
      "option": "no me gusto nada :)",
      "reason":"no me gusto el desempeño lol jajjaa"
    }
  ```
**the reason param is optional field**

* Success Response:
   * code : 200
   ```javascript
    {
      "message": "the cancel subscription of plan has been accept successfully"
    }   
   ```

* Error Response:
   * code: 400
   ```javascript
   {
      "message": "the plan does not exist"
   } 
   ```
* Notes: 

this service has been three error message one the plan does not exits, the other two are by empty field
   
## Cancel subcription
The token of user is required to call this service

* Url

   http://127.0.0.1:8080/payment/

* Method

   **GET**

* Url Params

   **None**

* Data Params
  
  **None**

* Success Response:
   * code : 200
   ```javascript
      [
        {
            "id": 1,
            "list": [
                "lorem impsu 1",
                "lorem impsu 2",
                "lorem impsu 3"
            ],
            "description": "lorem imsu asdjasuqweqiwh lkljlskadasdkn asdljkasld qwiehqowe alsdn lasd"
        } 
      ]
   ```
* Notes: 

   **None**

## Credit card
The token of user is required to call this service

* Url

   http://127.0.0.1:8080/payment/card/

* Method

   **POST**

* Url Params

   **None**

* Data Params
  ```javascript
  {
    "first_name":"",
    "last_name": "olivero",
    "number_card":"4032036441888582",
    "type_card":"mastercard",
    "cod_security":"321",
    "date_expiration":"2022-01-01"
  } 
  ```

* Success Response:
   * code : 200
   ```javascript
   {
      "id": 9,
    "first_name": "carlos",
    "last_name": "olivero",
    "type_card": "mastercard",
    "number_card": "4032036441888582",
    "cod_security": "321",
    "date_expiration": "2022-01-01",
    "message": "the credit card has been saved successfully"
   } 
   ```

* Error Response:
   * code: 400
   ```javascript
   {
    "message": "first_name: This field may not be blank."
   } 
   ```
* Notes: 
this service will activate the error messages when empty fields are missing, as well as when a credit card number or date error is repeated

## Credit card
The token of user is required to call this service

* Url

   http://127.0.0.1:8080/payment/card/

* Method

   **GET**

* Url Params

   **None**

* Data Params
  
  **None**

* Success Response:
   * code : 200
   ```javascript
       [
          {
              "number_card": "4032036441888581",
              "id": 1,
              "month": "01",
              "year": "23",
              "last_name": "carlos",
              "first_name": "olivero",
              "cod_security": "200"
          },
          {
              "number_card": "123456789102",
              "id": 2,
              "month": "01",
              "year": "23",
              "last_name": "carlos",
              "first_name": "olivero",
              "cod_security": "300"
          }     
        ] 
   ```

* Error Response:
   * code: 400
   ```javascript
   {
      "message":"error"
   } 
   ```
* Notes: 

   **None**

## Credit card
The token of user is required to call this service

* Url

   http://127.0.0.1:8080/payment/card/idcard/

* Method

   **PUT**

* Url Params

   **None**

* Data Params
  ```javascript
  {
  "first_name":"carlos",
  "last_name": "olivero",
  "number_card":"4032036441888582",
  "type_card":"mastercard",
  "cod_security":"321",
  "date_expiration":"2022-01-01"
  } 
  ```

* Success Response:
   * code : 200
   ```javascript
   {
      "id": 9,
    "first_name": "carlos",
    "last_name": "olivero",
    "type_card": "mastercard",
    "number_card": "4032036441888582",
    "cod_security": "321",
    "date_expiration": "2022-01-01",
    "message": "the information of your credit card has been updated successfully"
   } 
   ```

* Error Response:
   * code: 400
   ```javascript
   {
      "message":"cod_security: This field may not be blank."
   } 
   ```
* Notes: 

In the case the service post, the same conditions apply to message error  
 
## Credit card
The token of user is required to call this service

* Url

   http://127.0.0.1:8080/payment/card/idcard/

* Method

   **DELETE**

* Url Params

   **None**

* Data Params
  
  **None**

* Success Response:
   * code : 200
   ```javascript
   {
    "message": "The credit card has deleted form your account"
   } 
   ```
   
* Notes: 

   **None**


