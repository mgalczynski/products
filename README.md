# Installation
To install this tool you need to either
* install dependencies from [requirements.txt](requirements.txt) in your system
* create [virtual env](https://docs.python.org/3/tutorial/venv.html) and then install dependencies from [requirements.txt](requirements.txt) to this venv by executing `pip install -r requirements.txt`

# Tool usage
`python3 main.py CSV_GZ_FILE URL_JSON_FILE [PORT]`
* `CSV_GZ_FILE` location of csv.gz file
* `URL_JSON_FILE` url with json file

# Endpoints
* `/[?length=LENGTH]` get n cheapest products
* `/PRODUCT_ID` get product information by id

## Entity (product) structure

API endpoints returns the product data as JSON with the following fields:

- `id` as a string
- `name` as a string
- `brand` as a string
- `retailer` as a string
- `price` as a float
- `in_stock` as a boolean

Any fields that aren't available for a product are returned as json `null`.

# Configuration
In [config.py](config.py) you can adjust default length of cheapest products endpoint response and if this tool should ignore duplicates in input 

# Cats

![Cats](cats.gif)