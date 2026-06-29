# SecureStego Developer Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Coding Standards](#coding-standards)
5. [Backend Development](#backend-development)
6. [Frontend Development](#frontend-development)
7. [Testing](#testing)
8. [Debugging](#debugging)
9. [Adding New Features](#adding-new-features)
10. [Performance Optimization](#performance-optimization)
11. [Security Best Practices](#security-best-practices)
12. [Deployment](#deployment)
13. [Troubleshooting](#troubleshooting)
14. [Contributing](#contributing)

## Getting Started

### Prerequisites

- **Node.js** v16 or higher
- **Python** v3.8 or higher
- **npm** or **yarn**
- **pip**
- **Git**

### Clone the Repository

```bash
git clone <repository-url>
cd project-root
```

### Initial Setup

1. **Backend Setup**
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
```

2. **Frontend Setup**
```bash
cd ../frontend
npm install
cp .env.example .env
# Edit .env with your configuration
```

3. **Start Development Servers**
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Development Environment Setup

### Recommended IDE

- **VS Code** with extensions:
  - Python (Microsoft)
  - Pylance (Microsoft)
  - ESLint (Microsoft)
  - Prettier (Prettier)
  - Tailwind CSS IntelliSense (Tailwind Labs)

### VS Code Settings

Create `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

### Git Hooks

Install pre-commit hooks:
```bash
pip install pre-commit
cd backend
pre-commit install
```

## Project Structure

### Backend Structure

```
backend/app/
├── main.py                    # Application entry point
├── config/                    # Configuration
│   └── settings.py           # Environment-based settings
├── models/                    # Data models
│   └── schemas.py            # Pydantic schemas
├── routes/                    # API endpoints
│   ├── encryption.py         # Encryption routes
│   ├── steganography.py      # Image steganography routes
│   ├── video_steganography.py
│   ├── audio_steganography.py
│   └── document_steganography.py
├── services/                  # Business logic
│   ├── crypto_service.py     # Encryption/decryption
│   ├── steganography_service.py
│   ├── video_steganography_service.py
│   ├── audio_steganography_service.py
│   ├── document_steganography_service.py
│   └── platform_verification_service.py
├── repositories/             # Data access layer
├── middleware/                # Custom middleware
├── validators/               # Input validation
├── core/                      # Core application logic
├── utils/                     # Utilities
│   ├── logging_config.py
│   ├── exceptions.py
│   ├── payload_serializer.py
│   └── payload_deserializer.py
├── verification/             # Platform signature verification
├── image_processing/         # Image processing modules
├── video_processing/         # Video processing modules
├── audio_processing/         # Audio processing modules
├── document_processing/      # Document processing modules
└── steganography/            # Steganography algorithms
```

### Frontend Structure

```
frontend/src/
├── components/
│   ├── layout/               # Layout components
│   └── ui/                   # Reusable UI components
├── pages/                    # Page components
├── services/                 # API services
├── utils/                    # Utilities
├── hooks/                    # Custom React hooks
├── context/                  # React context providers
├── types/                    # Type definitions
├── constants/                # Application constants
├── assets/                   # Static assets
├── App.jsx                   # Main app with routing
└── main.jsx                  # React entry point
```

## Coding Standards

### Python (Backend)

#### Style Guide

- Follow PEP 8
- Use Black for formatting
- Use Pylint for linting
- Maximum line length: 100 characters

#### Naming Conventions

- **Classes**: `PascalCase` (e.g., `CryptoService`)
- **Functions/Methods**: `snake_case` (e.g., `encrypt_message`)
- **Variables**: `snake_case` (e.g., `encrypted_data`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`)
- **Private members**: `_leading_underscore` (e.g., `_internal_method`)

#### Docstring Format

```python
def encrypt_message(self, message: str, password: str) -> Dict[str, str]:
    """
    Encrypt a message using Argon2id key derivation and AES-256-GCM.
    
    This method:
    1. Derives a key using Argon2id
    2. Encrypts the message using AES-256-GCM
    3. Returns the encrypted data with salt and IV
    
    Parameters:
    message (str):
        Plaintext message to encrypt.
    password (str):
        User password for key derivation.
        
    Returns:
    Dict[str, str]: Dictionary containing:
        - ciphertext: Base64 encoded encrypted data
        - salt: Base64 encoded salt
        - iv: Base64 encoded IV
        - algorithm: Encryption algorithm used
        - kdf: Key derivation function used
        
    Raises:
    ValueError: If encryption fails.
    """
```

#### Type Hints

Always use type hints for function signatures:
```python
from typing import Dict, Optional, List

def process_data(data: Dict[str, Any]) -> Optional[List[str]]:
    pass
```

### JavaScript/React (Frontend)

#### Style Guide

- Follow Airbnb JavaScript Style Guide
- Use ESLint for linting
- Use Prettier for formatting
- Maximum line length: 100 characters

#### Naming Conventions

- **Components**: `PascalCase` (e.g., `HideMessage`)
- **Functions**: `camelCase` (e.g., `encryptMessage`)
- **Variables**: `camelCase` (e.g., `encryptedData`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `API_BASE_URL`)
- **Private members**: `_leadingUnderscore` (e.g., `_internalMethod`)

#### Component Structure

```jsx
import React, { useState, useEffect } from 'react';
import { Button } from './ui/Button';

/**
 * Component description.
 * 
 * Why this exists:
 * - Explain the purpose
 * - Explain the design decision
 */
const ComponentName = ({ prop1, prop2 }) => {
  const [state, setState] = useState(null);
  
  useEffect(() => {
    // Effect logic
  }, [dependency]);
  
  const handleClick = () => {
    // Handler logic
  };
  
  return (
    <div className="container">
      {/* JSX */}
    </div>
  );
};

export default ComponentName;
```

#### Hooks

Custom hooks should be prefixed with `use`:
```javascript
export const useEncryption = () => {
  // Hook logic
};
```

## Backend Development

### Adding a New API Endpoint

1. **Define the Schema** in `backend/app/models/schemas.py`:
```python
class NewRequest(BaseModel):
    """Request schema for new endpoint."""
    field1: str = Field(..., description="Field description")

class NewResponse(BaseModel):
    """Response schema for new endpoint."""
    success: bool = True
    data: Dict[str, Any]
```

2. **Create the Route** in `backend/app/routes/new_route.py`:
```python
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import NewRequest, NewResponse
from app.services.new_service import new_service

router = APIRouter(prefix="/new", tags=["new"])

@router.post("/endpoint", response_model=NewResponse)
async def new_endpoint(request: NewRequest):
    """Endpoint description."""
    try:
        result = new_service.process(request)
        return NewResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
```

3. **Register the Router** in `backend/app/main.py`:
```python
from app.routes.new_route import router as new_router

app.include_router(new_router, prefix=settings.api_prefix)
```

### Adding a New Service

1. **Create the Service** in `backend/app/services/new_service.py`:
```python
from typing import Dict
from app.utils.logging_config import get_logger

logger = get_logger(__name__)

class NewService:
    """
    Service for new functionality.
    
    Why this exists:
    - Explain the purpose
    - Explain the design decision
    """
    
    def __init__(self):
        """Initialize the service."""
        logger.info("NewService initialized")
    
    def process(self, data: Dict) -> Dict:
        """Process data."""
        logger.info("Processing data")
        # Processing logic
        return result

# Global service instance
new_service = NewService()
```

### Adding a New Exception

1. **Add to Exception Hierarchy** in `backend/app/utils/exceptions.py`:
```python
class NewError(SecureStegoException):
    """Base exception for new errors."""
    pass

class SpecificNewError(NewError):
    """Specific new error."""
    pass
```

## Frontend Development

### Adding a New Page

1. **Create the Page Component** in `frontend/src/pages/NewPage.jsx`:
```jsx
import React from 'react';
import { Button } from '../components/ui/Button';

const NewPage = () => {
  return (
    <div className="min-h-screen bg-gray-900">
      {/* Page content */}
    </div>
  );
};

export default NewPage;
```

2. **Add Route** in `frontend/src/App.jsx`:
```jsx
import NewPage from './pages/NewPage';

// Add to routes
<Route path="/new" element={<NewPage />} />
```

### Adding a New Service

1. **Create the Service** in `frontend/src/services/newService.js`:
```javascript
import { API_BASE_URL } from '../constants';

export async function newOperation(data) {
  const response = await fetch(`${API_BASE_URL}/api/new/endpoint`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return response.json();
}
```

2. **Export from Index** in `frontend/src/services/index.js`:
```javascript
export { newOperation } from './newService';
```

### Adding a New Hook

1. **Create the Hook** in `frontend/src/hooks/useNew.js`:
```javascript
import { useState, useCallback } from 'react';
import { newOperation } from '../services';

export const useNew = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const execute = useCallback(async (data) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await newOperation(data);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  return { execute, isLoading, error };
};
```

## Testing

### Backend Testing

#### Unit Tests

Create tests in `backend/tests/`:
```python
import pytest
from app.services.crypto_service import crypto_service

def test_encrypt_message():
    """Test message encryption."""
    result = crypto_service.encrypt_message("test", "password")
    assert result["success"] is True
    assert "ciphertext" in result
```

#### Run Tests

```bash
cd backend
pytest tests/
pytest tests/ -v  # Verbose output
pytest tests/ --cov=app  # With coverage
```

### Frontend Testing

#### Unit Tests

Create tests in `frontend/src/__tests__/`:
```javascript
import { render, screen } from '@testing-library/react';
import HideMessage from '../pages/HideMessage';

test('renders hide message page', () => {
  render(<HideMessage />);
  expect(screen.getByText('Hide Secret Message')).toBeInTheDocument();
});
```

#### Run Tests

```bash
cd frontend
npm test
npm test -- --coverage
```

## Debugging

### Backend Debugging

#### Using VS Code Debugger

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

#### Logging

Logs are written to console with the format:
```
timestamp - logger_name - level - message
```

Set log level in `.env`:
```env
log_level=DEBUG
```

### Frontend Debugging

#### Using Browser DevTools

1. Open Chrome DevTools (F12)
2. Use React DevTools extension
3. Check Console for errors
4. Use Network tab for API calls

#### VS Code Debugging

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Chrome: Launch",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

## Adding New Features

### Feature Development Workflow

1. **Create a Feature Branch**
```bash
git checkout -b feature/new-feature
```

2. **Implement the Feature**
   - Backend: Add routes, services, models
   - Frontend: Add pages, services, hooks
   - Tests: Add unit and integration tests

3. **Test the Feature**
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test

# Manual testing
# Start both servers and test the feature
```

4. **Update Documentation**
   - Update API.md if new endpoints
   - Update ARCHITECTURE.md if architecture changes
   - Update README.md if user-facing changes

5. **Commit and Push**
```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

6. **Create Pull Request**
   - Describe the feature
   - Link to any issues
   - Request review

## Performance Optimization

### Backend Optimization

#### Database Queries (Future)

- Use indexes for frequently queried fields
- Use pagination for large result sets
- Cache frequently accessed data

#### File Processing

- Use streaming for large files
- Process files in chunks
- Clean up temporary files promptly

#### API Response Times

- Use async/await for I/O operations
- Implement caching for expensive operations
- Use connection pooling for external services

### Frontend Optimization

#### Code Splitting

```javascript
const LazyComponent = React.lazy(() => import('./LazyComponent'));
```

#### Memoization

```javascript
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
```

#### Image Optimization

- Use WebP format
- Implement lazy loading
- Use responsive images

## Security Best Practices

### Backend Security

#### Input Validation

- Always validate user input
- Use Pydantic models for validation
- Sanitize file uploads

#### Secret Management

- Never commit secrets to git
- Use environment variables
- Rotate secrets regularly

#### Error Handling

- Never expose sensitive data in errors
- Log errors for debugging
- Return generic error messages to users

### Frontend Security

#### XSS Prevention

- Use React's built-in XSS protection
- Sanitize user input
- Use `dangerouslySetInnerHTML` sparingly

#### CSRF Protection

- Implement CSRF tokens (future)
- Use SameSite cookie attribute
- Validate origin headers

#### Content Security Policy

- Implement CSP headers (backend)
- Use inline scripts sparingly
- Validate external resources

## Deployment

### Backend Deployment

#### Docker

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t securestego-backend .
docker run -p 8000:8000 securestego-backend
```

#### Production Server

Use Gunicorn with Uvicorn workers:
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment

#### Docker

Create `frontend/Dockerfile`:
```dockerfile
FROM node:16-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
```

Build and run:
```bash
docker build -t securestego-frontend .
docker run -p 80:80 securestego-frontend
```

#### Static Hosting

Build and deploy:
```bash
cd frontend
npm run build
# Upload dist/ folder to hosting provider
```

## Troubleshooting

### Common Backend Issues

#### ImportError

**Problem**: Module not found
**Solution**: Ensure virtual environment is activated and dependencies installed

#### KeyError

**Problem**: Missing environment variable
**Solution**: Check `.env` file exists and has required variables

#### CORS Errors

**Problem**: Frontend cannot access backend
**Solution**: Add frontend URL to `cors_origins` in settings

### Common Frontend Issues

#### API Connection Failed

**Problem**: Cannot connect to backend
**Solution**: Ensure backend is running on correct port

#### Build Errors

**Problem**: Build fails with errors
**Solution**: Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

#### Module Not Found

**Problem**: Import errors
**Solution**: Check import paths and ensure file exists

## Contributing

### Code Review Process

1. Create feature branch
2. Implement changes with tests
3. Update documentation
4. Submit pull request
5. Address review comments
6. Merge to main branch

### Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Maintenance tasks

Example:
```bash
git commit -m "feat: add video steganography support"
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
```

## Additional Resources

### Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### Tools

- [Black](https://black.readthedocs.io/) - Python formatter
- [Pylint](https://pylint.org/) - Python linter
- [ESLint](https://eslint.org/) - JavaScript linter
- [Prettier](https://prettier.io/) - JavaScript formatter

### Security

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Cryptography Best Practices](https://cryptography.io/en/latest/)
- [Argon2id Specification](https://datatracker.ietf.org/doc/html/rfc9106)
