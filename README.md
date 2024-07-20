# Currency Exchange API

This project provides an API for managing currencies and exchange rates.

## Installation

To install the dependencies, run the following commands:

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows Users

If you are using Windows, activate the virtual environment with the following command:

```sh
venv\Scripts\activate
```

## Database Initialization

To initialize the database, run the following command:

```sh
python init_db.py
```

## Running the Project

To run the project, execute the following command:

```sh
python main.py
```

## Currencies

### Get All Currencies

- **URL:** `/currencies`
- **Method:** GET
- **Description:** Returns a list of all currencies.
- **Example Response:**
  ```json
  [
      {
          "id": 0,
          "name": "United States dollar",
          "code": "USD",
          "sign": "$"
      },
      {
          "id": 0,
          "name": "Euro",
          "code": "EUR",
          "sign": "€"
      }
  ]
  ```

- **HTTP Response Codes:**
  - **Success:** 200
  - **Error (e.g., database unavailable):** 500


### Get Currency Information

- **URL:** `/currency/EUR`
- **Method:** GET
- **Description:** Returns information about a currency by its code.
- **Example Response:**
  ```json
  {
      "id": 0,
      "name": "Euro",
      "code": "EUR",
      "sign": "€"
  }
  ```
- **HTTP Response Codes:**
  - **Success:** 200
  - **Missing currency code in URL:** 400
  - **Currency not found:** 404
  - **Error (e.g., database unavailable):** 500


### Add New Currency

- **URL:** `/currencies`
- **Method:** POST
- **Description:** Adds a new currency.
- **Request Body:**
  ```json
  {
      "name": "Euro",
      "code": "EUR",
      "sign": "€"
  }
  ```
- **HTTP Response Codes:**
  - **Success:** 201
  - **Missing required form field:** 400
  - **Currency with this code already exists:** 409
  - **Error (e.g., database unavailable):** 500


## Exchanges

### Get All Exchange Rates

- **URL:** `/exchangeRates`
- **Method:** GET
- **Description:** Returns a list of all exchange rates.
- **Example Response:**
  ```json
  [
      {
          "id": 0,
          "baseCurrency": {
              "id": 0,
              "name": "United States dollar",
              "code": "USD",
              "sign": "$"
          },
          "targetCurrency": {
              "id": 1,
              "name": "Euro",
              "code": "EUR",
              "sign": "€"
          },
          "rate": 0.99
      }
  ]
  ```
- **HTTP Response Codes:**
  - **Success:** 200
  - **Error (e.g., database unavailable):** 500

### Get Specific Exchange Rate

- **URL:** `/exchangeRate/USDRUB`
- **Method:** GET
- **Description:** Returns information about a specific exchange rate. The currency pair is specified by consecutive currency codes in the request URL.
- **Example Response:**
  ```json
  {
      "id": 0,
      "baseCurrency": {
          "id": 0,
          "name": "United States dollar",
          "code": "USD",
          "sign": "$"
      },
      "targetCurrency": {
          "id": 1,
          "name": "Euro",
          "code": "EUR",
          "sign": "€"
      },
      "rate": 0.99
  }
  ```
- **HTTP Response Codes:**
  - **Success:** 200
  - **Missing currency codes in URL:** 400
  - **Exchange rate for the pair not found:** 404
  - **Error (e.g., database unavailable):** 500

### Add New Exchange Rate

- **URL:** `/exchangeRates`
- **Method:** POST
- **Description:** Adds a new exchange rate.
- **Request Body:**
  ```json
  {
      "baseCurrencyCode": "USD",
      "targetCurrencyCode": "EUR",
      "rate": 0.99
  }
  ```
- **Example Response:**
  ```json
  {
      "id": 0,
      "baseCurrency": {
          "id": 0,
          "name": "United States dollar",
          "code": "USD",
          "sign": "$"
      },
      "targetCurrency": {
          "id": 1,
          "name": "Euro",
          "code": "EUR",
          "sign": "€"
      },
      "rate": 0.99
  }
  ```
- **HTTP Response Codes:**
  - **Success:** 201
  - **Missing required form field:** 400
  - **Currency pair with this code already exists:** 409
  - **One or both currencies in the pair do not exist in the database:** 404
  - **Error (e.g., database unavailable):** 500

### Update Exchange Rate

- **URL:** `/exchangeRate/USDRUB`
- **Method:** PATCH
- **Description:** Updates an existing exchange rate. The currency pair is specified by consecutive currency codes in the request URL.
- **Request Body:**
  ```json
  {
      "rate": 0.99
  }
  ```
- **Example Response:**
  ```json
  {
      "id": 0,
      "baseCurrency": {
          "id": 0,
          "name": "United States dollar",
          "code": "USD",
          "sign": "$"
      },
      "targetCurrency": {
          "id": 1,
          "name": "Euro",
          "code": "EUR",
          "sign": "€"
      },
      "rate": 0.99
  }
  ```
- **HTTP Response Codes:**
  - **Success:** 200
  - **Missing required form field:** 400
  - **Currency pair not found in the database:** 404
  - **Error (e.g., database unavailable):** 500

### Currency Exchange

- **URL:** `/exchange?from=BASE_CURRENCY_CODE&to=TARGET_CURRENCY_CODE&amount=$AMOUNT`
- **Method:** GET
- **Description:** Calculates the conversion of a specified amount from one currency to another.
- **Example Request:** `GET /exchange?from=USD&to=AUD&amount=10`
- **Example Response:**
  ```json
  {
      "baseCurrency": {
          "id": 0,
          "name": "United States dollar",
          "code": "USD",
          "sign": "$"
      },
      "targetCurrency": {
          "id": 1,
          "name": "Australian dollar",
          "code": "AUD",
          "sign": "A$"
      },
      "rate": 1.45,
      "amount": 10.00,
      "convertedAmount": 14.50
  }
  ```
- **HTTP Response Codes:**
  - **Success:** 200
  - **Missing required query parameter:** 400
  - **Exchange rate for the pair not found:** 404
  - **Error (e.g., database unavailable):** 500