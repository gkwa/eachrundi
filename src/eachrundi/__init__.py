import argparse
import pathlib
import urllib.parse

import jinja2
import jinja2.filters


class FailUndefined(jinja2.Undefined):
    def __str__(self):
        raise ValueError(f"Variable {self._undefined_name} is undefined")

    def __iter__(self):
        raise ValueError(f"Variable {self._undefined_name} is undefined")

    def __bool__(self):
        return False


def url_encode(value):
    return urllib.parse.quote(str(value), safe="")


def render_template(template_name: str, data: dict) -> str:
    TEMPLATES_PATH = pathlib.Path(__file__).resolve().parent / "templates"
    loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
    env = jinja2.Environment(
        loader=loader,
        undefined=FailUndefined,
        keep_trailing_newline=True,
    )

    env.filters["url_encode"] = url_encode
    template = env.get_template(template_name)
    return template.render(**data)


def write_output(output_path: pathlib.Path, content: str) -> None:
    with open(output_path, "w") as f:
        f.write(content)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate project files from templates"
    )
    parser.add_argument(
        "--project",
        default="streambox/faris",
        help="Project name (default: streambox/faris)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project = args.project

    output_dir = pathlib.Path("output")
    output_dir.mkdir(exist_ok=True)

    template_data = {
        "start.sh.j2": {},
        "requirements.yml.j2": {
            "project": project,
        },
        "cleanup_files.sh.j2": {},
        "command01.sh.j2": {
            "project": project,
            "payload": "payload01.json",
            "outfile": "command01-output.json",
        },
        "command02.sh.j2": {
            "project": project,
            "payload": "payload02.json",
            "outfile": "command02-output.json",
        },
        "entrypoint.sh.j2": {},
        "README.md.j2": {
            "project": project,
        },
        "Dockerfile.j2": {},
        "run_test.sh.j2": {},
        "run.sh.j2": {
            "project": project,
        },
        "script1.sh.j2": {
            "project": project,
        },
        "all.sh.j2": {},
        "token_cleanup.sh.j2": {
            "project": project,
        },
    }

    for template_file, data in template_data.items():
        data["project"] = project
        output_path = output_dir / template_file.replace(".j2", "")
        rendered = render_template(template_file, data)
        write_output(output_path, rendered)
        if ".sh" in template_file.lower():
            output_path.chmod(0o755)
