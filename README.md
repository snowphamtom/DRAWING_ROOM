# DRAWING_ROOM

A webpage shelf for design concepts.

**Not MAGPIE** (19/658,750 stays that filing).  
**Not CeilingGate** (All Gas ship stays that repo).  
**Not Seraphim Organizer.**

This room only holds plates: a title, a short glance, an optional link, an optional image.

## Current Status (2026-11-08) — Residual-Honest

| Surface | Status |
|---------|--------|
| Concept shelf (`docs/concepts.json`) | Live, editable by push |
| CDN face | https://cdn.jsdelivr.net/gh/snowphamtom/DRAWING_ROOM@main/docs/index.html |
| GitHub Pages | URL reserved; Settings → Pages still needs human flip (404 until then) |
| Vercel | Blocked on team `monstersink` re-auth (403 last measured) |
| Scope | Design-concept plates only; no product rename, no MAGPIE claim |

## Live

Working public face (CDN mirror of `docs/`, not a new product):  
https://cdn.jsdelivr.net/gh/snowphamtom/DRAWING_ROOM@main/docs/index.html

GitHub Pages URL (still 404 until Settings → Pages is flipped):  
https://snowphamtom.github.io/DRAWING_ROOM/

## Add a plate

Edit `docs/concepts.json` and push. The page reads that file.

```json
{
  "id": "plate-04",
  "title": "Name of the concept",
  "glance": "One honest sentence.",
  "href": "https://example.com",
  "image": "plates/optional.png",
  "state": "open"
}
```

`state` is `live` (has a public face), `open` (shelf waiting), or `hold` (do not ship).

## Local

```bash
python3 -m http.server 8080 --directory docs
```
