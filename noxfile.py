from __future__ import annotations

import logging
import os
import shutil
import stat
import sys
from pathlib import Path
from typing import Any, Mapping

import nox

DUMMY_PATH = Path(".hexdoc/dummy_book")

PDOC_FAVICON = "https://github.com/hexdoc-dev/hexdoc/raw/main/media/hexdoc.png"
PDOC_LOGO_LINK = "https://pypi.org/project/hexdoc/"
PDOC_LOGO = "https://github.com/hexdoc-dev/hexdoc/raw/main/media/hexdoc.svg"
PDOC_EDIT_URL = "https://github.com/hexdoc-dev/hexdoc/blob/main/src/hexdoc/"

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = [
    "pyright",
    "test",
    "test_build",
    "test_hexcasting",
    "test_copier",
]


# tests


@nox.session
def pyright(session: nox.Session):
    session.install("--upgrade", "pyright")
    session.install("-e", ".[test]")

    if os.getenv("RUNNER_DEBUG") == "1" or "--verbose" in session.posargs:
        session.run("pyright", "--version")
        session.run("pyright", "--warnings", "--verbose")
    else:
        session.run("pyright", "--warnings")


@nox.session(tags=["test"])
def test(session: nox.Session):
    session.install(".[test]")

    session.run("pytest", *session.posargs)


@nox.session(tags=["test"])
def test_build(session: nox.Session):
    session.install("-e", ".[test]", "-e", "./submodules/HexMod")

    env = {
        "GITHUB_REPOSITORY": "GITHUB_REPOSITORY",
        "GITHUB_SHA": "GITHUB_SHA",
        "GITHUB_PAGES_URL": "GITHUB_PAGES_URL",
        "DEBUG_GITHUBUSERCONTENT": "DEBUG_GITHUBUSERCONTENT",
    }

    session.run("hexdoc", "build", "--branch=main", env=env)

    session.run(
        "hexdoc",
        "--quiet-lang=ru_ru",
        "--quiet-lang=zh_cn",
        "build",
        "--branch=main",
        "--props=submodules/HexMod/doc/hexdoc.toml",
        env=env,
    )


@nox.session(tags=["test", "post_build"])
def test_hexcasting(session: nox.Session):
    session.install("-e", ".[test]", "-e", "./submodules/HexMod")

    session.run("pytest", "-m", "hexcasting", *session.posargs)


@nox.session(tags=["test", "post_build"])
def test_copier(session: nox.Session):
    session.install("-e", ".[test]", "-e", "./submodules/HexMod")

    template_repo = Path("submodules/hexdoc-hexcasting-template")
    rendered_template = template_repo / ".ctt" / "test_copier"

    shutil.rmtree(rendered_template, ignore_errors=True)
    session.run("ctt", "--base-dir", str(template_repo))
    session.run("git", "init", str(rendered_template), external=True)

    session.run("pytest", "-m", "copier", *session.posargs)


# pre-commit


@nox.session(python=False)
def precommit_pyright(session: nox.Session):
    session.run("pip", "install", "--upgrade", "pyright")
    session.run("pip", "install", "-e", ".[test]")

    session.run("pyright", "--warnings", *session.posargs)


# CI/CD


@nox.session
def pdoc(session: nox.Session):
    # docs for the docs!
    session.install("-e", ".[pdoc]")

    sys.path.insert(0, "src")

    from hexdoc.__version__ import VERSION

    sys.path.pop(0)

    commit = run_silent_external(session, "git", "rev-parse", "--short", "HEAD")

    session.run(
        "pdoc",
        "hexdoc",
        "--favicon",
        PDOC_FAVICON,
        "--logo-link",
        PDOC_LOGO_LINK,
        "--logo",
        PDOC_LOGO,
        "--edit-url",
        f"hexdoc={PDOC_EDIT_URL}",
        "--footer-text",
        f"Version: {VERSION} ({commit})",
        *session.posargs,
    )


@nox.session
def tag(session: nox.Session):
    session.install("packaging")

    sys.path.insert(0, "src")

    from hexdoc.__version__ import VERSION

    sys.path.pop(0)

    from packaging.version import Version

    message = "Automatic PEP 440 release tag"

    # validate some assumptions to make this simpler
    version = Version(VERSION)
    assert version.epoch != 0
    assert len(version.release) == 3

    major, minor, _ = version.release
    tag = f"v{version.epoch}!{major}"

    # always update the prerelease tag, and also update the release tag if needed
    update_git_tag(session, tag=tag + ".dev", message=message)
    if not version.is_prerelease:
        update_git_tag(session, tag=tag, message=message)

    tag += f".{minor}"

    update_git_tag(session, tag=tag + ".dev", message=message)
    if not version.is_prerelease:
        update_git_tag(session, tag=tag, message=message)


# development helpers


@nox.session
def hexdoc(session: nox.Session):
    session.install(".")
    session.run("hexdoc", *session.posargs)


@nox.session
def dummy_setup(session: nox.Session):
    session.install("copier")

    from copier import run_copy  # type: ignore

    sys.path.insert(0, ".")

    from test.tree import write_file_tree

    sys.path.pop(0)

    logging.getLogger("plumbum.local").setLevel(logging.WARNING)
    run_copy(
        "gh:hexdoc-dev/hexdoc-mod-template",
        DUMMY_PATH,
        cleanup_on_error=False,
        defaults=True,
        overwrite=True,
        data=dict(
            modid="dummy",
            author="author",
            multiloader=False,
        ),
    )

    session.log(f"write_file_tree({DUMMY_PATH}, ...)")
    write_file_tree(
        DUMMY_PATH,
        {
            "doc": {
                "resources": {
                    "assets/dummy/patchouli_books/dummybook": {
                        "en_us": {
                            "categories/foo.json": {
                                "name": "Dummy Category",
                                "icon": "minecraft:amethyst_shard",
                                "description": "Foo bar baz qux quux corge grault garply waldo fred plugh xyzzy thud",
                                "sortnum": 0,
                            },
                            "entries/bar.json": {
                                "name": "Dummy Entry",
                                "category": "dummy:foo",
                                "icon": "minecraft:textures/mob_effect/nausea.png",
                                "sortnum": 0,
                                "pages": [
                                    {
                                        "type": "patchouli:text",
                                        "text": "Dummy Page",
                                    },
                                    {
                                        "type": "dummy:example",
                                        "example_value": "insert funny message here",
                                    },
                                ],
                            },
                            "entries/patchistuff.json": {
                                "name": "Patchouli Stuff",
                                "category": "dummy:foo",
                                "icon": "minecraft:book",
                                "sortnum": 0,
                                "pages": [
                                    {
                                        "type": "patchouli:multiblock",
                                        "name": "MultiBlock Test",
                                        "multiblock": {
                                            "pattern": [
                                                [
                                                    " GRG ",
                                                    "GGRGG",
                                                    "RRRRR",
                                                    "GGRGG",
                                                    " GRG ",
                                                ],
                                                [
                                                    "GG GG",
                                                    "G   G",
                                                    "     ",
                                                    "G   G",
                                                    "GG GG",
                                                ],
                                                [
                                                    "G   G",
                                                    "     ",
                                                    "     ",
                                                    "     ",
                                                    "G   G",
                                                ],
                                                [
                                                    "G   G",
                                                    "     ",
                                                    "  0  ",
                                                    "     ",
                                                    "G   G",
                                                ],
                                                [
                                                    "_WWW_",
                                                    "WWWWW",
                                                    "WWWWW",
                                                    "WWWWW",
                                                    "_WWW_",
                                                ],
                                            ],
                                            "mapping": {
                                                "G": "minecraft:gold_block",
                                                "W": "#minecraft:wool",
                                                "R": "minecraft:terracotta",
                                            },
                                        },
                                        "text": "Multi Block Test !",
                                    },
                                    {
                                        "type": "patchouli:quest",
                                        "trigger": "story/smelt_iron",
                                        "text": "Wow, what a wonderful quest this is here",
                                    },
                                ],
                            },
                            "entries/otherrecipes.json": {
                                "name": "More Recipe Types",
                                "category": "dummy:foo",
                                "icon": "minecraft:stonecutter",
                                "sortnum": 0,
                                "pages": [
                                    {
                                        "type": "patchouli:stonecutting",
                                        "recipe": "dummy:test_stonecutting",
                                        "text": "Very true and valid stonecutting recipe",
                                    },
                                    {
                                        "type": "patchouli:smithing",
                                        "recipe": "dummy:test_smithing_trim",
                                        "text": "Pretty armor!",
                                    },
                                    {
                                        "type": "patchouli:crafting",
                                        "recipe": "dummy:test_crafting",
                                    },
                                ],
                            },
                            "entries/smelting.json": {
                                "name": "Smelting",
                                "category": "dummy:foo",
                                "icon": "minecraft:furnace",
                                "sortnum": 0,
                                "pages": [
                                    {
                                        "type": "patchouli:smelting",
                                        "recipe": "dummy:test_smelting",
                                        "text": "Smelting Time !",
                                    },
                                    {
                                        "type": "patchouli:smoking",
                                        "recipe": "dummy:test_smoking",
                                        "text": "Smoking Time !",
                                    },
                                    {
                                        "type": "patchouli:campfire_cooking",
                                        "recipe": "dummy:test_campfire",
                                        "text": "Campfire Time !",
                                    },
                                    {
                                        "type": "patchouli:blasting",
                                        "recipe": "dummy:test_blasting",
                                        "text": "Blasting Time !",
                                    },
                                ],
                            },
                        },
                    },
                    "data/dummy": {
                        "patchouli_books/dummybook/book.json": {
                            "name": "Dummy Book",
                            "landing_text": "Lorem ipsum dolor sit amet",
                            "use_resource_pack": True,
                            "i18n": False,
                        },
                        "recipes": {
                            "test_blasting.json": {
                                "type": "minecraft:blasting",
                                "experience": 0.1,
                                "ingredient": {"item": "minecraft:raw_iron"},
                                "result": "minecraft:iron_ingot",
                            },
                            "test_campfire.json": {
                                "type": "minecraft:campfire_cooking",
                                "experience": 0.1,
                                "ingredient": {"item": "minecraft:potato"},
                                "result": "minecraft:baked_potato",
                            },
                            "test_crafting.json": {
                                "type": "minecraft:crafting_shaped",
                                "pattern": [" DD", " SD", "S  "],
                                "key": {
                                    "S": {"item": "minecraft:stick"},
                                    "D": {"item": "minecraft:diamond"},
                                },
                                "result": {
                                    "item": "minecraft:diamond_pickaxe",
                                    "count": 3,
                                },
                            },
                            "test_smelting.json": {
                                "type": "minecraft:smelting",
                                "cookingtime": 200,
                                "experience": 0.1,
                                "ingredient": {"item": "minecraft:sand"},
                                "result": "minecraft:glass",
                            },
                            "test_smithing_trim.json": {
                                "type": "minecraft:smithing_trim",
                                "base": {"item": "minecraft:netherite_chestplate"},
                                "template": {
                                    "item": "minecraft:wayfinder_armor_trim_smithing_template"
                                },
                                "addition": {"item": "minecraft:gold_ingot"},
                            },
                            "test_smoking.json": {
                                "type": "minecraft:smoking",
                                "experience": 0.1,
                                "ingredient": {"item": "minecraft:potato"},
                                "result": "minecraft:baked_potato",
                            },
                            "test_stonecutting.json": {
                                "type": "minecraft:stonecutting",
                                "ingredient": {"item": "minecraft:stone"},
                                "result": "minecraft:stone_bricks",
                                "count": 9,
                            },
                        },
                    },
                },
                "hexdoc.toml": (
                    """\
                    modid = "dummy"
                    book = "dummy:dummybook"
                    default_lang = "en_us"
                    default_branch = "main"

                    resource_dirs = [
                        "resources",
                        { modid="minecraft" },
                        { modid="hexdoc" },
                    ]
                    export_dir = "src/hexdoc_dummy/_export/generated"

                    [template]
                    icon = "icon.png"
                    include = [
                        "dummy",
                        "hexdoc",
                    ]

                    [template.args]
                    mod_name = "Dummy"
                    author = "author"
                    show_landing_text = true
                    """
                ),
            },
            "gradle.properties": (
                """\
                modVersion=1.0.0
                minecraftVersion=1.20.1
                """
            ),
        },
    )

    with session.chdir(DUMMY_PATH):
        session.run("git", "init", ".", external=True)
        session.run("git", "add", ".", external=True)
        session.run("git", "commit", "-m", "Initial commit", external=True)


@nox.session
def dummy_hexdoc(session: nox.Session):
    session.install("-e", ".", "-e", f"./{DUMMY_PATH.as_posix()}")

    with session.chdir(DUMMY_PATH):
        session.run("hexdoc", *session.posargs)


@nox.session
def dummy_serve(session: nox.Session):
    session.install("-e", ".", "-e", f"./{DUMMY_PATH.as_posix()}")

    with session.chdir(DUMMY_PATH):
        session.run("nodemon", "--config", "./doc/nodemon.json", external=True)


@nox.session(python=False)
def dummy_clean(session: nox.Session):
    if DUMMY_PATH.is_dir():
        session.log(f"Removing directory: {DUMMY_PATH}")
        shutil.rmtree(DUMMY_PATH, onerror=on_rm_error)


# utils (not sessions)


def run_silent_external(
    session: nox.Session,
    *args: str,
    env: Mapping[str, str] | None = None,
):
    return run_silent(session, *args, env=env, external=True)


def run_silent(
    session: nox.Session,
    *args: str,
    env: Mapping[str, str] | None = None,
    external: bool = False,
):
    output: str | None = session.run(
        *args,
        env=env,
        silent=True,
        external=external,
    )
    assert output
    return output.strip()


def update_git_tag(session: nox.Session, *, tag: str, message: str):
    return session.run(
        "git",
        "tag",
        "-fam",
        message,
        tag,
        external=True,
        env=dict(
            GIT_COMMITTER_NAME="GitHub Actions",
            GIT_COMMITTER_EMAIL="41898282+github-actions[bot]@users.noreply.github.com",
        ),
    )


def on_rm_error(func: Any, path: str, exc_info: Any):
    # from: https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
    path_ = Path(path)
    path_.chmod(stat.S_IWRITE)
    path_.unlink()
