#!/usr/bin/env bash
# Run a blind Codex leg inside a bubblewrap jail that can see the ratified
# specification and nothing else.
#
# Why a jail and not an instruction: a smoke test on 2026-08-10 showed Codex
# ignoring its piped stdin, running `rg -F 'Custos 4.2 — Candidate' /tmp
# /var/tmp`, finding a stray copy of the edition on disk, and answering from
# that. Its "read-only" sandbox restricts writes, not reads. On this box the
# reachable filesystem also holds a superseded 4.1 edition, a pull-request
# triage dump, and two custos checkouts complete with reviews/ and vectors/ —
# every one of them forbidden by docs/blind-brief.md. Containment has to be
# mechanical.
#
# The jail also gets a fresh HOME carrying only credentials, because
# ~/.codex holds sessions/ and memories_1.sqlite from earlier Codex runs on
# this project. A leg that can read its predecessors' transcripts is not blind.
#
# Usage: run-epsilon.sh <brief.md> <spec.md> <outfile>
set -euo pipefail

BRIEF="${1:?brief path}"; SPEC="${2:?spec path}"; OUT="${3:?output path}"
RATIFIED=68cc5c9b7164b33dffcf7b705a0d1301fe108c647d35638fec61d52d29b2775a

got=$(sha256sum "$SPEC" | cut -d' ' -f1)
[ "$got" = "$RATIFIED" ] || { echo "REFUSING: $SPEC is not the ratified edition ($got)" >&2; exit 2; }

JAIL=$(mktemp -d)
mkdir -p "$JAIL/work" "$JAIL/.codex"
cp "$SPEC" "$JAIL/work/custos-4.2.md"
cp ~/.codex/auth.json "$JAIL/.codex/auth.json"
[ -f ~/.codex/config.toml ] && cp ~/.codex/config.toml "$JAIL/.codex/config.toml"
git -C "$JAIL/work" init -q .

NODE_BIN=$(dirname "$(command -v codex)")
NVM_ROOT=$(cd "$NODE_BIN/.." && pwd)

# --tmpfs /tmp hides the stray editions and dumps; the real $HOME is never
# bound, so ~/code does not exist on the filesystem inside the jail.
#
# Codex's own sandbox is bypassed deliberately: it is bubblewrap too and
# cannot nest inside this one. The containment here is the outer jail, which
# is strictly tighter than what Codex would have applied to itself.
nice -n 19 bwrap \
  --ro-bind /usr /usr --ro-bind /etc /etc \
  --ro-bind-try /bin /bin --ro-bind-try /sbin /sbin \
  --ro-bind-try /lib /lib --ro-bind-try /lib64 /lib64 \
  --ro-bind "$NVM_ROOT" "$NVM_ROOT" \
  --ro-bind-try /run/systemd/resolve /run/systemd/resolve \
  --proc /proc --dev /dev --tmpfs /tmp \
  --bind "$JAIL" "$JAIL" \
  --setenv HOME "$JAIL" --setenv PATH "$NODE_BIN:/usr/bin:/bin" \
  --share-net --die-with-parent \
  --chdir "$JAIL/work" \
  codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox "$(cat "$BRIEF")" > "$OUT" 2>&1 < /dev/null

echo "--- containment audit: paths outside the jail ---"
if grep -oE '(/home/[^ "]*|/tmp/[^ "]*|/var/[^ "]*)' "$OUT" \
   | grep -vE "^${JAIL}(/|$)|^/tmp/?$" | sort -u | grep .; then
  echo "AUDIT FAILED — the run above touched paths outside the jail. Discard it." >&2
  exit 3
fi
echo "clean — no paths outside $JAIL appear in the transcript"
echo "jail retained for inspection: $JAIL"
