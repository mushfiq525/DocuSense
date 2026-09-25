# Backups of GitLab.com

This policy specifies requirements for backups of GitLab.com

##### Tags:

* [Security\_policy](https://handbook.gitlab.com/tags/security_policy/)
* [Security\_policy\_caplscsi](https://handbook.gitlab.com/tags/security_policy_caplscsi/)

#### This is a Controlled Document

In line with GitLab’s regulatory obligations, changes to [controlled documents](https://handbook.gitlab.com/handbook/security/controlled-document-procedure/) must be approved or merged by a code owner. All contributions are welcome and encouraged.

 Visibility: Audit 

## Purpose

This policy outlines how GitLab performs, monitors, and validates backups and restorations of GitLab.com.
These procedures are critical for ensuring data recovery and disaster recovery for customer data.

## Scope

GitLab.com’s backup strategy includes both monitoring and restore validation.

Customer data is stored in the following locations:

1. All PostgreSQL databases for GitLab.com
2. Object storage for GitLab.com, including packages, LFS, uploads, and CI data
3. The CustomersDot database, which manages subscriptions and purchases
4. Git repositories

## Not in Scope

1. Customer Data stored in the Redis cache
   1. Data queued for processing
   2. Sessions and other cached data

## Roles & Responsibilities

| Role | Responsibility |
| --- | --- |
| GitLab Team Members | Ensure adherence to the requirements outlined in this policy |
| Engineering (Code Owners) | Approve significant changes and exceptions to this policy |

## Procedure

GitLab defines:

* The services requiring backups
* The frequency of backups, data retention periods, and restoration processes
* The procedures for data restoration for Disaster Recovery scenarios

### Backup and Restore

#### PostgreSQL Databases

| Area | Details |
| --- | --- |
| Backup frequency | A full backup is taken every hour, with continuous transaction log archival. |
| Storage | Stored in [GCS](https://cloud.google.com/storage) |
| Encryption | Backup data is encrypted in transit and at rest |
| Retention | 14 days (7 days for CustomersDot database) |
| Loss prevention | [Soft Delete](https://cloud.google.com/storage/docs/soft-delete) enabled, with 7 day retention |
| Location/redundancy | [Multi-region geo redundancy](https://cloud.google.com/storage/docs/availability-durability) |
| Monitoring | All databases are continuously monitored to ensure successful backups, with alerts triggered for missing backups. |
| Restore validation | Regular restoration from disk snapshots and replaying WAL segments |

#### Git Repositories

| Area | Details |
| --- | --- |
| Backup frequency | Repositories are backed up hourly using block-level disk snapshots. |
| Storage | Stored as GCP [Standard snapshots](https://cloud.google.com/compute/docs/disks/snapshots) |
| Encryption | Snapshots are encrypted at rest |
| Retention | 14 days |
| Loss prevention | Retained after source disk deletion |
| Location/redundancy | [Multi-region geo redundancy](https://cloud.google.com/storage/docs/availability-durability) |
| Monitoring | All disks are monitored, with alerts triggered for missing snapshots |
| Restore validation | Conducted by randomly sampling disks and restoring recent snapshots. |

#### Object Storage

Data stored in Object Storage (GCS) benefits from Google’s [99.999999999% annual durability](https://cloud.google.com/storage/docs/storage-classes#descriptions) and multi-region bucket redundancy. To enhance data protection, [Object Versioning](https://cloud.google.com/storage/docs/object-versioning) and [Soft Delete](https://cloud.google.com/storage/docs/soft-delete) are enabled.

Automated restore validation is not required for Object Storage due to its inherent protections through versioning and soft delete.

## Exceptions

Exceptions to this policy will be managed in accordance with the [Information Security Policy Exception Management Process](https://handbook.gitlab.com/handbook/security/controlled-document-procedure/#exceptions).

## References

* [Records Retention & Disposal](https://handbook.gitlab.com/handbook/security/policies_and_standards/records-retention-deletion/)
* [Disaster Recovery runbooks](https://gitlab.com/gitlab-com/runbooks/-/tree/master/docs/disaster-recovery)
* [GameDays](https://gitlab.com/gitlab-com/runbooks/-/blob/master/docs/disaster-recovery/gameday.md)

Last modified April 22, 2026: [Implement GCS bucket policy changes: 14-day retention in default storage, remove coldline storage (`ccf9b967`)](https://gitlab.com/gitlab-com/content-sites/handbook/commit/ccf9b967)

[View page source](https://gitlab.com/gitlab-com/content-sites/handbook/blob/main/content/handbook/engineering/gitlab-com/policies/backup/_index.md)
-
[Edit this page](https://gitlab.com/-/ide/project/gitlab-com/content-sites/handbook/edit/main/-/content/handbook/engineering/gitlab-com/policies/backup/_index.md)
-
please [contribute](https://handbook.gitlab.com/handbook/about/contributing/).
[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)