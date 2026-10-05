import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # AI for Statistics and Data Science

    **Prof. Eric A. Suess**

    *September 26, 2026*

    This guide is a practical map of current AI tools for university statistics and data-science work. Product features change quickly, and university access is controlled locally. The product claims below were checked against primary documentation on **September 20, 2026**. Always follow your instructor's academic-integrity rules and your university's IT and data policies.

    ## Why move beyond a web chat interface?

    A web chat is excellent for questions, explanations, and small pasted examples. Working closer to the project---in a desktop app, editor, notebook, or terminal---can give an AI tool richer context and let it produce real artifacts rather than text that you must copy manually.

    | Closer-to-project benefit | What it enables | Responsibility it adds |
    |---|---|---|
    | Project files and folders | Read related scripts, data dictionaries, and documentation together | Limit access to the intended folder; exclude secrets and restricted data |
    | Direct editing | Create or revise `.R`, `.py`, `.qmd`, and test files | Review every diff; keep version-control checkpoints |
    | Terminal access | Run code, linters, renders, and tests | Commands execute with real permissions and can damage or disclose data |
    | Notebooks and scripts | Repeat the same analysis from raw data to result | Record dependencies, seeds, and any steps that were not executed |
    | Version control | Inspect a change set and restore earlier work | Do not let an agent push, publish, or merge without explicit review |

    The central tradeoff is **capability versus authority**. More context can improve an answer, while more permissions increase the consequences of a mistake or prompt injection. A good workflow is: start read-only, make a narrow request, inspect the proposed change, run checks, and keep the human researcher accountable for the result.

    ## ChatGPT Edu

    ChatGPT Edu is an institution-managed offering rather than a feature every student automatically receives. OpenAI's current plan documentation groups Edu with organization plans that can provide administrative capabilities such as role-based access control, domain verification, data-retention/residency controls, analytics, and compliance/audit features. Business, Enterprise, and Edu workspace data covered by OpenAI's services is encrypted in transit and at rest and is not used to train OpenAI models by default. These statements do **not** mean that third-party apps, local files, browser profiles, or source-system logs all share the same retention or control boundary. See [OpenAI's plan comparison](https://learn.chatgpt.com/docs/pricing) and [ChatGPT Work local-security documentation](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-local-security).

    An Edu workspace may include ChatGPT and Codex surfaces, file and data-analysis workflows, shared workspace administration, and optional connected tools. Actual availability can differ by university, role, operating system, region, rollout stage, and administrator settings. Therefore:

    - Use the university's official access page or invitation, not an independently purchased account, when coursework requires the institutional workspace.
    - Confirm that the active workspace is the university workspace before uploading course material.
    - Ask campus IT which features are licensed and enabled. A feature visible in public documentation may be disabled locally.
    - Treat institutional controls as one layer of protection, not permission to upload identifiable student records or restricted research data.

    ## ChatGPT desktop app and university authentication

    OpenAI documents a ChatGPT desktop app for macOS, Windows, and Linux. Download it only through the link in the [official desktop-app guide](https://learn.chatgpt.com/docs/app), open the app, and sign in with the ChatGPT account your university tells you to use. OpenAI's current authentication documentation says that the desktop app opens a browser-based sign-in flow. Managed-workspace membership, provisioning, seats, roles, and permissions still determine which surfaces are available; successful authentication alone does not grant every capability. See [OpenAI authentication](https://learn.chatgpt.com/docs/auth).

    If your university enforces SSO, complete the institution's browser sign-in and any required MFA. Do not paste a university password, recovery code, API key, or session token into a chat or source file. If the workspace does not appear, stop and follow campus IT guidance rather than creating a second identity or bypassing SSO.

    ### File and app access is explicit and feature-specific

    Do not treat “the desktop app can use files” as unrestricted computer access.

    - A chat upload supplies the files you deliberately attach to that conversation.
    - Opening a folder or choosing a working location supplies that selected context; [the desktop guide](https://learn.chatgpt.com/docs/app) says ChatGPT can use files and context in the location you choose.
    - Connected apps use the authorized account and the actions exposed by that integration.
    - Browser or computer-use features have their own approvals and may inherit access from an already signed-in session.
    - Local agentic work can read, edit, and run tools only within its effective OS, workspace, sandbox, and approval permissions.

    The [local-security guide](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-local-security) explicitly separates file access, computer use, browser access, and connected apps. Grant only the capability needed for the current task, and verify the active workspace and approval prompt before allowing a write or external action.

    ## Codex

    Codex is OpenAI's agentic software-development environment. Current official documentation exposes it through the ChatGPT desktop app, a terminal CLI, an editor extension, and cloud workflows. Unlike ordinary code completion, Codex can inspect a project, edit files, run installed tools, and report verification results. The [Codex CLI guide](https://learn.chatgpt.com/docs/codex/cli) emphasizes local-repository work, user-selected permissions, and repeatable scripting/CI workflows.

    For local work, OpenAI documents two authentication paths: **Sign in with ChatGPT** for subscription access or use an **API key** for usage-based access. `codex login` starts the browser flow for ChatGPT sign-in. A university-managed ChatGPT account can work when the institution has provisioned the user, assigned an eligible seat/role, enabled the relevant Codex surface, and permitted the required login flow. Plan eligibility, administrator enablement, quotas, device-code access, and SSO requirements are institution-specific. Codex cloud requires ChatGPT sign-in. See [OpenAI authentication](https://learn.chatgpt.com/docs/auth).

    Safe first use:

    ```bash
    # Install only after checking the current official instructions:
    curl -fsSL https://chatgpt.com/codex/install.sh | sh

    cd path/to/a-version-controlled-project
    codex --sandbox read-only --ask-for-approval on-request
    ```

    The install command and read-only permission form are documented in the [CLI quickstart](https://learn.chatgpt.com/docs/codex/cli) and [agent approvals and security guide](https://learn.chatgpt.com/docs/agent-approvals-security). Start by asking Codex to explain the repository or propose a plan. Before allowing edits, create a Git checkpoint, restrict the working directory, inspect commands, review the diff, and run appropriate tests. Never embed credentials in a prompt or repository; use university-approved authentication and credential storage.

    ## A paired statistics example in R and Python

    Suppose five students report weekly study hours and receive quiz scores. We will compute the same sample size, means, sample standard deviations, and Pearson correlation in both languages.

    | Student | Study hours | Quiz score |
    |---:|---:|---:|
    | 1 | 2 | 68 |
    | 2 | 3 | 72 |
    | 3 | 4 | 78 |
    | 4 | 5 | 83 |
    | 5 | 6 | 91 |

    ### R with Tidyverse conventions

    ```r
    library(tidyverse)

    students <- tibble(
      student = 1:5,
      study_hours = c(2, 3, 4, 5, 6),
      quiz_score = c(68, 72, 78, 83, 91)
    )

    summary_r <- students |>
      summarise(
        n = n(),
        mean_study_hours = mean(study_hours),
        sd_study_hours = sd(study_hours),
        mean_quiz_score = mean(quiz_score),
        sd_quiz_score = sd(quiz_score),
        correlation = cor(study_hours, quiz_score)
      )

    summary_r
    ```

    ### Equivalent Python using the standard library
    """)
    return


@app.cell
def _():
    from math import sqrt
    from statistics import mean, stdev

    students = [
        {"student": 1, "study_hours": 2, "quiz_score": 68},
        {"student": 2, "study_hours": 3, "quiz_score": 72},
        {"student": 3, "study_hours": 4, "quiz_score": 78},
        {"student": 4, "study_hours": 5, "quiz_score": 83},
        {"student": 5, "study_hours": 6, "quiz_score": 91},
    ]

    hours = [row["study_hours"] for row in students]
    scores = [row["quiz_score"] for row in students]

    mean_hours = mean(hours)
    mean_score = mean(scores)
    cross_products = sum(
        (x - mean_hours) * (y - mean_score)
        for x, y in zip(hours, scores)
    )
    correlation = cross_products / sqrt(
        sum((x - mean_hours) ** 2 for x in hours)
        * sum((y - mean_score) ** 2 for y in scores)
    )

    summary_python = {
        "n": len(students),
        "mean_study_hours": mean_hours,
        "sd_study_hours": stdev(hours),
        "mean_quiz_score": mean_score,
        "sd_quiz_score": stdev(scores),
        "correlation": correlation,
    }

    print(summary_python)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both programs produce, to three decimals:

    | Statistic | Value |
    |---|---:|
    | $n$ | 5 |
    | Mean study hours | 4.000 |
    | Sample SD of study hours | 1.581 |
    | Mean quiz score | 78.400 |
    | Sample SD of quiz score | 9.072 |
    | Pearson correlation | 0.993 |

    **Interpretation:** in these five observations, study hours and quiz score have a very strong positive linear association. This tiny observational example does not establish that additional study time caused higher scores; other variables and sampling uncertainty are not addressed.

    **Rendering arrangement:** the two source chunks are deliberately marked `eval: false` because one Quarto render does not automatically provide both R/knitr and Python/Jupyter execution engines. They were executed independently with the locally installed R and Python interpreters, without installing packages, and their matching results are reported above.

    ## Google Antigravity

    The verified current name is **Google Antigravity**. Google's documentation now distinguishes four surfaces rather than a single “VS Code replacement”:

    - **Antigravity 2.0:** a standalone desktop command center for agents working across projects, workspaces, and worktrees.
    - **Antigravity CLI:** a keyboard-oriented terminal interface with agent and subagent workflows.
    - **Antigravity SDK:** a Python framework for custom agent deployments.
    - **Antigravity IDE:** a full editor-centered development environment with agent, terminal, browser, autocomplete, and artifact surfaces.

    See Google's [surface overview](https://www.antigravity.google/docs/home) and [IDE overview](https://www.antigravity.google/docs/ide/overview/). The IDE supplies an integrated editing experience, while the CLI can be run from a terminal beside any editor, including VS Code. They are not the same product surface, and official documentation does not justify treating Antigravity as merely a VS Code skin. Google also states that the Antigravity IDE is not supported for enterprise customers; it directs enterprise configurations to Antigravity 2.0 or the CLI.

    For a safe first session, use a test repository, keep `toolPermission` at `request-review`, keep `artifactReviewPolicy` at `asks-for-review`, and leave non-workspace access disabled. Those settings and their meanings are in the [official CLI reference](https://www.antigravity.google/docs/cli/reference/). Installation, account eligibility, models, quotas, and enterprise policy can change; use the current “Get Started” link for the selected surface rather than copying an old third-party command.

    ## Four Harnesses

    These four CLI coding-agent harnesses have different defaults; none is universally best.

    | Tool | Official installation source | Authentication/provider model | Permissions and safe start | Strengths and limitations |
    |---|---|---|---|---|
    | OpenAI Codex CLI | [Codex CLI quickstart](https://learn.chatgpt.com/docs/codex/cli); current installer: <code>curl -fsSL https://chatgpt.com/codex/install.sh &#124; sh</code> | ChatGPT subscription sign-in or OpenAI API key; managed access depends on workspace provisioning and roles | Start with `codex --sandbox read-only --ask-for-approval on-request` | Integrated OpenAI desktop/IDE/cloud ecosystem and OS sandbox controls; access, usage, and features depend on plan and admin settings |
    | OpenCode | [OpenCode v2 docs](https://opencode.ai/v2/docs); one documented option is `npm install -g @opencode/cli` | Many model providers; connect interactively with `/connect` or configure a provider | Start `opencode` in a disposable or version-controlled folder; add explicit `ask`/`deny` rules for shell, edits, and pushes | Provider choice and granular ordered permission rules; broad defaults require deliberate hardening, and v1/v2 configuration names differ |
    | Pi Agent | [Pi documentation](https://pi.dev/docs/latest); `npm install -g --ignore-scripts @earendil-works/pi-coding-agent` | `/login` for supported subscriptions or provider API keys/environment configuration | Start `pi` only in a trusted test project; use a container/VM when isolation matters | Minimal, extensible terminal harness; importantly, core Pi has **no built-in sandbox** and runs tools/extensions with the invoking user's permissions |
    | Prime Agent | [Prime Agent repository and documentation](https://github.com/PrimeIntellect-ai/prime-agent); current installer: <code>curl --proto '=https' --proto-redir '=https' -fsSL https://app.primeintellect.ai/prime-agent/install.sh &#124; sh</code> | `/login` supports several subscription and API-key providers; model access depends on the selected provider and account | Start in a disposable clone or clean worktree that you can inspect and restore; use an external sandbox or restricted environment for untrusted code | Persistent Python REPL, built-in subagents, durable continual-harness state, skills, and background sessions; model-generated Python and commands run with the user's OS permissions and are not security-sandboxed |

    OpenCode's [v2 permission documentation](https://opencode.ai/v2/docs/permissions) warns that shell commands retain the host user's filesystem, process, and network authority; use narrow rules and block actions such as `git push`. Pi's [security documentation](https://pi.dev/docs/latest/security) distinguishes project trust from sandboxing and recommends an OS/container boundary for untrusted or unattended work. Prime Agent's [official documentation](https://github.com/PrimeIntellect-ai/prime-agent#readme) likewise states that its worker and Python-kernel process boundaries are not a security sandbox. Installation commands run third-party code: read the current official installation page and your university policy before running one.

    ## What is an AI agent?

    An AI agent is a model-driven system that can use tools and take a sequence of actions toward an objective. An ordinary chat mainly returns a response; code completion predicts text near the cursor. An agent can inspect state, form or revise a plan, call a file/editor/shell/browser tool, observe the result, and continue.

    A useful loop is:

    1. **Observe:** read the request, relevant files, current outputs, and constraints.
    2. **Plan:** choose a small next action and identify what would count as success.
    3. **Act:** call an authorized tool within the available permissions.
    4. **Verify:** inspect the diff, output, test, render, or external state.
    5. **Report or iterate:** surface evidence, uncertainty, and remaining work.

    Context includes the prompt, selected files, project instructions, tool results, and sometimes durable memory. Persistence may mean saved conversations, files, scheduled work, or a running session; it does not make an agent infallible. Delegation lets a primary agent assign bounded subtasks to other agents, but it also multiplies cost, context-management problems, and opportunities for inconsistent results.

    Common risks include prompt injection hidden in webpages or repository text, excessive permissions, accidental disclosure, destructive commands, silent statistical or coding errors, unexpected usage cost, and work that cannot be reproduced because inputs or steps were not recorded. An approval dialog is useful only when a person understands the requested action.

    ## Spynel and Hermes

    ### Spynel

    Spynel is a **classic coordination program**, not an AI agent. Its local documentation describes provider-neutral application, harness, and orchestration boundaries. It coordinates external AI/coding harnesses; durable Markdown tasks represent finite objectives, goals represent measurable multi-round outcomes, and fresh review sessions can evaluate results. Spynel owns lifecycle claiming and leases, while dispatched agents do the substantive work and record evidence. This description was checked using the locally installed `spynel docs architecture`, `spynel docs tasks`, and `spynel docs goals` pages on September 20, 2026.

    That makes Spynel an orchestration/control layer around agents, not a model that independently reasons. Setup is workspace- and installation-specific; students should use the installed command's `spynel docs`, `spynel --help`, and local workspace contract rather than copying private configuration or assuming that a chat message alone completes a durable task.

    ### Hermes Agent

    In this CLI-agent context, the strongest authoritative match for “Hermes” is **Hermes Agent by Nous Research**. It is a separate agent product, not Spynel and not merely a Hermes language model. The official documentation describes CLI and desktop surfaces, persistent memory/skills, multiple tool backends, messaging gateways, scheduled automations, and subagent delegation. It can use Nous Portal, OpenRouter, OpenAI, or compatible endpoints. See the [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/).

    The official docs offer desktop installers and a CLI-only installation route; they identify `hermes setup --portal` as a first-time setup path. Do not run a remote install script without first inspecting it and checking institutional policy. Provider accounts, messaging connections, remote hosts, memory, and terminal tools each expand the data and permission boundary. “Hermes” is an overloaded name in AI and research, so this identification applies specifically to the surrounding agent-tool context.

    ## Herdr for running agents

    The verified spelling is **Herdr**. Its documentation calls it a terminal workspace manager for AI coding agents: a persistent background server owns real terminal panes, while the UI groups panes into project workspaces and reports recognized agent states such as working, blocked, done, or idle. It can run Codex, OpenCode, Pi, Hermes Agent, and other terminal processes; it does not replace their models, authentication, permissions, or sandboxes. See [Herdr's agent guide](https://herdr.dev/docs/agents/) and [quick start](https://herdr.dev/docs/quick-start/).

    A basic workflow after completing the official installation is:

    ```bash
    cd path/to/a-project
    herdr
    # In a Herdr pane, start one configured agent, for example:
    codex --sandbox read-only --ask-for-approval on-request
    ```

    Give each project its own workspace, split panes only when parallel work is genuinely independent, watch the sidebar for agents requiring decisions, and inspect each agent's output/diff yourself. Detaching leaves the server and agents running; `herdr` reattaches, and `herdr server stop` ends the session. Detection may be approximate when an agent lacks a direct integration, when a wrapper hides the foreground process, or when nested terminal multiplexers are used. Persistent panes also mean processes and costs may continue while the UI is detached.

    ## Omarchy: an agent-oriented Linux environment

    The intended product is **Omarchy**, not Oh My Pi. Omarchy is an open-source, opinionated Linux distribution created by David Heinemeier Hansson (DHH). It builds on Arch Linux and presents a keyboard-first environment with selected defaults rather than asking a new user to assemble every component. Its official site calls it “agentic Linux” and emphasizes a malleable computer whose configuration can be inspected and changed. This makes it a whole operating-system environment, not an AI model, coding-agent CLI, or editor plug-in. See the [official Omarchy site](https://omarchy.org/) and [project repository](https://github.com/omacom/omarchy).

    ### Intended workflow and AI's documented role

    Omarchy is aimed at people who want a ready-to-use but customizable Linux workstation, especially for keyboard-centered development. Its [AI manual](https://omarchy.org/manual/ai/) treats coding agents as first-class tools: launchers for several agent CLIs are prepared but downloaded only when first invoked, the user can choose a default agent, and an Omarchy-specific skill teaches supported agents how to tailor the system. The manual warns that this skill is experimental, recommends planning before changes, and tells users to be prepared to roll back mistakes. DHH's own essay, [“The malleable computer”](https://world.hey.com/dhh/the-malleable-computer-7c187a9b), documents the broader idea: users can employ AI to adapt open-source applications and Omarchy system elements that would otherwise demand specialized knowledge.

    Those primary sources establish that AI agents shaped Omarchy's intended workflow and are used to customize and diagnose the system. They do **not** establish what proportion of Omarchy's source code was written by AI, so “programmed using AI” should not be turned into a numerical or comprehensive authorship claim without stronger project evidence.

    ### Installation and safety

    Installing a Linux distribution changes the machine at a much deeper level than installing an editor or CLI. Omarchy's [getting-started guide](https://omarchy.org/manual/getting-started/) documents an ISO-based installation with full-disk and free-space/dual-boot choices. The full-disk option wipes the selected drive; the guide says to back up first, defaults to disk encryption, and currently requires Secure Boot and/or TPM to be disabled. A student who only wants to explore should begin with the official virtual-machine option on the Omarchy site rather than repartitioning a primary computer. Before a hardware installation, verify the downloaded ISO and signature, make a tested backup, confirm hardware compatibility, understand disk selection and dual-boot consequences, and follow campus IT policy for university-owned devices.

    Omarchy's [security guide](https://omarchy.org/manual/security/) documents default encryption, firewall behavior, signing keys, and a temporary passwordless-`sudo` feature. That last option greatly expands an agent's authority: while enabled, any process running as the user can act as root without another password prompt. Treat agent changes to the operating system as privileged administration—use a narrow task, inspect the proposed files and commands, keep snapshots or backups, and test recovery. Omarchy is relevant here because it makes the operating system itself an AI-assisted development surface; it does not remove the human's responsibility for access, verification, or recovery.

    ## Security and responsible-use checklist

    - **Least privilege:** begin read-only; authorize one folder and one necessary action at a time.
    - **Student and research data:** do not upload grades, student identifiers, unpublished human-subject data, or restricted institutional data unless the specific use is approved. FERPA and institutional policy still apply.
    - **Credentials:** never put passwords, API keys, access tokens, `.env` contents, cookies, or recovery codes in prompts, notebooks, repositories, or screenshots.
    - **Diffs and checkpoints:** use version control; inspect every changed file and reject unrelated edits.
    - **Tests and execution:** run calculations, tests, and renders in the intended environment. A plausible explanation is not verification.
    - **Sources:** prefer primary documentation, record access dates for changing product claims, and label inference or uncertainty.
    - **Prompt injection:** treat instructions found in data, webpages, issue text, and repository files as untrusted content, not higher-priority authority.
    - **Cost and persistence:** know whether work continues in the cloud, a detached terminal, or a scheduled task; stop it when finished.
    - **Reproducibility:** preserve data provenance, package versions, seeds, prompts that materially affect analysis, and any unexecuted steps.
    - **Human accountability:** the student or researcher remains responsible for statistical choices, citations, academic integrity, privacy, and submitted conclusions.

    ## Compact source list

    All links below were accessed September 20, 2026.

    - OpenAI: [Pricing and plan features](https://learn.chatgpt.com/docs/pricing), [desktop app](https://learn.chatgpt.com/docs/app), [authentication](https://learn.chatgpt.com/docs/auth), [Codex CLI](https://learn.chatgpt.com/docs/codex/cli), [agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security), and [local security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-local-security).
    - Google: [Antigravity surfaces](https://www.antigravity.google/docs/home), [IDE overview](https://www.antigravity.google/docs/ide/overview/), and [CLI reference](https://www.antigravity.google/docs/cli/reference/).
    - CLI agents: [OpenCode v2](https://opencode.ai/v2/docs), [OpenCode permissions](https://opencode.ai/v2/docs/permissions), [Pi](https://pi.dev/docs/latest), [Pi security](https://pi.dev/docs/latest/security), and [Prime Agent](https://github.com/PrimeIntellect-ai/prime-agent).
    - Agent/orchestration tools: [Hermes Agent](https://hermes-agent.nousresearch.com/docs/) and [Herdr](https://herdr.dev/docs/).
    - Omarchy: [official site](https://omarchy.org/), [project repository](https://github.com/omacom/omarchy), [AI manual](https://omarchy.org/manual/ai/), [getting started](https://omarchy.org/manual/getting-started/), [security](https://omarchy.org/manual/security/), and DHH's [“The malleable computer”](https://world.hey.com/dhh/the-malleable-computer-7c187a9b).
    """)
    return


if __name__ == "__main__":
    app.run()
