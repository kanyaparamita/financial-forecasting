# Financial Forecasting System

A real-time financial forecasting system that predicts Cash Flow, Revenue, Expenses, and Profit using machine learning models. The system consists of a FastAPI backend and a Streamlit dashboard for visualization.

## Features

- Real-time financial forecasting
- Multiple forecast types:
  - Cash Flow
  - Revenue
  - Expenses
  - Profit
- Interactive dashboard with visualizations
- Live data updates
- Dual database architecture:
  - Source database (cloud) for historical data
  - Application database (local) for forecasts and metrics
- Containerized deployment with Docker

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Databases**: 
  - Source: Cloud PostgreSQL (read-only)
  - Application: Local PostgreSQL (read/write)
- **ML Models**: Prophet, scikit-learn, TensorFlow
- **Visualization**: Plotly
- **Containerization**: Docker

## Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Docker and Docker Compose
- Access to source PostgreSQL database
- PostgreSQL client tools (optional)

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd financial-forecasting
```

### 2. Set up Python environment
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Install development tools
pip install black isort pytest
```

### 3. Set up environment variables
```bash
# Copy the example environment file to config folder
cp config/.env.example config/.env

# Edit the environment file
nano config/.env  # or use your preferred editor

# Update SOURCE_DATABASE_URL in .env with your cloud database connection string
```

### 4. Start the application
```bash
# Option 1: Using Docker (Recommended for production)
docker-compose up --build

# Option 2: Local development
# Terminal 1: Start FastAPI
uvicorn src.api.main:app --reload

# Terminal 2: Start Streamlit
streamlit run src/visualization/dashboard.py
```

### Development Tools

For local development, you can use these tools in your virtual environment:

```bash
# Format code
black .
isort .

# Run tests
pytest

# Run linter
flake8

# Run type checking
mypy .
```

## Database Architecture

### Source Database (Cloud)
- **Purpose**: Stores historical financial data
- **Access**: Read-only
- **Location**: Cloud instance
- **Configuration**: Set in `SOURCE_DATABASE_URL` environment variable

### Application Database (Local)
- **Purpose**: Stores forecast results and metrics
- **Access**: Read/write
- **Location**: Docker container
- **Configuration**: Managed by docker-compose

## Usage

### Accessing the Services

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501
- **Application Database**: localhost:5432

### Database Management

```bash
# Access the local application database
docker-compose exec app_db psql -U user -d app_db

# View database logs
docker-compose logs -f app_db
```

### Development Workflow

#### Local Development (Using Virtual Environment)

1. **Start Development Environment**
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start FastAPI backend
uvicorn src.api.main:app --reload --port 8000

# In another terminal, start Streamlit dashboard
streamlit run src/visualization/dashboard.py --port 8501
```

2. **Development Tasks**
```bash
# Run tests
pytest tests/

# Format code
black .
isort .

# Check types
mypy .

# Run linter
flake8
```

3. **Database Access**
```bash
# Connect to source database (cloud)
psql $SOURCE_DATABASE_URL

# Connect to local application database
psql $APP_DATABASE_URL
```

#### Docker Development

1. **Start Docker Environment**
```bash
# Build and start all services
docker-compose up --build

# Or start in detached mode
docker-compose up -d
```

2. **Development in Docker**
Make code changes - Changes reflect automatically due to volume mounting
```bash
# View logs
docker-compose logs -f

# Access application database
docker-compose exec app_db psql -U user -d app_db

# Restart specific service
docker-compose restart api
```

#### Switching Between Local and Docker Development

1. **From Local to Docker**
```bash
# Stop local services
# (Ctrl+C in terminals running FastAPI and Streamlit)

# Start Docker services
docker-compose up --build
```

2. **From Docker to Local**
```bash
# Stop Docker services
docker-compose down

# Start local services
source venv/bin/activate
uvicorn src.api.main:app --reload
streamlit run src/visualization/dashboard.py
```

3. **Environment Variables**
- Local development: Use `.env` file
- Docker development: Use `docker-compose.yml` environment variables
- Make sure both environments have the same variable values

#### Common Development Tasks

1. **Adding New Dependencies**
```bash
# Local development
pip install new-package
pip freeze > requirements.txt

# Docker development
docker-compose build --no-cache
```

2. **Database Migrations**
```bash
# Local development
alembic upgrade head

# Docker development
docker-compose exec api alembic upgrade head
```

3. **Testing**
```bash
# Local development
pytest tests/

# Docker development
docker-compose exec api pytest tests/
```

4. **Debugging**
```bash
# Local development
# Use your IDE's debugger
# Set breakpoints in code

# Docker development
# Add logging statements
# View logs with: docker-compose logs -f
```

#### Best Practices

1. **Code Changes**
- Make changes in your local environment first
- Test thoroughly before switching to Docker
- Use version control for all changes

2. **Database Management**
- Keep source database read-only
- Use migrations for application database changes
- Backup application database regularly

3. **Environment Switching**
- Always stop services before switching
- Verify environment variables are correct
- Check logs for any issues

4. **Development Tools**
- Use black and isort for consistent formatting
- Run tests in both environments
- Check types with mypy
- Use flake8 for linting

## Project Structure

```
financial-forecasting/
├── src/
│   ├── data/
│   │   ├── database.py      # Database connections
│   │   ├── models.py        # SQLAlchemy models
│   │   └── preprocessor.py  # Data preprocessing
│   ├── models/              # ML models for forecasting
│   │   ├── cash_flow.py
│   │   ├── revenue.py
│   │   ├── expense.py
│   │   └── profit.py
│   ├── api/
│   │   ├── main.py         # FastAPI application
│   │   └── endpoints.py     # API routes
│   └── visualization/
│       └── dashboard.py     # Streamlit dashboard
├── notebooks/         # Jupyter notebooks for development
├── tests/             # Test files
├── config/            # Configuration files
│   ├── .env.example   # Example environment variables
│   └── .env           # Actual environment variables (gitignored)
├── docker/            # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
└── requirements.txt   # Python dependencies
```

## API Endpoints

- `GET /`: Health check
- `GET /health`: System status
- `GET /api/forecasts/cash-flow`: Cash flow forecasts
- `GET /api/forecasts/revenue`: Revenue forecasts
- `GET /api/forecasts/expenses`: Expense forecasts
- `GET /api/forecasts/profit`: Profit forecasts

## Data Storage

### Forecast Results
- Stored in local application database
- Includes predictions, confidence intervals, and timestamps
- Tracked by forecast type and model version

### Model Metrics
- Performance metrics stored locally
- Includes MSE, RMSE, MAE
- Tracked by model version and evaluation date

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license here]

## Contact

[Add your contact information here] 