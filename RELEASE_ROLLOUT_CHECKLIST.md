# Release and Rollout Checklist

## 1. Pre-Release Quality Gate

- [ ] Run static checks and formatting.
- [ ] Run type checks.
- [ ] Run full Django test suite.
- [ ] Run websocket/realtime tests.
- [ ] Verify no editor diagnostics in changed files.

Reference commands:
- Windows: `scripts/dry_run_migration.ps1`
- Linux/macOS: `scripts/dry_run_migration.sh`

## 2. Data and Migration Dry Run

- [ ] Export production database backup.
- [ ] Restore backup to staging.
- [ ] Run `manage.py migrate --plan` and review.
- [ ] Run migrations on staging clone.
- [ ] Validate record counts before/after migration.
- [ ] Validate task/category relationships and uncategorized behavior.

## 3. Deployment Readiness

- [ ] Build and tag Docker image.
- [ ] Validate entrypoint sequence (migrate, collectstatic, superuser command).
- [ ] Validate nginx upstream and websocket proxy paths.
- [ ] Confirm environment variables in deployment target.
- [ ] Confirm Redis and Postgres connectivity.

## 4. Rollout Steps

- [ ] Deploy to staging.
- [ ] Run smoke tests for auth, list, create, complete, undo, delete, uncategorized flow.
- [ ] Validate realtime updates across two browser sessions.
- [ ] Validate PWA install + service worker behavior.
- [ ] Deploy to production with monitored window.

## 5. Post-Deploy Verification

- [ ] Check application logs for errors.
- [ ] Confirm websocket event throughput and error rates.
- [ ] Confirm p95 response latency is within target.
- [ ] Confirm no migration anomalies in data integrity checks.

## 6. Rollback Plan

- [ ] Keep previous container image tag ready.
- [ ] Keep latest production DB backup accessible.
- [ ] Document rollback command sequence.
- [ ] Practice rollback in staging before production cutover.
