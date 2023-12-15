# Books Library API

A comprehensive RESTful API for library management built with Python Tornado and PostgreSQL. This API provides secure access control, user authentication, and complete library management functionality.

## 🚀 Features

- **RESTful API**: Complete REST API with proper HTTP methods
- **User Authentication**: Secure login/logout with JWT tokens
- **Role-Based Access**: Admin, Authenticated, and Anonymous user types
- **Book Management**: CRUD operations for books and categories
- **Shopping Cart**: Add books to cart and checkout functionality
- **Order Management**: Track past orders and order history
- **Advanced Filtering**: Regex-based search with multiple value support
- **PostgreSQL Database**: Robust database with proper relationships
- **Security**: Password hashing and secure authentication

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Tornado web framework
- psycopg2 for database connectivity

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/books-library-api.git
   cd books-library-api
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**:
   ```bash
   # Create database
   createdb library_db
   
   # Run SQL scripts
   psql -d library_db -f psql_scripts/init.sql
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run the application**:
   ```bash
   python src/main.py
   ```

## 🚀 Quick Start

### API Endpoints

#### Authentication
- `POST /library_api/register` - Register new user
- `GET /library_api/login` - User login
- `POST /library_api/logout` - User logout

#### Book Management
- `GET /library_api/fetch_books` - Get all books with filtering
- `POST /library_api/add_book` - Add new book (Admin only)
- `PATCH /library_api/update_book_details` - Update book (Admin only)
- `DELETE /library_api/delete_book` - Delete book (Admin only)

#### Category Management
- `GET /library_api/fetch_category` - Get all categories
- `POST /library_api/create_category` - Create category (Admin only)
- `PATCH /library_api/update_category` - Update category (Admin only)

#### Shopping Cart
- `GET /library_api/list_books_in_cart` - View cart items
- `POST /library_api/add_to_cart` - Add book to cart
- `POST /library_api/checkout_order` - Checkout cart

#### Order Management
- `GET /library_api/fetch_user_past_orders` - User's order history
- `GET /library_api/fetch_all_past_orders` - All orders (Admin only)

## 📚 Usage Examples

### Register a New User
```bash
curl -X POST http://localhost:8888/library_api/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "name": "John Doe"
  }'
```

### Login
```bash
curl -X GET "http://localhost:8888/library_api/login?email=user@example.com&password=securepassword"
```

### Fetch Books with Filtering
```bash
curl -X GET "http://localhost:8888/library_api/fetch_books?title=Python&category=Programming"
```

### Add Book to Cart
```bash
curl -X POST http://localhost:8888/library_api/add_to_cart \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"book_idx": 1}'
```

## 🏗️ Project Structure

```
books-library-api/
├── src/                    # Source code
│   ├── main.py            # Application entry point
│   ├── handlers/          # Request handlers
│   ├── models/            # Database models
│   ├── utils/             # Utility functions
│   └── config.py          # Configuration
├── psql_scripts/          # Database scripts
│   └── init.sql           # Database initialization
├── tests/                 # Test files
├── requirements.txt        # Python dependencies
├── setup.py              # Package configuration
├── Pipfile               # Pipenv configuration
├── README.md             # This file
└── LICENSE               # MIT License
```

## 🔧 Core Components

### User Types
- **Admin**: Full access and administrative privileges
- **Authenticated User**: Registered and logged-in users
- **Anonymous User**: Unregistered users with limited access

### Authentication Methods
1. **Cookie-based**: Generated on login with 3-day expiry
2. **Basic Token**: Email and password authentication

### Parameter Types
- **[M]**: Mandatory parameters
- **[O]**: Optional parameters

### Advanced Features
- **Regex Filtering**: Regular expressions for better search
- **Multiple Values**: Use `<>` delimiter for multiple values
- **Cascading Deletes**: Proper database relationships
- **Error Handling**: Comprehensive error responses

## 🔗 API Documentation

### GET Endpoints

#### `/library_api/login`
- **Description**: Log in user based on email and password
- **User Allowed**: Anonymous
- **Parameters**: `email [M]`, `password [M]`

#### `/library_api/fetch_books`
- **Description**: Fetch all books with optional filtering
- **User Allowed**: Anonymous
- **Parameters**: `title [O]`, `book_idx [O]`, `author [O]`, `published_year [O]`, `category [O]`
- **Features**: Regex filtering, multiple value support

#### `/library_api/fetch_category`
- **Description**: Fetch all available categories
- **User Allowed**: Admin

### POST Endpoints

#### `/library_api/register`
- **Description**: Register a new user
- **User Allowed**: Anonymous
- **Parameters**: `email [M]`, `password [M]`, `name [O]`

#### `/library_api/add_book`
- **Description**: Create a new book
- **User Allowed**: Admin
- **Parameters**: `title [M]`, `author [M]`, `category_idx [M]`, `published_year [M]`, `price [M]`, `tags [M]`, `stock_unit [M]`

### PATCH Endpoints

#### `/library_api/update_book_details`
- **Description**: Update existing book details
- **User Allowed**: Admin
- **Parameters**: `title [O]`, `author [O]`, `category_idx [O]`, `published_year [O]`, `price [O]`

### DELETE Endpoints

#### `/library_api/delete_book`
- **Description**: Delete existing book with cascading
- **User Allowed**: Admin

## 🛡️ Security Features

- **Password Hashing**: Secure password storage with bcrypt
- **JWT Tokens**: Stateless authentication
- **Role-Based Access**: Granular permission control
- **Input Validation**: Comprehensive parameter validation
- **SQL Injection Protection**: Parameterized queries
- **Error Handling**: Secure error responses

## 🎨 Database Schema

### Tables
- **users**: User account information
- **categories**: Book categories
- **books**: Book information
- **cart**: Shopping cart items
- **orders**: Order history
- **order_items**: Order details

### Relationships
- Proper foreign key relationships
- Cascading deletes for data integrity
- Indexed columns for performance

## 🚀 Deployment

### Local Development
```bash
python src/main.py
```

### Production Deployment
```bash
# Using gunicorn
gunicorn src.main:app --workers 4 --bind 0.0.0.0:8888

# Using Docker
docker build -t books-library-api .
docker run -p 8888:8888 books-library-api
```

### Environment Variables
```bash
DATABASE_URL=postgresql://user:password@localhost/library_db
SECRET_KEY=your-secret-key
DEBUG=False
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ayush Agrawal**
- Email: ayushagrwal031220@gmail.com
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Tornado web framework
- PostgreSQL database
- JWT for authentication
- Python community for excellent libraries

## 📈 Roadmap

- [ ] GraphQL API support
- [ ] Real-time notifications
- [ ] Advanced search with Elasticsearch
- [ ] Mobile app API endpoints
- [ ] Payment integration
- [ ] Email notifications
- [ ] Analytics dashboard
- [ ] Multi-tenant support
- [ ] API rate limiting
- [ ] Comprehensive testing suite

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/books-library-api/issues) page
2. Create a new issue with detailed information
3. Contact the author directly

---

**Happy Coding! 🚀📚**