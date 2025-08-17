# 🧪 Testing Summary Report
**Project:** Equipment Status Tracker Application  
**Author:** Devendra Singh  
**Date:** *5/08/2025* 

---

## 📊 Summary

This document provides a comprehensive summary of the testing activities performed on the Equipment Status Tracker Application. The testing covered manual functional testing, API automation, and frontend UI automation across multiple phases.

### Key Findings
- **Total Bugs Found:** 7
- **Critical Issues:** 0
- **High Priority Issues:** 4 (Bugs #1, #2, #3, #5)
- **Medium Priority Issues:** 1 (Bug #4)
- **Low Priority Issues:** 2 (Bugs #6, #7)

---

## 🎯 Testing Objectives Achieved

✅ **Core Functionality Verification**
- Equipment listing and display
- Equipment creation and validation
- Status updates and persistence
- History tracking and display
- Real-time updates across sessions

✅ **API Automation Coverage**
- All documented endpoints automated
- Happy path scenarios validated
- Error handling and edge cases covered
- Data consistency verified

✅ **Frontend Automation**
- Key user workflows automated
- Cross-browser compatibility tested
- Error scenarios handled
- Real-time update verification

---

## 🐛 Bug Summary

### Bug #1: Active Status Count Mismatch Between Summary and List
**Severity:** High  
**Status:** Open  
**Priority:** P2  
**Type:** Functional  
**Description:** The UI summary displays "Active: 3", and the API (GET /api/equipment) returns three items with status "Active", but the detailed equipment list only shows two Active items. This inconsistency between the summary and the list indicates a data/display synchronization issue and can mislead users about the actual state.  
**Steps to Reproduce:** 
1. Call GET /api/equipment and verify equipments count with status "Active".
2. Open the application UI and observe the summary indicator showing "Active: 3".
3. Compare the counts and note the discrepancy: summary/API show 3, list shows 2.  
**Expected Behavior:** The number of Active items should be consistent across the summary, the detailed list, and the API response. It should be same as the API response and displayed in the list.  
**Actual Behavior:** The summary shows "Active: 3" and the API returns 2 Active items, and two Active items appear in the list view as well.  
**Impact:** Users are misled about the actual equipment status, affecting decision-making and operational visibility.  
**API Response Evidence:** 
```json
{
  "success": true,
  "data": [
    {"id": 4, "name": "Loader Volvo L120", "status": "Active", "location": "Site C"},
    {"id": 7, "name": "Excavator Test CAT 321", "status": "Active", "location": "Site AB"}
  ],
  "count": 7
}
```

### Bug #2: Failed to Update Equipment Status from Under Maintenance to Active or Idle
**Severity:** High  
**Status:** Open  
**Priority:** P1  
**Type:** Functional  
**Description:** When attempting to change an equipment item's status from "Under Maintenance" to either "Active" or "Idle", the operation fails and an error message is shown: "failed update the status". The status remains stuck at "Under Maintenance". This breaks a core workflow and prevents accurate state tracking.  
**Steps to Reproduce:** 
1. Open the Equipment Status Tracker application with an equipment item currently in "Under Maintenance" or update the status of an item/equipment to "Under Maintenance"
2. Open the status dropdown for that item.
3. Select "Active" (repeat for "Idle" in a separate attempt).
4. Observe the error message and the resulting status.
5. Optionally retry the change to confirm the failure is consistent.  
**Expected Behavior:** The status should successfully update to the selected value ("Active" or "Idle"), the badge should reflect the new status, and the change should be recorded in the history without any error message.  
**Actual Behavior:** An error message "failed update the status" appears, and the equipment remains in "Under Maintenance". The status does not change and no successful update is recorded.  
**Impact:** Core functionality is broken - users cannot transition equipment out of maintenance status, severely impacting operational workflows.

### Bug #3: Equipment History Modal Does Not Open After Status is Set to Under Maintenance
**Severity:** High  
**Status:** Open  
**Priority:** P1  
**Type:** Functional  
**Description:** After changing an equipment item's status to "Under Maintenance", clicking the "History" button does not open/respond. The user is unable to view the status change history for that item, blocking visibility into recent transitions.  
**Steps to Reproduce:** 
1. Open the Equipment Status Tracker application.
2. Select an equipment item and change its status to "Under Maintenance".
3. Confirm the status update is reflected in the badge.
4. Click the "History" button/link for that equipment.
5. Observe that the history modal does not open/respond.  
**Expected Behavior:** The history modal should open and display the full sequence of status changes for the equipment, including the transition to "Under Maintenance".  
**Actual Behavior:** Clicking "History" after setting status to "Under Maintenance" doesn't respond; the history view does not open and no information is shown.  
**Impact:** Users lose visibility into equipment status history, which is critical for maintenance tracking and operational decision-making.  
**Note:** Before updating status, history is shown; after updating status as 'under maintenance', history button is not responding.

### Bug #4: Missing Validation for Equipment Name and Equipment Location When Adding New Equipment
**Severity:** Medium  
**Status:** Open  
**Priority:** P2  
**Type:** Validation  
**Description:** The add equipment form does not enforce proper validation on the Equipment Name and Equipment Location fields. Users can create equipment by entering numbers only or special characters only, excessively long strings, without any warning or error. As a result, equipment records are created with invalid data.  
**Steps to Reproduce:** 
1. Open the add equipment form by clicking on 'Add Equipment' button.
2. Enter special characters (*$%#@{}) or potentially unsafe input 
Name or Location and submit.
3. Enter an excessively long string (e.g., 500+ characters) in Name or Location and submit.
4. Observe that the form accepts these values and the new equipment appears in the list with the invalid Name/Location.  
**Expected Behavior:** The form should validate Equipment Name and Location before submission:
• Enforce reasonable length limits (e.g., max 100 characters).
• Either restrict or sanitize unsafe/special characters.
• Provide clear inline error messages when validation fails and prevent submission until corrected.  
**Actual Behavior:** The form accepts overly long, and special-character-laden values for Equipment Name and Location without any error or feedback. Equipment is created with these invalid values.  
**Impact:** Data integrity is compromised, potentially leading to display issues, security vulnerabilities, and poor user experience.

### Bug #5: 500 Internal Server Error on Rapid Page Refresh After Status Update
**Severity:** High  
**Status:** Open  
**Priority:** P1  
**Type:** Functional/UI  
**Description:** After updating the status of an equipment item (especially equipment created via API), rapidly refreshing the page—either by clicking the browser refresh icon multiple times or repeatedly hitting the in-app refresh button—causes a 500 Internal Server Error. The failure also surfaces more generally when a user quickly triggers multiple refreshes in succession after a status change.  
**Steps to Reproduce:** 
1. Create an equipment item via the API (POST /api/equipment).
2. Open the application UI and locate that equipment.
3. Update its status (e.g., change to Idle then Active).
4. Immediately after the status update, rapidly refresh the page multiple times by:
   o Scenario A: Clicking the browser refresh/reload icon repeatedly.
   o Scenario B: Clicking the in-app refresh button repeatedly.
5. Observe that a 500 Internal Server Error is displayed.
6. Repeat the same for any equipment (not just API-created) by updating status and doing rapid refreshes to confirm reproducibility.  
**Expected Behavior:** The page should handle rapid refresh requests gracefully. Status updates should persist, and repeated refresh actions should show appropriate loading/feedback without resulting in a server error. No 500 error should be thrown.  
**Actual Behavior:** A 500 Internal Server Error is shown after rapid successive refreshes following a status update. The application fails to recover cleanly, and the user cannot reliably see the current equipment state.  
**Impact:** Application becomes unusable after rapid refresh actions, affecting user experience and potentially causing data loss or inconsistency.

### Bug #6: Duplicate Scrollbar Appears When Scrolling History Modal
**Severity:** Low  
**Status:** Open  
**Priority:** P3  
**Type:** UI/UX  
**Description:** When the history modal is opened for equipment with enough entries to require scrolling, two scrollbars are visible: the modal's internal scrollbar and the page-level/outer scrollbar. As the user scrolls inside the modal, the outer page scrollbar is also displayed and can move, causing visual clutter.  
**Steps to Reproduce:** 
1. Open the Equipment Status Tracker application.
2. Select equipment with a long history (enough entries to enable scrolling).
3. Click the "History" button to open the history modal.
4. Scroll within the modal content.
5. Observe that both the modal has its own scrollbar and the surrounding page also shows a scrollbar (and may scroll or appear active).  
**Expected Behavior:** Only the history modal should display a scrollbar when its content overflows. The background page should not show an active scrollbar or scroll while the modal is being interacted with, keeping focus and scroll behavior confined to the modal.  
**Actual Behavior:** Both the modal and the underlying page display scrollbars when the history content is scrolled, leading to duplicate scroll indicators and possible background movement.  
**Impact:** Visual clutter and poor user experience, though functionality remains intact.  
**Attachment:** Screen recording is attached

### Bug #7: Redundant Flicker - "Refreshing" Button State and Global Loader Appear Together
**Severity:** Low  
**Status:** Open  
**Priority:** P3  
**Type:** UI/UX  
**Description:** When the user triggers a refresh—either by clicking the in-app refresh button or using the browser's reload control—the UI shows two overlapping loading indicators: the refresh button switches to "Refreshing" briefly, along with the global page-level loader appears. The result is a visually redundant flicker/hand-off that can confuse users about the progress of the action.  
**Steps to Reproduce:** 
1. Open the Equipment Status Tracker with equipment already loaded.
2. Scenario A: Click the in-app refresh button.
3. Scenario B: Click the browser reload/refresh icon (full page reload).
4. In both scenarios, observe the sequence of loading feedback: first the refresh control changes state, then the global loader appears immediately after.
5. Note the quick transition/flicker between the two indicators.  
**Expected Behavior:** One clear, non-conflicting loading indicator is presented. The refresh button should not change to refreshing when there is already a page loader.  
**Actual Behavior:** Both the button-level "Refreshing" indicator and the global page loader appear in rapid succession, causing a visual flicker and redundant feedback.  
**Impact:** Confusing user experience with redundant loading indicators, though functionality is not affected.  
**Attachment:** Screen recording attached

---

## 📈 Test Coverage Summary

### Manual Testing Coverage
- **Test Cases Executed:** [29] out of [29]
- **Pass Rate:** [75.86]%
- **Areas Covered:**
  - Equipment Management
  - Status Updates
  - History Tracking
  - Real-time Updates
  - Error Handling
  - Usability Testing

### API Automation Coverage
- **Framework:** pytest + requests + Python
- **Endpoints Tested:** 4/4 (100%)
- **Test Scenarios:** Comprehensive coverage including happy path, negative, and edge cases
- **Test Cases:** [32]
- **Pass Rate:** [100%]
- **Coverage Areas:**
  - GET /api/equipment
  - POST /api/equipment
  - POST /api/equipment/{id}/status
  - GET /api/equipment/{id}/history
- **Reporting:** Structured test results with detailed logs

### Frontend Automation Coverage
- **Test Cases:** [17]
- **Pass Rate:** [X]%
- **Browsers Tested:** [chromium and firefox]
- **Coverage Areas:**
  - Equipment List Display
  - Add Equipment Flow
  - Status Update Flow
  - History Modal
  - Error Scenarios

---

## ⚠️ Critical Issues & Risks

### High Priority Issues
1. **Bug #2: Failed to Update Equipment Status from Under Maintenance** - Core functionality broken, users cannot transition equipment out of maintenance status
2. **Bug #3: Equipment History Modal Does Not Open After Status is Set to Under Maintenance** - Users lose visibility into equipment status history
3. **Bug #5: 500 Internal Server Error on Rapid Page Refresh** - Application becomes unusable after rapid refresh actions
4. **Bug #1: Active Status Count Mismatch Between Summary and List** - Users are misled about actual equipment status

### Medium Priority Issues
1. **Bug #4: Missing Validation for Equipment Name and Equipment Location** - Data integrity compromised, potential security vulnerabilities

### Low Priority Issues
1. **Bug #6: Duplicate Scrollbar Appears When Scrolling History Modal** - Visual clutter and poor user experience
2. **Bug #7: Redundant Flicker - "Refreshing" Button State and Global Loader** - Confusing user experience with redundant loading indicators

---

## 📊 Performance Metrics

### API Performance
- **Average Response Time:** [290]ms
- **Peak Response Time:** [345]ms

---

### Tools Used
- **Manual Testing:** [Chrome and firefox broswers, Postman and Swagger]
- **API Testing:** pytest, requests
- **Frontend Testing:** Playwright
- **Reporting:** Allure Reports

---

## 📋 Test Artifacts

### Reports Generated
- [ ] Manual Test cases along with Results
- [ ] API Automation Test Reports
- [ ] Frontend Automation Reports
- [ ] Bug Report

### Documentation
- [ ] Test Plan
- [ ] Test Cases and Test Results
- [ ] Bug Report
- [ ] README.md [Setup Instructions and Execution Guide]

---

## ✅ Conclusion

The testing phase has been completed successfully with comprehensive coverage of the Equipment Status Tracker Application. While 7 bugs were identified, the core functionality is working as expected. The automation framework is in place for regression testing.

---

**Report Prepared By:** Devendra Singh
