#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道53宿 + 起点・終点の英語説明文データベース
"""

# 説明文: data_number → 英語説明文
DESCRIPTIONS_EN = {
    # 起点
    0: "The starting point of the Tokaido and all five major routes from Edo. This historic bridge has been the center of transportation and commerce from the Edo period to modern Tokyo, where countless travelers began their long journeys.",
    
    # 江戸エリア（1-15宿）
    1: "The first post town on the Tokaido. During the Edo period, it bustled with pleasure quarters and tea houses, attracting many travelers.",
    
    2: "A post town famous for the Rokugo River crossing at Tamagawa. It flourished as a renowned site in Musashi Province with many travelers passing through.",
    
    3: "A historically significant post town that became an open port in the late Edo period. Located in present-day Kanagawa Ward, Yokohama, it prospered as a foreign settlement.",
    
    4: "A post town known for the difficult Gonta-zaka slope. Ancient Tokaido roads still remain, and it was depicted in Hiroshige's ukiyo-e prints.",
    
    5: "One of the largest post towns on the Tokaido. As a transportation hub at the junction with Kamakura Road, it bustled with many travelers.",
    
    6: "A post town that flourished as a temple town of Yugyoji Temple. It was also the junction point of Enoshima Road, the pilgrimage route to Enoshima Shrine.",
    
    7: "An important post town at the Sagami River ferry crossing. Located in the center of the Sagami Plain, it is now famous for its Tanabata Festival. During the Edo period, it flourished as a key point on the Tokaido.",
    
    8: "A beautiful pine-lined post town overlooking Sagami Bay. Loved as a villa location for politicians and writers in the Meiji era, it is still visited by many tourists as a hot spring resort.",
    
    9: "A large post town that flourished as a castle town of the Hojo clan. A historic tourist destination centered around Odawara Castle, known for products like kamaboko and pickled plums. Travelers would rest here before tackling the steep mountain roads of Hakone.",
    
    10: "The most difficult mountain checkpoint post town feared on the Tokaido. An important rest stop for travelers crossing the steep 'Hakone Hachiri' mountain roads, it continues to be loved as one of Japan's premier hot spring tourist destinations worldwide.",
    
    11: "A post town famous for the spring water from Mount Fuji. It has long prospered as a temple town of Mishima Taisha Shrine.",
    
    12: "A port town facing Suruga Bay, proud of its fresh seafood. Known as the birthplace of dried fish, it is also popular as a scenic spot with views of Mount Fuji.",
    
    13: "A post town depicted in Hiroshige's ukiyo-e as a scenic spot with views of Mount Fuji. Beautiful scenery still remains today.",
    
    14: "A post town located at the foot of Mount Fuji. It is an area where the culture and history of the Edo period remain strong.",
    
    15: "A post town famous for Hiroshige's snow scenes. It charms visitors with beautiful views of Mount Fuji and historic streetscapes.",
    
    # 東海道エリア（16-34宿）
    16: "A small post town along Suruga Bay famous for sakura shrimp. A scenic location where you can enjoy beautiful coastline and stunning views of Mount Fuji, also depicted in Hiroshige's ukiyo-e.",
    
    17: "A post town that prospered as a villa location for politicians in the Meiji era. A place that served as a stage for history and politics.",
    
    18: "A port town currently functioning as Shimizu Port. It played an important role as a distribution center for Shizuoka tea.",
    
    19: "A post town that developed as a castle town of Sunpu Castle. It was also the political center where Tokugawa Ieyasu spent his later years.",
    
    20: "A post town famous for tororo soup. The birthplace of this historic specialty dish said to have been visited by Matsuo Basho, still attracting many tourists seeking its famous cuisine.",
    
    21: "A mountain post town known as a production area of Shizuoka tea. A land where beautiful tea plantation landscapes spread.",
    
    22: "A modern post town famous for Shizuoka tea and soccer. An attractive region where tradition and modernity merge, also known for wisteria flowers.",
    
    23: "A post town that prospered with Oigawa River crossings. The stage of the saying 'Even Hakone's eight ri can be crossed on horseback, but the impassable Oi River.'",
    
    24: "A post town famous for the Oigawa Railway's steam locomotives. A popular tourist destination blessed with tea plantations and hot springs, serving as an important base for travelers crossing the Oi River.",
    
    25: "A mountain post town famous for the Yonaki-ishi (Night-crying Stone) legend. A historic post town located at the foot of Sayo-no-Nakayama Pass.",
    
    26: "A post town that prospered as a castle town of Kakegawa Castle. The beautifully restored castle tower is still a highlight.",
    
    27: "The middle point of the Tokaido 53 stations, famous as 'Doman-naka' (dead center). A modern region flourishing with the tea industry, also serving as the starting point for pilgrimage to the Enshu Three Mountains.",
    
    28: "A post town that played an important role as a crossing point of the Tenryu River. A scenic location overlooking Enshu-nada.",
    
    29: "A castle town famous for eel cuisine. The central city of western Shizuoka Prefecture, also flourishing with the musical instrument industry.",
    
    30: "A post town that prospered at the Lake Hamana crossing. Even now, you can enjoy beautiful lakeside scenery and fresh seafood, particularly famous for eel dishes.",
    
    31: "A post town with an important checkpoint alongside Hakone. A historically significant point known for strict inspections.",
    
    32: "A coastal post town facing Enshu-nada. A beginner-friendly route where you can walk while feeling the sea breeze, with magnificent Pacific Ocean views spreading out.",
    
    33: "A valuable post town where the honjin building still exists. It retains a strong atmosphere of Edo-period post towns.",
    
    34: "A post town that prospered as a castle town of Yoshida Castle. Now developed as Toyohashi City, the gateway to Mikawa Province.",
    
    # 近畿エリア（35-53宿）
    35: "A post town famous for beautiful pine tree-lined roads. It prospered as the political and cultural center of Mikawa Province.",
    
    36: "A small post town adjacent to Goyu-juku. A land where historic cedar tree-lined roads are beautifully preserved.",
    
    37: "A post town famous for murasaki-mai (purple wheat). The beautiful rural landscape depicted in Hiroshige's ukiyo-e is charming.",
    
    38: "A historic castle town as the birthplace of Tokugawa Ieyasu. A tourist destination centered around Okazaki Castle.",
    
    39: "Present-day Chiryu City. It prospered as a post town famous for Chiryu Shrine and horse markets, attracting many merchants.",
    
    40: "A traditional craft post town famous for Narumi tie-dye. Beautiful indigo dyeing techniques are still passed down today.",
    
    41: "A post town that developed as a temple town of Atsuta Shrine. One of Japan's three great shrines, famous for the Kusanagi sword.",
    
    42: "A port town on Ise Bay famous for the 'Shichiri-no-Watashi' ferry and clam dishes. It prospered as a castle town.",
    
    43: "A post town that developed as a commercial port. Still occupying an important position as an industrial city in Mie Prefecture.",
    
    44: "A small post town with beautiful rural landscapes spreading out. A healing route walking through peaceful agricultural villages, where you can enjoy the nature of the four seasons.",
    
    45: "A small post town located in a quiet agricultural area. A place where old Japanese countryside scenery remains, where leisurely time flows.",
    
    46: "A post town that prospered as a castle town of Kameyama Castle. It was also important as a junction point of the Tokaido and Ise Kaido.",
    
    47: "The most beautifully preserved post town with Edo period streetscapes. Designated as an Important Preservation District for Groups of Traditional Buildings.",
    
    48: "A mountain post town located at the foot of Suzuka Pass. It prospered as a base for crossing the pass, located right next to Seki-juku.",
    
    49: "The first post town upon entering Omi Province after crossing Suzuka Pass. Also famous for Tsuchiyama tea production.",
    
    50: "A post town that prospered as a castle town of Minakuchi Castle. It has a prestigious history as a lodging place for Tokugawa shoguns during imperial visits.",
    
    51: "A small post town known for 'Ishibe no Sakichi.' Though a small post town, it played an important role as a transportation hub, known as the gateway to Omi Province.",
    
    52: "A transportation hub where the Tokaido and Nakasendo merge. The honjin is preserved and conveys the appearance of those days.",
    
    53: "The last post town on the Tokaido. A cultural post town located on the shores of Lake Biwa, famous for Otsu paintings.",
    
    # 終点
    54: "The endpoint of the Tokaido at Sanjo Ohashi Bridge in Kyoto. Built by order of Toyotomi Hideyoshi in 1590, it saw many travelers come and go as the western terminus of the Tokaido during the Edo period. A historic bridge still spanning the Kamo River today."
}
