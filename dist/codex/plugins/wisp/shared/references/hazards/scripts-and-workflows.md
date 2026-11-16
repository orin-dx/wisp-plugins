# Script, Workflow, and Template Hazard Reference

Patterns are leads, not findings. Confirm a reachable bad outcome in the environment that runs the file: the CI runner, shell, and tool versions, or the consumer that receives a generated template. Applies to shell scripts, CI workflow YAML, `jq` filters, and generated files.

## Disabled errexit

- Signal: a shell function relies on `set -e` but is called on the left of `||` or `&&`, or inside `if`.
- Confirm: a failing command inside the function lets execution continue to a later write or post.
- Refute: each command's status is checked explicitly, or the caller does not depend on the function's early exit.

## Failure read as nothing to do

- Signal: `|| true`, `|| return 0`, `2>/dev/null`, `jq ... // empty`, an ignored exit code, or an empty result treated as complete.
- Confirm: a missing tool, failed lookup, or renamed key produces the same outcome as a legitimate empty result.
- Refute: the failure is reported distinctly, or leniency applies only to user input.

## Test double wider than the real tool

- Signal: a stub or fake for `git`, `gh`, `cargo`, or `npm` accepts any arguments, or ignores the filter or flag it stands in for.
- Confirm: dropping or misspelling a required flag still passes tests, and the real tool's help rejects or ignores it.
- Refute: a contract test runs the real tool against the same argument grammar.

## Generated output never run as its consumer

- Signal: tests for a generator assert golden bytes or only the project's own configuration.
- Confirm: the consumer's environment differs in a way that changes behavior, such as an attached or detached checkout, another runner, or a clean tree.
- Refute: a test generates the file for a scratch repository and runs its commands the way the consumer's CI does.

## Pins and labels without an owner

- Signal: action SHAs, tool versions, runner labels, or credential lists repeated across files; floating tags; templates outside the pin checker.
- Confirm: copies differ, or a label or version no longer resolves.
- Refute: one owner generates the copies and a check compares them, or a scheduled job verifies resolution.

## Release path first run at release

- Signal: a change to a release or publish workflow is verified only by lint and unit tests.
- Confirm: a step such as planning, building a target, or pushing a tag runs for the first time at release.
- Refute: a rehearsal on the pull request runs planning and a real build.

## Failure that looks like regression

- Signal: a step downloads or reads state and a failed read is reported as a pass or a metric change.
- Confirm: the failure and a legitimate negative result produce the same signal.
- Refute: the step reports the failure distinctly before comparing.
