# SDLC vs TDLC – V-Model & Agile QA Integration

# Hands-On 2: V-Model Analysis & Shift-Left Testing

Submit Location: `v_model_analysis.md`

---

# Task 1: V-Model Mapping

## 9. Complete V-Model Diagram

The V-Model illustrates how Software Development Lifecycle (SDLC) phases on the left side correspond directly to Software Testing Lifecycle (TDLC) verification and validation phases on the right side, with Coding at the bottom vertex.

```
       SDLC (Development / Left Side)                  TDLC (Testing / Right Side)
       ==============================                  ===========================

       +----------------------------+                  +----------------------------+
       |   Requirements Analysis    |----------------->|     Acceptance Testing     |
       +----------------------------+                  +----------------------------+
                     \                                        /
                      \                                      /
                       +----------------------------+       /
                       |       System Design        |----->+----------------------------+
                       +----------------------------+      |       System Testing       |
                                     \                     +----------------------------+
                                      \                               /
                                       +----------------------------+/
                                       |    Architecture Design     |----------------->+----------------------------+
                                       +----------------------------+                  |    Integration Testing     |
                                                     \                                 +----------------------------+
                                                      \                                              /
                                                       +----------------------------+               /
                                                       |       Module Design        |------------->+----------------------------+
                                                       +----------------------------+              |        Unit Testing        |
                                                                     \                             +----------------------------+
                                                                      \                                           /
                                                                       +-----------------------------------------+
                                                                       |                 CODING                  |
                                                                       +-----------------------------------------+
```

### Flow Breakdown
1. **Left Side (SDLC - Verification):** Sequential degradation of user requirements into detailed technical design specs down to executable code.
2. **Bottom Vertex:** **Coding / Implementation** phase where source code is written.
3. **Right Side (TDLC - Validation):** Hierarchical testing layers validating each corresponding SDLC artifact, moving upward from low-level unit tests to high-level customer acceptance tests.

---

## 10. SDLC to TDLC Phase Mappings & Test Artifacts

During the early development phases on the left side of the V-Model, QA engineers prepare test strategies, test plans, and test case specifications concurrently with system design rather than waiting for code completion.

| SDLC Phase (Left Side) | Corresponding TDLC Phase (Right Side) | Test Artifact Produced During SDLC Phase | Description of Artifact & Purpose |
| --- | --- | --- | --- |
| **Requirements Analysis** | **Acceptance Testing** | **Acceptance Test Plan & UAT Test Suites** | Defines high-level business acceptance criteria, user story scenarios, and acceptance test scripts based on User Requirement Specifications (URS). |
| **System Design** | **System Testing** | **System Test Plan & Functional Test Cases** | Maps functional requirements to end-to-end system test cases, API specification tests, and performance/security non-functional test plans. |
| **Architecture Design** | **Integration Testing** | **Integration Test Plan & API Contract Tests** | Outlines test scenarios for component interactions, DB connection pools, external service dependencies, and interface protocol specs. |
| **Module Design** | **Unit Testing** | **Unit Test Specifications & Mock Framework Specs** | Specifies class/function level test cases, boundary value conditions, edge cases, unit test fixtures, and mock object definitions. |
| **Coding** | **Code Execution** | **Test Execution Scripts & Automated Suites** | Automated pytest/JUnit/Selenium scripts ready to be triggered against the built code. |

---

## 11. Entry & Exit Criteria for All Four Testing Levels

Entry and Exit Criteria establish quality gates that govern when testing phases begin and when a phase is deemed complete.

### 1. Unit Testing
* **Entry Criteria:**
  1. Module code compilation succeeds with zero compilation errors or warnings.
  2. Developers complete code self-inspection / peer code review.
  3. Unit test framework (e.g., `pytest`, `unittest`) and mock objects are configured.
* **Exit Criteria:**
  1. 100% of planned unit test cases executed.
  2. Code coverage threshold met (e.g., minimum 85% statement coverage and 80% branch coverage).
  3. All high/critical unit test failures resolved.

### 2. Integration Testing
* **Entry Criteria:**
  1. Unit testing phase exit criteria fully satisfied.
  2. Integrated components (API controllers, ORM models, Database instances) deployed to test environment.
  3. Interface contracts and database schemas frozen.
* **Exit Criteria:**
  1. All component interface and API data flow test cases executed successfully.
  2. No blocking integration or database persistence defects open.
  3. Integration test report published and approved by Technical Lead.

### 3. System Testing
* **Entry Criteria:**
  1. Integration testing successfully completed and signed off.
  2. Complete Course Management API build deployed to a staging environment mimicking production.
  3. System test environment, test data (courses, departments, credentials), and automated test suites ready.
* **Exit Criteria:**
  1. 100% of functional end-to-end system test cases executed.
  2. Zero open Critical (P1) or High (P2) defects.
  3. Non-functional requirements (response time under load $\le$ 300ms) verified and satisfied.

### 4. User Acceptance Testing (UAT)
* **Entry Criteria:**
  1. System testing exit criteria met and test summary report signed off by QA Lead.
  2. User documentation, Swagger OpenAPI UI docs (`/docs`), and release notes complete.
  3. UAT environment provisioned with realistic college administration test datasets.
* **Exit Criteria:**
  1. All business acceptance criteria satisfied for student/course workflows.
  2. Formal sign-off and approval obtained from College Admin / Business Stakeholders.
  3. Final production release readiness checklist completed.

---

## 12. Early QA Engagement Points in the V-Model

QA engagement must occur during early SDLC phases on the left side of the V-Model (*Shift-Left Testing*) to prevent defects before coding begins.

### Engagement Point 1: Requirements Review Phase (Left Side Top)
* **Activity in Course Management API:**
  - QA participates in requirements refinement sessions with business analysts and product owners.
  - **Concrete Action:** QA reviews requirements for `POST /api/courses/` and identifies missing or ambiguous rules (e.g., *"What happens if course code contains lowercase letters? Is course code unique per department or globally unique?"*).
  - **Benefit:** Clarifying these rules *before* design/coding prevents expensive rework and API specification mismatches.

### Engagement Point 2: Architecture & System Design Review Phase (Left Side Middle)
* **Activity in Course Management API:**
  - QA reviews technical architecture blueprints, database ER diagrams, and Swagger/OpenAPI contracts (`openapi.json`).
  - **Concrete Action:** QA evaluates API testability and database constraints (e.g., checking if `course_code` has a `UNIQUE` constraint at the database schema level or only in python code, and ensuring error response schemas follow standard JSON error formats).
  - **Benefit:** Catches database constraint gaps and untestable design decisions before database migrations and endpoints are implemented.

---

# Task 2: Agile QA & Shift-Left Testing

## 13. Three Problems of Traditional Waterfall Testing in Course Management API

In a traditional Waterfall methodology, testing occurs sequentially after all development phases are completed. This introduces severe risks:

| Waterfall Problem | Description & Application to Course Management API |
| --- | --- |
| **1. Late Defect Discovery** | Bugs are only uncovered at the end of the project during System Testing. For instance, if an architectural flaw in authentication or database foreign key constraints is discovered during API system testing, all backend routes and database schemas have already been implemented, making fixes difficult. |
| **2. Exponentially High Cost of Defect Fixes** | Fixing a requirement or design defect late in Waterfall is 10x to 100x more expensive. Catching an ambiguous course code validation rule during requirements review costs minutes of documentation edit; finding it after API endpoints, database tables, and UI forms are built requires major code refactoring. |
| **3. Compressed Testing Schedule & Delayed Feedback** | Development phase overruns push out the testing start date, compressing the QA window. QA engineers are forced to execute tests in a rush, increasing the risk of shipping critical bugs or missing performance benchmarks under tight release deadlines. |

---

## 14. QA Engineer Responsibilities in Agile Ceremonies

In Agile frameworks (Scrum/Kanban), QA is integrated continuously from day one across all four core Agile ceremonies:

| Agile Ceremony | QA Engineer Role & Responsibilities |
| --- | --- |
| **1. Sprint Planning** | - Reviews user stories and ensures they satisfy the *Definition of Ready (DoR)*.<br>- Collaborates with developers and product owners to write clear, testable **Acceptance Criteria**.<br>- Estimates testing story points and identifies required test environments, mock data, and automation tasks. |
| **2. Daily Standup** | - Provides quick status updates on test execution and test automation progress.<br>- Identifies and raises **blocking issues** (e.g., test environment downtime, unmerged code PRs, missing test data).<br>- Coordinates with developers for immediate retesting of fixed bugs. |
| **3. Sprint Review (Demo)** | - Demonstrates verified features and passes acceptance tests to product owners and stakeholders.<br>- Confirms that completed user stories meet the agreed-upon **Definition of Done (DoD)**.<br>- Presents automated test execution reports and quality metrics. |
| **4. Sprint Retrospective** | - Discusses what went well and what quality challenges occurred during the sprint.<br>- Identifies process bottlenecks (e.g., late PR merges or insufficient unit test coverage).<br>- Proposes concrete **process improvements** (e.g., introducing static code analysis tools or automated smoke tests in CI/CD). |

---

## 15. Concrete Shift-Left Practices Applied to Course Management API

*Shift-Left Testing* involves executing testing activities earlier in the SDLC to prevent defects rather than relying solely on post-build detection.

```
Traditional Testing:    [ Requirements ] -> [ Architecture ] -> [ Coding ] -> [ TESTING ]
Shift-Left Testing:     [ Req / TEST ]  -> [ Arch / TEST ]  -> [ Code / TEST ] -> [ Validate ]
```

### (a) Reviewing Requirements for Testability
* **Application to API:** QA evaluates user story requirements prior to sprint commitment. For example, when reviewing the requirement for `POST /api/courses/`, QA asks: *"What is the maximum allowed character length for course_name? What HTTP status code should be returned if department does not exist?"* Clarifying these edge cases eliminates ambiguities before code is written.

### (b) Writing Test Cases Before Code (TDD / BDD)
* **Application to API:** QA and developers write executable acceptance test scenarios in Behavior Driven Development (BDD) Gherkin format (`Given-When-Then`) or write `pytest` unit test specifications *before* the backend endpoints are coded. Developers then write code specifically to pass these predefined tests.

### (c) Static Code Analysis
* **Application to API:** Integrating automated static analysis linters (e.g., `flake8`, `black`, `pylint`, `SonarQube`, `bandit`) into developer pre-commit hooks and GitHub Actions PR workflows. This detects code smells, unused variables, formatting issues, and security vulnerabilities (e.g., SQL injection risks or hardcoded secrets) automatically during code commits.

### (d) API Contract Testing Before Integration
* **Application to API:** Defining and freezing the OpenAPI / Swagger specification (`openapi.yaml`) early. QA uses mock servers (e.g., `Prism` or `Postman Mock Server`) to validate frontend and API consumer request/response contracts before backend business logic and database integration are finished.

---

## 16. User Story Acceptance Criteria (Given-When-Then / Gherkin Format)

**User Story:** *"As a college admin, I want to create a new course, so that students can enroll in it."*

```gherkin
Feature: Course Creation Management

  # Scenario 1: Happy Path (Successful Course Creation)
  Scenario: Successfully create a new course with valid details
    Given the Course Management API service is active and running
    And I am logged in as an authorized "College Admin" user
    When I submit a POST request to "/api/courses/" with the following valid course details:
      | field       | value                     |
      | course_name | Database Management System|
      | course_code | CS201                     |
      | credits     | 4                         |
      | department  | Computer Science          |
    Then the API response status code should be 201 Created
    And the response payload should contain an auto-generated "id"
    And the response body should match the submitted course details
    And a new record for course code "CS201" should exist in the database catalog

  # Scenario 2: Duplicate Course Code Rejection
  Scenario: Reject course creation when course code already exists
    Given a course with course_code "CS201" already exists in the system database
    And I am logged in as an authorized "College Admin" user
    When I submit a POST request to "/api/courses/" with course_code "CS201":
      | field       | value                     |
      | course_name | Advanced Database Systems |
      | course_code | CS201                     |
      | credits     | 3                         |
      | department  | Computer Science          |
    Then the API response status code should be 409 Conflict
    And the response error message should state "Course code CS201 already exists."
    And no duplicate record should be inserted into the database

  # Scenario 3: Validation Failure for Missing Required Fields
  Scenario: Fail course creation when mandatory field course_name is missing
    Given I am logged in as an authorized "College Admin" user
    When I submit a POST request to "/api/courses/" missing the mandatory field "course_name":
      | field       | value            |
      | course_code | CS205            |
      | credits     | 3                |
      | department  | Computer Science |
    Then the API response status code should be 400 Bad Request
    And the response body should contain a field validation error for "course_name"
    And the course should not be created in the system
```
