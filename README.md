# DRAWING_ROOM

A webpage shelf for design concepts.

**Not MAGPIE** (19/658,750 stays that filing).  
**Not CeilingGate** (All Gas ship stays that repo).  
**Not Seraphim Organizer.**

This room only holds plates: a title, a short glance, an optional link, an optional image.

## Current Status (2026-11-08) — Residual-Honest

| Surface | Status |
|---------|--------|
| **Primary live face** | http://sequesteredyeti.art/DRAWING_ROOM/ (user-site mirror; custom domain) |
| CDN face | https://cdn.jsdelivr.net/gh/snowphamtom/DRAWING_ROOM@main/docs/index.html |
| Source of truth | This repo (`docs/`). Mirror on user site keeps custom domain path alive. |
| Project Pages workflow | Present. Optional if Settings → Pages is enabled. |
| Scope | Design-concept plates only; no product rename, no MAGPIE claim |

## Live

**Working now:**  
http://sequesteredyeti.art/DRAWING_ROOM/  
https://cdn.jsdelivr.net/gh/snowphamtom/DRAWING_ROOM@main/docs/index.html

## Add a plate

Edit `docs/concepts.json` in this repo and push. Then mirror the same change into `snowphamtom.github.io/DRAWING_ROOM/concepts.json` (or re-run the mirror step) so the custom-domain face stays in sync.

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
