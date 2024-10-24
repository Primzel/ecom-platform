
# Database Setup
1. **Set up PostgreSQL using Docker**:
   ```bash
   docker-compose up -d postgres
   ```

2. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
