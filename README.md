# BODYFRAME Pack

Mod pack for the BODYFRAME launcher (Minecraft 1.21.1, NeoForge 21.1.267).

- `manifest.json` - list of files the launcher keeps in sync (path, size, sha256, download URL).
- Mod jars live in the GitHub release `mods` (they are too big for plain git).
- `tools/make_manifest.py` regenerates the manifest from the jars in `mods/`.

## Updating a mod
1. Put the new jar into `mods/` (remove the old one).
2. Upload it to the `mods` release: `gh release upload mods mods/<file>.jar` (and delete the old asset).
3. Regenerate the manifest with the new asset URLs and push it. Launchers pick it up on the next Play.
