# Daraz E-Commerce QA Automation Framework

A mid-level QA automation framework built using **Python, Playwright, Pytest, Page Object Model, Allure Reporting, Logging, Data-Driven Testing, Screenshots, Tracing, and Video Recording**.

This project automates key user flows on **Daraz Nepal** and is designed as a portfolio project for QA Automation / SDET roles.

---

## Tech Stack

- Python
- Playwright
- Pytest
- Page Object Model (POM)
- Allure Report
- JSON Test Data
- Python Logging
- Pytest Fixtures
- Pytest Markers

---

## Current Test Coverage

The framework currently automates the following flow:

1. Open Daraz Nepal
2. Search for a product
3. Verify search URL
4. Verify product results are displayed
5. Get first product name
6. Get first product price
7. Open first product
8. Verify product details page
9. Compare listing product name with product details name
10. Compare listing price with product details price

The same test is executed using multiple search terms:

- laptop
- mobile
- headphones

---

## Project Structure

```text
E-commerce-qa/
│
├── pages/
│   ├── home_page.py
│   ├── search_page.py
│   └── product_page.py
│
├── tests/
│   ├── test_homepage.py
│   ├── test_login.py
│   └── test_search.py
│
├── testdata/
│   └── search_data.json
│
├── utils/
│   ├── config.py
│   ├── data_loader.py
│   └── logger.py
│
├── screenshots/
├── traces/
├── test-results/
├── allure-results/
├── reports/
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md