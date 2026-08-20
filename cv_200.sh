#!/usr/bin/env bash
# cross-verify.sh - auto-dev cross-model verifier bridge (deep-reasoning loop 6.2).
#
# Sends a verification PROMPT to an INDEPENDENT model (no-anchoring: the verifier
# is told it did not write the work) and prints its critique on stdout. Provider
# is chosen by $AUTO_DEV_CROSS_MODEL plus the matching API key. If none is
# available, or the provider call fails (timeout / non-2xx after retries), it
# prints a structured downgrade line and exits 2, so the caller falls back to the
# same-family devil's-advocate panel. NEVER blocks the loop.
#
# Hardening (docs/hardening-plan.md, Phase 4 - script half):
#   - every call is bounded by --max-time ($AUTO_DEV_CROSS_TIMEOUT, default 45s);
#   - transient 429 / 5xx are retried with backoff (--retry, default 2);
#   - the HTTP status is captured and a non-200 is NORMALIZED - an error body is
#     never piped through extract() as if it were a critique (the old silent
#     degradation bug);
#   - on any downgrade it prints CROSS_MODEL_DOWNGRADE model=.. http=.. reason=".."
#     then exits 2 (the agreed "use the DA panel" signal is preserved).
#
# Usage:  cross-verify.sh "verification prompt"     (or pipe the prompt on stdin)
# Extends the operator's shared/cross_model_verification.md with a DeepSeek case.
set -u

PROMPT="${1:-}"
[ -z "${PROMPT}" ] && PROMPT="$(cat 2>/dev/null || true)"
[ -z "${PROMPT}" ] && { echo "CROSS_MODEL_AVAILABLE=none (empty prompt)"; exit 2; }
MODEL="${AUTO_DEV_CROSS_MODEL:-}"
TIMEOUT="${AUTO_DEV_CROSS_TIMEOUT:-45}"   # seconds, whole-call bound
RETRY="${AUTO_DEV_CROSS_RETRY:-2}"        # attempts on transient 429/5xx (curl backoff)
# Resolve a Python 3 interpreter under any common name (python3 on *nix; python/py on
# Windows). Without this, a box that ships `python` but not `python3` silently degrades
# extract() to raw JSON. node / cat remain the last-resort fallbacks.
PY="$(command -v python3 || command -v python || command -v py || true)"

json_escape() { # JSON-encode stdin as a string literal
  "${PY:-python3}" -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null \
    || node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>process.stdout.write(JSON.stringify(s)))'
}
extract() { # pull message text from a provider JSON response on stdin
  "${PY:-python3}" -c "import json,sys
d=json.load(sys.stdin)
print($1)" 2>/dev/null || cat
}

# downgrade MODEL HTTP REASON -> structured line + exit 2 (the "use the DA panel" signal).
# Printed instead of an error body so a failed call can never masquerade as a critique.
downgrade() {
  echo "CROSS_MODEL_DOWNGRADE model=${1:-none} http=${2:-none} reason=\"${3:-unavailable}\""
  echo "CROSS_MODEL_AVAILABLE=none (${3:-unavailable})"
  exit 2
}

# http_post URL AUTH_HEADER JSON_BODY -> prints the raw curl result: the response body,
# a newline, then the HTTP status code as the LAST line (via -w). The caller splits it in
# ITS OWN scope -- http_post runs inside a $(...) subshell, so a global it sets would NOT
# survive back to the caller. --max-time bounds the whole call; --retry adds curl's
# exponential backoff on transient 429/5xx. Split with the hcode/hbody helpers below.
http_post() {
  local url="$1" auth="$2" body="$3"
  curl -sS --max-time "${TIMEOUT}" --retry "${RETRY}" \
    -w '\n%{http_code}' \
    -H "${auth}" -H "Content-Type: application/json" \
    -d "${body}" "${url}" 2>/dev/null
}
# hcode RAW -> the HTTP status (last line), or "timeout" on a curl failure / non-numeric.
hcode() { local c="${1##*$'\n'}"; case "${c}" in (*[!0-9]*|"") c="timeout" ;; esac; printf '%s' "${c}"; }
# hbody RAW -> the response body (everything before the last line).
hbody() { printf '%s' "${1%$'\n'*}"; }

P="$(printf '%s' "${PROMPT}" | json_escape)"
SYS="You are an independent verification assistant. You did NOT write the work under review. Find the most serious weaknesses; if rigorous, say so explicitly."
S="$(printf '%s' "${SYS}" | json_escape)"

case "${MODEL}" in
  deepseek*)
    [ -n "${DEEPSEEK_API_KEY:-}" ] || { echo "CROSS_MODEL_AVAILABLE=none (no DEEPSEEK_API_KEY)"; exit 2; }
    RAW="$(http_post http://127.0.0.1:8801/v200 \
      "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
      "{\"model\":\"${MODEL}\",\"temperature\":0.1,\"max_tokens\":2000,\"messages\":[{\"role\":\"system\",\"content\":${S}},{\"role\":\"user\",\"content\":${P}}]}")"
    [ "$(hcode "${RAW}")" = "200" ] || downgrade "${MODEL}" "$(hcode "${RAW}")" "deepseek call failed after ${RETRY} retries"
    hbody "${RAW}" | extract 'd["choices"][0]["message"]["content"]'
    ;;
  gpt-5*|gpt*)
    [ -n "${OPENAI_API_KEY:-}" ] || { echo "CROSS_MODEL_AVAILABLE=none (no OPENAI_API_KEY)"; exit 2; }
    RAW="$(http_post https://api.openai.com/v1/chat/completions \
      "Authorization: Bearer ${OPENAI_API_KEY}" \
      "{\"model\":\"${MODEL}\",\"temperature\":0.1,\"max_tokens\":2000,\"messages\":[{\"role\":\"system\",\"content\":${S}},{\"role\":\"user\",\"content\":${P}}]}")"
    [ "$(hcode "${RAW}")" = "200" ] || downgrade "${MODEL}" "$(hcode "${RAW}")" "openai call failed after ${RETRY} retries"
    hbody "${RAW}" | extract 'd["choices"][0]["message"]["content"]'
    ;;
  gemini*)
    [ -n "${GOOGLE_AI_API_KEY:-}" ] || { echo "CROSS_MODEL_AVAILABLE=none (no GOOGLE_AI_API_KEY)"; exit 2; }
    RAW="$(http_post "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${GOOGLE_AI_API_KEY}" \
      "X-Goog-Api-Client: auto-dev-cross-verify" \
      "{\"contents\":[{\"parts\":[{\"text\":${P}}]}],\"generationConfig\":{\"temperature\":0.1,\"maxOutputTokens\":2000}}")"
    [ "$(hcode "${RAW}")" = "200" ] || downgrade "${MODEL}" "$(hcode "${RAW}")" "gemini call failed after ${RETRY} retries"
    hbody "${RAW}" | extract 'd["candidates"][0]["content"]["parts"][0]["text"]'
    ;;
  *)
    echo "CROSS_MODEL_AVAILABLE=none (set AUTO_DEV_CROSS_MODEL to deepseek-*, gpt-*, or gemini-*)"
    exit 2
    ;;
esac
