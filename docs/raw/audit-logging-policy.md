# GitLab Audit Logging Policy

##### Tags:

* [Security\_policy](https://handbook.gitlab.com/tags/security_policy/)
* [Security\_policy\_au](https://handbook.gitlab.com/tags/security_policy_au/)

#### This is a Controlled Document

In line with GitLab’s regulatory obligations, changes to [controlled documents](https://handbook.gitlab.com/handbook/security/controlled-document-procedure/) must be approved or merged by a code owner. All contributions are welcome and encouraged.

 Visibility: Audit 

## Purpose

To ensure the proper operation and security of GitLab.com, GitLab logs critical information system activity.

## Scope

The audit logging policy applies to all systems within our production environment. The production environment includes all endpoints and cloud assets used in hosting GitLab.com and its subdomains. This may include third-party systems that support the business of GitLab.com.

## Roles & Responsibilities

| Role | Responsibility |
| --- | --- |
| GitLab Team Members | Responsible for following the requirements in this policy |
| Security Team | Responsible for implementing and executing this policy |
| System Owners | Definition of individual audit log criteria; Definition and execution of system audit log procedures |
| Security Management (Code Owners) | Responsible for approving significant changes and exceptions to this policy |

## Policy

* GitLab shall log and monitor critical information system activity.
* Logs must be retained for a defined period of time.
* Logs must not be modified and or deleted.
* Access to audit log data must be limited based on the principle of least privilege.

Inline with GitLab’s Continuous Monitoring Controls
System Owners are responsible for determining what constitutes “critical information system activity” in their respective system based on their experience and professional judgement

Such activity is then documented either in the handbook or a runbook, whichever is found to be appropriate.

Audit logging process must be created and implemented by the department(s) or team(s) responsible for a given system.

## Exceptions

Exceptions to this policy will be tracked as per the [Information Security Policy Exception Management Process](https://handbook.gitlab.com/handbook/security/controlled-document-procedure/#exceptions).

## References

* [What is considered production](https://gitlab.com/gitlab-com/gl-security/security-assurance/team-commercial-compliance/compliance/-/blob/master/production_definition.md)
* [Production Architecture](https://handbook.gitlab.com/handbook/engineering/infrastructure-platforms/production/architecture/)

Last modified July 26, 2026: [Update broken link and remove empty Configuration Management bullet in audit-logging-policy (`eca9c220`)](https://gitlab.com/gitlab-com/content-sites/handbook/commit/eca9c220)

[View page source](https://gitlab.com/gitlab-com/content-sites/handbook/blob/main/content/handbook/security/security-and-technology-policies/audit-logging-policy.md)
-
[Edit this page](https://gitlab.com/-/ide/project/gitlab-com/content-sites/handbook/edit/main/-/content/handbook/security/security-and-technology-policies/audit-logging-policy.md)
-
please [contribute](https://handbook.gitlab.com/handbook/about/contributing/).
[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)