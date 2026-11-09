# Glossary - Yggdra Unison: Seiken Buyuuden (NDS, 2009)

Binding for every translator and reviewer. Agents propose additions in reports; only the controller edits this file.
`tools/batches.py check` enforces every table row: if the JP form occurs in a line, one of the EN forms (split on
` / `) must occur in its English; an `Avoid` spelling fails the check.

## Rulings (asked of the user once; options and reasons in docs/decisions.md)
- Honorifics: kept, hyphenated, after a name: -san, -chan, -kun, -dono, -sama (D1; lint checks them after a
  katakana name). Titles are words, not honorifics: 王女 Princess, 陛下 Your Majesty / His Majesty, 殿下 Your
  Highness, 姫様/お姫様 Princess, 兄様 brother. Name order: Western (only given names occur).
- Romanisation: official Atlus English (Yggdra Union GBA/PSP, Blaze Union PSP) where one exists (D2), else Hepburn
  without macrons.
- Credits: English (D3). Abbreviations: never to fit; engine work first (D4). Report a line that cannot fit as LONG.
- Register: Atlus's Yggdra Union localisation is the model: plain modern English, fantasy-court formality for royals
  and knights, rough slang for bandits and thieves, no Japanese flavour words beyond the honorifics.
- Sound effects and roars: English onomatopoeia, keep the length feel: グワォォォ -> "Grrwaaargh!", ケケケッ ->
  "Kekekeh!", フフフ -> "Heh heh heh..." (or "Hmhmhm..." for a lady), ガハハハ -> "Gwahahaha!".

## Style rules
- Punctuation: 「」 -> "...", 『』 -> '...', … / ・・・ -> ..., keep !? / ?! as the JP has it, ー (stretched vowel) -> repeated letter,
  ～ -> ~ (allowed: the font has ~), full-width space -> one space. No [ ] < > (no glyphs).
- Box sizes are tight (dialogue bubble 142 px x 2 lines, about 22-26 letters a line). Fit by rephrasing, never by
  cutting meaning or abbreviating. Use `tools/batches.py wrap ID "text"` to break lines.
- Voices: docs/style-reference.md.

## Characters (unit table F5380; speaker ids in the batches are these)
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ユグドラ | Yggdra | | Princess of Fantasinia, holder of the Gran Centurio | |
| ミラノ | Milanor | | thief king, "Silver Wolf" | Milano |
| デュラン | Durant | | knight, leader of the Third Cavalry | Duran |
| キリエ | Kylier | | Griffon Rider, rides Al | Kyrie |
| ニーチェ | Nietzsche | | naive Undine girl | |
| ロズウェル | Roswell | | Necromancer, head of House Branthese (Black Rose) | |
| ロザリィ | Rosary | | Witch, head of House Esmeralda (White Rose) | |
| ラッセル | Russell | | Astral Fencer (魔剣士) | Russel |
| クルス | Cruz | | revolutionary, Karona Resistance | Kurusu |
| エレナ | Elena | | trainee assassin, Leon's sister | |
| ゴードン | Gordon | | Temple Knight, "Gordon of Steel" | |
| ガルカーサ | Gulcasa | | Bronquian Emperor, the Flame Emperor (焔帝) | Garcasa |
| ネシア | Nessiah | | imperial strategist, the Fallen Angel | Nesia |
| アイギナ | Aegina | | Twin Valkyrie | Aigina |
| ルシエナ | Luciana | | Twin Valkyrie | Lucienne |
| レオン | Leon | | the Black Knight | |
| エミリオ | Emilia | | Dragon General, Scarlet Princess (緋雪姫); hates being called a child | Emilio |
| バルドゥス | Baldus | | Dragon General, God of War (軍神) | |
| ユーディ | Eudy | | Court Magician | Yudi |
| ジルヴァ | Zilva | | assassin | Jilva |
| インザーギ | Inzaghi | | mercenary captain | |
| カナン | Canaan | | militia "hero", Monica's lover | Kanan |
| モニカ | Monica | | village girl from Flaube (フラウベ) | |
| イシーヌ | Ishiene | | Undine general, Emelone's right hand | |
| エメローネ | Emelone | | Queen of Embellia (Undines) | Emerone |
| コブン | Flunky | | Milanor's loyal underling (Atlus name) | Kobun |
| オルテガ | Ortega | | brigand king | |
| ドルト | Dort | | desert bandit king, old-man speech | Dolt |
| ミゼル | Mizer | | bounty hunter, shoe mania | Mizel |
| アマレウス | Amareus | | assassin serving Juvelon | |
| マルディム | Mardym | | archbishop, schemer | Mardim |
| ユベロン | Juvelon | | cardinal, coward | Yuberon |
| ヨハイム | Johaim | | pope ousted by Juvelon (MS_M_08 texture only; no official form found) | Yohaim |
| ユグドラ・ユリル・アルトワルツ | Yggdra Yuril Artwaltz | | full name (MS_PRO_001 texture) | |
| バロイ | Baroi | | archmage, founder of both Rose houses | Baloy |
| バーラバーサ | Barabasa | | sun god of Dort's bandits (MS_PRO_007, EPI_MES_07 textures) | |
| アリエス | Aries | | 告死天使 Angel of Death, fell at Lost Aries (MS_N_16) | |
| パメラ | Pamela | | ghost witch, money-mad, cheeky | |
| シモベ | Shimobe | | Nessiah's "eternal servant" | |
| ソドム | Sodom | | magic warrior | |
| マモリガミ | Mamorigami | | "living fortress" | |
| ミステール | Mistel | | "full-time housewife" (専業主婦) | Mistere |
| フローネ | Flone | | Russell's late fiancee | |
| 名無し兵士 | Nameless Soldier | | | |
| ブライ | Bly | | Mistel's grandfather (official Atlus) | Brai |
| ブロンガ | Brongaa | | official Atlus spelling | Bronga |

## Places
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ファンタジニア | Fantasinia | | kingdom | |
| ブロンキア | Bronquia / Bronquian | | empire | |
| エンベリア | Embellia | | Undine realm | |
| ヴァーレンヒルズ | Verlaine Hills | | 西 West / 東 East | |
| パルティナ | Paltina | | 北 North / 南 South | |
| カローナ | Karona | | Castle Karona | |
| フレアヴェルク | Flarewerk | | imperial capital | |
| ドロミノス | Drominos | | Drominos Marsh | |
| ジェノマ | Genoma | | Fort Genoma | |
| ロナリス | Lonaris | | Fort Lonaris | |
| イシュナート | Ishnad | | Fortress of Ishnad | |
| カノッサ | Canossa | | Canossa Road | |
| マキナ・ブリッジ | Machina Bridge | | | |
| フラム | Framm | | Framm Granary | |
| マルドゥーク | Marduk | | | |
| 嘆きの谷 | Valley of Lament | | | |
| ロスト・アリエス | Lost Aries | | | |
| ルナミナ | Lunamina | | Lunamina Pass | |
| レネシー | Lenessey | | Lenessey Mountains / volcanic region | |
| 白薔薇 | White Rose / Esmeralda | | 白薔薇館 White Rose Manor; 白薔薇家 House Esmeralda | |
| 黒薔薇 | Black Rose / Branthese | | 黒薔薇館 Black Rose Manor; 黒薔薇家 House Branthese | |
| フローランド | Floland | | | |
| フェリナス | Phelinas | | Phelinas Lakeside | |
| ロルカ | Lorca | | Lorca Lakeside | |
| オーランド | Orlando | | Orlando Plains | |
| 狼の口 | Jaws of the Wolf | | | |
| ノルン | Norn | | Norn Canyon | |
| ニルルド | Nyllard | | Nyllard Desert | |
| ミネルロード | Minerroad | | | |
| オズ | Oz | | Holy City of Oz | |
| ロンバルディア | Lombardia | | | |
| ロンバルド | Lombard | | city at the centre of Lombardia (MS_N_33) | |
| 修羅門 | Asura Gate | | Fortress of Ishnad (MS_N_06) | |
| ロドニー街道 / アルウィン大河 / カルナ運河 | Rodney Road / Alwin River / Karna Canal | | MS_N_09, MS_N_26 | |
| メリアータ | Meriata | | St. Meriata | |
| アンカルジア | Ancardia | | Ancardia, the Lost Paradise | |
| 凱旋門 | Arc of Triumph | | | |
| エリーゼ | Elise | | Undine water capital | |

## Factions and houses
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ブランテーゼ | Branthese | | House Branthese (Roswell) | |
| エスメラルダ | Esmeralda | | House Esmeralda (Rosary) | |
| テンプルナイツ | Temple Knights | | | |
| 聖騎士 | Temple Knight | | 聖騎士団 Temple Knights, 聖騎士領 Temple Knight Lands | holy knight / Holy Knight / holy knights / Holy Knights |
| エンベリア公国 | Duchy of Embellia / Embellian Duchy | | Emelone's realm | Principality |
| メリア | Meria | | the Meria faith; 教国 = Theocracy of Meria | |
| 新生ブロンキア帝国 | New Bronquian Empire | | | |
| 森の共同戦線 | Forest Alliance | | | |

## Classes (F5B88)
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| フェンサー | Fencer | | | |
| ヴァルキリー | Valkyrie | | | |
| ウンディーネ | Undine | | | |
| バンディット | Bandit | | | |
| グリフライダー | Griffon Rider | | | |
| ネクロマンサー | Necromancer | | | |
| ドラグーン | Dragoon | | | |
| タクティシャン | Tactician | | | |
| ジ・エインシャント | The Ancient | | | |
| スケルトン | Skeleton | | | |
| ゴーレム | Golem | | | |

## Game terms
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| 聖剣 | Holy Sword | | | |
| ユニゾンアタック | Unison Attack | | | |
| ユニゾン | Unison | | | |
| インパクトサークル | Impact Circle | | | |
| メダリオン | Medallion | | | |
| デュエル | Duel | | デュエルイベント Duel Event | |
| スマッシュヒット | Smash Hit | | | |
| クリティカルヒット | Critical Hit | | | |
| ノックバック | Knockback | | | |
| クラスチェンジ | Class Change | | | |
| 守将 | commander | | the general holding a territory | |
| 焔帝 | Flame Emperor | | Gulcasa | |
| 軍神 | God of War | | Baldus | |
| 戦乙女 | Valkyrie | | 双生の戦乙女 Twin Valkyries | |
| 黒騎士 | Black Knight | | Leon | |
| 魔剣士 | Astral Fencer | | Russell | |
| 銀狼 | Silver Wolf | | Milanor | |
| 宮廷魔術師 | Court Magician | | Eudy | |
| 緋雪姫 | Scarlet Princess | | Emilia | |
| 専業主婦 | housewife | | Mistel ("full-time housewife") | |
| 堕天 | Fallen | | 堕天のネシア Nessiah the Fallen | |
| 堕天使 | Fallen Angel | | Nessiah epithets (EDMES36) | |
| 預言者 | Prophet | | Nessiah epithets | |
| 教皇 | Pope | | Juvelon epithets | |
| 枢機卿 | Cardinal | | Juvelon | |
| 魔導師 | Mage | | Pamela, Rosary (大魔導師 Magus in the White Rose epithet) | |
| 流神 | Evangelist | | 流神の聖者 Evangelist Mardym (EDMES26 coinage, no Atlus name) | |
| 卑屈姫 | Sulky Princess | | Emilia epithet (EDMES18) | |
| ユミラ | Yumira | | Nessiah, SPMES030036 (Hepburn, no Atlus name found) | |
| ユメール | Yumeru | | ユメール人 "a Yumeru" (SPMES030036) | |
| 珍園 | Oddgarden | | 珍園マセラマティ item (both twins) | |
| 神園 | Godgarden | | 神園マセラマティ item (both twins) | |
| ロコン | Rokon | | 巨獣ロコンの骨 Bone of Giant Rokon | Rocon |
| ヤーデ | Yade | | 幻獣ヤーデのツノ Horn of Phantom Yade | |
| 一本鬼 | One-Horned Oni | | 豪槍一本鬼 One-Horned Oni Lance | |
| 賞金稼ぎ | Bounty Hunter | | Mizer | |

## Cards (A7E44; card names are also CARDNAME textures)
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| メイクドール | Make Doll | | | |
| ネクロゲート | Necrogate | | | |
| メデューサアイ | Medusa Eye | | | |
| ポイズンブレス | Poison Breath | | | |
| グラヴィティカオス | Gravity Chaos | | | |
| アイテムブレイク | Item Break | | | |
| スティール | Steal | | | |
| ブラッディクロー | Bloody Claw | | | |
| チャリオット | Chariot | | | |
| シールドバリア | Shield Barrier | | | |
| フレイム | Flame | | | |
| ブリザード | Blizzard | | | |
| サンダーボルト | Thunderbolt | | | |
| バニッシュ | Banish | | | |
| ドラゴンキラー | Dragon Killer | | | |
| アースクウェイク | Earthquake | | | |
| マインドチェンジ | Mind Change | | | |
| レヴォリューション | Revolution | | | |
| ジハード | Jihad | | | |
| サンクチュアリ | Sanctuary | | | |
| リフレッシュメント | Refreshment | | | |
| キスオブデス | Kiss of Death | | | |
| フォーチュン | Fortune | | | |
| ミラージュ | Mirage | | | |
| バンシーズクライ | Banshee's Cry | | | |
| アイヴィウィップ | Ivy Whip | | | |
| サンドストーム | Sandstorm | | | |
| マントラップ | Mantrap | | | |
| ロックフォール | Rockfall | | | |
| エースガード | Ace Guard | | | |
| ジェノサイド | Genocide | | | |
| リィンカーネーション | Reincarnation | | | |
| リヴェリオン | Rebellion | | | |
| ダイヤモンドダスト | Diamond Dust | | | |
| コーマカルマ | Coma Karma | | | |
| ジャッジメント・ゼロ | Judgment Zero | | | |

## Decisions from earlier batches
- b001-b004 faction lands (…領): Imperial / Kingdom / Embellian / Milanor's / Nessiah's / Forest / Theocracy /
  Bandit / Brigand / Black Rose / White Rose / Temple Knight Lands. Armies (…軍/団): Imperial Army, Royal Army,
  Embellian Army, Theocracy Army, Forest Army, Nessiah's Army, Thieves (Milanor), Bandits (Dort), Brigands (Ortega),
  Temple Knights, Black/White Rose Army. ネシア勢力 Nessiah's Forces; メリア教国 Theocracy of Meria.
- b001-b004 items: ドゼウ Loach, 斬鉄剣 Steelcutter, ロザリオ Rosario (not Rosary), サザンクロス Southern Cross,
  グランドクロス Grand Cross; キルアウト Kill Out; ユニット出撃 Unit Sorties.
- b001-b004 composite sentences (pieces joined by code before one draw, so a break may sit in any piece; lint checks
  every combination; keep these joins): "Battle won! " + army + " took\n" + territory + "!"; "Capital taken!\n" +
  lands + " are " + "all yours!"; "Headed here: " + unit + ",\n" + "already scheduled to go."; "Already sent: " +
  unit + ".\nBack in " + digits + " turn(s)."; "This turn's strategy card:\n" + card + "."; "This item is held by\n("
  + unit + ")\nso it can't be selected.". The Edit tool strips trailing spaces: set a piece ending in a space with
  `python tools/setval.py work/tl/bNNN.out.tsv ID 'text '`.
- b017-b024: 親分 Boss (Flunky to Milanor); ザコ small fry; 猊下 Your Eminence; 守り神様 guardian god (not the
  Mamorigami unit); オレ様 = Inzaghi's boastful "me" (the great me), never a name + -sama.
- b025-b032: 姐さん (Flunky) Sis; 砲台 cannon (capture-point cannon); アンク Ankh (Verlaine's Ankhs, Yggdra
  Union); 山賊 brigands (Ortega's), 盗賊 bandits (Dort's) / thieves (Milanor's).
- Phase 6 review fixes: weapon 槍 = Lance in item names too (魔槍 Demon Lance, 悲槍 Sorrow Lance, story "lance");
  ぶちクルス epithet = Hothead Cruz (EDMES20; ぶち elsewhere is the verb prefix, so no table row);
  ビッグオブ / グレートオブ / キングオブ / ゴッドオブ魔導師 = Big of / Great of / King of / God of Mages (broken-English
  gag kept).
- b005-b008 (help/system): 作戦カード strategy card; 攻撃兵器 siege weapon; 戦意 morale; 集落 village; 都市 city;
  鑑定所 Appraiser; 本拠地 home base; 攻撃拠点 attack base; 拠点 base; 出撃 deploy (出撃ボタン Sortie button);
  褒賞 reward; 戦功値 merit; 密偵 spies; 勢力 faction; 火炎/冷気/雷撃/暗黒/神聖 Fire/Ice/Lightning/Dark/Holy;
  夜間/昼間戦闘 night/day battle; 水辺 waterside; 戦力確認 Check Forces; ミラノ盗賊団 Milanor's Thieves;
  エンベリア公国 Duchy of Embellia (b009-b012 wrote "Principality": fix to Duchy in review); 五頭竜将 Five Dragon
  Generals; 敵将 foe general; 戦力外通告 dismiss; 探索 explore; ドルト盗賊団 Dort's Bandits; オルテガ山賊団 Ortega Brigands; 領主 lord;
  Texture atlases (phase 8): アイテム図鑑 Item Catalog; カード事典 Card Catalog; サウンドモード Sound Mode; 称号 Titles
  (配下/領主称号 Unit/Lord Titles); 残存戦力 Strength; terrain 街区 Town 街道 Road 荒野 Waste 砂漠 Desert 城砦 Fort
  森林 Forest 水辺 Water 草原 Plain 毒沼 Swamp 山岳 Peaks; speeds 激遅 Crawl 遅い Slow 普通 Normal 速い Fast; move
  types 騎馬 Horse 哨戒 Scout 水棲 Swim 鈍足 Heavy 飛行 Fly 歩行 Foot 夜襲 Night 竜騎 Dragon (20-px cells).
  ▲/▼ dropped, the sign carries it (ATK+2, DEF-1). Composite: "Attack base: " + n + " more can deploy!";
  unit + " will explore."; "This item is held by (" + unit + ")\nso it can't be selected."; unit + " has\njoined
  your forces!".
