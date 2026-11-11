Yggdra Unison: Seiken Buyuuden - English translation patch
==========================================================

Unofficial fan translation of Yggdra Unison: Seiken Buyuuden
(ユグドラ・ユニゾン 聖剣武勇伝; Nintendo DS, Sting, 2009).
Project page, source and bug reports:
https://github.com/minhnhattonthat/yggdra-unison-seiken-buyuuden-en

This zip holds only the patch and this README. It contains no game data.
Do not ask for or share patched ROMs.


What you need
-------------
Your own dump of the Japanese game, exactly this one:
  No-Intro: Yggdra Unison - Seiken Buyuuden (Japan).nds
  Size:   33554432 bytes
  CRC32:  B077FF01
  MD5:    63270f61c87f5f558f7ac3e63e495956
  SHA-1:  ef4d5e4fe56f9a0d3d114c0bd395db20d8dcb7f5

Any other dump (another revision, a trimmed or already-patched file) will not work.


How to patch
------------
The patch is xdelta (VCDIFF). Use any xdelta3 patcher:
  - Windows: xdelta UI or DeltaPatcher
  - Web: https://www.marcrobledo.com/RomPatcher.js/
  - Command line: xdelta3 -d -s "Yggdra Unison - Seiken Buyuuden (Japan).nds" @PATCH@ yggdra_en.nds

Patched ROM:
  CRC32:  @PATCHED_CRC32@
  SHA-1:  @PATCHED_SHA1@


Playing
-------
Tested in DeSmuME. Start from a cold boot of the patched ROM: savestates made
on the Japanese game or an older patch keep the old text and code in memory.


What is translated
------------------
  - Battle barks, duel events, prisoner and reward talk, tutorial
  - Menus, items, cards, skills, help, system messages
  - Prologues, faction intros, rumors, banners, HUD and menu graphics
  - Endings: epithets, epilogues, Hall of Fame, credits
Names follow Atlus's English Yggdra Union where one exists.


Known issues (cosmetic)
-----------------------
  - Some labels in small fixed cells are squeezed or short ("Btl / KO / Kill"
    on the record page, "Land" / "Gear" in Unit Info, battle HUD army names).
  - A few 6-px labels inside the tutorial's illustration shots stay Japanese
    (illegible at that size in either language).
Please report anything else at the project page (Issues); a savestate helps.


Credits
-------
Translation, hacking and tools: minhnhattonthat
Fonts: the game's own Latin glyphs; Liberation fonts (SIL OFL 1.1) for redrawn
graphics text.
Yggdra Unison: Seiken Buyuuden is (c) Sting. This project is not affiliated
with Sting or Atlus.

The translation was made with extensive AI assistance (Claude by Anthropic,
with Codex for review passes). Corrections are very welcome.
