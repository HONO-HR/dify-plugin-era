# Privacy Policy: ERA by HONO plugin for Dify

## What the plugin does with data

The plugin sends each tool request to the ERA MCP endpoint that you enter in its settings. That endpoint is part of your organisation's HONO HRMS, on a `hono.ai` or `honohr.com` domain. The plugin returns ERA's answer to your Dify app.

- **Sent to ERA:** the tool name and the arguments that your Dify app or agent fills in (for example a date range or a search term), plus your ERA MCP API key for authentication.
- **Returned from ERA:** the HR data that your ERA account is allowed to see, such as your leave balance, attendance, team details or company policies.
- **Stored by the plugin:** nothing. The plugin keeps no data of its own and writes no logs. Dify stores your MCP URL and encrypted API key as provider credentials in your workspace.
- **Third parties:** the plugin talks only to HONO. It contacts no other service.

All tools in this plugin are read-only. It cannot apply, approve, cancel or change anything in HONO.

## Where data goes after that

- HONO processes requests under your organisation's agreement with HONO and HONO's privacy policy: https://hono.ai/privacy-policy
- What Dify and your chosen language model do with tool results is covered by Dify's policy and your model provider's policy, not by this plugin.

## Your controls

- Use a **read-only** ERA MCP key.
- Revoke the key at any time in ERA under Profile > MCP keys. The plugin stops working at once.
- Your HONO administrator can turn off MCP access for the whole workspace.

## Contact

connect@hono.ai
