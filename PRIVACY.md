# Privacy Policy: ERA by HONO plugin for Dify

## What the plugin does with data

The plugin sends each tool request to ERA: to HONO's public connector (`mcp.hono.ai`) when you sign in with HONO, or to the ERA MCP URL you enter when you use an API key. Both are part of HONO HRMS, on a `hono.ai` or `honohr.com` domain. The plugin returns ERA's answer to your Dify app.

- **Sent to ERA:** the tool name and the arguments that your Dify app or agent fills in (for example a date range or a search term), plus your HONO sign-in token or ERA MCP API key for authentication. When you sign in with HONO, the plugin also registers a client with HONO for your Dify callback URL.
- **Returned from ERA:** the HR data that your ERA account is allowed to see, such as your leave balance, attendance, team details or company policies, and the result of any action you confirm.
- **Stored by the plugin:** nothing. The plugin keeps no data of its own and writes no logs. Dify stores your HONO sign-in tokens, or your MCP URL and encrypted API key, as provider credentials in your workspace.
- **Third parties:** the plugin talks only to HONO. It contacts no other service.

Some tools act in HONO on your behalf, such as applying or cancelling leave or approving a request. They never act on the first call: ERA first returns a summary and a single-use confirmation token, and the action runs only when the call is repeated with that token. A read-only ERA key blocks all of these tools.

## Where data goes after that

- HONO processes requests under your organisation's agreement with HONO and HONO's privacy policy: https://hono.ai/privacy-policy
- What Dify and your chosen language model do with tool results is covered by Dify's policy and your model provider's policy, not by this plugin.

## Your controls

- Use a **read-only** ERA MCP key if the Dify app only needs to read data.
- Revoke the key at any time in ERA under Profile > MCP keys, or remove the sign-in in Dify. The plugin stops working at once.
- Your HONO administrator can turn off MCP access for the whole workspace.

## Contact

connect@hono.ai
