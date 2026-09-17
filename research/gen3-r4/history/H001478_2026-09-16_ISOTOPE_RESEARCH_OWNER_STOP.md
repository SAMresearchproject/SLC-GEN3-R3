---
entry_id: H001478
entry_date: 2026-09-16
entry_type: AUTHORITY_CHANGE
status: IMMUTABLE_HISTORY
supersedes: H001477
affects_live:
  - SAM_LIVE/05_ATOM3D_CURRENT.md
  - SAM_LIVE/11_STORAGE_CURRENT.md
---

# Owner stops the isotope interaction research loop

Sean directs "shut it down" after clarifying that the implemented interaction
analysis loop did not implement the desired isotope construction expansion.
The project STOP marker is set. sam-isotope-research.service and
sam-isotope-reports.timer are disabled and inactive; reporting and failure-notice
services are inactive with MainPID0. The exact project binary has no remaining
workers on lilhelper, recorded in HELPER_STOP.json. Results, queue, native models,
failures, source and checkpoints remain preserved. No deletion is performed.

SAM_REVIEW/campaigns/GEN3_ISOTOPE_RESEARCH1/STATUS.json is STOPPED_BY_OWNER.
EMAIL_POLICY.json remains unapproved and reporting is DISABLED_BY_OWNER;
no isotope emails were sent. The project-specific automatic cleanup is inactive.
No restart or replacement campaign is authorized by this stop. Other projects
and the installed SLC/CE runtime remain unchanged.
