# VERIFY-4: What enters the context window

Date: 2026-11-07. Question: which sources put the most characters into the conversation, so that cuts go where they matter. Tool: `python3 tools/transcript-metrics.py context --match 'Projects-pages$|orin-dx-site'`. Sessions: the two audited projects. Characters, not tokens (divide by about 4). Each tool result is counted once; the model re-reads the whole context every turn, so an early large item costs more than its size.

## Result (16.2M characters)

| Origin | Characters | Share |
| :-- | :-- | :-- |
| Tool results | 6.82M | 42% |
| Tool-call inputs (not delegation) | 6.02M | 37% |
| User text | 1.49M | 9% |
| Assistant text | 1.38M | 9% |
| Delegation prompts (`Agent`) | 0.46M | 3% |

Tool results by tool: Bash 77.5%, Artifact 10.0%, Read 3.6%, WebSearch 2.7%, Agent 2.1%, WebFetch 1.4%. Tool-call inputs by tool: Bash 4.44M, Write 0.66M, SendMessage 0.51M, Agent 0.46M, Workflow 0.14M, Read 0.12M.

## What it shows

- **Bash is about 60% of everything**: 5.28M characters of output and 4.44M of command text. The input side is long inline scripts and heredocs, which the earlier result-only measure (77% of results) hid. Cutting output alone reaches at most about 33% of the conversation; command text is the other half of the lever.
- **The five largest single results are `Artifact` reads of 50,000 to 56,000 characters each**: a read returns the whole published page. Reading a page back to confirm a publish, or to edit it, should be by path or a targeted diff, not the full HTML.
- **Delegation prompts are small (3%)**, and handoff results through `Agent` are 2% of results. The multi-agent plumbing is not the context cost; the work done in the main thread is.
- **`SendMessage` inputs (0.51M)** are as large as the delegation prompts: continuing agents with long messages.

## What it does not show

- Characters, not billed tokens, and no cache effect.
- Two projects, one author, and a period that included the unusual spec marathon; the shares will move on other work.
- It does not separate resident context (agent descriptions, skill bodies, memory), which is loaded every session and is measured statically: 45 agent descriptions about 6.9k tokens (`scripts/check-platform-limits.py`).

## Implications for the plugins

1. Skills that run commands should say to keep output short (filter, cap, show failing lines) and to write long scripts to a file, not inline.
2. Skills that publish artifacts should not read the page back whole.
3. The resident cost (descriptions, skill bodies) is a separate, static lever; the review-slop branch already cut descriptions by half and has not been ported here.
