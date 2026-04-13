# DuoTasker Remake Plan

## 1) Current App Understanding (Full Inventory)

This is what the current app does today, grouped by area so the remake keeps all behavior.

### Product features in production
- User auth: register, login, logout.
- Task CRUD flow:
	- create task from main page,
	- complete task,
	- undo complete,
	- delete task (with client-side countdown behavior).
- Category system:
	- category metadata (name, icon, important flag, uncategorized flag, keywords),
	- task listing grouped by category,
	- uncategorized task handling page,
	- assign category to uncategorized tasks,
	- keyword-based auto-category while creating tasks.
- Realtime updates through Django Channels + Redis websocket group.
- PWA basics:
	- web manifest,
	- service worker registration and caching.
- Admin support for Category and Task.
- Dockerized deployment behind Nginx, with Postgres and Redis.
- Startup auto superuser creation through management command.

### Backend structure
- Django project package: DuoTasker.
- Main app package: base.
- Data models:
	- Category,
	- Task.
- HTTP endpoints in base.urls + base.views.
- Websocket endpoint /ws/tasks/ with TaskListConsumer.
- Template filter get_uncategorized.
- Minimal model tests and dedicated test settings.

### Frontend structure
- Server-rendered Django templates:
	- base layout,
	- list page,
	- login page,
	- register page (currently empty),
	- uncategorized tasks page.
- Inline page JavaScript for websocket handling and task actions.
- Bulma + Font Awesome integration.

### Ops and delivery
- Dockerfile + entrypoint script.
- docker-compose stack:
	- app,
	- nginx,
	- postgres,
	- redis.
- Helper scripts for Docker image push.

## 2) Observed Gaps To Fix In Remake

These are major quality/performance/workflow issues that the remake should eliminate.

- Domain consistency:
	- view code references removed fields (completed_at),
	- view code references wrong attribute names (task.name vs task.title).
- Separation of concerns:
	- business logic mixed in views and template JS,
	- Celery decorators/schedule declarations are placed incorrectly.
- Reliability:
	- websocket event method names do not align cleanly with sent event types,
	- endpoints expected by frontend are missing (for example get_tasks).
- Security and correctness:
	- DEBUG is not parsed to boolean safely,
	- ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS are single-string patterns,
	- missing input validation and explicit form use for task creation.
- Performance:
	- no database indexing strategy for frequent filters/sorts,
	- client and template loops can trigger extra queries,
	- no caching strategy beyond basic service worker static cache.
- Testing coverage:
	- mostly model tests, little integration/API/websocket coverage.
- Developer workflow:
	- no lint/format/type-check pipeline,
	- no CI quality gates,
	- requirements file encoding inconsistency.

## 3) Target Architecture For New App

### Core principles
- Keep all existing features fully compatible for users.
- Introduce clear boundaries: domain, application services, interfaces.
- Design for predictable performance and easy testing.
- Prefer explicit APIs over implicit template-side behavior.

### Proposed stack
- Backend: Django 5.x + Django REST Framework for API layer.
- Realtime: Channels with explicit event schema.
- Async/background:
	- Celery with dedicated tasks module,
	- Redis broker + result backend if needed.
- Database: PostgreSQL with tuned indexes and constraints.
- Frontend option A (recommended): Django templates + HTMX/Alpine for progressive enhancement.
- Frontend option B: separate SPA only if product scope grows quickly.
- Build/runtime:
	- multi-stage Docker build,
	- Gunicorn/Uvicorn workers,
	- Nginx reverse proxy.

### New codebase layout
- apps/users
- apps/tasks
- apps/categories
- apps/realtime
- apps/core (shared utilities/settings)
- apps/pwa
- tests/unit
- tests/integration
- tests/e2e
- config/settings/base.py, local.py, prod.py, test.py

## 4) Feature Parity + Improvements Matrix

### Auth
- Keep: register/login/logout.
- Improve:
	- complete register template and validation UX,
	- optional email verification/reset flows,
	- stronger session/security defaults.

### Task lifecycle
- Keep: create, complete, undo, delete.
- Improve:
	- transactional service methods,
	- soft-delete or audit trail option,
	- undo window implemented server-side with durable scheduling,
	- idempotent endpoints.

### Categories and auto-categorization
- Keep: importance ordering, uncategorized bucket, keyword auto-match.
- Improve:
	- normalization and deduplication of keywords,
	- configurable matching (exact, contains, regex-safe option),
	- category reassignment history,
	- bulk categorization actions.

### Realtime sync
- Keep: live updates across users.
- Improve:
	- single canonical event contract,
	- reconnect/backoff strategy,
	- optimistic UI with conflict handling,
	- integration tests for websocket events.

### PWA
- Keep: installable manifest + offline cache behavior.
- Improve:
	- cache versioning policy,
	- stale-while-revalidate strategy,
	- explicit offline fallback page,
	- lighthouse performance/accessibility targets.

### Admin
- Keep: manage categories and tasks.
- Improve:
	- admin actions for bulk updates,
	- richer filters/search,
	- readonly audit fields.

## 5) Performance Plan

- Data layer:
	- add indexes on Task.completed, Task.category_id, Category.is_important, Category.is_uncategorized,
	- enforce constraints and nullability consistency,
	- prefetch/select_related where appropriate.
- App layer:
	- move filtering/sorting into optimized query services,
	- reduce template-side heavy logic,
	- add caching for mostly-static category lists.
- Realtime:
	- compact websocket payloads,
	- event throttling/debouncing where useful,
	- monitor channel layer latency.
- Frontend:
	- split/minify static assets,
	- avoid duplicated inline scripts,
	- optimize initial render path.

## 6) Better Workflow Plan

### Developer experience
- Standardize tooling:
	- ruff + black + isort,
	- mypy (or pyright) for type checks,
	- pre-commit hooks.
- Provide Makefile/Taskfile commands for common flows.
- Use .env.example with validated settings loader.

### CI/CD
- GitHub Actions pipeline:
	- lint,
	- type-check,
	- unit/integration tests,
	- security scan (pip-audit/bandit),
	- Docker build validation.
- Optional preview environments per PR.

### Observability
- Structured logs in JSON.
- Error tracking (Sentry or equivalent).
- Health/readiness endpoints.
- Baseline metrics dashboard (request latency, error rates, websocket events).

## 7) Implementation Roadmap

### Phase 0 - Discovery and freeze (1 week)
- Confirm feature parity acceptance checklist.
- Define domain language and event contracts.
- Freeze current bug list and migration strategy.

### Phase 1 - New foundation (1-2 weeks)
- Create new settings split and app boundaries.
- Implement users/tasks/categories models and services.
- Add test harness and linters in CI.

### Phase 2 - Feature parity core (2-3 weeks)
- Implement auth, task lifecycle, category workflows.
- Implement uncategorized reassignment flow.
- Build parity templates/UI or API + UI layer.

### Phase 3 - Realtime + async correctness (1-2 weeks)
- Implement websocket event bus and contract tests.
- Move delete countdown/cleanup to robust async jobs.
- Add reconnect logic and race-condition handling.

### Phase 4 - PWA + performance hardening (1 week)
- Replace service worker strategy with versioned caching.
- Add query optimizations, caching, and load tests.
- Validate lighthouse and responsiveness targets.

### Phase 5 - Cutover and cleanup (1 week)
- Data migration and backfill scripts.
- Blue/green or staged rollout.
- Post-cutover bug bash and documentation updates.

## 8) Definition of Done For Remake

- 100% of existing user-facing features available and verified.
- No known regressions in auth, tasks, categories, realtime, and PWA installability.
- Automated test coverage includes:
	- unit tests for services/models,
	- integration tests for endpoints,
	- websocket integration tests,
	- key e2e UI paths.
- CI pipeline is green on all gates.
- Measurable performance improvement targets met:
	- lower p95 request latency,
	- lower query count on main list page,
	- faster first contentful paint.

## 9) Immediate Next Actions

1. Use the formal feature parity checklist in FEATURE_PARITY_CHECKLIST.md as the gate for all remake milestones.
2. Choose frontend direction (template-enhanced vs SPA) before coding.
3. Scaffold the new modular Django project and CI pipeline first.
4. Re-implement task/category flows through service layer and tests before UI polish.
