# 🗂️ Test Plan  
**Project:** Equipment Status Tracker Application  
**Author:** Devendra Singh  
**Date:** *2/08/2025*  
**Version:** 1.0

---

## 📘 1. Overview

This plan explains how the Equipment Status Tracker application will be tested end-to-end. The work is done in three parts: first manual/functional testing to understand how the app behaves and catch immediate issues; then API testing to validate backend behavior and ensure data consistency; and finally frontend/UI automation to cover user flows, real-time updates, and error handling using what was learned earlier. The focus is on core functionality, timely updates, error resilience, and clear evidence of testing.

## 🎯 2. Objectives

- Verify main flows: equipment listing, creation, status changes, history viewing, and real-time updates.  
- Identify and document defects through manual testing.  
- Automate backend checks to ensure API correctness and consistency.  
- Automate key UI workflows with stability.  
- Provide clear, repeatable test artifacts and a summary of remaining risks.

## ⚙️ 3. Assumptions

- Frontend is reachable and reflects status changes in real time without a full page reload.  
- API endpoints are available as documented and return structured JSON.  
- Status values are limited to: Active, Idle, Under Maintenance.  
- No authentication is required for the core flows.  
- Real-time updates are delivered via the app’s sync mechanism and observable across sessions.

## 📌 4. Scope & Order

### Phase 1: Manual / Functional Testing

Start here to learn the system and verify expected behavior.

**Covered manually:**
- Equipment list display (data, status badges, loading)  
- Adding equipment (valid/invalid)  
- Status updates and persistence  
- History modal (content, order, pagination)  
- Real-time sync across sessions  
- Error conditions (network failure, invalid input)  
- Basic usability (responsiveness, badge colors, keyboard navigation)

**Approach:**  
Run structured test cases (happy path, negative, edge), perform exploratory checks (rapid status toggling, concurrent edits), measure update propagation delay, record actual vs expected, and capture issues.

### Phase 2: API Testing

Automate backend expectations and data flow validation.

**Endpoints included:**
- `GET /api/equipment`  
- `POST /api/equipment`  
- `POST /api/equipment/{id}/status`  
- `GET /api/equipment/{id}/history`

**Focus:**
- Happy paths (create, list, update, history)  
- Invalid inputs (missing fields, unsupported status, bad IDs)  
- Schema/structure validation  
- Chained flow validation (create → update → history → list reflects current state)  
- Error codes and messages  
- Basic performance checks

**Approach:**  
Use `pytest` + `requests`, generate unique test data, validate responses, log request/response, and fail fast on deviations.

### Phase 3: Frontend / UI Automation

Automate user-facing flows with dependency on stable backend behavior.

**Covered in automation:**
- Equipment list load and badge correctness  
- Adding equipment via UI  
- Status change and persistence  
- History modal interactions  
- Real-time update (trigger via API, verify in UI)  
- Error scenarios (API failure, network issues)  
- Basic accessibility (keyboard interaction)  
- Cross-browser if applicable

**Approach:**  
Apply Page Object Model, use explicit waits/polling for sync, combine API triggers with UI verification, capture failure context (screenshots/logs), and group critical flows for smoke validation.

## 🧪 5. Test Data Strategy

- Use unique equipment names (timestamp or UUID) per run to avoid collisions.  
- Cover all valid status transitions.  
- Include negative inputs: empty name, invalid status value, malformed payload.  
- Simulate concurrent updates to validate history order and consistency.

## 🛠️ 6. Environment & Tools

- **Frontend:** Multiple browser sessions for real-time comparison; responsive viewport testing.  
- **API:** Direct interaction with documented endpoints.  
- **Automation:**  
  - API: `pytest` + `requests` + `jsonschema`  
  - UI: Playwright (or equivalent) with Page Object Model  
- **Reporting:** HTML / Allure-style reports; optional JUnit/XML for CI.  
- **Support:** Network throttling (DevTools), environment configuration, logging utilities.

## 🚦 7. Entry & Exit Criteria

**Entry Criteria:**  
- Frontend and API are reachable.  
- Test case templates and automation scaffolds are in place.  
- Test data generation is configured.

**Exit Criteria:**  
- All high-priority manual and automated tests executed.  
- Reports generated.  
- No unresolved critical issues, or they are documented with risk.  
- Coverage summary available.

## 📊 8. Metrics

- Feature coverage vs plan  
- Defects by severity and source  
- Automation pass rate and stability  
- Real-time update delay  
- API response times  
- Smoke test reliability

## ⚠️ 9. Risks & Actions

| Risk | Impact | Mitigation |
|------|--------|------------|
| Real-time delay or inconsistency | UI shows outdated status | Poll until update appears with timeout; log time differences |
| API contract change | Tests break or give wrong results | Validate response structure early and fail fast on mismatch |
| Network issues during runs | Intermittent or false failures | Retry transient errors; mark and differentiate them |
| UI layout or rendering changes | Visual misalignment or broken views | Capture baseline snapshots and compare |

## ⏱️ 10. Timeline (4 days)

- **Day 1:** Manual/functional exploration and execution; start API happy-path automation.  
- **Day 2:** Complete API coverage (negative & chained); build core frontend/UI automation and validate real-time sync.  
- **Day 3:** Complete frontend/UI automation coverage; edge and error case testing; initial reporting.
- **Day 4:** Finalize all reports (manual + automation), comprehensive testing summary, and package submission.

## 📦 11. Deliverables

- Test Plan
- Manual test cases with results  
- Bug/defect reports  
- API automation suite and execution results  
- Frontend/UI automation suite and reports  
- README with setup, execution steps, assumptions, and summary  
- Test coverage summary and residual risk note  

## 🗂️ 12. Submission Summary

- Final summary included: scope covered, key findings, defects identified, and remaining risks.  
- All artifacts (manual matrix, automation reports, bug reports) are organized and linked in the README for review.
