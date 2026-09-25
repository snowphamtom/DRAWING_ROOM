# DRAWING_ROOM

A webpage shelf for design concepts.

**Not MAGPIE** (19/658,750 stays that filing).
**Not CeilingGate** (All Gas ship stays that repo).
**Not Seraphim Organizer.**

This room only holds plates: a title, a short glance, an optional link, an optional image.

## Live

Working public face (CDN mirror of `docs/`, not a new product):
https://cdn.jsdelivr.net/gh/snowphamtom/DRAWING_ROOM@main/docs/index.html

GitHub Pages URL (still 404 until Settings → Pages is flipped):
https://snowphamtom.github.io/DRAWING_ROOM/

Vercel deploy of this repo needs the Vercel connector re-authed for team `monstersink` (403 this pass).

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
