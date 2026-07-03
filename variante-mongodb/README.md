# Mini Inventory API

This is a FastAPI project for a Mini Inventory API that uses MongoDB as the database. The API allows for managing products and movements within an inventory system.

## Project Structure

```
mini-inventory-api
├── app
│   ├── main.py                # Entry point of the FastAPI application
│   ├── models
│   │   ├── product.py         # Defines the Product model
│   │   └── movement.py        # Defines the Movement model
│   ├── routes
│   │   ├── products.py        # Routes for managing products
│   │   └── movements.py       # Routes for managing movements
│   ├── schemas
│   │   ├── product.py         # Pydantic schemas for product validation
│   │   └── movement.py        # Pydantic schemas for movement validation
│   ├── validations
│   │   ├── product.py         # Validation logic for products
│   │   └── movement.py        # Validation logic for movements
│   └── db
│       └── mongodb.py         # MongoDB connection and CRUD operations
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd mini-inventory-api
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up MongoDB:**
   Ensure you have a MongoDB instance running. Update the connection details in `app/db/mongodb.py` as necessary.

5. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## API Usage

### Products

- **Create a Product:** `POST /products`
- **Retrieve Products:** `GET /products`
- **Update a Product:** `PUT /products/{product_id}`
- **Delete a Product:** `DELETE /products/{product_id}`

### Movements

- **Register a Movement:** `POST /movements`
- **Retrieve Movements:** `GET /movements`

## Testing

To run tests, ensure you have pytest installed and run:
```
pytest
```

## License

This project is licensed under the MIT License.