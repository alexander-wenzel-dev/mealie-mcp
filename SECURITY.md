# Security Policy

## Reporting a vulnerability

Please report security issues privately. Use the GitHub "Report a vulnerability"
button under the repository Security tab to open a private advisory. Do not open a
public issue for a suspected vulnerability.

Include what you observed, how to reproduce it, and the impact you expect. You
will get an acknowledgement, and a fix or a decision once the report is assessed.

## Handling your Mealie token

This server talks to a Mealie instance with an API token you provide through
`MEALIE_API_TOKEN`. Treat that token as a secret.

- The token often has broad or admin rights on your Mealie instance. Anyone who
  can reach the running server can act with those rights.
- Keep the token in your MCP client config or environment, never in a committed
  file. `.env` is git-ignored for this reason.
- Do not paste real tokens, hostnames, or full request URLs into issues, pull
  requests, or logs. Use `mealie.example.com` and placeholder values in examples.

The server does not log tokens, passwords, or request bodies that may carry
secrets, and it redacts the `Authorization` header.
