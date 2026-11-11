# Context hygiene

## Outcome

Keep bulk out of the conversation so the model reads what decides the work. In two audited projects, shell commands and their output were about 60% of all characters; delegation was 3%. Record exact commands and their terminal results in the artifact; keep the raw stream out of the thread.

## Applicability

Apply when a step runs commands, reads large files, or publishes pages. It does not relax evidence rules: a result still needs its exact command, its terminal state and what it did not cover.

## Rules

- Run a long script from a file. Write it once, run it by path, and keep it if the artifact cites it. Do not paste scripts or heredocs into a command.
- Filter before reading. Request the failing lines, the summary line or a count, for example a test runner's failure section or `--stat` instead of a full diff. Re-run without the filter only for the part under investigation.
- Cap output. Pipe unbounded listings and logs through a line limit or write them to a file and read the relevant range.
- Read files by range when the question is local. Read whole only when the whole decides the answer.
- Pass artifacts by path and hash. Persist a large artifact and give the next agent the path, not the content.
- Do not read a published page back whole. Check the publish result, or fetch the one file or range that changed.
- Look at one image at a time, and pass screenshots by path.

## Refutation

A filter that hides the line that matters is worse than no filter. When a filtered result is surprising, an exit code is non-zero without visible cause, or a count disagrees with expectation, re-run with the full output once.

## Disposition

State in the artifact which results were filtered and how, so a reviewer can reproduce them.
