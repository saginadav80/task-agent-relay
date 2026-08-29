# Security Policy

TaskAgentRelay can execute actions on a local machine. Security reports therefore receive a different treatment from ordinary bugs and feature requests.

## Do not disclose vulnerabilities publicly

Please do **not** open a public GitHub issue with exploit details, credentials, secrets, filesystem escape techniques, command-injection payloads, or other sensitive information.

Use GitHub's private vulnerability reporting / Security Advisory mechanism when it is available for this repository. If private reporting is not available, contact the maintainer privately through GitHub before publishing technical details.

## What to report privately

Examples include:

- bypassing workspace restrictions;
- executing commands outside an intended capability boundary;
- bypassing an approval requirement;
- credential or secret exposure;
- remote execution that was not explicitly authorized;
- authentication or authorization bypasses;
- unsafe deserialization or task injection that can cause unintended execution.

## After a report

The maintainer will investigate, determine severity and affected versions, prepare a fix where appropriate, and coordinate disclosure.

Please include enough information to reproduce the issue privately, but avoid sharing real credentials or personal data.

## Supported versions

During early development, the latest development release is the primary supported version. Security fixes may be backported when practical.
