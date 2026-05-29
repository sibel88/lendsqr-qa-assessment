# Lendsqr Adjutor QA Automation Assessment

This repository contains automated API tests for Task 2 of the Lendsqr QA assessment.

## Scope

The tests cover selected Adjutor APIs from the Nigerian Country Specific Endpoints section. The scripts validate:

- HTTP status code
- JSON response body/message
- Response time

## Setup

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

5. Add your Adjutor API key to `.env`.

Never commit the real API key.

## Configure endpoints

Open `config/endpoints.json` and update the endpoint paths, request parameters, expected status codes, and expected response messages based on the Adjutor API documentation and your account access.

At least 2 endpoints per API module should be retained.

## Run tests

```bash
pytest -v tests/ --html=adjutor-test-report.html --self-contained-html
```

## Output

The command generates:

- Terminal pass/fail results
- `adjutor-test-report.html`
- Response-time logs printed in the test output

## Test summary

Update this section after running the tests:

| Module | Endpoint | Status | Result | Response Time | Notes |
|---|---|---:|---|---:|---|
| Platform Data | Pricing | TBD | TBD | TBD | Update after execution |
| Platform Data | Wallet Balance | TBD | TBD | TBD | Update after execution |
| Validation | BVN Validation | TBD | TBD | TBD | Use permitted test data only |
| Validation | Bank Account Validation | TBD | TBD | TBD | Use permitted test data only |

## Security notes

- API keys are loaded through environment variables.
- Real keys are excluded from the repository.
- Test data should be dummy data or data explicitly permitted by the assessment.
- Sensitive response payloads should not be committed.
