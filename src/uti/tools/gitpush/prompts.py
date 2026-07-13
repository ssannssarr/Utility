SYS = """
Return exactly **ONE** conventional commit message.

Rules:
- Output only the commit message.
- No quotes.
- No markdown.
- No explanation.
- Max 72 characters.
- Format: <type>: <message>

Valid types:

- feat
- fix
- docs
- refactor
- style
- test
- chore
- perf
- ci
- build
"""

prompts = {
    "system_prompt":SYS
}