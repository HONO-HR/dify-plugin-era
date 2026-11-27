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

To allow reads only, use a **read-only** ERA API key. ERA then refuses every write tool.

## Setup

### Sign in with HONO (recommended)

No key and no URL.

1. **Once per Dify workspace (admin):** install **ERA by HONO** from the Marketplace. Open **Tools > ERA by HONO**, open the OAuth client settings, leave the form blank and click **Save**. The plugin registers itself with HONO, so there is nothing to fill in. Dify only needs this saved once before anyone can sign in.
2. **Each person:** open **Tools > ERA by HONO > Authorize** and choose **OAuth**. HONO's sign-in page opens. Enter your company workspace (for example `acme`, or your HONO domain), then your HONO login, and approve.

Dify keeps you signed in and renews the sign-in by itself. Your HONO administrator must have turned on **MCP access** for the workspace.

### API key (alternative)

1. In ERA, open **Profile > MCP keys** and click **New MCP key**. Leave **Everyday HR tools only** unticked so that all 202 tools work. Tick **Read-only** if the Dify app should only read data.
2. Copy the key (starts with `hno_live_`, shown only once) and the **MCP URL** on the same page, for example `https://yourcompany.hono.ai/api/yourcompany/mcp`.
3. In Dify, open **Tools > ERA by HONO > Authorize**, choose **API Key**, paste both and click **Save**. Dify checks them with ERA before it saves.

The plugin sends a key only to `https://` URLs on `hono.ai` or `honohr.com`, and a HONO sign-in only to `mcp.hono.ai`.

### Who the tools act as

Every tool runs as the person who signed in (or whose key it is). Anyone using a Dify app built on that sign-in sees that person's data and acts as that person. Give each person their own sign-in, and do not share an app built on your sign-in.

## Usage

Add any ERA tool to an agent, chatflow or workflow. Examples:

- An agent with `get_leave_balance`, `get_holiday_list` and `apply_leave` answers "How many casual leaves do I have?" and then applies leave for Friday once you confirm.
- A workflow runs `get_team_attendance` every morning and posts the summary to a channel.
- A knowledge assistant uses `search_knowledge_base` and `list_org_policies` to answer policy questions with HONO as the source.

Each tool returns ERA's answer as JSON when it is structured, and always as text. Inputs that take a list or an object are passed as JSON text, for example `["Name","Code"]`.

## Troubleshooting

- **HTTP 401:** the sign-in or key was revoked or expired. Sign in again, or create a new key.
- **HTTP 403:** MCP access is off for your workspace, or the key has an IP allowlist. Ask your HONO administrator.
- **HTTP 429:** you hit your workspace's ERA message limit. Wait a minute.
- **"no oauth available client config" in Dify:** a workspace admin has not saved the plugin's OAuth client settings yet (step 1 above).
- **"Tool not found" or a write is refused:** the key is limited to everyday tools or is read-only. Create a key without those limits.

## Privacy

See [PRIVACY.md](PRIVACY.md). In short: the plugin stores nothing and talks only to your HONO workspace.

## Source and support

- Source: https://github.com/HONO-HR/dify-plugin-era
- Support: connect@hono.ai
