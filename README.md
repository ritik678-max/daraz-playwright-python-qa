# Daraz E-Commerce QA Automation Framework

A portfolio-level QA Automation / SDET framework built using **Python, Playwright, Pytest, Page Object Model, API Testing, Allure Reporting, Logging, Data-Driven Testing, Docker, GitHub Actions, Parallel Execution, Cross-Browser Testing, Screenshots, Tracing, Video Recording, Retry Handling, and Environment Configuration**.

The project automates key user flows on **Daraz Nepal** and also includes REST API automation using a public test API.

---

## Project Objectives

This framework was built to demonstrate practical QA Automation / SDET skills including:

- UI automation
- API automation
- Page Object Model
- Data-driven testing
- Cross-browser testing
- Parallel execution
- Failure artifact collection
- Allure reporting
- API schema validation
- Logging
- Docker execution
- CI/CD integration
- Multi-environment configuration
- Retry handling
- Test categorization
- Safe production-site testing

---

## Tech Stack

- Python
- Playwright
- Pytest
- Requests
- JSON Schema
- Page Object Model
- Allure Report
- Pytest-xdist
- Pytest-rerunfailures
- Python-dotenv
- Docker
- Docker Compose
- Git
- GitHub
- GitHub Actions
- JSON Test Data
- Python Logging

---

# Framework Features

The framework currently supports:

- Page Object Model architecture
- UI automation
- API automation
- Data-driven testing
- Pytest fixtures
- Pytest markers
- Dynamic configuration
- Multi-environment execution
- Cross-browser execution
- Headless and headed execution
- Parallel test execution
- Worker-safe logging
- Automatic retries
- Failure screenshots
- Playwright traces
- Failure video recording
- Allure reporting
- Allure environment information
- Allure executor information
- API request logging
- API response logging
- API request/response Allure attachments
- JSON schema validation
- Docker execution
- Docker Compose support
- GitHub Actions CI configuration

---

# UI Test Coverage

## Homepage

The framework verifies:

- Daraz homepage loads successfully
- Correct URL is opened

---

## Login

The framework verifies:

- Login modal opens
- Email / phone field is visible
- Password field is visible
- Login button is visible

No real credentials are used.

---

## Product Search

The search automation performs the following flow:

1. Open Daraz Nepal
2. Search for a product
3. Wait for search results
4. Verify search result URL
5. Verify product results are displayed
6. Get first product name
7. Get first product price
8. Open first product
9. Wait for product details page
10. Verify product URL
11. Verify product title
12. Verify product price
13. Compare listing product name with product details name
14. Compare listing price with product details price

The same test is executed using multiple search terms:

- laptop
- mobile
- headphones

Test data is loaded from:

```text
testdata/search_data.json
```

---

# Cart Validation

The framework includes safe cart validation on the Daraz production website.

Flow:

```text
Open Daraz
↓
Search Product
↓
Open Product
↓
Click Add to Cart
↓
Verify Authentication Prompt
```

For an unauthenticated guest user, Daraz requires authentication before proceeding.

The test verifies:

- Add to Cart button is visible
- Add to Cart button is enabled
- Login prompt appears
- Email / phone field appears
- Password field appears
- Login button appears

The test intentionally stops before login, checkout, or payment.

---

# API Test Coverage

The framework also includes REST API automation using:

```text
https://jsonplaceholder.typicode.com
```

Current API coverage includes:

- GET users
- GET post
- POST create post
- PUT update post
- DELETE post

---

## API Validation

API tests validate:

- HTTP status codes
- Response body
- Required fields
- Response values
- JSON response structure
- JSON schema

Example validations include:

```python
assert response.status_code == 200
assert body["id"] == 1
assert "title" in body
assert "body" in body
```

Schema validation is implemented using:

```text
jsonschema
```

---

# Reusable API Client

A reusable API client is implemented in:

```text
utils/api_client.py
```

It supports:

```text
GET
POST
PUT
DELETE
```

The API client also automatically records:

- HTTP method
- URL
- query parameters
- request payload
- response status
- response body

These details are logged and attached to Allure reports.

---

# Project Structure

```text
E-commerce-qa/
│
├── .github/
│   └── workflows/
│       └── playwright-tests.yml
│
├── pages/
│   ├── home_page.py
│   ├── search_page.py
│   ├── product_page.py
│   └── cart_page.py
│
├── tests/
│   ├── api/
│   │   ├── test_posts_api.py
│   │   └── test_users_api.py
│   │
│   ├── test_homepage.py
│   ├── test_login.py
│   ├── test_search.py
│   └── test_cart.py
│
├── testdata/
│   └── search_data.json
│
├── utils/
│   ├── api_client.py
│   ├── config.py
│   ├── constants.py
│   ├── data_loader.py
│   ├── logger.py
│   └── schemas.py
│
├── allure-results/
├── reports/
├── screenshots/
├── test-results/
├── traces/
│
├── .dockerignore
├── .env.example
├── .gitignore
├── conftest.py
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# Page Object Model

The framework separates page interaction logic from test logic.

Current page objects:

```text
HomePage
SearchPage
ProductPage
CartPage
```

Example:

```python
home_page.open()

home_page.search_product(
    "laptop"
)

search_page.wait_for_results()

search_page.open_first_product()

product_page.wait_for_product_details()
```

This improves:

- readability
- maintainability
- reusability
- scalability

---

# Test Data

Search data is stored separately from test logic.

File:

```text
testdata/search_data.json
```

Example:

```json
{
  "search_terms": [
    "laptop",
    "mobile",
    "headphones"
  ]
}
```

Pytest parametrization executes the same test with each search term.

---

# Pytest Markers

The framework uses markers to organize test execution.

Available markers:

```text
smoke
regression
search
api
```

Example:

```bash
pytest -m smoke
```

Run API tests:

```bash
pytest -m api
```

Run regression tests:

```bash
pytest -m regression
```

---

# Environment Configuration

The project supports environment-based configuration.

Example:

```text
.env.qa
.env.dev
.env.staging
```

The active environment can be selected using:

```powershell
$env:TEST_ENV="staging"
```

Configuration values include:

```text
BASE_URL
BROWSER
HEADLESS
WORKERS
DEFAULT_TIMEOUT
EXECUTION_TYPE
```

---

# Example Environment File

Create:

```text
.env.example
```

Example:

```env
TEST_ENV=qa
BASE_URL=https://www.daraz.com.np/
BROWSER=chromium
HEADLESS=true
WORKERS=2
DEFAULT_TIMEOUT=10000
EXECUTION_TYPE=local
```

Real environment files should not contain committed secrets.

---

# Cross-Browser Testing

The framework supports:

```text
Chromium
Firefox
WebKit
```

Example:

```powershell
$env:BROWSER="firefox"
pytest -m smoke
```

Chromium:

```powershell
$env:BROWSER="chromium"
pytest -m smoke
```

WebKit:

```powershell
$env:BROWSER="webkit"
pytest -m smoke
```

---

# Headed and Headless Execution

Headless:

```powershell
$env:HEADLESS="true"
pytest -m smoke
```

Headed:

```powershell
$env:HEADLESS="false"
pytest -m smoke
```

---

# Parallel Execution

Parallel execution is implemented using:

```text
pytest-xdist
```

Example:

```bash
pytest -m smoke -n 2
```

The framework uses worker-specific logging such as:

```text
automation_gw0.log
automation_gw1.log
```

A stable default for the Daraz live website is:

```text
2 workers
```

---

# Retry Handling

Transient failures are handled using:

```text
pytest-rerunfailures
```

The framework currently uses controlled retries to avoid hiding genuine defects.

Example:

```ini
--reruns 1
--reruns-delay 2
```

---

# Logging

Logs are stored inside:

```text
reports/
```

Example:

```text
reports/automation.log
```

Parallel runs create:

```text
reports/automation_gw0.log
reports/automation_gw1.log
```

Logs include:

- test execution
- search operations
- page navigation
- API requests
- API responses
- PASS results
- FAIL results
- SKIPPED tests
- artifact locations

---

# Failure Screenshots

When a UI test fails, a screenshot is automatically captured.

Stored in:

```text
screenshots/
```

Example:

```text
screenshots/main_test_guest_add_product_to_cart.png
```

---

# Playwright Tracing

Failure traces are automatically recorded.

Stored in:

```text
traces/
```

Example:

```text
traces/main_test_product_search.zip
```

The trace can be inspected using Playwright Trace Viewer.

---

# Video Recording

Browser execution is recorded during tests.

Failure videos are stored inside:

```text
test-results/
```

Failure videos are automatically attached to Allure reports.

---

# Allure Reporting

Test results are generated inside:

```text
allure-results/
```

Run:

```bash
allure serve allure-results
```

Allure reports include:

- test steps
- test severity
- feature
- story
- parameters
- screenshots
- trace files
- failure videos
- logs
- API request details
- API response details
- environment metadata
- executor metadata

---

# Allure Environment Information

The framework automatically generates:

```text
allure-results/environment.properties
```

Example:

```text
Environment=qa
Base_URL=https://www.daraz.com.np/
Browser=chromium
Headless=True
Workers=2
```

---

# Allure Executor Information

The framework automatically generates:

```text
allure-results/executor.json
```

The executor can identify test execution from:

```text
Local
Docker
GitHub Actions
```

---

# Docker

The framework supports Docker execution.

Build the image:

```bash
docker build -t daraz-qa .
```

Run:

```bash
docker run daraz-qa
```

---

# Docker Compose

The project also supports Docker Compose.

Run:

```bash
docker compose up --build
```

Artifact directories are mounted so test results remain available outside the container.

Mounted directories include:

```text
allure-results
reports
screenshots
traces
test-results
```

---

# GitHub Actions

CI configuration is located at:

```text
.github/workflows/playwright-tests.yml
```

The workflow is configured to:

1. Checkout repository
2. Set up Python
3. Install dependencies
4. Install Playwright Chromium
5. Run API tests
6. Run UI smoke tests
7. Upload Allure results
8. Upload logs
9. Upload screenshots
10. Upload Playwright traces
11. Upload videos

---

# Installation

Clone the repository:

```bash
git clone https://github.com/ritik678-max/daraz-playwright-python-qa.git
```

Move into the project:

```bash
cd daraz-playwright-python-qa
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install chromium firefox webkit
```

---

# Running Tests

Run all tests:

```bash
pytest -s
```

Run smoke tests:

```bash
pytest -s -m smoke
```

Run API tests:

```bash
pytest -s -m api
```

Run regression tests:

```bash
pytest -s -m regression
```

Run search tests:

```bash
pytest -s -m search
```

Run with parallel workers:

```bash
pytest -s -m smoke -n 2
```

Run a specific test:

```bash
pytest -s tests/test_cart.py
```

---

# Generate Allure Report

Run tests first:

```bash
pytest -s
```

Then:

```bash
allure serve allure-results
```

---

# Safety Approach

This project intentionally avoids unsafe automation against the production e-commerce website.

The framework does not:

- place real orders
- make payments
- bypass authentication
- bypass OTP
- bypass CAPTCHA
- use real customer credentials

Production-site tests stop before any financial or destructive action.

---

# Current Framework Architecture

```text
                    Test Data
                       │
                       ▼
                Pytest Test Layer
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
   Page Object Layer          API Test Layer
          │                         │
          ▼                         ▼
      Playwright                API Client
          │                         │
          ▼                         ▼
      Daraz Nepal              REST API
          │
          ▼
 Failure Artifacts
          │
 ┌────────┼─────────┬─────────┐
 ▼        ▼         ▼         ▼
Logs  Screenshot   Trace     Video
          │
          ▼
     Allure Report
```

---

# Skills Demonstrated

This project demonstrates practical knowledge of:

- Manual QA concepts
- UI automation
- API automation
- Python
- Playwright
- Pytest
- Page Object Model
- REST API testing
- JSON schema validation
- Data-driven testing
- Cross-browser testing
- Parallel testing
- Failure debugging
- Logging
- CI/CD
- Docker
- Git
- GitHub
- GitHub Actions
- Environment configuration
- Test reporting

---

# Future Improvements

Potential future improvements include:

- authenticated test environment flows
- API authentication testing
- contract testing
- additional negative API scenarios
- test data factories
- mock API testing
- database validation
- accessibility testing
- performance testing
- mobile automation using Appium

---

# Author

**Ritik Thakur**

QA Automation / SDET Portfolio Project

GitHub:

```text
https://github.com/ritik678-max
```