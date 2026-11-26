# ERA by HONO

Use your HONO HRMS in Dify apps, workflows and agents. ERA is the AI layer of [HONO](https://hono.ai) HRMS. This plugin gives Dify 202 HR tools through your organisation's ERA workspace: 177 that read data and 25 that act on your behalf.

**Read:**
- **Leave:** balance, history, policy, leave types, expiring leave, encashment
- **Attendance:** calendar, punch log, missing punches, overtime, shift roster
- **Pay:** payroll summary, salary difference, loans, reimbursements, travel expenses
- **People and team:** profile, directory search, team attendance, team leave calendar, team pulse
- **Performance and learning:** goal sheet, reviews, 360 feedback, PMS cycle, courses, learning programs
- **Hiring:** open and approved positions, referrals, recruitment pipeline, offer status
- **Self-service:** letters, policies, knowledge base, support tickets, pending approvals

**Act (always after a confirmation step):** apply or cancel leave, on-duty, overtime and attendance regularisation; mark attendance; approve or reject requests; request letters and course enrollment; submit expenses and reimbursement claims; raise, escalate or follow up on support tickets and approvals.

Every answer respects your HONO permissions: you see and do exactly what you could in HONO.

## How write tools work

A write tool never acts on the first call. The first call returns `status: "confirmation_required"` with a summary of what will happen and a `confirmToken`. The action runs only when the same tool is called again with the same inputs plus that `confirmToken`, within 5 minutes. In an agent, the model shows you the summary, waits for your yes, then calls again. In a workflow, a single tool node only returns the summary, so nothing is changed.

To allow reads only, create a **read-only** ERA key. ERA then refuses every write tool.

## Requirements

- A HONO HRMS account in a workspace where your HONO administrator has turned on **MCP access** in ERA.
- An ERA MCP API key.

## Setup

1. Sign in to ERA. Open **Profile > MCP keys** and click **New MCP key**.
2. Leave **Everyday HR tools only** unticked, so that all 202 tools work. Tick **Read-only** if the Dify app should only read data.
3. Create the key and copy it. It starts with `hno_live_`. You see it only once.
4. On the same page, copy your **MCP URL**. It looks like `https://yourcompany.hono.ai/api/yourcompany/mcp`.
5. In Dify, install **ERA by HONO** from the Marketplace. Then open **Tools > ERA by HONO > Authorize**.
6. Paste the MCP URL and the API key. Click **Save**. Dify checks the key with ERA before it saves.

The plugin accepts only `https://` URLs on `hono.ai` or `honohr.com`, so your key is never sent anywhere else.

## Usage

Add any ERA tool to an agent, chatflow or workflow. Examples:

- An agent with `get_leave_balance`, `get_holiday_list` and `apply_leave` answers "How many casual leaves do I have?" and then applies leave for Friday once you confirm.
- A workflow runs `get_team_attendance` every morning and posts the summary to a channel.
- A knowledge assistant uses `search_knowledge_base` and `list_org_policies` to answer policy questions with HONO as the source.

Each tool returns ERA's answer as JSON when it is structured, and always as text. Inputs that take a list or an object are passed as JSON text, for example `["Name","Code"]`.

## Troubleshooting

- **HTTP 401:** the key was revoked, expired or belongs to another workspace. Create a new key.
- **HTTP 403:** MCP access is off for your workspace, or the key has an IP allowlist. Ask your HONO administrator.
- **HTTP 429:** you hit your workspace's ERA message limit. Wait a minute.
- **"Tool not found" or a write is refused:** the key is limited to everyday tools or is read-only. Create a key without those limits.

## Privacy

See [PRIVACY.md](PRIVACY.md). In short: the plugin stores nothing and talks only to your HONO workspace.

## Source and support

- Source: https://github.com/HONO-HR/dify-plugin-era
- Support: connect@hono.ai
