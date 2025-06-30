# 🚇 TBM Advance Rate Calculator

A professional-grade web application for calculating tunnel boring machine (TBM) advance rates using multiple engineering methodologies. This tool provides accurate predictions for TBM performance across various geological and operational conditions.

![TBM Calculator](https://img.shields.io/badge/TBM-Calculator-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green) ![Docker](https://img.shields.io/badge/Docker-Ready-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Overview

The TBM Advance Rate Calculator is a comprehensive engineering tool that combines empirical data correlations, theoretical rock mechanics principles, and machine learning-based regression methods to predict tunnel boring machine performance. It supports multiple TBM types and geological conditions commonly encountered in tunnel construction projects.

## ✨ Key Features

### 🔬 **Multi-Method Calculation Engine**
- **Empirical Method**: Based on field data correlations and industry best practices
- **Theoretical Method**: Rock/soil mechanics principles with UCS calculations
- **Regression Method**: Machine learning-based predictions with feature engineering
- **Hybrid Approach**: Intelligent weighting of methods based on data availability

### 🛠️ **TBM Types Supported**
- **EPB (Earth Pressure Balance)**: Suitable for cohesive soils and mixed ground
- **Slurry TBM**: Ideal for granular soils and high water pressure conditions
- **Open TBM**: Used for stable rock conditions
- **Mix Shield**: Versatile for changing ground conditions

### 🌍 **Geological Conditions**
- Clay, Sand, Silt, Gravel
- Soft Rock, Medium Rock, Hard Rock
- Mixed ground conditions
- Variable water pressure and depth scenarios

### 📊 **Advanced Analytics**
- Real-time risk assessment
- Automated recommendations
- Confidence scoring
- Performance optimization suggestions
- Daily advance predictions

### 🎨 **Professional Interface**
- Modern, responsive web design
- Interactive API documentation (OpenAPI/Swagger)
- Real-time input validation
- Example scenarios for different tunnel types

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kilickursat/tbm-advance-rate-calculator.git
   cd tbm-advance-rate-calculator
   ```

2. **Deploy with Docker (Recommended)**
   ```bash
   chmod +x start.sh
   ./start.sh docker
   ```

3. **Access the application**
   - **Main Application**: http://localhost
   - **API Documentation**: http://localhost/docs
   - **Alternative Docs**: http://localhost/redoc
   - **Health Check**: http://localhost/api/v1/health

### Alternative Installation Methods

#### Python Environment
```bash
./start.sh python
```

#### Development Mode
```bash
./start.sh dev
```

#### Run Tests
```bash
./start.sh test
```

## 📚 Usage Guide

### Web Interface
1. Navigate to http://localhost
2. Select your TBM type and specifications
3. Input geological parameters
4. Configure operational settings
5. Click "Calculate" to get advance rate predictions
6. Review risk assessment and recommendations

### API Usage

#### Calculate Advance Rate
```bash
curl -X POST "http://localhost/api/v1/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "tbm_diameter": 6.2,
    "tbm_type": "epb",
    "cutterhead_power": 2000,
    "soil_type": "clay",
    "thrust_force": 15000,
    "cutterhead_speed": 2.5,
    "depth": 15,
    "water_pressure": 1.5
  }'
```

#### Get Example Scenarios
```bash
curl "http://localhost/api/v1/examples"
```

## 🏗️ Technical Architecture

### Backend Stack
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.11**: Core programming language
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for production deployment

### Frontend
- **HTML5**: Modern semantic markup
- **TailwindCSS**: Utility-first CSS framework
- **Vanilla JavaScript**: No heavy frameworks, fast loading

### Deployment
- **Docker**: Containerized application
- **Docker Compose**: Multi-service orchestration
- **Nginx**: Reverse proxy and load balancer
- **Production-ready**: Health checks, logging, security headers

### Calculation Methods
- **Empirical Models**: Field data correlations from industry databases
- **Rock Mechanics**: UCS-based cutting force calculations
- **Penetration Resistance**: Soil mechanics principles
- **Feature Engineering**: Advanced parameter correlations

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/calculate` | POST | Calculate TBM advance rate |
| `/api/v1/examples` | GET | Get example scenarios |
| `/api/v1/soil-types` | GET | Available soil/rock types |
| `/api/v1/tbm-types` | GET | Available TBM types |
| `/api/v1/health` | GET | Health monitoring |
| `/docs` | GET | Interactive API documentation |
| `/redoc` | GET | Alternative API documentation |

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
# Application Configuration
DEBUG=false
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-change-in-production

# Security Configuration
ALLOWED_HOSTS=["localhost", "127.0.0.1", "*"]

# Database Configuration (for future use)
DATABASE_URL=sqlite:///./tbm_calculator.db
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
./start.sh test
```

Test coverage includes:
- Unit tests for calculation methods
- API endpoint testing
- Input validation testing
- Error handling verification

## 🌐 Deployment Options

### Local Development
- Docker Compose (recommended)
- Python virtual environment
- Development mode with auto-reload

### Cloud Platforms
- **Heroku**: Ready with Procfile
- **Railway**: One-click deployment
- **DigitalOcean App Platform**: app.yaml included
- **AWS/GCP/Azure**: Docker container compatible

### Production Considerations
- SSL/HTTPS configuration available
- Environment-based configuration
- Health monitoring endpoints
- Rate limiting and security headers
- Horizontal scaling support

## 📖 Example Scenarios

The application includes pre-configured examples for:

1. **Metro Tunnel - Soft Ground**: Urban subway construction in clay
2. **Highway Tunnel - Mixed Ground**: Road tunnel through variable geology
3. **Water Tunnel - Hard Rock**: Water supply tunnel in strong rock
4. **Mining Tunnel - Soft Rock**: Mining access in weathered rock
5. **Slurry TBM - Sandy Ground**: Large diameter tunnel in sand

## ⚠️ Important Disclaimers

### 🔓 **Open Source Development**
This application has been developed using **publicly available open source information** from the internet, including:
- Academic research papers and publications
- Industry standards and best practices
- Open source software libraries and frameworks
- Publicly available technical documentation
- General engineering principles and methodologies

### 🏢 **No Proprietary Information**
**IMPORTANT**: This project does **NOT** contain or utilize:
- Proprietary company information or trade secrets
- Copyrighted or patented algorithms from commercial software
- Confidential engineering data or methodologies
- Licensed software components requiring royalty payments
- Any intellectual property that violates copyright or patent rights

### 📝 **Intellectual Property Compliance**
- All calculation methods are based on publicly available engineering principles
- No reverse engineering of commercial software has been performed
- All third-party libraries used are open source with compatible licenses
- The project respects all intellectual property rights and licensing terms

### 🎓 **Educational and Research Purpose**
This tool is intended for:
- Educational purposes and learning
- Research and development activities
- General engineering calculations and analysis
- Open source community contribution

### ⚖️ **Legal Responsibility**
Users are responsible for:
- Ensuring compliance with local regulations and standards
- Validating results against project-specific requirements
- Using the tool in accordance with professional engineering practices
- Understanding the limitations and assumptions of the calculation methods

### 🔬 **Engineering Validation**
This software provides calculations based on general engineering principles. For critical engineering decisions:
- Always validate results with qualified professionals
- Consider project-specific geological and operational conditions
- Use additional analysis methods and tools
- Follow applicable industry standards and codes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No warranty provided
- ❌ No liability assumed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 🆘 Support

### Documentation
- **API Documentation**: http://localhost/docs (when running)
- **Quick Start Guide**: [QUICKSTART.md](QUICKSTART.md)
- **Issues**: [GitHub Issues](https://github.com/kilickursat/tbm-advance-rate-calculator/issues)

### Community
- Report bugs via GitHub Issues
- Request features via GitHub Issues
- Contribute improvements via Pull Requests

## 🏆 Acknowledgments

- FastAPI framework developers for the excellent web framework
- Open source community for various libraries and tools
- Tunnel engineering community for sharing knowledge and best practices
- Academic researchers for publishing methodologies and case studies

## 📊 Project Statistics

- **Languages**: Python, JavaScript, HTML, CSS
- **Framework**: FastAPI
- **Deployment**: Docker, Nginx
- **Testing**: Pytest with comprehensive coverage
- **Documentation**: OpenAPI/Swagger, ReDoc
- **Status**: Production Ready ✅

## 🔮 Future Enhancements

- [ ] Machine learning model training on expanded datasets
- [ ] Additional TBM types and specialized configurations
- [ ] Advanced geological modeling integration
- [ ] Real-time monitoring dashboard
- [ ] Historical project database
- [ ] Mobile application
- [ ] Multi-language support

---

**Built with ❤️ for the tunnel engineering community using open source technologies**

For questions, suggestions, or contributions, please visit our [GitHub repository](https://github.com/kilickursat/tbm-advance-rate-calculator).
