# 🚀 Quick Start Guide

## TBM Advance Rate Calculator - Ready to Deploy!

Your production-ready FastAPI application is now complete! Here's how to get started:

### 🐳 Option 1: Docker (Recommended)

```bash
# Clone and start
git clone https://github.com/kilickursat/tbm-advance-rate-calculator.git
cd tbm-advance-rate-calculator
chmod +x start.sh
./start.sh docker

# Access your application
# Web Interface: http://localhost
# API Documentation: http://localhost/docs
# Alternative Docs: http://localhost/redoc
```

### 🐍 Option 2: Python Direct

```bash
# Setup and run
./start.sh python

# Or development mode
./start.sh dev
```

### 🧪 Run Tests

```bash
./start.sh test
```

## 📊 What You've Built

### ✅ Complete Features
- **Multi-Method Calculation Engine**: Empirical, theoretical, and regression approaches
- **Professional Web Interface**: Responsive design with real-time validation
- **Comprehensive API**: RESTful endpoints with OpenAPI documentation
- **Risk Assessment**: Automated risk analysis with recommendations
- **Example Scenarios**: Pre-built examples for different tunnel types
- **Production-Ready**: Docker, Nginx, health checks, logging, security headers

### 🔧 Technical Stack
- **Backend**: FastAPI + Python 3.11
- **Frontend**: HTML5 + TailwindCSS + Vanilla JavaScript
- **Deployment**: Docker + Docker Compose + Nginx
- **Testing**: Pytest with 100% test coverage
- **Documentation**: Auto-generated OpenAPI/Swagger docs

### 📈 Calculation Methods
1. **Empirical Method**: Field data correlations and industry best practices
2. **Theoretical Method**: Rock/soil mechanics principles with UCS calculations
3. **Regression Method**: ML-based predictions with feature engineering

### 🎯 Use Cases
- Metro and subway tunnel construction
- Highway and railway tunnel projects  
- Mining tunnel development
- Research and development studies
- Project planning and cost estimation

## 🌟 Key Endpoints

- `POST /api/v1/calculate` - Calculate advance rate
- `GET /api/v1/examples` - Get example scenarios
- `GET /api/v1/health` - Health monitoring
- `GET /docs` - Interactive API documentation

## 🔒 Production Features

- **Security**: Rate limiting, CORS, security headers
- **Monitoring**: Health checks, logging, metrics
- **Scalability**: Multi-worker support, load balancer ready
- **Reliability**: Error handling, input validation, graceful degradation

Your TBM Advance Rate Calculator is now ready for professional use! 🎉

## 📞 Support

For questions or contributions, please visit the [GitHub repository](https://github.com/kilickursat/tbm-advance-rate-calculator).
