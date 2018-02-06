# Documentation of services app Product
## Country List
* Url

  http://127.0.0.1:8080/country-list/

* Method

  **GET**

* Url Params

  **None**

* Data Params
 
  **None**

* Success Response:
   * code: 200
    ```javascript
     [
      {
          "id": 1,
          "name": "Brazil",
          "code": "BR"
      },
      {
          "id": 2,
          "name": "Canada",
          "code": "CA"
      }
  ]
   ```  
* Notes:
 
  get country list associate to domain amazon 
  
## Country
Token is required to this service

* Url

  http://127.0.0.1:8080/country/

* Method

  **GET**

* Url Params

  **None**

* Data Params
 
  **None**

* Success Response:
   * code: 200
    ```javascript
     [
      {
          "name": "United States",
          "code": "US"
      }
     ]
   ```  
* Notes:
  
 get all the countries of the amazon accounts associated with the profile the ezonseller
 
 ## Search Amazon Prodcut
 Token is required to this service
 
 * Url

  http://127.0.0.1:8080/product/amazon-search/
  
  example  /product/amazon-search/?keyword=apple macbook pro&category=All&country=US&limit=5&offset=0

* Method

  **GET**

* Url Params

  **keyword** title of product to search
  
  **category** category of product
  
  **country** country to search the product, this depend the country your register in amazon associate account
  
  **limit** limit of product to get
  
  **offset** pagination of product

* Data Params

  **None**

* Success Response:
   * code: 200
    ```javascript
     [
      {
          "features": [
              "3.1GHz dual-core Intel Core i5 processor with Turbo Boost up to 3.5GHz",
              "16GB 2133MHz LPDDR3 memory",
              "256GB SSD storage",
              "Intel Iris Plus Graphics 650",
              "Touch Bar and Touch ID"
          ],
          "detail_page_url": "https://www.amazon.com/Apple-MacBook-Retina-3-1GHz-Version/dp/B075V8D6XM?SubscriptionId=AKIAJNSQTMKQ2VCLMZPQ&tag=ezonseller-20&linkCode=xm2&camp=2025&creative=165953&creativeASIN=B075V8D6XM",
          "title": "Apple 13\" MacBook Pro, Retina, Touch Bar, 3.1GHz Intel i5 Dual Core, 16GB RAM, 256GB SSD, Silver (Newest Version)",
          "availability": "Usually ships in 24 hours",
          "price_and_currency": [
              1999,
              "USD"
          ],
          "offer_url": "http://www.amazon.com/dp/B075V8D6XM/?tag=ezonseller-20",
          "large_image_url": "https://images-na.ssl-images-amazon.com/images/I/41Wc8svntML.jpg",
          "asin": "B075V8D6XM"
      },
      {
          "features": [
              "Fifth-generation Intel Core processors",
              "Lasts up to an incredible 12 hours between charges",
              "Incredibly thin 0.68-inch design weighing only 2.96 pounds",
              "Experience wireless performance up to 3x faster than the previous Wi-Fi generation",
              "SSD storage is up to 17x faster than a 5400-rpm notebook hard drive"
          ],
          "detail_page_url": "https://www.amazon.com/Apple-13-3-MacBook-Air-Silver/dp/B015WXL0C6?psc=1&SubscriptionId=AKIAJNSQTMKQ2VCLMZPQ&tag=ezonseller-20&linkCode=xm2&camp=2025&creative=165953&creativeASIN=B015WXL0C6",
          "title": "Apple 13.3\" MacBook Air ( Silver)",
          "availability": "Usually ships in 24 hours",
          "price_and_currency": [
              844.49,
              "USD"
          ],
          "offer_url": "http://www.amazon.com/dp/B015WXL0C6/?tag=ezonseller-20",
          "large_image_url": "https://images-na.ssl-images-amazon.com/images/I/51GRACqhHbL.jpg",
          "asin": "B015WXL0C6"
      },
      {
          "total_items": 50
      }
    ]
   ```  
* Error Response:
  this service have many message error, check the code in app product to see all messages an validations
  
  * code: 400
   ```javascript
   {
       'message': 'the limit is required, cant be empty'
       'message': 'the offset is required, cant be empty'
       'message': 'the title cant be empty'
       'message': 'the country cant be empty'
       'message': 'the category cant be empty'
       'message': 'the country you are sending is not assigned to your account'
       'message': 'the country does not exist'
   }
   ``` 
* Notes:
 
  **None**
  
 ## Last products Amazon
 Token is required to this service
 
 * Url

  http://127.0.0.1:8080/product/amazon-lastsearch/

* Method

  **GET**

* Url Params

  **None**

* Data Params
 
  **None**

* Success Response:
   * code: 200
    ```javascript
     [
      {
          "title": "Apple 13\" MacBook Pro, Retina, Touch Bar, 3.1GHz Intel i5 Dual Core, 16GB RAM, 256GB SSD, Silver (Newest Version)",
          "features": "3.1GHz dual-core Intel Core i5 processor with Turbo Boost up to 3.5GHz16GB 2133MHz LPDDR3 memory256GB SSD storageIntel Iris Plus Graphics 650Touch Bar and Touch ID",
          "availability": "Usually ships in 24 hours",
          "asin": "B075V8D6XM",
          "detail_page_url": "https://www.amazon.com/Apple-MacBook-Retina-3-1GHz-Version/dp/B075V8D6XM?SubscriptionId=AKIAJNSQTMKQ2VCLMZPQ&tag=ezonseller-20&linkCode=xm2&camp=2025&creative=165953&creativeASIN=B075V8D6XM",
          "large_image_url": "https://images-na.ssl-images-amazon.com/images/I/41Wc8svntML.jpg",
          "price_and_currency": "1999 USD",
          "offer_url": "http://www.amazon.com/dp/B075V8D6XM/?tag=ezonseller-20"
      }
      ]
   ```  
* Notes:
 
 this service save one product whem the user search product in amazon, max to show is 12 whem it exceeds the limit delete the firts product save
  
 ## Search Ebay Product 
 Token is required to this service
 
 * Url

  http://127.0.0.1:8080/product/ebay-search/
  
  example /product/ebay-search/?keyword=ps4&country=UK&limit=5&offset=0

* Method

  **POST**

* Url Params

  **keyword** title of product to search
  
  **country** country the product to search, depend the country associate to amazon account
  
  **limit** limit of product to get
  
  **offset** pagination of product

* Data Params

  **None**
  
* Success Response:
   * code: 200
    ```javascript
     [
      {
          "title": "PS4 Pro White 1TB Console",
          "galleryURL": "http://thumbs1.ebaystatic.com/m/mj_61T4TqnMiPqUbaO26WjA/140.jpg",
          "country": "GB",
          "itemId": "382275028220",
          "location": "United Kingdom",
          "sellingStatus": "299.85GBP",
          "viewItemURL": "http://www.ebay.co.uk/itm/PS4-Pro-White-1TB-Console-/382275028220",
          "globalId": "EBAY-GB"
      },
      {
          "title": "Sony PlayStation 4 PS4 Pro 1TB STAR WARS: Battlefront II Limited Edition Bundle",
          "galleryURL": "http://thumbs1.ebaystatic.com/m/mIK95jqVbNJtoPnF8CLM_Xg/140.jpg",
          "country": "GB",
          "itemId": "332541265624",
          "location": "Leyland,United Kingdom",
          "sellingStatus": "96.85GBP",
          "viewItemURL": "http://www.ebay.co.uk/itm/Sony-PlayStation-4-PS4-Pro-1TB-STAR-WARS-Battlefront-II-Limited-Edition-Bundle-/332541265624",
          "globalId": "EBAY-GB"
      },
      {
          "total_items": 100
      }
    ]
   ```  
* Error Response:

this service have many message error, check the code in app product to see all messages an validations
  * code: 400
   ```javascript
   {
        'message': 'The limit is required, cant be empty'
        'message': 'The offset is required, cant be empty'
        'message': 'The keyword cant be empty'
        'message': 'The country cant be empty'
        'message': 'The country you send does not exist in global ebay api'
   }
   ``` 
* Notes:
 
  **None**
  
 ## CRUD Amazon account
 Token is required to this service
 * Url

  http://127.0.0.1:8080/product/amazon/

* Method

  **POST**

* Url Params

  **None**

* Data Params
 ```javascript
  {
    "country_id":14,
    "associate_tag":"prueba",
    "access_key_id":"AJASKD12LJASLDKJ123",
    "secrect_access_key":"g8kbaskdo71y2mbzjc7612u3jaspoqwjebcsadasd"
  }
 ```

* Success Response:
   * code: 200
    ```javascript
    {
        "id": 6,
        "secrect_access_key": "g870VvsBmBbb5YuWrmME7hJ/ZgIc12wtHdfm6q5I",
        "access_key_id": "AKIAJNSQTMKQ2VCLMZPQ",
        "country": "United States",
        "associate_tag": "ezonseller-20",
        "modified": "2018-02-01T15:15:06.333767Z",
        "message": "the ebay account has been saved successfully"
    }
   ```  
* Error Response:
this service posse many massage error please check the code and validiation to see all message

  * code: 400
   ```javascript
   {
     "message":"The amazon associate username is required"
   }
   ``` 
* Notes:
 
  **None**
  
 ## CRUD Amazon account
 Token is required to this service
 * Url

  http://127.0.0.1:8080/product/amazon/

* Method

  **GET**

* Url Params

  **None**

* Data Params
 
  **None**
 
* Success Response:
   * code: 200
    ```javascript
    [
      {
          "id": 6,
          "secrect_access_key": "g870VvsBmBbb5YuWrmME7hJ/ZgIc12wtHdfm6q5I",
          "access_key_id": "AKIAJNSQTMKQ2VCLMZPQ",
          "country": "United States",
          "associate_tag": "ezonseller-20",
          "modified": "2018-02-01T15:15:06.333767Z",
      }
    ]
   ```  
* Notes:
 
  **None**
  
 ## CRUD Amazon account
 Token is required to this service
 * Url

  http://127.0.0.1:8080/product/amazon/id/

* Method

  **PUT**

* Url Params

  **None**

* Data Params
in this service only cant be editing the access_key_id and secrect_access_key
 
 ```javascript
  {
    "associate_tag":"prueba",
    "access_key_id":"AJASKD12LJASLDKJ123",
    "secrect_access_key":"g8kbaskdo71y2mbzjc7612u3jaspoqwjebcsadasd"
  }
 ```

* Success Response:
   * code: 200
    ```javascript
   {
        "id": 6,
        "secrect_access_key": "g870VvsBmBbb5YuWrmME7hJ/ZgIc12wtHdfm6q5I",
        "access_key_id": "AKIAJNSQTMKQ2VCLMZPQ",
        "country": "United States",
        "associate_tag": "ezonseller-20",
        "modified": "2018-02-01T15:15:06.333767Z",
        "message": "the ebay account has been updated successfully"
    }
   ```  
* Error Response:
 this service posse many massage error please check the code and validiation to see all message
 
  * code: 400
   ```javascript
   {
     "message":"The amazon associate username is required"
   }
   ``` 
* Notes:
 
  **None**
  
 ## CRUD Amazon account
 Token is required to this service
 * Url

  http://127.0.0.1:8080/product/amazon/id/

* Method

  **DELETE**

* Url Params

  **None**

* Data Params
 
 **None**

* Success Response:
   * code: 200
    ```javascript
   {
     "message":"The amazon key has been deleted"
   }
   ``` 
* Notes:
 
  **None**
  
 ## CRUD Ebay account
 Token is required to this service
 * Url

  http://127.0.0.1:8080/product/ebay/

* Method

  **POST**

* Url Params

  **None**

* Data Params
 ```javascript
  {
	  "client_id":"carlosol-prueba-PRD-asd123122sad-e9162g7123"
  }
 ```

* Success Response:
   * code: 200
    ```javascript
    {
        "client_id":"carlosol-prueba-PRD-asd123122sad-e9162g7123"
        "id": 3,
        "modified": "2018-01-18T14:13:54.488699Z",
        "message": "the ebay account has been saved successfully"
    }
   ```  
* Error Response:
this service posse many massage error please check the code and validiation to see all message

  * code: 400
   ```javascript
     {
       "message": "The ebay client_id exist"
     }
   ``` 
* Notes:
 
  **None**
  
 ## CRUD Ebay account
 Token is required to this service
 * Url

  http://127.0.0.1:8080/product/ebay/ 

* Method

  **GET**

* Url Params

  **None**

* Data Params

  **None**

* Success Response:
   * code: 200
    ```javascript
   [
    {
       "client_id":"carlosol-prueba-PRD-asd123122sad-e9162g7123"
        "id": 3,
        "modified": "2018-01-18T14:13:54.488699Z"
    }
   ]
   ``` 
* Notes:
 
  **None**
  
 ## CRUD Ebay account
 Token is required to this service
 * Url

  http://127.0.0.1:8080/product/ebay/id/

* Method

  **PUT**

* Url Params

  **None**

* Data Params
 ```javascript
   {
    "client_id":"carlosol-prueba-PRD-asd123122sad-e9162g7123"
   } 
 ```

* Success Response:
   * code: 200
    ```javascript
    {
        "client_id":"carlosol-prueba-PRD-asd123122sad-e9162g7123"
        "id": 3,
        "modified": "2018-01-18T14:13:54.488699Z",
        "message": "the ebay account has been updated successfully"
    }
   ```  
* Error Response:
  this service posse many massage error please check the code and validiation to see all message
  
  * code: 400
   ```javascript
   {
      "message":"the client_id cant be empty"   
   }
   ``` 
* Notes:
 
  **None**
  
 ## CRUD Ebay account
 Token is required to this service
 * Url

  http://127.0.0.1:8080/product/ebay/id/

* Method

  **DELETE**

* Url Params

  **None**

* Data Params
 
  **None**

* Success Response:
   * code: 200
    ```javascript
   {
     "message":"The ebay key has been deleted"
   }
   ```  
* Notes:
 
  **None**
 
