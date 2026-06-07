# Email Insight

Modern OSINT and business intelligence web application for email, domain, and company research using only publicly available information.

## Tech Stack

- **Frontend**: Next.js 15 (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python 3.12)
- **Database**: PostgreSQL (Supabase)
- **Authentication**: JWT (python-jose)
- **AI**: OpenAI GPT-4o-mini
- **Deployment**: Vercel (Frontend) + Render (Backend)

## Features

- **Email Lookup**: Public email intelligence including domain, MX records, Gravatar, WHOIS
- **Domain Intelligence**: DNS records, SPF/DKIM/DMARC, hosting detection, WHOIS
- **Company Intelligence**: Tech stack detection, social media discovery, website metadata
- **AI Summaries**: Automated AI-generated summaries and risk assessments
- **Search History**: Saved searches, analytics dashboard, export reports (JSON/CSV/HTML)
- **User Dashboard**: Activity tracking, risk distribution, monthly trends
- **Dark Mode**: Full dark/light/system theme support
- **Mobile Responsive**: Fully responsive design

## Project Structure

```
email-insight/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes (auth, email, domain, company, search, dashboard)
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic (email, dns, whois, gravatar, ai, export)
│   │   ├── middleware/    # Auth middleware, rate limiting
│   │   ├── utils/        # Validators, helpers
│   │   ├── config.py     # App configuration
│   │   ├── database.py   # Database connection
│   │   └── main.py       # FastAPI application
│   ├── alembic/          # Database migrations
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js App Router pages
│   │   │   ├── (auth)/   # Login, register, password reset
│   │   │   ├── dashboard/
│   │   │   ├── search/
│   │   │   ├── history/
│   │   │   └── settings/
│   │   ├── components/   # React components (layout, ui, dashboard, search)
│   │   ├── lib/          # API client, utilities
│   │   └── types/        # TypeScript types
│   ├── vercel.json
│   └── .env.local.example
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL database (or Supabase account)
- OpenAI API key (for AI features)

### Backend Setup

1. Navigate to backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` with your database URL and secrets:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/email_insight
   JWT_SECRET_KEY=your-random-secret-key
   OPENAI_API_KEY=sk-your-openai-key
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   API will be available at http://localhost:8000
   API Docs at http://localhost:8000/api/docs

### Frontend Setup

1. Navigate to frontend:
   ```bash
   cd frontend
   npm install
   ```

2. Copy environment file:
   ```bash
   cp .env.local.example .env.local
   ```

3. Edit `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXTAUTH_SECRET=your-nextauth-secret
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

   App will be available at http://localhost:3000

## Deployment

### Frontend (Vercel)

1. Push frontend to GitHub
2. Import repository in Vercel
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL`: Backend API URL
   - `NEXTAUTH_SECRET`: Random secret string
4. Deploy

### Backend (Render)

1. Push backend to GitHub
2. Create new Web Service on Render
3. Set:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env.example`
5. Deploy

### Database (Supabase)

1. Create Supabase project
2. Get connection string
3. Run migrations:
   ```bash
   DATABASE_URL=postgresql://... alembic upgrade head
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Get current user
- `POST /api/auth/change-password` - Change password
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password

### Email Lookup
- `POST /api/email/lookup` - Full email intelligence lookup
- `GET /api/email/gravatar` - Check Gravatar

### Domain Intelligence
- `GET /api/domain/lookup` - Full domain intelligence
- `GET /api/domain/dns` - DNS records
- `GET /api/domain/whois` - WHOIS info
- `GET /api/domain/security` - Email security (SPF/DKIM/DMARC)

### Company Intelligence
- `GET /api/company/lookup` - Company info
- `GET /api/company/metadata` - Website metadata
- `GET /api/company/tech-stack` - Technology detection
- `GET /api/company/social` - Social media discovery

### Search History
- `GET /api/search/history` - Search history
- `GET /api/search/analytics` - Search analytics
- `GET /api/search/{id}` - Search detail
- `DELETE /api/search/{id}` - Delete search
- `POST /api/search/export` - Export reports

### Dashboard
- `GET /api/dashboard/stats` - Dashboard statistics

## Security Notes

- All data is sourced from **publicly available information only**
- No access to private accounts, private emails, or restricted data
- Rate limiting is enabled by default
- JWT authentication with token refresh
- Input validation and sanitization on all endpoints
- SQL injection prevention via SQLAlchemy ORM

## License

MIT
