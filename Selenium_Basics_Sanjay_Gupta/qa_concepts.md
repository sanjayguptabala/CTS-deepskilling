# QA Concepts & Selenium Basics

# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

Submit Location: `qa_concepts.md`

---

# Task 1: Map Testing Types to a Real System

## 1. Testing Levels Applied to the Course Management API

### Unit Testing
* **Definition:** Unit Testing verifies an individual function, method, or unit of logic in complete isolation from external dependencies (e.g., using mocks for database or network calls).
* **Concrete Test Case:**
  | Field | Details |
  | --- | --- |
  | **Function Under Test** | `create_course(name, code, credits, department)` |
  | **Objective** | Verify that `create_course()` instantiates a valid `Course` object and computes default values correctly when passed valid inputs. |
  | **Input Data** | `name="Python Programming"`, `code="CS101"`, `credits=4`, `department="Computer Science"` |
  | **Expected Result** | Returns a `Course` instance with matching fields and status `Active`. No DB calls executed. |
  | **Classification** | **Functional Testing** |

### Integration Testing
* **Definition:** Integration Testing validates the interaction and data flow between two or more integrated components or modules (e.g., API route handler + Database ORM layer).
* **Concrete Test Case:**
  | Field | Details |
  | --- | --- |
  | **Components Integrated**| API Endpoint Handler (`POST /api/courses/`) + PostgreSQL/MySQL Database persistence layer. |
  | **Objective** | Verify that submitting a valid payload through the endpoint inserts a new row into the `courses` database table. |
  | **Input Data** | HTTP POST JSON: `{"name": "Data Structures", "code": "CS201", "credits": 3, "department": "CS"}` |
  | **Expected Result** | HTTP 201 Created returned; a query `SELECT * FROM courses WHERE code='CS201'` returns the exact record. |
  | **Classification** | **Functional Testing** |

### System Testing
* **Definition:** System Testing evaluates the complete, fully integrated software system against specified business requirements across an end-to-end user workflow.
* **Concrete Test Case:**
  | Field | Details |
  | --- | --- |
  | **End-to-End Workflow** | Course Lifecycle Flow: `Create Course` $\rightarrow$ `Fetch Course List` $\rightarrow$ `Update Course Details` $\rightarrow$ `Delete Course`. |
  | **Objective** | Verify complete end-to-end CRUD operations via API requests and ensure overall system state consistency. |
  | **Test Steps** | 1. `POST /api/courses/` (Create CS301)<br>2. `GET /api/courses/CS301` (Verify details)<br>3. `PUT /api/courses/CS301` (Update credits to 4)<br>4. `DELETE /api/courses/CS301` (Remove course)<br>5. `GET /api/courses/CS301` (Verify 404 Not Found). |
  | **Expected Result** | All operations succeed with correct HTTP status codes (201, 200, 200, 200, 404) and DB reflects final deletion. |
  | **Classification** | **Functional Testing** |

### User Acceptance Testing (UAT)
* **Definition:** UAT tests the application from the end-user's perspective (e.g., College Admin) to confirm it satisfies business needs and is ready for operational deployment.
* **Concrete Test Case:**
  | Field | Details |
  | --- | --- |
  | **User Persona** | College Academic Administrator |
  | **Objective** | Add a new elective course to the academic catalog for the upcoming semester and ensure students can enroll. |
  | **Test Steps** | 1. Admin logs into the Course Management Portal / OpenAPI interface (`/docs`).<br>2. Navigates to "Add New Course".<br>3. Submits "Advanced AI & ML" for Spring 2026.<br>4. Verifies course appears under public student enrollment catalog. |
  | **Expected Result** | Course is successfully registered, marked as available for registration, and visible in student catalog. |
  | **Classification** | **Functional Testing** |

---

## 2. Functional vs. Non-Functional Testing

| Feature / Dimension | Functional Testing | Non-Functional Testing |
| --- | --- | --- |
| **Core Question** | *"Does the system do what it is supposed to do?"* | *"How well does the system perform its functions?"* |
| **Focus Area** | Business logic, calculations, API responses, CRUD operations, boundary conditions. | Response times, throughput, security vulnerability, reliability, scalability, usability. |
| **Requirement Basis** | Functional Requirements Specification (FRS), User Stories. | Non-Functional Requirements (NFR), Service Level Agreements (SLAs). |
| **Example** | Verifying `POST /api/courses/` returns HTTP 201 when a course is created. | Verifying `POST /api/courses/` processes requests within 200ms under 500 concurrent requests. |

### Non-Functional Test Example (API Performance & Load Testing)
* **Test Type:** Performance & Reliability Testing
* **Scenario:** Verify the load handling and response time latency of the Course Management API under peak registration load.
* **Specification:** Execute 500 concurrent `GET /api/courses/` requests for 5 minutes using JMeter / Locust.
* **Acceptance Criteria:**
  - Average response latency $\le$ 300 ms.
  - 99th percentile response latency $\le$ 800 ms.
  - Error rate (HTTP 5xx responses) must be 0.00%.

---

## 3. Black-Box Testing vs. White-Box Testing

| Parameter | Black-Box Testing | White-Box Testing |
| --- | --- | --- |
| **Knowledge of Code** | Testing performed **without** knowledge of internal source code, structure, or implementation details. | Testing performed **with** full access and knowledge of internal source code, control structures, and architecture. |
| **Testing Focus** | System behavior, inputs/outputs, user interfaces, compliance with functional specifications. | Internal logic paths, code coverage, statement coverage, branch condition coverage, exception handling. |
| **Techniques Used** | Equivalence Partitioning, Boundary Value Analysis, Decision Tables, Use Case Testing. | Control Flow Testing, Data Flow Testing, Path Coverage, Statement/Branch Coverage. |
| **Primary Performer** | **QA Engineers / Software Testers / Business Analysts / End-Users** | **Software Developers / Automation Engineers / Unit Testers** |

### Summary
* **QA Testers** typically perform **Black-Box Testing** to ensure the software behaves correctly according to user requirements from an external viewpoint.
* **Developers** typically perform **White-Box Testing** during unit and integration testing to ensure code quality, logic correctness, and branch coverage.

---

## 4. Formal Test Cases for `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass / Fail |
| --- | --- | --- | --- | --- | --- | --- |
| **TC_API_001** | Verify successful creation of a new course with all valid required fields. | 1. API server is active and reachable.<br>2. Database connection is healthy. | 1. Send `POST /api/courses/`<br>Payload:<br>`{"course_name": "Web Development", "course_code": "CS105", "credits": 3, "department": "Computer Science"}`<br>2. Inspect HTTP status code and response body. | HTTP Status: `201 Created`<br>Response contains generated `id` (e.g. `id: 101`), correct field values, and creation timestamp. | | |
| **TC_API_002** | Verify system rejects course creation when a duplicate `course_code` is provided. | 1. API server is active.<br>2. Course with `course_code: "CS105"` already exists in DB. | 1. Send `POST /api/courses/`<br>Payload:<br>`{"course_name": "Advanced Web", "course_code": "CS105", "credits": 4, "department": "Computer Science"}`<br>2. Inspect HTTP status code and response error detail. | HTTP Status: `409 Conflict` (or `400 Bad Request`).<br>Response payload contains clear error message: `"Course code CS105 already exists."` | | |
| **TC_API_003** | Verify validation failure when mandatory field `course_name` is omitted. | 1. API server is active. | 1. Send `POST /api/courses/`<br>Payload:<br>`{"course_code": "CS108", "credits": 3, "department": "CS"}` (missing `course_name`).<br>2. Inspect HTTP status code and validation response. | HTTP Status: `400 Bad Request` (or `422 Unprocessable Entity`).<br>Response details missing mandatory field: `course_name`. | | |

---

# Task 2: Defect Lifecycle & Severity Classification

## 5. Complete Defect Lifecycle

The defect (bug) lifecycle describes the series of states a defect transitions through from initial discovery by a QA tester to final closure and verification.

```
       +--------------+
       |     NEW      |
       +-------+------+
               |
               v
       +--------------+
       |   ASSIGNED   |
       +-------+------+
               |
       +-------+-------+------------------+
       |               |                  |
       v               v                  v
+--------------+ +-----------+     +--------------+
|   REJECTED   | | DEFERRED  |     |     OPEN     |
+--------------+ +-----------+     +-------+------+
                                          |
                                          v
                                   +--------------+
                                   |    FIXED     |
                                   +-------+------+
                                          |
                                          v
                                   +--------------+
                                   |    RETEST    |
                                   +-------+------+
                                          |
                        +-----------------+-----------------+
                        |                                   |
                        v (Failed)                          v (Passed)
                 +--------------+                    +--------------+
                 |   REOPENED   |                    |   VERIFIED   |
                 +-------+------+                    +-------+------+
                         |                                  |
                         v                                  v
                   (Back to Open)                    +--------------+
                                                     |    CLOSED    |
                                                     +--------------+
```

### State Descriptions

1. **New:** When a defect is logged by a tester for the first time, it is set to `New`.
2. **Assigned:** The Lead or QA Manager assigns the defect to a developer for evaluation.
3. **Open:** The developer begins analyzing, debugging, and working on a fix for the defect.
4. **Fixed:** The developer finishes coding the bug fix, passes local tests, and deploys the build to the test environment.
5. **Retest:** The bug report is assigned back to the QA tester to execute verification test steps on the new build.
6. **Verified:** The tester verifies that the bug no longer occurs in the test environment and the feature behaves as expected.
7. **Closed:** If retesting passes, the tester or QA Lead updates the bug status to `Closed`.

### Alternate & Exception Paths

* **Rejected Path (`New` $\rightarrow$ `Rejected`):**
  - **Reason:** The developer or team leads determine that the reported behavior is not a bug (e.g., works as designed according to specification, invalid test environment setup, or tester misunderstanding).
  - **Resolution:** Marked as `Rejected` with explanatory comments.

* **Deferred Path (`Assigned` / `Open` $\rightarrow$ `Deferred`):**
  - **Reason:** The bug is confirmed to be valid, but fixing it is postponed to a future release sprint due to low business impact, tight current release deadlines, or pending design changes.
  - **Resolution:** Deferred to backlog for prioritization in subsequent releases.

* **Reopened Path (`Retest` $\rightarrow$ `Reopened`):**
  - **Reason:** During retesting, the tester discovers the defect is still reproducible or that the code change introduced a regression.
  - **Resolution:** Reopened and assigned back to developer (`Reopened` $\rightarrow$ `Open`).

* **Duplicate Path (`New` / `Open` $\rightarrow$ `Duplicate`):**
  - **Reason:** The defect is identical to another bug already logged in the system.

---

## 6. Severity & Priority Classification for Course Management API Bugs

| Bug Scenario | Severity | Priority | Justification & Rationale |
| --- | --- | --- | --- |
| **a) `POST /api/courses/` returns HTTP 500 Internal Server Error for all requests.** | **Critical** | **P1** | **Severity (Critical):** Core system capability (course creation) is completely broken, preventing any new data entry.<br>**Priority (P1):** Immediate fix required because development, testing, and business workflows are blocked. |
| **b) Course names longer than 150 characters are silently truncated without an error.** | **Medium** | **P2** | **Severity (Medium):** Causes silent data loss/corruption, but system does not crash and normal-length courses function correctly.<br>**Priority (P2):** Needs to be scheduled in the current sprint to prevent invalid catalog data. |
| **c) The `/docs` Swagger page has a typo in the API description.** | **Low** | **P4** | **Severity (Low):** Minor cosmetic/documentation issue with zero impact on functional behavior or code execution.<br>**Priority (P4):** Lowest fix urgency; can be updated opportunistically in future doc cleanups. |
| **d) Login with correct credentials occasionally returns HTTP 401 on the first attempt (intermittent).** | **High** | **P1** | **Severity (High):** Impacts core authentication security/reliability and degrades user trust.<br>**Priority (P1):** Intermittent auth defects signal deeper architectural or race-condition flaws requiring immediate investigation before production release. |

---

## 7. Formal Defect Report for Bug (a)

| Defect Field | Details |
| --- | --- |
| **Defect ID** | `DEF-2026-001` |
| **Title** | `POST /api/courses/ returns HTTP 500 Internal Server Error for all valid payloads` |
| **Project / Module** | Course Management API / Course Creation Module |
| **Environment** | Staging Environment (OS: Windows 11, DB: PostgreSQL v15.2, Python: 3.11, FastAPI: 0.104) |
| **Build Version** | `v1.2.0-rc3` |
| **Severity** | **Critical** |
| **Priority** | **P1 (Urgent)** |
| **Reporter** | QA Test Lead |
| **Assigned To** | Backend Lead Developer |
| **Preconditions** | 1. Course API service is active at `http://staging.api.local:8000`.<br>2. Valid authentication token acquired. |
| **Steps to Reproduce** | 1. Launch API client (Postman or Swagger UI at `http://staging.api.local:8000/docs`).<br>2. Select endpoint `POST /api/courses/`.<br>3. Provide valid headers: `Content-Type: application/json`, `Authorization: Bearer <valid_token>`.<br>4. Enter valid body payload:<br>```json<br>{\n  "course_name": "Database Management Systems",\n  "course_code": "CS202",\n  "credits": 4,\n  "department": "Computer Science"\n}<br>```<br>5. Click **Execute** / Send request. |
| **Expected Result** | HTTP Status Code `201 Created` returned. Response body contains created course object with auto-generated ID. Record persists in DB. |
| **Actual Result** | HTTP Status Code `500 Internal Server Error` returned.<br>Response payload:<br>`{"detail": "Internal Server Error: Unhandled exception in route handler"}` |
| **Attachments** | `screenshot_500_error.png` (Attached Postman error log & server traceback screenshot). |

---

## 8. Difference Between Severity and Priority

| Dimension | Severity | Priority |
| --- | --- | --- |
| **Definition** | Severity measures the **technical impact** or severity of the defect on system operation, functionality, or data integrity. | Priority measures the **business urgency** of fixing the defect relative to release schedules and user needs. |
| **Driven By** | Technical complexity, system crash, data corruption, scope of functional block. | Business value, client visibility, release deadlines, user impact. |
| **Determined By** | **QA Tester / Test Lead** (based on functional specs and impact). | **Product Manager / Project Manager / Business Owner** (based on timelines). |
| **Focus** | How severe is the bug to the system? | How quickly must the bug be resolved? |

### Real-World Example: High Severity but Low Priority

* **Scenario:** An internal administrative web application crashes with an unhandled `NullPointerException` (HTTP 500 error) whenever an admin clicks a link labeled **"Download 2018 Legacy Tax Archive (Deprecated)"** located in the bottom footer.
* **Severity = High / Critical:** 
  - The application experiences a complete page crash/error state whenever the link is activated.
* **Priority = Low (P3 / P4):** 
  - The feature pertains to an obsolete 2018 legacy file that is never accessed by normal business users during daily operations. 
  - It does not impact core operational workflows (e.g., billing, user registration, active course enrollment).
  - Therefore, fixing it is deferred until routine maintenance sprints, demonstrating that **High Severity does not automatically mean High Priority**.
