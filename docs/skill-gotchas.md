# Skill gotchas (one line each: reference file, then the fact)

- references/setup.md: `fetch_emu.py` failed on this machine (504, then SSL CERTIFICATE_VERIFY_FAILED in urllib); `gh release download qa-2 -R minhnhattonthat/desmume` works. The zip unpacks to `tools/desmume/desmume-qa/`, which emu.py still finds.
- references/pipeline.md §Recon: kanji template matching (MS Gothic / Yu Gothic, 12-16 px, bbox-normalised correlation) got only 2-9/32 right on a bold outlined 16x16 4bpp DS font; budget for reading kanji by eye from sheets.
- references/platform-nds.md: Sting's DATA.SFS keeps its directory (hash, size, sector) inside arm9.bin, not in the archive; found by searching arm9 for the sector sequence of known file starts (stride-12 u32 1,4,6,7).
