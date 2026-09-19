# Backend

### Local Setup
1. Clone this repo
2. cd backend
3. cp .env.example .env
4. Add values to environement variables
5. **Install required packages:** uv sync
6. **Create all tables:** uv run alembic upgrade head
7. **Run:** uv run fastapi dev
