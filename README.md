# DRAWING_ROOM

A webpage shelf for design concepts.

**Not MAGPIE** (19/658,750 stays that filing).
**Not CeilingGate** (All Gas ship stays that repo).
**Not Seraphim Organizer.**

This room only holds plates: a title, a short glance, an optional link, an optional image.

## Live

GitHub Pages (`docs/`):
https://snowphamtom.github.io/DRAWING_ROOM/

If the URL 404s, turn on Pages:
Repo → Settings → Pages → Deploy from branch `main` / folder `/docs`.

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
