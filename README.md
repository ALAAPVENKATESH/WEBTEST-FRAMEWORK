# 🚀 Advanced Website Testing Tool

A comprehensive Flask web application that provides detailed analysis of websites including SEO, Security, Performance, and more.

## ✨ Features

### 🔗 **Link Testing**
- Find broken links and validate all URLs
- Check link status codes
- Identify redirect chains

### ⚡ **Performance Analysis**
- Measure page load time
- Performance grading (A-F)
- Speed recommendations

### 🎯 **SEO Analysis**
- Meta tag analysis (title, description, keywords)
- Open Graph and Twitter Card detection
- Mobile-friendliness check
- Canonical URL verification
- SEO scoring and recommendations

### 🔒 **Security Testing**
- HTTPS verification
- Security headers analysis
- HSTS, CSP, X-Frame-Options checks
- Security grading and recommendations

### 🖼️ **Image Analysis**
- Broken image detection
- Alt text validation
- Image optimization recommendations

### 📱 **UI Element Detection**
- Navbar, footer, button, form detection
- UI completeness scoring

### 📊 **Advanced Analytics**
- Overall website scoring (0-100)
- Grade-based evaluation (A-F)
- Detailed recommendations
- Test history and comparison

### 🎨 **Modern UI/UX**
- Beautiful gradient design
- Responsive layout
- Progress indicators
- Interactive elements
- Mobile-friendly interface

### 📋 **Test Management**
- Test history storage
- Export results as JSON
- API endpoints for programmatic access
- Batch testing capabilities

## 🛠️ Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python main.py
```

3. **Open your browser and go to:** `http://localhost:5000`

## 📖 Usage

### Web Interface
1. Enter a website URL in the input field
2. Click "Run Comprehensive Test"
3. View detailed results with grades and recommendations
4. Access test history and export results

### API Usage
```bash
curl -X POST http://localhost:5000/api/test \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## 📁 Project Structure

```
webtest-framework/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── routes.py          # Route definitions
│   └── templates/         # HTML templates
│       ├── index.html     # Home page
│       ├── result.html    # Results page
│       └── history.html   # Test history
└── tests/
    ├── test_links.py      # Link testing
    ├── test_performance.py # Performance testing
    ├── test_ui.py         # UI element testing
    ├── test_seo.py        # SEO analysis
    ├── test_security.py   # Security testing
    └── test_images.py     # Image analysis
```

## 🔧 Dependencies

- **Flask** - Web framework
- **Requests** - HTTP library
- **BeautifulSoup4** - HTML parsing

## 🎯 Scoring System

### Overall Score (0-100)
- **90-100**: Excellent (A)
- **80-89**: Good (B)
- **70-79**: Fair (C)
- **60-69**: Needs Improvement (D)
- **0-59**: Poor (F)

### Individual Test Grades
Each test category (SEO, Security, Images, etc.) receives its own grade based on specific criteria.

## 🚀 Advanced Features

### Test History
- Automatic storage of test results
- View previous tests with scores
- Export individual test results

### API Endpoints
- `/api/test` - Programmatic testing
- `/export/<index>` - Export test results
- `/history` - View test history

### Responsive Design
- Works on desktop, tablet, and mobile
- Modern gradient UI
- Interactive hover effects

## 🔮 Future Enhancements

- [ ] Batch URL testing
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Custom test configurations
- [ ] Performance benchmarking
- [ ] Accessibility testing
- [ ] Mobile responsiveness testing
- [ ] Database integration

## 🤝 Contributing

Feel free to contribute by:
- Adding new test modules
- Improving the UI/UX
- Enhancing scoring algorithms
- Adding new features

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for better web testing**
