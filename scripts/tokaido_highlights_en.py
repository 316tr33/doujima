#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道ハイライトキーワード 日本語→英語翻訳辞書
"""

HIGHLIGHTS_EN = {
    # 数字・順序
    "17の温泉地": "17 Hot Spring Areas",
    "53番目宿": "53rd Post Town",
    
    # 交通・施設
    "SL列車": "Steam Locomotive",
    "五街道起点": "Starting Point of Five Routes",
    "交通要衝": "Transportation Hub",
    "渡し場": "Ferry Crossing",
    "渡し舟": "Ferry Boat",
    "七里の渡し": "Shichiri Ferry",
    "大井川": "Oi River",
    "大井川温泉": "Oi River Hot Spring",
    "天竜川": "Tenryu River",
    "浜名湖": "Lake Hamana",
    "琵琶湖": "Lake Biwa",
    "芦ノ湖と富士山": "Lake Ashi & Mt. Fuji",
    "駿河湾": "Suruga Bay",
    "相模川渡し場跡": "Sagami River Ferry Site",
    "川越": "River Crossing",
    
    # 食べ物・名物
    "うなぎ料理": "Eel Cuisine",
    "かまぼこ博物館": "Kamaboko Museum",
    "とろろ汁": "Tororo Soup",
    "名物料理": "Specialty Cuisine",
    "桜えび": "Sakura Shrimp",
    "干物": "Dried Fish",
    "海産物": "Seafood",
    "海苔": "Seaweed",
    "蛤料理": "Clam Dishes",
    "近江牛": "Omi Beef",
    "静岡茶": "Shizuoka Tea",
    "茶産業": "Tea Industry",
    "土山茶": "Tsuchiyama Tea",
    
    # 地域・位置
    "どまん中": "Dead Center",
    "中間地点": "Midpoint",
    "最終休憩地": "Final Rest Stop",
    "東海道完歩地点": "Tokaido Completion Point",
    "三河国": "Mikawa Province",
    "近江国": "Omi Province",
    "江戸・東京中心": "Edo/Tokyo Center",
    "日本の道路元標": "Japan's Road Origin Marker",
    
    # 城・歴史的建造物
    "小田原城": "Odawara Castle",
    "掛川城": "Kakegawa Castle",
    "岡崎城": "Okazaki Castle",
    "桑名城": "Kuwana Castle",
    "水口城": "Minakuchi Castle",
    "亀山城": "Kameyama Castle",
    "吉田城": "Yoshida Castle",
    "駿府城": "Sunpu Castle",
    "浜松城": "Hamamatsu Castle",
    "天守閣": "Castle Tower",
    "城下町": "Castle Town",
    
    # 神社仏閣
    "三嶋大社": "Mishima Taisha Shrine",
    "熱田神宮": "Atsuta Shrine",
    "知立神社": "Chiryu Shrine",
    "三大神社": "Three Great Shrines",
    "草薙剣": "Kusanagi Sword",
    "遊行寺": "Yugyoji Temple",
    "本覚寺": "Honkakuji Temple",
    "平塚八幡宮": "Hiratsuka Hachimangu",
    "門前町": "Temple Town",
    
    # 関所・検問
    "箱根関所": "Hakone Checkpoint",
    "関所": "Checkpoint",
    "検問所": "Inspection Station",
    "歴史遺跡": "Historic Site",
    
    # 景観・自然
    "富士山景観": "Mt. Fuji Views",
    "富士山眺望": "Mt. Fuji Vista",
    "富士山湧水": "Mt. Fuji Spring Water",
    "富士山麓の宿場": "Mt. Fuji Foothill Post Town",
    "東海道松並木": "Tokaido Pine Tree Avenue",
    "松並木": "Pine Tree-Lined Road",
    "杉並木": "Cedar Tree Avenue",
    "茶畑": "Tea Plantations",
    "茶畑景観": "Tea Field Scenery",
    "田園風景": "Rural Landscape",
    "農村風景": "Agricultural Scenery",
    "農村地帯": "Farming Area",
    "海岸線": "Coastline",
    "湖景色": "Lake View",
    "潮風": "Sea Breeze",
    "遠州灘": "Enshu-nada",
    "雪景色": "Snow Scenery",
    "浮世絵": "Ukiyo-e",
    "歌川広重": "Hiroshige Utagawa",
    
    # 峠・山道
    "箱根関所": "Hakone Checkpoint",
    "権太坂の急坂": "Steep Gonta-zaka Slope",
    "東海道古道": "Ancient Tokaido Road",
    "宿場の歴史道": "Historic Post Town Road",
    "小夜の中山": "Sayo-no-Nakayama",
    "鈴鹿峠": "Suzuka Pass",
    "峠道": "Mountain Pass",
    "峠越え拠点": "Pass Crossing Base",
    "山間宿場": "Mountain Post Town",
    
    # 歴史・文化
    "江戸時代": "Edo Period",
    "江戸文化": "Edo Culture",
    "江戸街並み": "Edo Streetscape",
    "明治時代": "Meiji Era",
    "歴史保存地区": "Historic Preservation District",
    "伝統建造物": "Traditional Buildings",
    "商業中心": "Commercial Hub",
    "政治中心": "Political Center",
    "文化中心": "Cultural Center",
    "文化的": "Cultural",
    "政治史": "Political History",
    "開港史跡": "Port Opening Historic Site",
    "神奈川台関門跡": "Kanagawadai Checkpoint Ruins",
    "製紙産業の歴史": "Papermaking History",
    
    # 宿場関連
    "宿場町": "Post Town",
    "宿場文化": "Post Town Culture",
    "宿場まつり": "Post Town Festival",
    "宿場交流館": "Post Town Exchange Hall",
    "大宿場": "Large Post Town",
    "小宿場": "Small Post Town",
    "本陣現存": "Extant Honjin",
    "本陣保存": "Preserved Honjin",
    "本陣跡": "Honjin Ruins",
    "本陣・脇本陣跡": "Honjin & Waki-honjin Ruins",
    
    # 道・街道
    "街道分岐": "Highway Junction",
    "鎌倉道分岐点": "Kamakura Road Junction",
    "江島道分岐": "Enoshima Road Junction",
    "諺の舞台": "Proverb Stage",
    
    # 人物
    "徳川家康": "Tokugawa Ieyasu",
    "生誕地": "Birthplace",
    "松尾芭蕉": "Matsuo Basho",
    "豊臣秀吉建立": "Built by Toyotomi Hideyoshi",
    "旧伊藤博文邸": "Former Ito Hirobumi Residence",
    
    # 産業・経済
    "楽器産業": "Musical Instrument Industry",
    "商業港": "Commercial Port",
    "工業都市": "Industrial City",
    "港町文化": "Port Town Culture",
    "清水港": "Shimizu Port",
    "馬市": "Horse Market",
    
    # 伝統工芸
    "伝統工芸": "Traditional Crafts",
    "鳴海絞り": "Narumi Tie-Dye",
    "藍染め": "Indigo Dyeing",
    
    # 特殊な場所・施設
    "別荘地": "Villa District",
    "日本初海水浴場": "Japan's First Beach",
    "夜泣き石": "Night-Crying Stone",
    "商店街": "Shopping Street",
    "現代の名所": "Modern Landmark",
    "現代文化": "Contemporary Culture",
    
    # その他の特徴
    "むらさき麦": "Purple Wheat",
    "サッカー": "Soccer",
    "七夕まつり": "Tanabata Festival",
    "岳南電車の街": "Gakunan Railway Town",
    "名産地": "Production Area",
    "水源豊富": "Abundant Water",
    "癒やし": "Healing",
    "静寂": "Tranquility",
    "自然保護": "Nature Conservation",
    "田舎道": "Country Road",
    "鴨川の名橋": "Famous Kamo River Bridge",
    
    # サッカー・スポーツ
    "サッカー": "Soccer"
}
