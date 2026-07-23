"""Refresh the AI image-gen tool snapshot from the live GitHub API.

Run this on your own machine (where api.github.com is reachable) to update the
CSV each month, then re-run examples/ai_image_tool_race.py to redraw the charts.

    python scripts/fetch_ai_tools.py

Set a GITHUB_TOKEN env var to raise the rate limit (optional, recommended):
    export GITHUB_TOKEN=ghp_xxx   # never commit this
"""

import csv
import datetime as dt
import os

import requests

# tool -> GitHub "owner/repo"
TOOLS = {
    "A1111 WebUI": "AUTOMATIC1111/stable-diffusion-webui",
    "ComfyUI": "Comfy-Org/ComfyUI",
    "Fooocus": "lllyasviel/Fooocus",
    "diffusers": "huggingface/diffusers",
    "InvokeAI": "invoke-ai/InvokeAI",
    "Flux": "black-forest-labs/flux",
    "Forge": "lllyasviel/stable-diffusion-webui-forge",
    "SD.Next": "vladmandic/sdnext",
}


def fetch(repo: str, headers: dict) -> dict:
    r = requests.get(f"https://api.github.com/repos/{repo}", headers=headers,
                     timeout=30)
    r.raise_for_status()
    return r.json()


def main() -> None:
    today = dt.date.today()
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    rows = []
    for tool, repo in TOOLS.items():
        d = fetch(repo, headers)
        created = d["created_at"][:10]
        age = max(1, (today - dt.date.fromisoformat(created)).days)
        rows.append({
            "tool": tool,
            "repo": repo,
            "stars": d["stargazers_count"],
            "forks": d["forks_count"],
            "open_issues": d["open_issues_count"],
            "created_at": created,
            "age_days": age,
            "stars_per_day": round(d["stargazers_count"] / age, 1),
            "as_of": today.isoformat(),
        })
        print(f"  {tool:12s} {d['stargazers_count']:>7} stars")

    out = f"data/ai_image_tools_{today:%Y-%m}.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote", out)


if __name__ == "__main__":
    main()
