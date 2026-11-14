#!/usr/bin/env python3
"""Build, verify, and safely install the canonical Agent Skill (Python 3.10+)."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "dividend-income-equity-analysis"
SOURCE = ROOT / NAME
INVENTORY = ROOT / "scripts" / "skill-package-files.txt"
DEFAULT_OUTPUT = ROOT / "dist" / "agent-skills"
MANIFEST = "bundle-manifest.json"
PLATFORMS = {
    "codex": (".agents", "skills"),
    "copilot": (".github", "skills"),
    "claude": (".claude", "skills"),
}
USER_PLATFORMS = {
    "codex": (".agents", "skills"),
    "copilot": (".copilot", "skills"),
    "claude": (".claude", "skills"),
}
REQUIRED = {
    "SKILL.md", "full-analysis.md", "schema.json", "workflow.md", "screen-mode.md",
    "safety-review.md", "economic-profile.md", "buy-zone.md", "output-template.md",
    "requirements-dev.txt", "templates/report.html", "examples/full-report.analysis.json",
    "scripts/decision_rules.py", "scripts/local_checks.py", "scripts/schema3_checks.py",
    "scripts/validate_analysis.py", "scripts/render_report.py",
}


class PackageError(Exception):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree_digest(files: dict[str, str]) -> str:
    return digest(json.dumps(files, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def safe_name(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name and not p.is_absolute() and "\\" not in name and
                all(part not in ("", ".", "..") for part in p.parts) and
                p.as_posix() == name and ":" not in name)


def scalar(value: str) -> str:
    """Accept a deliberately small, unambiguous YAML string subset without dependencies."""
    if not value:
        raise PackageError("Empty YAML scalar")
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise PackageError(f"Invalid quoted YAML scalar: {error}") from error
        if not isinstance(parsed, str):
            raise PackageError("YAML scalar must be a string")
        return parsed
    if value.startswith("'"):
        if not value.endswith("'") or re.search(r"(?<!')'(?!')", value[1:-1]):
            raise PackageError("Invalid single-quoted YAML scalar")
        return value[1:-1].replace("''", "'")
    if value[0] in "!&*{}[]|>@`%\"'" or " #" in value or re.search(r":(?:\s|$)", value):
        raise PackageError(f"Unsupported or invalid plain YAML scalar: {value}")
    return value


def validate_skill(files: dict[str, bytes]) -> None:
    missing = REQUIRED - files.keys()
    if missing:
        raise PackageError(f"Required skill files missing: {', '.join(sorted(missing))}")
    try:
        text = files["SKILL.md"].decode("utf-8")
    except UnicodeError as error:
        raise PackageError("SKILL.md must be UTF-8") from error
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise PackageError("SKILL.md needs YAML frontmatter")
    end = lines.index("---", 1)
    fields: dict[str, str] = {}
    metadata: set[str] = set()
    in_metadata = False
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  ") and in_metadata:
            match = re.fullmatch(r"  ([a-zA-Z0-9_-]+): (.+)", line)
            if not match or match[1] in metadata:
                raise PackageError(f"Invalid or duplicate YAML metadata: {line}")
            metadata.add(match[1])
            scalar(match[2])
            continue
        match = re.fullmatch(r"([a-z][a-z0-9-]*):(?: (.*))?", line)
        if not match or match[1] in fields:
            raise PackageError(f"Invalid or duplicate YAML frontmatter: {line}")
        key, value = match.groups()
        if key not in {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}:
            raise PackageError(f"Unsupported frontmatter field: {key}")
        in_metadata = key == "metadata"
        if in_metadata:
            if value is not None:
                raise PackageError("metadata must be a YAML mapping")
            fields[key] = "mapping"
        else:
            fields[key] = scalar(value or "")
    name, description = fields.get("name", ""), fields.get("description", "")
    if name != NAME or len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise PackageError("Invalid skill name or name does not match directory")
    if not description.strip() or len(description) > 1024:
        raise PackageError("description must have 1–1024 characters")
    if "compatibility" in fields and len(fields["compatibility"]) > 500:
        raise PackageError("compatibility exceeds 500 characters")
    if not "\n".join(lines[end + 1:]).strip():
        raise PackageError("SKILL.md has no instruction body")
    for document in ("SKILL.md", "full-analysis.md"):
        body = files[document].decode("utf-8")
        references = re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|json|html|py|txt))`", body)
        for ref in references:
            if not safe_name(ref) or ref not in files:
                raise PackageError(f"{document} references missing or unsafe file: {ref}")
    try:
        schema = json.loads(files["schema.json"])
    except (json.JSONDecodeError, UnicodeError) as error:
        raise PackageError(f"Invalid schema JSON: {error}") from error
    if schema.get("properties", {}).get("schema_version", {}).get("default") != "3.0":
        raise PackageError("Expected schema 3.0")


def inventory() -> list[str]:
    names = [line.strip() for line in INVENTORY.read_text(encoding="utf-8").splitlines()
             if line.strip() and not line.startswith("#")]
    if len(names) != len(set(names)) or any(not safe_name(name) or name == MANIFEST for name in names):
        raise PackageError("Inventory has duplicate or unsafe paths")
    return sorted(names)


def actual_files(directory: Path) -> set[str]:
    if directory.is_symlink() or not directory.is_dir():
        raise PackageError(f"Not a regular skill directory: {directory}")
    result = set()
    directories = []
    for path in directory.rglob("*"):
        if path.is_symlink():
            raise PackageError(f"Symlinks are not allowed in packages: {path}")
        if path.is_dir():
            directories.append(path)
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(directory)
        # Python's generated bytecode is harmless; never ignore other files.
        if "__pycache__" in rel.parts and path.suffix == ".pyc":
            continue
        result.add(rel.as_posix())
    for path in directories:
        relative = path.relative_to(directory)
        if "__pycache__" in relative.parts:
            continue
        prefix = relative.as_posix() + "/"
        if not any(name.startswith(prefix) for name in result):
            raise PackageError(f"Unexpected empty directory: {path}")
    return result


def source_files() -> dict[str, bytes]:
    names = inventory()
    found = actual_files(SOURCE)
    if found != set(names):
        raise PackageError(f"Inventory/source mismatch. Missing: {sorted(set(names)-found)}; "
                           f"unreviewed: {sorted(found-set(names))}")
    files = {name: (SOURCE / name).read_bytes() for name in names}
    validate_skill(files)
    return files


def provenance() -> dict[str, str | None]:
    def git(*args: str) -> str | None:
        try:
            result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
            return result.stdout.decode("utf-8").strip() if result.returncode == 0 else None
        except (OSError, UnicodeError):
            return None
    top = git("rev-parse", "--show-toplevel")
    if not top or Path(top).resolve() != ROOT:
        return {"commit": None, "status": "unknown"}
    commit = git("rev-parse", "--verify", "HEAD")
    status = git("status", "--porcelain=v1", "--untracked-files=all", "--",
                 NAME, "scripts/skill-package-files.txt", "scripts/skill_package.py")
    if not commit or status is None:
        return {"commit": commit, "status": "unknown"}
    return {"commit": commit, "status": "dirty" if status else "clean"}


def manifest_for(platform: str, files: dict[str, bytes]) -> dict:
    hashes = {name: digest(data) for name, data in sorted(files.items())}
    source = provenance()
    return {"manifest_version": 1, "skill_name": NAME, "platform": platform,
            "source_repository": "https://github.com/Alanjiao1988/skills-dividend-for-HK",
            "source_commit": source["commit"], "source_status": source["status"],
            "source_tree_sha256": tree_digest(hashes), "files": hashes}


def check_contents(files: dict[str, bytes], expected_platform: str | None = None) -> dict:
    try:
        manifest = json.loads(files[MANIFEST])
    except (KeyError, ValueError, UnicodeError) as error:
        raise PackageError(f"Missing or invalid {MANIFEST}: {error}") from error
    if (not isinstance(manifest, dict) or manifest.get("manifest_version") != 1 or
            manifest.get("skill_name") != NAME or manifest.get("platform") not in PLATFORMS):
        raise PackageError("Unrecognized package manifest")
    if expected_platform and manifest["platform"] != expected_platform:
        raise PackageError(f"Package is for {manifest['platform']}, not {expected_platform}")
    hashes = manifest.get("files")
    if not isinstance(hashes, dict) or not hashes or any(not isinstance(n, str) or not safe_name(n)
            or n == MANIFEST or not isinstance(h, str) or not re.fullmatch(r"[0-9a-f]{64}", h)
            for n, h in hashes.items()):
        raise PackageError("Invalid file inventory in package manifest")
    if set(files) != set(hashes) | {MANIFEST}:
        raise PackageError(f"Package file mismatch; missing: {sorted((set(hashes)|{MANIFEST})-set(files))}; "
                           f"unexpected: {sorted(set(files)-(set(hashes)|{MANIFEST}))}")
    for name, expected in hashes.items():
        if digest(files[name]) != expected:
            raise PackageError(f"Package file modified: {name}")
    if manifest.get("source_tree_sha256") != tree_digest(hashes):
        raise PackageError("Package source fingerprint does not match its files")
    validate_skill({name: files[name] for name in hashes})
    return manifest


def read_directory(directory: Path) -> dict[str, bytes]:
    return {name: (directory / name).read_bytes() for name in actual_files(directory)}


def read_archive(path: Path) -> dict[str, bytes]:
    try:
        with zipfile.ZipFile(path) as archive:
            result = {}
            for item in archive.infolist():
                if item.is_dir():
                    continue
                name = item.filename
                prefix = NAME + "/"
                if not name.startswith(prefix) or not safe_name(name[len(prefix):]):
                    raise PackageError(f"Unsafe archive path: {name}")
                rel = name[len(prefix):]
                if rel in result or (item.external_attr >> 16) & 0o170000 == 0o120000:
                    raise PackageError(f"Duplicate or symlink archive entry: {name}")
                if item.file_size > 20_000_000:
                    raise PackageError(f"Archive entry too large: {name}")
                result[rel] = archive.read(item)
            return result
    except (zipfile.BadZipFile, OSError) as error:
        raise PackageError(f"Cannot read archive {path}: {error}") from error


def read_package(path: Path, platform: str | None = None) -> tuple[dict[str, bytes], dict]:
    files = read_directory(path) if path.is_dir() else read_archive(path)
    return files, check_contents(files, platform)


def write_archive(path: Path, files: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(f"{NAME}/{name}", (1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)


def materialize(directory: Path, files: dict[str, bytes]) -> None:
    directory.mkdir(parents=True)
    for name, data in files.items():
        target = directory.joinpath(*PurePosixPath(name).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def build(output: Path) -> None:
    files = source_files()
    output.mkdir(parents=True, exist_ok=True)
    # Refuse to replace unmanaged or modified output, including an altered archive.
    for platform in PLATFORMS:
        directory, archive = output / platform / NAME, output / f"{platform}.zip"
        if directory.exists() or directory.is_symlink():
            read_package(directory, platform)
        if archive.exists() or archive.is_symlink():
            if archive.is_symlink():
                raise PackageError(f"Refusing to replace symlink: {archive}")
            read_package(archive, platform)
    for platform in PLATFORMS:
        manifest = manifest_for(platform, files)
        bundle = dict(files)
        bundle[MANIFEST] = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
        parent = output / platform
        parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".build-", dir=output) as tmp:
            temporary = Path(tmp) / NAME
            materialize(temporary, bundle)
            read_package(temporary, platform)
            new_zip = Path(tmp) / "package.zip"
            write_archive(new_zip, bundle)
            read_package(new_zip, platform)
            destination = parent / NAME
            if destination.exists():
                shutil.rmtree(destination)
            shutil.move(str(temporary), destination)
            os.replace(new_zip, output / f"{platform}.zip")
        print(f"Built {platform}: {destination} and {output / (platform + '.zip')}")


def verify(output: Path) -> None:
    canonical = source_files()
    expected = {name: digest(data) for name, data in canonical.items()}
    source = provenance()
    for platform in PLATFORMS:
        directory = output / platform / NAME
        archive = output / f"{platform}.zip"
        files, info = read_package(directory, platform)
        zip_files, zip_info = read_package(archive, platform)
        if info["files"] != expected:
            raise PackageError(f"{platform} distribution differs from canonical source")
        if info.get("source_commit") != source["commit"] or info.get("source_status") != source["status"]:
            raise PackageError(f"{platform} distribution has stale source provenance; rebuild it")
        if files != zip_files or info != zip_info:
            raise PackageError(f"{platform} directory and ZIP differ")
        print(f"Verified {platform}: {directory} and {archive}")


def destination(platform: str, project: Path | None, user: bool) -> Path:
    base = Path.home() if user else (project or Path.cwd()).expanduser().resolve()
    parts = USER_PLATFORMS[platform] if user else PLATFORMS[platform]
    return base.joinpath(*parts, NAME)


def install(args: argparse.Namespace) -> None:
    package = args.package or DEFAULT_OUTPUT / args.platform / NAME
    files, info = read_package(package, args.platform)
    target = destination(args.platform, args.project, args.user)
    if target.resolve() == SOURCE.resolve():
        raise PackageError("Refusing to replace canonical source")
    if target.exists() or target.is_symlink():
        existing, _ = read_package(target, args.platform)
        if existing == files:
            print(f"Already installed and verified: {target}")
            return
        if not args.update:
            raise PackageError(f"Existing installation differs: {target}; inspect it and use --update")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".skill-install-", dir=target.parent))
    keep_backup = False
    try:
        new = temporary / NAME
        previous = temporary / "previous"
        materialize(new, files)
        read_package(new, args.platform)
        if target.exists():
            target.rename(previous)
        try:
            new.rename(target)
        except OSError:
            if previous.exists():
                try:
                    previous.rename(target)
                except OSError as error:
                    keep_backup = True
                    raise PackageError(f"Install and rollback failed; previous files remain at {previous}: {error}") from error
            raise
    finally:
        if not keep_backup:
            shutil.rmtree(temporary, ignore_errors=True)
    print(f"Installed {args.platform}: {target}")
    print(f"Source commit: {info['source_commit'] or 'unknown'} ({info['source_status']}); "
          f"content SHA-256: {info['source_tree_sha256']}")


def check(args: argparse.Namespace) -> None:
    target = destination(args.platform, args.project, args.user)
    installed, info = read_package(target, args.platform)
    if args.against:
        expected, _ = read_package(args.against, args.platform)
        if installed != expected:
            raise PackageError("Installed version differs from the selected distribution")
    print(f"Installation verified: {target}")
    print(f"Source commit: {info['source_commit'] or 'unknown'} ({info['source_status']}); "
          f"content SHA-256: {info['source_tree_sha256']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("build", "verify"):
        p = sub.add_parser(command)
        p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    for command in ("install", "check"):
        p = sub.add_parser(command)
        p.add_argument("--platform", choices=PLATFORMS, required=True)
        scope = p.add_mutually_exclusive_group()
        scope.add_argument("--project", type=Path, help="project root (default: current directory)")
        scope.add_argument("--user", action="store_true", help="install for the current OS user")
        if command == "install":
            p.add_argument("--package", type=Path, help="built skill directory or platform ZIP")
            p.add_argument("--update", action="store_true", help="replace an intact managed older version")
        else:
            p.add_argument("--against", type=Path, help="also compare with this skill directory or ZIP")
    args = parser.parse_args()
    try:
        if args.command == "build":
            build(args.output.resolve())
        elif args.command == "verify":
            verify(args.output.resolve())
        elif args.command == "install":
            install(args)
        else:
            check(args)
    except (PackageError, OSError, ValueError) as error:
        print(f"Skill package error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
