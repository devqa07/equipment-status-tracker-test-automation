# Equipment Status Tracker - Frontend Automation

This project contains automated tests for the Equipment Status Tracker frontend application using Playwright and TypeScript.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Install browsers:
```bash
npm run install:browsers
```

## Running Tests

### Run all tests:
```bash
npm test
```

### Run tests in headed mode (see browser):
```bash
npm run test:headed
```

### Run specific test suites:
```bash
npm run test:add-equipment
npm run test:equipment-list
```

### Run tests with tags:
```bash
npm run test:smoke
npm run test:regression
```

## Reports

### View HTML report:
```bash
npm run report
```

### View Allure report:
```bash
npm run report:allure
```

## Project Structure

```
frontend-playwright-automation/
├── src/test/
│   ├── pages/          # Page Object Models
│   ├── components/     # Reusable components
│   ├── specs/          # Test specifications
│   └── utils/          # Helper functions
├── data/               # Test data and interfaces
├── fixtures/           # Setup and teardown
├── config/             # Configuration files
├── test-results/       # Test execution results
└── reports/            # Generated reports
```

## Configuration

- **Base URL**: https://qa-assignment-omega.vercel.app
- **Browsers**: Chrome, Firefox, Safari, Mobile Chrome, Mobile Safari
- **Reports**: HTML, Allure, JSON, JUnit

## Test Data

Test data is generated using Faker library to ensure realistic and varied test scenarios. 