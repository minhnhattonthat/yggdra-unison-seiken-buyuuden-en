# Synopsis - Yggdra Unison: Seiken Buyuuden

A "fandisc" real-time strategy spin-off of Yggdra Union (Sting, DS 2009). No linear plot: the player picks one of 12
armies (Yggdra and Milanor at first; 10 more unlock) and conquers the continent territory by territory. Most text
is short barks, so tone and character voice carry everything (docs/style-reference.md).

## Setting
Year 1490 M.D. Emperor Gulcasa's New Bronquian Empire takes Fort/Castle Karona on the Fantasinian border; the
King of Fantasinia dies. Unlike Yggdra Union, every power now strikes out to conquer the continent. Princess
Yggdra holds the Holy Sword Gran Centurio ("justice lies with the Holy Sword").

## Armies (faction table A7D00; leader in brackets)
New Bronquian Empire (Gulcasa), Kingdom of Fantasinia (Yggdra), Milanor's thieves (Milanor), Embellia, the Undine
realm (Emelone), House Branthese / Black Rose (Roswell), House Esmeralda / White Rose (Rosary), Ortega Brigands
(Ortega), Dort's Bandits (Dort), Theocracy of Meria (Juvelon), Temple Knights (Gordon), Forest Alliance (Kylier /
Pamela...), Nessiah's forces (Nessiah, DS-only; Mistel is the other DS-only playable).

## Turn structure (where text appears)
- Preparation: pick a face-down card; a scout reports battles between other generals and disasters (SPMES_WR:
  sentences built from fragments: place + "at" + event).
- Combat (300 s): capture the enemy general's fortress. Units clash; Unison Attacks via the Impact Circle. Duel
  Events (SPMES files) are short conversations when linked characters meet: lines change by attacker, win, loss
  or death. Battle barks (MESSAGE files): start, deploy, capture a village, defend, win/lose a clash, retreat.
- After a win: the captured general can be recruited (prisoner talk), units are rewarded with items they like or
  dislike (prize talk; item "who can equip" text is often a joke about the character), treasure hunts send a
  general into a 30-step labyrinth (found / found nothing lines: SPMES_TRE, MESSAGE).
- Medallions: two per turn, used for effects (MESSAGE lines).
- Ending: each character gets an epithet title by performance (EDMES: low ranks humorous or insulting, high ranks
  heroic), an epilogue paragraph, and a Hall of Fame line that depends on their VIT (MESSAGE168).

## Who is who (relations translators need)
- Yggdra <-> Milanor allies; Milanor calls her "Princess". Durant is her knight. Kylier likes Milanor.
- Roswell (Black Rose) and Rosary (White Rose) are rival heads of Verlaine's two houses.
- Aegina and Luciana are twin sisters (Twin Valkyries), Gulcasa's loyal subordinates; they may be of royal blood
  (Artwaltz) - don't reveal it unless a line does.
- Leon (Black Knight) is Elena's brother; Elena is a trainee assassin under Zilva ("Zilva-sama").
- Emilia is Gulcasa's half-sister ("Big Brother"); she hates being treated as a child.
- Baldus: old Bronquian general, archaic speech. Eudy: Court Magician. Inzaghi: mercenary captain, Luciana's man.
- Canaan and Monica: Bronquian village militia, lovers. Russell: ex-imperial Astral Fencer, mourns his fiancee Flone.
- Emelone: Undine queen; Ishiene her devoted general; Nietzsche a naive Undine girl. Undines are all women.
- Juvelon: cowardly cardinal; Mardym, his archbishop, manipulates him; Amareus, his devoted assassin.
- Ortega (brigands) and Dort (desert bandits) are rival bandit kings; Flunky is Milanor's dim, loyal underling.
- Mizer: bounty hunter after Yggdra, spends everything on shoes. Pamela: greedy, cheeky ghost witch.
- Mistel: a gentle "full-time housewife" who is far stronger than she looks. Nessiah: polite imperial strategist,
  secretly a Fallen Angel seeking revenge on the gods; Shimobe is his servant. Sodom and Mamorigami are monsters.
