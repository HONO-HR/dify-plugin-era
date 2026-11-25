# ERA by HONO

Use your HONO HRMS data in Dify apps, workflows and agents. ERA is the AI layer of [HONO](https://hono.ai) HRMS. This plugin gives Dify 73 **read-only** HR tools through your organisation's ERA workspace, covering:

- **Leave:** balance, history, policy, expiring leave, encashment
- **Attendance:** calendar, punch log, missing punches, overtime, shift roster
- **Pay:** payroll summary, salary difference, loans, reimbursements, travel expenses
- **People and team:** profile, directory search, team attendance, team leave calendar, team pulse
- **Performance and learning:** goal sheet, reviews, 360 feedback, PMS cycle, courses, training needs
- **Hiring:** open positions, referrals, recruitment pipeline, offer status
- **Self-service:** letters, policies, knowledge base, support tickets, pending approvals

Every answer respects your HONO permissions: you see exactly what you would see in HONO. The plugin cannot apply, approve, cancel or change anything.

## Requirements

- A HONO HRMS account in a workspace where your HONO administrator has turned on **MCP access** in ERA.
- An ERA MCP API key. A read-only key is recommended.

## Setup

1. Sign in to ERA. Open **Profile > MCP keys**.
2. Create a key and copy it. It starts with `hno_live_`. You see it only once.
3. On the same page, copy your **MCP URL**. It looks like `https://yourcompany.hono.ai/api/yourcompany/mcp`.
4. In Dify, install **ERA by HONO** from the Marketplace. Then open **Tools > ERA by HONO > Authorize**.
5. Paste the MCP URL and the API key. Click **Save**. Dify checks the key with ERA before it saves.

The plugin accepts only `https://` URLs on `hono.ai` or `honohr.com`, so your key is never sent anywhere else.

## Usage

Add any ERA tool to an agent, chatflow or workflow. Examples:

- An agent with `get_leave_balance`, `get_holiday_list` and `get_leave_policy` answers "How many casual leaves do I have, and can I take Friday off?"
- A workflow runs `get_team_attendance` every morning and posts the summary to a channel.
- A knowledge assistant uses `search_knowledge_base` and `list_org_policies` to answer policy questions with HONO as the source.

Each tool returns ERA's answer as JSON when it is structured, and always as text.

## Troubleshooting

- **HTTP 401:** the key was revoked, expired or belongs to another workspace. Create a new key.
- **HTTP 403:** MCP access is off for your workspace, or the key has an IP allowlist. Ask your HONO administrator.
- **HTTP 429:** you hit your workspace's ERA message limit. Wait a minute.

## Privacy

See [PRIVACY.md](PRIVACY.md). In short: the plugin stores nothing and talks only to your HONO workspace.

## Source and support

- Source: https://github.com/HONO-HR/dify-plugin-era
- Support: connect@hono.ai
