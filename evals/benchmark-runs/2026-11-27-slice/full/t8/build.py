"""Static site build pipeline: site.json + templates/ -> dist/."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).parent

def main():
    config = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    out = ROOT / config["output"]
    out.mkdir(exist_ok=True)
    for page in config["pages"]:
        template = (ROOT / "templates" / page["template"]).read_text(encoding="utf-8")
        variables = dict(config.get("defaults", {}))
        variables.update(page)
        html = template.format(**variables)
        (out / (page["name"] + ".html")).write_text(html, encoding="utf-8")
        print("built", page["name"])
    return 0

if __name__ == "__main__":
    sys.exit(main())
