# NeuraNova Learn

A comprehensive educational platform featuring AR/VR simulations, AI-driven personalized learning, multilingual support (21 languages), NFT gamification, and real-time global collaboration.

## 🚀 Features

### Core Functionality
- **AR/VR Simulations**: Interactive 3D molecular visualizations and scientific simulations using React Three Fiber and ViroReact
- **AI Predictive Learning**: Personalized learning paths with dropout prevention using GPT-4o
- **Multilingual Support**: 21 languages with real-time translation using mT5
- **NFT Gamification**: Blockchain-based achievement rewards on Ethereum Sepolia testnet
- **Avatar System**: Professional avatar models with lip-sync using SadTalker
- **Real-Time Collaboration**: Global learning sessions with WebRTC (Agora) and Whisper voice translation
- **200,000+ Lessons**: Interactive STEM content from OER Commons and GPT-4o generation
- **Teacher/Parent Dashboards**: Progress monitoring with ESG reports

### Technology Stack
- **Mobile**: React Native with Expo, ViroReact for AR/VR
- **Web**: React with Vite, React Three Fiber for 3D graphics
- **Backend**: FastAPI with PostgreSQL
- **AI/ML**: OpenAI GPT-4o, Hugging Face Transformers (mT5, Whisper, SadTalker)
- **Blockchain**: Web3.py with Ethereum Sepolia testnet
- **Real-Time**: Agora SDK for WebRTC

## 📦 Project Structure

```
neuranova-learn/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── routers/  # API endpoints
│   │   ├── services/ # Business logic
│   │   ├── models.py # Database models
│   │   └── main.py   # Application entry
├── frontend/         # React web app
│   └── src/
│       ├── pages/    # Application pages
│       └── components/ # UI components
└── mobile/           # React Native app
    └── app/
        └── (tabs)/   # Mobile screens
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL (optional, SQLite used by default)
- Expo CLI
- Poetry for Python dependency management

### Backend Setup

```bash
cd backend
poetry install
cp .env.example .env
# Edit .env with your API keys
poetry run fastapi dev app/main.py
```

The backend will be available at `http://localhost:8000`

### Web Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The web app will be available at `http://localhost:5173`

### Mobile App Setup

```bash
cd mobile
npm install
cp .env.example .env
npx expo start
```

Scan the QR code with Expo Go app on your device

## 🔑 API Keys Required

### Free Tier Services (No Cost)
- **OpenAI GPT-4o**: For lesson generation and predictive learning
- **Alchemy**: For Ethereum testnet access
- **Agora**: For WebRTC real-time collaboration (10,000 minutes/month free)
- **Hugging Face**: For mT5 translation and SadTalker (free inference)

### Optional Integrations
- **Wolfram Alpha**: Free tier (2,000 calls/month)
- **Google Cloud Translation**: For language detection (optional)

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/token` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

#### Lessons
- `GET /api/lessons` - List lessons with filters
- `GET /api/lessons/{id}` - Get lesson details
- `POST /api/lesson-generation/generate` - Generate custom lesson with GPT-4o

#### Progress & Analytics
- `POST /api/progress` - Update user progress
- `GET /api/analytics/{user_id}` - Get AI-powered analytics

#### NFT Rewards
- `POST /api/nft/mint` - Mint achievement NFT
- `GET /api/nft/{user_id}` - Get user's NFT collection

#### Translation
- `POST /api/translation/translate` - Translate text between languages
- `GET /api/translation/supported-languages` - List supported languages

#### Collaboration
- `POST /api/collaboration/session` - Create real-time session
- `GET /api/collaboration/session/{id}` - Join existing session

## 🧪 Testing

### Unit Tests
```bash
cd backend
poetry run pytest
```

### Load Testing
```bash
cd backend
poetry run locust -f tests/load_test.py
```

### Mobile Testing
Test on physical devices (iPhone, Samsung, iPad) using Expo Go

## 🚀 Deployment

### Backend Deployment (AWS)
```bash
# Deploy to AWS free tier
# Instructions for AWS EC2 + RDS setup included in deployment guide
```

### Web Deployment (Cloudflare Pages)
```bash
cd frontend
npm run build
# Deploy dist/ folder to Cloudflare Pages
```

### Mobile Deployment (Expo)
```bash
cd mobile
npx expo build:android
npx expo build:ios
```

## 🎨 UI/UX Features

- **Neumorphic Design**: Soft shadows and gradients
- **Dark/Light Themes**: User preference support
- **Responsive Design**: Works on all screen sizes
- **Accessibility**: WCAG 2.1 AA compliant

## 🔒 Security

- **Zero-Trust Architecture**: All endpoints require authentication
- **Blockchain Security**: Student data encrypted and stored on-chain
- **JWT Authentication**: Secure token-based auth
- **CORS Protection**: Configured for production

## 🌍 Supported Languages

English, Mandarin Chinese, Spanish, Hindi, Arabic, French, Bengali, Portuguese, Russian, Urdu, Indonesian, German, Japanese, Turkish, Persian, Italian, Polish, Dutch, Swedish, Finnish, Norwegian

## 📖 Documentation

- [Architecture Overview](docs/architecture.md)
- [API Reference](docs/api.md)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)

## 🤝 Contributing

This is a private project. Contact the maintainer for contribution guidelines.

## 📝 License

Proprietary - All rights reserved

## 👥 Team

- **Project Lead**: Siavash Ariamehr (@siavash-ariamehr)
- **Development**: Devin AI

## 📞 Support

For questions or issues, contact: hamid.t1969@gmail.com

---

**Devin Session**: https://app.devin.ai/sessions/8c7160f103734641aa233838d8d5ac7f
