# Monitoring of GitLab.com

This policy specifies requirements for monitoring of GitLab.com

##### Tags:

* [Security\_policy](https://handbook.gitlab.com/tags/security_policy/)
* [Security\_policy\_caplscsi](https://handbook.gitlab.com/tags/security_policy_caplscsi/)

#### This is a Controlled Document

In line with GitLab’s regulatory obligations, changes to [controlled documents](https://handbook.gitlab.com/handbook/security/controlled-document-procedure/) must be approved or merged by a code owner. All contributions are welcome and encouraged.

 Visibility: Audit 

## Purpose

This policy specifies how GitLab ensures continuous monitoring of GitLab.com services, logging and capacity planning are defined.

GitLab implements these measures to ensure compliance with various policies and agreements within the cloud environment, and to ensure that any potential security issues are quickly identified.

## Scope

This policy applies to all GitLab.com monitoring services in support of the statutory, regulatory and contractual requirements of GitLab.

## Roles & Responsibilities

| Role | Responsibility |
| --- | --- |
| GitLab Team Members | Responsible for following the requirements in this procedure |
| Engineering, Security | Responsible for implementing and executing this procedure |
| Engineering (Code Owners) | Responsible for approving significant changes and exceptions to this procedure |

## Procedure

* GitLab defines how Availability is calculated in the [Service Level Agreement](https://handbook.gitlab.com/handbook/engineering/infrastructure-platforms/service-level-agreement/)
* GitLab defines how logs are collected, and analyzed
* GitLab defines capacity management procedures

### Log management

GitLab.com services emit network, system, and application logs, which are then stored, processed, and searched to provide a basis for incident and security incident investigations.

Logs are stored in a short-term and long-term storage, with their own respective retention policies:

* short-term storage: 30 days
* long-term storage: 365 days

Logs in short-term storage are used to actively monitor application activity, spam events, transient errors, system and network authentication
events, security events, and similar.

Logs in long-term storage are used to comply to the [Records Retention & Disposal](https://handbook.gitlab.com/handbook/security/policies_and_standards/records-retention-deletion/) policy. Logs in long-term storage are less granular and have less detail than those in short-term storage.

Detailed overview of architecture, tooling and workflows are listed on the [Logging](https://gitlab.com/gitlab-com/runbooks/-/blob/master/docs/logging/README.md) page.

### Capacity Planning

In order to scale GitLab.com infrastructure at the right time and to prevent incidents, GitLab employs a capacity planning process.

The focus of the capacity planning process is to perform historical data analysis to predict future growth.
From this analysis, GitLab leverages a process that provides information around saturation points, which are then delivered to service owners.
Service owners then use this process to act on this information.

The data sources used to feed the forecasting tool are historical saturation and utilization data used as part of standard monitoring of GitLab.com.

The output of our capacity planning process is considered ORANGE, and must be treated per [The Data Classification Standard](https://handbook.gitlab.com/handbook/security/policies_and_standards/data-classification-standard/#orange).

Detailed overview of architecture, tooling and workflows are listed on the [Capacity Planning](https://handbook.gitlab.com/handbook/engineering/infrastructure-platforms/capacity-planning/) page.

## Exceptions

Changes and exceptions to this policy must be approved by the appropriate Infrastructure team responsible for monitoring GitLab.com.

## References

* [Records Retention & Disposal](https://handbook.gitlab.com/handbook/security/policies_and_standards/records-retention-deletion/)

Last modified November 20, 2025: [Apply 1 suggestion(s) to 1 file(s) (`7a9fcc53`)](https://gitlab.com/gitlab-com/content-sites/handbook/commit/7a9fcc53)

[View page source](https://gitlab.com/gitlab-com/content-sites/handbook/blob/main/content/handbook/engineering/gitlab-com/policies/monitoring/_index.md)
-
[Edit this page](https://gitlab.com/-/ide/project/gitlab-com/content-sites/handbook/edit/main/-/content/handbook/engineering/gitlab-com/policies/monitoring/_index.md)
-
please [contribute](https://handbook.gitlab.com/handbook/about/contributing/).
[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)