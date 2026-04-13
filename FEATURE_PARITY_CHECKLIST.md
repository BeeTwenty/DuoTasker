# DuoTasker Feature Parity Checklist

Use this checklist during the remake to ensure every current behavior is preserved, then improved.

## Usage
- Mark [ ] as not done, [x] as complete.
- Fill Status as PASS, FAIL, or PARTIAL.
- Add evidence links to PRs, tests, and screenshots.

## 1) Auth and Access

| ID | Area | Current behavior to preserve | Acceptance criteria in new app | Status | Evidence |
|---|---|---|---|---|---|
| AUTH-01 | Register | User can register via register view | Valid user can create account and is redirected to login/success page | [ ] | |
| AUTH-02 | Login | User can log in via login page | Valid credentials create session and redirect to task list | [ ] | |
| AUTH-03 | Logout | User can log out via logout route | Session is terminated and user lands on configured post-logout page | [ ] | |
| AUTH-04 | Access control | Main task routes require login | Anonymous users are redirected to login for protected routes | [ ] | |

Reference routes: [base/urls.py](base/urls.py#L12), [base/urls.py](base/urls.py#L13), [base/urls.py](base/urls.py#L14), [base/views.py](base/views.py#L35)

## 2) Task Lifecycle

| ID | Area | Current behavior to preserve | Acceptance criteria in new app | Status | Evidence |
|---|---|---|---|---|---|
| TASK-01 | List tasks | Home page lists tasks grouped by category and uncategorized section | Task list renders grouped categories and uncategorized tasks consistently | [ ] | |
| TASK-02 | Create task | POST create task with title and optional category | New task persists and appears without full reload in active clients | [ ] | |
| TASK-03 | Complete task | Mark task completed from list action | Task state changes to completed and UI updates accordingly | [ ] | |
| TASK-04 | Undo complete | Undo completed state from list action | Task returns to active state and UI updates accordingly | [ ] | |
| TASK-05 | Delete task | Delete task action removes task | Task is removed from persistence and disappears in UI | [ ] | |
| TASK-06 | Auto delete window behavior | Current UI uses countdown before delete | New app implements deterministic undo/delete window behavior with tests | [ ] | |

Reference routes: [base/urls.py](base/urls.py#L7), [base/urls.py](base/urls.py#L8), [base/urls.py](base/urls.py#L9), [base/urls.py](base/urls.py#L10), [base/urls.py](base/urls.py#L11)
Reference logic: [base/views.py](base/views.py#L57), [base/views.py](base/views.py#L90), [base/views.py](base/views.py#L100), [base/views.py](base/views.py#L109)

## 3) Categories and Uncategorized Flow

| ID | Area | Current behavior to preserve | Acceptance criteria in new app | Status | Evidence |
|---|---|---|---|---|---|
| CAT-01 | Category model | Category has name, icon, is_important, is_uncategorized, keywords | All fields exist with clear validation and migration compatibility | [ ] | |
| CAT-02 | Ordering | Categories are ordered with important first then name | Category ordering is deterministic and tested | [ ] | |
| CAT-03 | Auto-category | Task creation attempts keyword-based category match | Matching strategy is configurable and covered by tests | [ ] | |
| CAT-04 | Uncategorized page | Dedicated uncategorized page lists tasks needing category | Page/API lists uncategorized tasks accurately | [ ] | |
| CAT-05 | Assign category to uncategorized | User can assign category to task from uncategorized flow | Assignment updates task and optional keyword learning behavior | [ ] | |
| CAT-06 | Uncategorized display in list | Main page can show uncategorized bucket using template tag | Uncategorized section/bucket is visible when tasks exist | [ ] | |

Reference model: [base/models.py](base/models.py#L5), [base/models.py](base/models.py#L20)
Reference routes: [base/urls.py](base/urls.py#L15), [base/urls.py](base/urls.py#L16)
Reference logic: [base/views.py](base/views.py#L118), [base/views.py](base/views.py#L154), [base/templatetags/category_tags.py](base/templatetags/category_tags.py#L7)

## 4) Realtime Sync (WebSockets)

| ID | Area | Current behavior to preserve | Acceptance criteria in new app | Status | Evidence |
|---|---|---|---|---|---|
| RT-01 | Websocket endpoint | Clients connect to /ws/tasks/ | Connection succeeds for authenticated users in supported deployment mode | [ ] | |
| RT-02 | Broadcast create | Create action broadcasts realtime event | Other connected clients receive create event and update UI | [ ] | |
| RT-03 | Broadcast complete | Complete action broadcasts realtime event | Other connected clients receive complete event and update UI | [ ] | |
| RT-04 | Broadcast undo | Undo action broadcasts realtime event | Other connected clients receive undo event and update UI | [ ] | |
| RT-05 | Broadcast delete | Delete action broadcasts realtime event | Other connected clients receive delete event and update UI | [ ] | |
| RT-06 | Event contract | Payload includes task_id, action, title | Event schema is documented, versioned, and tested | [ ] | |

Reference routing: [base/routing.py](base/routing.py#L7)
Reference consumer: [base/consumers.py](base/consumers.py#L5)
Reference frontend handlers: [base/templates/list.html](base/templates/list.html#L145), [base/templates/list.html](base/templates/list.html#L168), [base/templates/list.html](base/templates/list.html#L175), [base/templates/list.html](base/templates/list.html#L182)

## 5) PWA and Static Experience

| ID | Area | Current behavior to preserve | Acceptance criteria in new app | Status | Evidence |
|---|---|---|---|---|---|
| PWA-01 | Manifest | App serves web manifest | Manifest is valid and install prompt works on supported browsers | [ ] | |
| PWA-02 | Service worker registration | Base template registers service worker | Service worker installs/updates without breaking navigation | [ ] | |
| PWA-03 | Offline cache baseline | Static cache strategy exists | New cache strategy supports offline baseline and safe invalidation | [ ] | |

Reference templates/assets: [base/templates/base.html](base/templates/base.html#L10), [base/templates/base.html](base/templates/base.html#L15), [static/js/serviceworker.js](static/js/serviceworker.js#L1), [static/manifest.json](static/manifest.json)

## 6) Admin and Operations

| ID | Area | Current behavior to preserve | Acceptance criteria in new app | Status | Evidence |
|---|---|---|---|---|---|
| OPS-01 | Admin models | Category and Task are manageable in Django admin | Admin can create/edit/filter/search categories and tasks | [ ] | |
| OPS-02 | Auto superuser init | Startup command can create initial superuser from env | Command is idempotent and works in container startup | [ ] | |
| OPS-03 | Containerized deployment | App runs with app + nginx + postgres + redis | Compose stack boots and health checks pass | [ ] | |
| OPS-04 | ASGI websocket serving | ASGI app supports HTTP and websocket protocols | HTTP + WS both pass smoke tests behind proxy | [ ] | |

Reference admin: [base/admin.py](base/admin.py#L4), [base/admin.py](base/admin.py#L11)
Reference command: [base/management/commands/createinitialsuperuser.py](base/management/commands/createinitialsuperuser.py#L5)
Reference runtime: [DuoTasker/asgi.py](DuoTasker/asgi.py#L10), [docker-compose.yml](docker-compose.yml), [nginx.conf](nginx.conf)

## 7) Data and Migration Compatibility

| ID | Area | Current behavior to preserve | Acceptance criteria in new app | Status | Evidence |
|---|---|---|---|---|---|
| DATA-01 | Existing schema continuity | Existing Task and Category data can be migrated safely | Migration scripts run on a copy of production data with no loss | [ ] | |
| DATA-02 | Removed field handling | Legacy completed_at appears in migration history | Migration plan addresses historical field changes explicitly | [ ] | |
| DATA-03 | Null category semantics | Tasks may have null category (uncategorized) | New schema preserves uncategorized semantics | [ ] | |

Reference migrations: [base/migrations/0009_task_completed_at.py](base/migrations/0009_task_completed_at.py), [base/migrations/0010_remove_task_completed_at.py](base/migrations/0010_remove_task_completed_at.py)

## 8) Test Coverage Gate For Remake

| ID | Area | Required coverage in new app | Acceptance criteria | Status | Evidence |
|---|---|---|---|---|---|
| TEST-01 | Unit tests | Models and services for tasks/categories/users | Key domain logic has deterministic unit tests | [ ] | |
| TEST-02 | Integration tests | HTTP route behavior and auth restrictions | Critical routes pass integration suite | [ ] | |
| TEST-03 | Realtime tests | Websocket connect + event delivery | Event contract and delivery are tested end-to-end | [ ] | |
| TEST-04 | E2E flow | Create, complete, undo, delete, categorize | Core user journeys pass in CI | [ ] | |

Reference existing tests baseline: [base/tests.py](base/tests.py)

## 9) Known Legacy Quirks To Resolve During Parity

These must be intentionally addressed (not silently dropped):
- register template exists but is currently empty: [base/templates/register.html](base/templates/register.html)
- frontend calls get_tasks endpoint that does not exist in routes: [base/templates/list.html](base/templates/list.html#L302), [base/urls.py](base/urls.py)
- completed_at is referenced in view logic though removed by migration: [base/views.py](base/views.py#L94), [base/migrations/0010_remove_task_completed_at.py](base/migrations/0010_remove_task_completed_at.py)
- uncategorized flow uses task.name in one path though model uses title: [base/views.py](base/views.py#L136), [base/models.py](base/models.py#L21)

## 10) Sign-off

- Product sign-off: [ ]
- Engineering sign-off: [ ]
- QA sign-off: [ ]
- Performance baseline captured: [ ]
- Security review complete: [ ]
