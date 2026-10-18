# Control UI screenshot provenance

These six PNGs were copied from existing Playwright/UX validation artifacts in the Control source snapshot at `f7ae7b35d602a5e2cae141297ecdda8154f47172` on dev-drcontrol. They are **existing test captures**, not a fresh authenticated end-to-end walkthrough, and do not prove live delivery. They are not generated mockups. The original captures predate this documentation update and may depict historical UI states.

| File | Existing capture source |
| --- | --- |
| wizard-connect.png | `frontend/validation-output/wizard-v3-manual/01-empty-default.png` |
| wizard-sample-confirmation.png | `frontend/validation-output/wizard-v3-manual/05-after-confirmation.png` |
| wizard-deploy.png | `frontend/validation-output/wizard-v3-manual/09-stream-created.png` |
| route-protection.png | `frontend/validation-output/wizard-v3-manual/10-data-protection-persisted.png` |
| transform-add-field.png | `frontend/transform-add-field-menu-screenshot.png` |
| dashboard-overview.png | `frontend/dashboard-monitoring-screenshot.png` |

No login screen is included. Do not use these images to assert successful connection, vendor credentials, policy application or delivered events. Refresh captures from an authenticated non-production Control session before declaring full screenshot coverage.

## Additional historical captures (2026-10-19 docs update)

The PNG files named `01-*` through `10-*`, `05-before-confirmation.png`, and `transform-step-screenshot.png` were copied without fabrication from Control's `frontend/validation-output/wizard-v3-manual/`, `frontend/validation-output/wizard-v3-ux-simplify/after/`, and `frontend/transform-step-screenshot.png` in the same source snapshot. They represent historical Playwright/UX test states including **failure and blocked deploy**; none should be interpreted as successful real-world delivery. The exact original basename is preserved for traceability. No login image was added.
