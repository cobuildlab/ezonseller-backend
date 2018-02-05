# Documentation of services app Account
## Login
Grants access to a user to start in Page

* Url

  http://127.0.0.1:8080/login/

* Method

  **POST**

* Url Params

  **None**

* Data Params
 ```javascript
 {
  "username":"solrac",
  "password":"1234qwer"
 } 
 ```
 you can also send the mail

* Success Response:
   * code: 200
    ```javascript
   {
     "last_login": null,
     "Token": "05cf53d9a446c266a815f4ddfeed6cf7393ab2db",
     "id": 1
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "message":"user or pass invalid"
   }
   ``` 
  or

  * code: 400
  ```javascript
  {
    "message": "Inactive user, confirm your account to gain access to the system"
  }
  ```
* Notes:
 
  **None**

## Logout
Logout the user for page

* Url

  http://127.0.0.1:8080/logout/

* Method

  **POST**

* Url Params
  
  **None**

* Data Params
 ```javascript
 {
  "username":"solrac"
 } 
 ```
 you can also send the mail


* Success Response:
   * code: 200
    ```javascript
   {
     "message": "The user has disconnected from the system"
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "message":"the user not exist"
   }
   ``` 
* Notes:
 
  **None**

## Register
register a user in page

* Url

  http://127.0.0.1:8080/accounts/register/

* Method

  **POST**

* Url Params
  
  **None**

* Data Params
 ```javascript
 {
  "username":"solrac5",
  "first_name":"luis",
  "last_name":"olivero",
  "password":"carlos123",
  "email":"carlos5_zeta@hotmail.com"
 } 
 ```

* Success Response:
   * code: 201
    ```javascript
   {
     "message": "The email has been send",
     "username": "solrac5"
   }
   ```  
* Error Response:
  * code: 500
   ```javascript
   {
     "message":"The email cannot be sent and account not created"
   }
   ``` 
* Notes:
 
  **for complete the registraction, user has to confirm your accont, in the case with not realized the confirmation he cant do access to aplication.**

## Activate Account
this service is necesary to completed the registration account

* Url

   http://127.0.0.1:8080/activate/?uidb64=b'Mw'&token=4sj-4ed6eeea47d644d36ec5

* Method

   **POST**

* Url Params

   **None**
   
* Data Params
  
   **uidb64: required**

   **token: required**

* Success Response:
   * code : 200
   ```javascript
   {
    "message": "Thank you for your email confirmation. Now you can login your account."
   } 
   ```

* Error Response:
   * code: 400
   ```javascript
   {
    "message": "Activation link is invalid!"
   } 
   ```
   or

   * code: 400
   ```javascript
   {
     "message": "The user not exist"
   } 
   ```
* Notes: 

   **If the user does not confirm his account then he will not be able to access the page**

## Recovery password
recovery password, sending  code to email 

* Url

   http://127.0.0.1:8080/accounts/recoverypassword/

* Method

   **POST**

* Url Params

   **None**

* Data Params
  ```javascript
  {
   "email":"carlos5_zeta@hotmail.com"
  } 
  ```

* Success Response:
   * code : 200
   ```javascript
   {
     "message":"The email has been send"
   } 
   ```

* Error Response:
   * code: 500
   ```javascript
   {
     "message":"the email cannot be sent"
   } 
   ```
  or

   * code: 400
   ```javascript
   {
     "message":"The email not exist in databas"
   } 
   ```
* Notes: 
   **None**

## Change password

Change password the user

* Url

   http://127.0.0.1:8080/accounts/changepassword/

* Method

   **POST**

* Url Params

   **None**

* Data Params
  ```javascript
  {
   "code":"IQYQRS8NRXUN61ZZUPVC",
   "password":"carlos123"
  } 
  ```

* Success Response:
   * code : 200
   ```javascript
   {
    "message": "The password has been change successfully" 
   } 
   ```

* Error Response:
   * code: 400
   ```javascript
   {
     "message": "Invalid code, please write the correct code"
   } 
   ```
* Notes: 

   **This service should only be used, after making the request to change the password**

## Contact support
the user sends an email, with their doubts, payment problems or errors occurred

* Url

   http://127.0.0.1:8080/accounts/contact/

* Method

   **POST**

* Url Params

   **None**

* Data Params
  ```javascript
  {
   "title":"example title",
   "message":"nuevo mensajae",
   "email":"carlosolivero2@gmail.com"
  } 
  ```

* Success Response:
   * code : 200
   ```javascript
   {
     "message": "Your message has been send successfully"
   } 
   ```

* Error Response:
   * code: 500
   ```javascript
   {
     "message":"Your request cannot be sent"
   } 
   ```
* Notes:
 
   **None**

## Profile User
**Required Token the User**

recibe all information for the user

* Url

   http://127.0.0.1:8080/accounts/profile/

* Method

   **GET**

* Url Params

   **None**

* Data Params
  
   **None**

* Success Response:
   * code : 200
   ```javascript
  { "myPayPal": null,
    "type_plan": "Free",
    "amazon_account": [],
    "plan_subscription": [],
    "credit_cards": [],
    "last_name": "olivero",
    "first_name": "luis",
    "id_plan": 0,
    "username": "soulrac",
    "email": "emailadmin@mozej.com",
    "ebay_account": [],
    "photo": "",
    "id": 5,
    "photo64": null
  } 
  ```

* Error Response:
   * code: 500
   ```javascript
   {
    "message": "error"
   } 
   ```
* Notes: 

   **None**

## Profile User
**Required Token the User**

Edit all information the user

* Url

   http://127.0.0.1:8080/accounts/profile/id_user/

* Method

   **PUT**

* Url Params

   **None**

* Data Params
  ```javascript
  {
   "username":"solrac5",
   "first_name":"luis",
   "last_name":"olivero",
  }
  the profile image can also be edited 

* Success Response:
   * code : 200
   ```javascript
  {
   "last_name": "olivero",
    "id": 3,
    "first_name": "carlos",
    "username": "solrac",
    "email": "carlosolivero2@gmail.com",
    "photo": "http://127.0.0.1:8000/media/image.png"
  } 
  ```

* Error Response:
   * code: 500
   ```javascript
   {
    "message": "error"
   } 
   ```
* Notes: 

   **None**

## Profile User
**Required Token the User**

Edit the password in seccion the user

* Url

   http://127.0.0.1:8080/accounts/profile/id_user/changePassword/

* Method

   **PUT**

* Url Params

   **None**

* Data Params
  ```javascript
  {
    "old_password":"carlos123",
    "new_password":"carlos12"
  } 

* Success Response:
   * code : 200
   ```javascript
  {
    "message":"the password has been chnage sussefully",
    "token":"kusvduasdb123129837shdaasdjv12873y123skd"
  } 
  ```

* Error Response:
   * code: 500
   ```javascript
   {
    "message": "error"
   } 
   ```
* Notes: 

   **None**