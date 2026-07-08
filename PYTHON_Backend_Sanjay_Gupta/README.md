# Course Management Microservices Architecture

This project decomposes the original monolithic Course Management API into a modular microservices architecture.

## Bounded Contexts

Below is the list of identified bounded contexts and service boundaries:

| Service Name | Responsibility | Endpoints It Owns | Database It Owns |
| :--- | :--- | :--- | :--- |
| **Auth Service** | Handles user registration, authentication, password hashing, and JWT token issuing. | `POST /api/v1/auth/register/`<br>`POST /api/v1/auth/login/` | `auth.db` |
| **Course Service** | Manages courses, departments, and credits. | `GET /api/courses/`<br>`POST /api/courses/`<br>`GET /api/courses/<id>/`<br>`PUT /api/courses/<id>/`<br>`DELETE /api/courses/<id>/` | `courses.db` |
| **Student Service** | Manages student profiles and handles course enrollments. | `GET /api/students/`<br>`POST /api/students/`<br>`GET /api/students/<id>/`<br>`PUT /api/students/<id>/`<br>`DELETE /api/students/<id>/`<br>`POST /api/students/<id>/enroll` | `students.db` |
| **Notification Service**| Simulates background tasks like sending confirmation emails after enrollment. | Triggered internally or via events. | No persistent database (or simple `notifications.db`) |

---

## Inter-Service Communication Trade-offs

Microservices must communicate with each other. There are two primary paradigms:

### 1. Synchronous Communication (e.g., HTTP/REST, gRPC)
- **Concept**: A service calls another service and waits for a response (blocking call). In our task, the **Student Service** calls the **Course Service** via HTTP (`GET /api/courses/{id}/`) to verify a course exists before performing enrollment.
- **Pros**:
  - **Simplicity**: Easy to implement, verify, and reason about.
  - **Immediate Response**: The client gets instant confirmation of data validity (e.g., "This course does not exist").
  - **No Eventual Consistency Delay**: Data is checked and written atomically from the caller's viewpoint.
- **Cons**:
  - **Tight Runtime Coupling**: If the Course Service is offline or slow, the Student Service's enrollment endpoint fails or times out.
  - **Cascading Failures**: A failure in one downstream service can cascade back up to the user.
  - **Performance Overhead**: Cumulative latency of chained HTTP requests.

### 2. Asynchronous Communication (e.g., Message Queues like RabbitMQ, Apache Kafka, AWS SQS)
- **Concept**: A service publishes an event (message) to a broker and immediately returns. Downstream services subscribe to these messages and process them at their own pace.
- **Pros**:
  - **Temporal Decoupling**: If the Notification Service is down, the Student Service can still enroll the student. The message stays in the queue until the service is healthy again.
  - **High Fault Tolerance**: No single point of failure; failures are buffered.
  - **Scalability**: Message consumers can be scaled up or down easily.
  - **Performance**: High throughput as the publisher doesn't block.
- **Cons**:
  - **Complexity**: Requires broker setup, management, and code to handle message retry, dead-letter queues, and idempotency.
  - **Eventual Consistency**: Data states might not sync instantly across all databases.
  - **Harder Debugging**: Tracing request flows through multiple asynchronous queues is more difficult than single call stacks.

---

### When to Use a Message Queue (RabbitMQ / Kafka)
1. **Long-Running / Non-Critical Work**: Tasks like sending emails, processing images/PDFs, generation of reports, or heavy audit logging should always be asynchronous.
2. **High Throughput Data Ingestion**: Gathering telemetry, tracking user clicks, or processing IoT data streams (Kafka is great for this).
3. **Decoupled Workflows**: Whenever immediate consistency is not required, and you want to ensure the caller remains active even if downstream processors are temporarily offline.
