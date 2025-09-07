// 東海道ウォーク ルート管理システム
// routes.html から抽出されたルート詳細データと表示機能

// ルート詳細データ
const routeData = {
  beginner: {
    title: "初心者コース",
    icon: "🌱",
    description:
      "東海道ウォーク入門に最適な、アクセスが良く見どころ豊富な5宿場を巡るコース",
    stations: [
      {
        number: 1,
        name: "日本橋",
        reading: "にほんばし",
        reason: "東海道の起点、歴史の始まり",
      },
      {
        number: 6,
        name: "藤沢",
        reading: "ふじさわ",
        reason: "遊行寺の門前町として栄えた宿場",
      },
      {
        number: 10,
        name: "箱根",
        reading: "はこね",
        reason: "関所と温泉で有名な難所の宿場",
      },
      {
        number: 15,
        name: "由比",
        reading: "ゆい",
        reason: "薩埵峠からの富士山の眺めが絶景",
      },
      {
        number: 53,
        name: "三条大橋",
        reading: "さんじょうおおはし",
        reason: "東海道の終点、京都の玄関口",
      },
    ],
    tips: [
      "各宿場間は電車でのアクセスが可能です",
      "1日1〜2宿場のペースでゆっくり楽しめます",
      "観光案内所で詳しい情報を入手できます",
      "写真撮影スポットが多く記念に残ります",
    ],
    duration: "1-2日",
    distance: "約20km",
    difficulty: "★☆☆☆☆",
  },
  scenic: {
    title: "風景コース",
    icon: "🌸",
    description:
      "四季折々の美しい自然風景と富士山の絶景を楽しめる8宿場を巡るコース",
    stations: [
      {
        number: 8,
        name: "平塚",
        reading: "ひらつか",
        reason: "湘南の海岸線と田園風景",
      },
      {
        number: 9,
        name: "大磯",
        reading: "おおいそ",
        reason: "松並木と相模湾の美しい景色",
      },
      {
        number: 11,
        name: "三島",
        reading: "みしま",
        reason: "富士山の眺望と楽寿園の自然",
      },
      {
        number: 15,
        name: "由比",
        reading: "ゆい",
        reason: "薩埵峠からの富士山絶景ポイント",
      },
      {
        number: 16,
        name: "蒲原",
        reading: "かんばら",
        reason: "雪景色で有名な広重の浮世絵の舞台",
      },
      {
        number: 22,
        name: "岡部",
        reading: "おかべ",
        reason: "梅の里として知られる風光明媚な宿場",
      },
      {
        number: 32,
        name: "白須賀",
        reading: "しらすか",
        reason: "遠州灘の海岸美と潮風",
      },
      {
        number: 45,
        name: "庄野",
        reading: "しょうの",
        reason: "鈴鹿山麓の自然豊かな里山風景",
      },
    ],
    tips: [
      "春は桜、秋は紅葉が美しい季節です",
      "富士山の眺望は天候に左右されるため天気予報をチェック",
      "カメラや望遠レンズがあると景色をより楽しめます",
      "早朝出発で朝日に照らされる富士山を狙いましょう",
    ],
    duration: "3-4日",
    distance: "約35km",
    difficulty: "★★★☆☆",
  },
  onsen: {
    title: "温泉コース",
    icon: "♨️",
    description:
      "歩いた疲れを癒やす温泉がある宿場を中心とした、リラックス重視のコース",
    stations: [
      {
        number: 7,
        name: "平塚",
        reading: "ひらつか",
        reason: "湘南ひらつか温泉で海を眺めながら入浴",
      },
      {
        number: 10,
        name: "箱根",
        reading: "はこね",
        reason: "箱根温泉郷で豊富な泉質を楽しむ",
      },
      {
        number: 11,
        name: "三島",
        reading: "みしま",
        reason: "楽寿園温泉で富士の伏流水を感じる",
      },
      {
        number: 18,
        name: "島田",
        reading: "しまだ",
        reason: "島田温泉で大井川の清流に癒される",
      },
      {
        number: 28,
        name: "見附",
        reading: "みつけ",
        reason: "磐田温泉で遠州平野を一望",
      },
      {
        number: 43,
        name: "桑名",
        reading: "くわな",
        reason: "多度温泉で養老山系の恵みを堪能",
      },
    ],
    tips: [
      "温泉の営業時間を事前に確認しておきましょう",
      "タオルや入浴用品を持参すると便利です",
      "日帰り入浴料金は1000円前後が一般的です",
      "温泉街での宿泊もおすすめです",
    ],
    duration: "2-3日",
    distance: "約28km",
    difficulty: "★★☆☆☆",
  },
  history: {
    title: "歴史探訪コース",
    icon: "🏯",
    description:
      "江戸時代の面影と重要な歴史的出来事の舞台を巡る本格的な歴史学習コース",
    stations: [
      {
        number: 1,
        name: "日本橋",
        reading: "にほんばし",
        reason: "五街道の起点、江戸の中心地",
      },
      {
        number: 3,
        name: "神奈川",
        reading: "かながわ",
        reason: "開港場として外国文化の玄関口",
      },
      {
        number: 10,
        name: "箱根",
        reading: "はこね",
        reason: "箱根関所で江戸時代の検問システムを学ぶ",
      },
      {
        number: 20,
        name: "府中",
        reading: "ふちゅう",
        reason: "駿府城下町として徳川家康ゆかりの地",
      },
      {
        number: 25,
        name: "日坂",
        reading: "にっさか",
        reason: "山中の険しい峠道と一里塚",
      },
      {
        number: 27,
        name: "袋井",
        reading: "ふくろい",
        reason: "東海道五十三次のちょうど真ん中",
      },
      {
        number: 41,
        name: "宮",
        reading: "みや",
        reason: "熱田神宮の門前町として栄えた",
      },
      {
        number: 47,
        name: "関",
        reading: "せき",
        reason: "東海道三関の一つ、鈴鹿関の要衝",
      },
      {
        number: 50,
        name: "水口",
        reading: "みなくち",
        reason: "水口城の城下町",
      },
      {
        number: 53,
        name: "三条大橋",
        reading: "さんじょうおおはし",
        reason: "京都の玄関口、公家文化の中心",
      },
    ],
    tips: [
      "各宿場の歴史資料館や博物館を訪問しましょう",
      "地元のボランティアガイドの説明を聞くと理解が深まります",
      "江戸時代の地図と現在の地図を比較してみましょう",
      "参勤交代や飛脚制度について事前学習がおすすめ",
    ],
    duration: "4-5日",
    distance: "約45km",
    difficulty: "★★★★☆",
  },
  complete: {
    title: "完全踏破コース",
    icon: "🎯",
    description:
      "日本橋から京都三条大橋まで、東海道五十三次すべてを踏破する究極のチャレンジ",
    stations: [
      {
        number: "1-17",
        name: "江戸エリア",
        reading: "えどえりあ",
        reason: "日本橋から興津まで17宿場",
      },
      {
        number: "18-32",
        name: "東海道エリア",
        reading: "とうかいどうえりあ",
        reason: "島田から白須賀まで15宿場",
      },
      {
        number: "33-53",
        name: "近畿エリア",
        reading: "きんきえりあ",
        reason: "新居から三条大橋まで21宿場",
      },
    ],
    tips: [
      "十分な体力づくりと装備の準備が必要です",
      "宿泊場所の事前予約は必須です",
      "荷物は最小限に抑え、宅配便を活用しましょう",
      "天候不良時の避難場所を把握しておきましょう",
      "家族や知人に行程を伝えておきましょう",
      "途中でのドロップアウトも選択肢として考えておきましょう",
    ],
    duration: "2-3週間",
    distance: "約500km",
    difficulty: "★★★★★",
    special: true,
  },
};

// ルート詳細表示機能
function initRouteDetails() {
  const detailButtons = document.querySelectorAll(".route-details-btn");
  const detailSection = document.getElementById("routeDetails");
  const detailContent = document.getElementById("routeDetailContent");

  if (!detailButtons.length || !detailSection || !detailContent) {
    console.log("Routes: 必要な要素が見つかりません");
    return;
  }

  detailButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const routeType = this.getAttribute("data-route");
      showRouteDetails(routeType);
    });
  });
}

function showRouteDetails(routeType) {
  const route = routeData[routeType];
  const detailSection = document.getElementById("routeDetails");
  const detailContent = document.getElementById("routeDetailContent");
  
  if (!route || !detailSection || !detailContent) {
    console.log("Routes: ルート詳細の表示に失敗しました");
    return;
  }

  const stationsHtml = route.stations
    .map((station) => {
      if (route.special) {
        return `
                    <div class="area-block">
                        <h4>${station.name}</h4>
                        <p class="area-reading">${station.reading}</p>
                        <p class="area-description">${station.reason}</p>
                    </div>
                `;
      } else {
        return `
                    <div class="station-item">
                        <div class="station-number">${station.number}</div>
                        <div class="station-info">
                            <h4>${station.name}</h4>
                            <p class="station-reading">${station.reading}</p>
                            <p class="station-reason">${station.reason}</p>
                        </div>
                    </div>
                `;
      }
    })
    .join("");

  const tipsHtml = route.tips.map((tip) => `<li>${tip}</li>`).join("");

  detailContent.innerHTML = `
            <div class="route-detail-header">
                <div class="route-detail-icon">${route.icon}</div>
                <h2>${route.title}</h2>
                <button class="close-detail-btn" onclick="hideRouteDetails()">×</button>
            </div>
            <div class="route-detail-body">
                <p class="route-description">${route.description}</p>
                
                <div class="route-summary">
                    <div class="summary-item">
                        <span class="summary-label">所要時間</span>
                        <span class="summary-value">${route.duration}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">距離</span>
                        <span class="summary-value">${route.distance}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">難易度</span>
                        <span class="summary-value">${route.difficulty}</span>
                    </div>
                </div>

                <div class="route-stations">
                    <h3>${route.special ? "エリア構成" : "含まれる宿場"}</h3>
                    <div class="${route.special ? "areas-list" : "stations-list"}">
                        ${stationsHtml}
                    </div>
                </div>

                <div class="route-tips">
                    <h3>ポイント・注意事項</h3>
                    <ul>
                        ${tipsHtml}
                    </ul>
                </div>

                <div class="route-actions">
                    <a href="stations.html" class="btn btn-primary">宿場町詳細を見る</a>
                    <a href="guide.html" class="btn btn-secondary">歩き方ガイド</a>
                </div>
            </div>
        `;

  detailSection.style.display = "block";
  detailSection.scrollIntoView({ behavior: "smooth" });
}

// 詳細を閉じる関数
function hideRouteDetails() {
  const detailSection = document.getElementById("routeDetails");
  if (detailSection) {
    detailSection.style.display = "none";
  }
}

// グローバル関数として設定
window.hideRouteDetails = hideRouteDetails;

// DOMContentLoaded時の初期化
document.addEventListener("DOMContentLoaded", function () {
  initRouteDetails();
});