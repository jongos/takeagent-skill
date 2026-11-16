# takeagent-skill v0.1.5

Research privacy, concise responses and release secret scanning.

- Explicitly withhold research names, links, identifiers, raw text and provenance, including in exports or saved notes. Explain financing logic in original wording instead.
- Preserve the user's own project evidence and funding-source information.
- Match TakeAgent's conversational standard: answer first, normally 80-180 words or less for simple questions, with more detail on request. Include only conditions that change the answer or next step; omit routine disclaimers.
- Add checksum-pinned Gitleaks scans of Git history and expanded packages to CI.

Reviewed all five preceding release ZIPs and public Git history: no detected secrets. Local credential-value comparison found no matches. Behavioral acceptance cases now cover disclosure attempts, accidental tool metadata, project evidence and relevant conditions. Host-specific behavioral testing remains separate from packaging checks.
