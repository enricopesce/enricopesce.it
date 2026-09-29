#!/usr/bin/env python3
"""Fail the build when generated Hugo output violates the site's SEO contract."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


BASE_URL = "https://www.enricopesce.it/"
BASE_HOST = urlparse(BASE_URL).netloc


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonicals: list[str] = []
        self.alternates: dict[str, str] = {}
        self.description = ""
        self.html_lang = ""
        self.h1_count = 0
        self.images: list[dict[str, str]] = []
        self.json_ld: list[str] = []
        self.links: list[str] = []
        self.meta: list[dict[str, str]] = []
        self.refresh = False
        self.title = ""
        self._capture_title = False
        self._capture_json = False
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key.lower(): value or "" for key, value in attrs_list}
        tag = tag.lower()
        if tag == "html":
            self.html_lang = attrs.get("lang", "").lower()
        elif tag == "title":
            self._capture_title = True
            self._buffer = []
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            self.meta.append(attrs)
            if attrs.get("name", "").lower() == "description":
                self.description = attrs.get("content", "").strip()
            if attrs.get("http-equiv", "").lower() == "refresh":
                self.refresh = True
        elif tag == "link":
            rel = attrs.get("rel", "").lower().split()
            href = attrs.get("href", "")
            if "canonical" in rel:
                self.canonicals.append(href)
            if "alternate" in rel and attrs.get("hreflang"):
                self.alternates[attrs["hreflang"].lower()] = href
        elif tag == "img":
            self.images.append(attrs)
        elif tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self._capture_json = True
            self._buffer = []

        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title" and self._capture_title:
            self.title = "".join(self._buffer).strip()
            self._capture_title = False
            self._buffer = []
        elif tag == "script" and self._capture_json:
            self.json_ld.append("".join(self._buffer).strip())
            self._capture_json = False
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._capture_title or self._capture_json:
            self._buffer.append(data)


def normalize_url(value: str) -> str:
    parsed = urlparse(value)
    path = parsed.path or "/"
    if not Path(path).suffix and not path.endswith("/"):
        path += "/"
    return f"{parsed.scheme or 'https'}://{parsed.netloc or BASE_HOST}{path}"


def local_path(output: Path, url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != BASE_HOST:
        return None
    path = unquote(parsed.path or "/").lstrip("/")
    candidate = output / path
    if parsed.path.endswith("/") or not candidate.suffix:
        candidate /= "index.html"
    return candidate


def robots_value(page: PageParser) -> str:
    for meta in page.meta:
        if meta.get("name", "").lower() == "robots":
            return meta.get("content", "").lower()
    return ""


def properties(page: PageParser, name: str) -> list[str]:
    return [
        meta.get("content", "")
        for meta in page.meta
        if meta.get("property", "").lower() == name.lower()
    ]


def parse_sitemaps(output: Path, errors: list[str]) -> set[str]:
    urls: set[str] = set()
    queue = [output / "sitemap.xml"]
    seen: set[Path] = set()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    while queue:
        sitemap = queue.pop()
        if sitemap in seen:
            continue
        seen.add(sitemap)
        try:
            root = ET.parse(sitemap).getroot()
        except (OSError, ET.ParseError) as exc:
            errors.append(f"invalid sitemap {sitemap}: {exc}")
            continue
        if root.tag.endswith("sitemapindex"):
            for loc in root.findall("sm:sitemap/sm:loc", namespace):
                target = local_path(output, (loc.text or "").strip())
                if target is not None:
                    if target.name == "index.html":
                        target = target.parent.with_suffix(".xml")
                    queue.append(target)
        else:
            for loc in root.findall("sm:url/sm:loc", namespace):
                if loc.text:
                    urls.add(normalize_url(loc.text.strip()))
    return urls


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> int:
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    errors: list[str] = []
    pages: dict[Path, PageParser] = {}
    canonical_pages: dict[str, tuple[Path, PageParser]] = {}

    if not output.is_dir():
        print(f"SEO audit: output directory not found: {output}", file=sys.stderr)
        return 2

    for html_file in sorted(output.rglob("*.html")):
        parser = PageParser()
        try:
            parser.feed(html_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot parse {html_file}: {exc}")
            continue
        pages[html_file] = parser
        if parser.refresh:
            continue

        relative = html_file.relative_to(output)
        label = str(relative)
        robots = robots_value(parser)
        is_404 = relative.name == "404.html"

        if len(parser.canonicals) != 1:
            errors.append(f"{label}: expected exactly one canonical, found {len(parser.canonicals)}")
            continue
        canonical = normalize_url(parser.canonicals[0])
        canonical_target = local_path(output, canonical)
        if canonical not in canonical_pages or canonical_target == html_file:
            canonical_pages[canonical] = (html_file, parser)

        if not parser.title:
            errors.append(f"{label}: missing title")
        if not parser.description and not is_404:
            errors.append(f"{label}: missing meta description")
        if not robots:
            errors.append(f"{label}: missing robots directive")
        if not is_404 and "index" in robots and "noindex" not in robots and parser.h1_count != 1:
            errors.append(f"{label}: expected one h1, found {parser.h1_count}")
        for image in parser.images:
            if "alt" not in image:
                errors.append(f"{label}: image without alt attribute: {image.get('src', '')}")

        if "index" in robots and "noindex" not in robots:
            expected = local_path(output, canonical)
            if expected != html_file:
                errors.append(f"{label}: indexable canonical is not self-referencing: {canonical}")

        for raw_json in parser.json_ld:
            try:
                document = json.loads(raw_json)
            except json.JSONDecodeError as exc:
                errors.append(f"{label}: invalid JSON-LD: {exc}")
                continue
            graph = document.get("@graph", []) if isinstance(document, dict) else []
            for entity in graph:
                if not isinstance(entity, dict) or entity.get("@type") != "BlogPosting":
                    continue
                required = ("headline", "description", "datePublished", "dateModified", "author", "image")
                for key in required:
                    if not entity.get(key):
                        errors.append(f"{label}: BlogPosting missing {key}")
                if "articleBody" in entity:
                    errors.append(f"{label}: BlogPosting duplicates articleBody in the document head")
                try:
                    if parse_datetime(entity["dateModified"]) < parse_datetime(entity["datePublished"]):
                        errors.append(f"{label}: dateModified precedes datePublished")
                except (KeyError, TypeError, ValueError):
                    errors.append(f"{label}: invalid BlogPosting publication dates")
                author = entity.get("author", {})
                if not isinstance(author, dict) or not author.get("name") or not author.get("url"):
                    errors.append(f"{label}: BlogPosting author must expose name and URL")
                if not properties(parser, "og:image"):
                    errors.append(f"{label}: article missing og:image")
                if not properties(parser, "og:image:alt"):
                    errors.append(f"{label}: article missing og:image:alt")

    sitemap_urls = parse_sitemaps(output, errors)
    for canonical, (html_file, page) in canonical_pages.items():
        label = str(html_file.relative_to(output))
        robots = robots_value(page)
        is_indexable = "index" in robots and "noindex" not in robots
        is_404 = html_file.name == "404.html"
        is_self_canonical = local_path(output, canonical) == html_file
        if is_indexable and not is_404 and canonical not in sitemap_urls:
            errors.append(f"{label}: indexable canonical absent from sitemap: {canonical}")
        if not is_indexable and is_self_canonical and canonical in sitemap_urls:
            errors.append(f"{label}: noindex canonical present in sitemap: {canonical}")

        for language, target_url in page.alternates.items():
            if language == "x-default":
                continue
            target_canonical = normalize_url(target_url)
            target = canonical_pages.get(target_canonical)
            if target is None:
                errors.append(f"{label}: hreflang target is not a canonical page: {target_url}")
                continue
            source_language = next(
                (lang for lang, href in page.alternates.items() if normalize_url(href) == canonical and lang != "x-default"),
                page.html_lang,
            )
            reciprocal = target[1].alternates.get(source_language)
            if not reciprocal or normalize_url(reciprocal) != canonical:
                errors.append(
                    f"{label}: hreflang {language} target does not reciprocate {source_language}: {target_url}"
                )

        for reference in page.links:
            if reference.startswith(("#", "mailto:", "tel:", "data:", "javascript:", "//")):
                continue
            absolute = urljoin(canonical, reference)
            target_path = local_path(output, absolute)
            if target_path is not None and not target_path.exists():
                errors.append(f"{label}: broken internal reference: {reference}")

        path_parts = urlparse(canonical).path.strip("/").split("/")
        term_index = 1 if path_parts and path_parts[0] == "it" else 0
        if len(path_parts) == term_index + 2 and path_parts[term_index] in {"tags", "categories"}:
            html = html_file.read_text(encoding="utf-8")
            article_count = len(re.findall(r'class="[^"]*\btag-entry\b[^"]*"', html))
            if article_count == 1 and is_indexable:
                errors.append(f"{label}: single-article taxonomy term must be noindex")
            if article_count >= 2 and not is_indexable:
                errors.append(f"{label}: useful taxonomy hub with {article_count} articles must be indexable")

    for sitemap_url in sitemap_urls:
        path = urlparse(sitemap_url).path
        if re.search(r"/page/\d+/$", path) or path.endswith("/search/"):
            errors.append(f"sitemap contains excluded URL: {sitemap_url}")
        target = local_path(output, sitemap_url)
        if target is None or not target.exists():
            errors.append(f"sitemap URL has no generated page: {sitemap_url}")

    article_urls: set[str] = set()
    for canonical, (_, page) in canonical_pages.items():
        for raw_json in page.json_ld:
            try:
                graph = json.loads(raw_json).get("@graph", [])
            except (json.JSONDecodeError, AttributeError):
                continue
            if any(isinstance(entity, dict) and entity.get("@type") == "BlogPosting" for entity in graph):
                article_urls.add(canonical)

    for rss_file in (output / "index.xml", output / "it" / "index.xml"):
        try:
            root = ET.parse(rss_file).getroot()
        except (OSError, ET.ParseError) as exc:
            errors.append(f"invalid RSS feed {rss_file}: {exc}")
            continue
        for link in root.findall("./channel/item/link"):
            item_url = normalize_url((link.text or "").strip())
            if item_url not in article_urls:
                errors.append(f"{rss_file.relative_to(output)}: non-article item in RSS: {item_url}")

    robots_file = output / "robots.txt"
    robots_text = robots_file.read_text(encoding="utf-8") if robots_file.exists() else ""
    if f"Sitemap: {BASE_URL}sitemap.xml" not in robots_text:
        errors.append("robots.txt: missing production sitemap directive")

    llms_file = output / "llms.txt"
    if llms_file.exists():
        for url in re.findall(r"https://www\.enricopesce\.it/[^\s)>]*", llms_file.read_text(encoding="utf-8")):
            target = local_path(output, url.rstrip(".,"))
            if target is not None and not target.exists():
                errors.append(f"llms.txt: broken internal URL: {url}")
    else:
        errors.append("missing llms.txt")

    if errors:
        print(f"SEO audit failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    aliases = sum(1 for page in pages.values() if page.refresh)
    indexable = sum(
        1
        for _, page in canonical_pages.values()
        if "index" in robots_value(page) and "noindex" not in robots_value(page)
    )
    print(
        "SEO audit passed: "
        f"{len(canonical_pages)} canonical HTML pages, {indexable} indexable pages, "
        f"{len(sitemap_urls)} sitemap URLs, {len(article_urls)} articles, {aliases} aliases."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
