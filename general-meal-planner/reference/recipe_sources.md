# Recipe source workflow

開菜單前，若使用者沒有禁止上網，先查詢料理資料源取得真實料理靈感，再依病人限制調整。

## 優先來源

1. TasteAtlas：傳統名菜、地區代表菜、在地食材與常見調味。
2. Gastronomixs：食材搭配、風味積木、香草辛香料、酸味、油脂與口感元素。
3. The World's 50 Best Restaurants：當代餐飲趨勢、名廚技法與高端料理呈現方式。

## 使用方式

只擷取料理概念、食材組合、風味方向與烹調技法。不可直接複製完整食譜或大量原文。每道料理都必須轉成符合病人疾病限制的版本。

## 候選菜色表欄位

- 餐別
- 候選料理名稱
- 靈感來源
- 原始料理特色
- 保留元素
- 替換或刪除元素
- 疾病客製化理由
- DRIS 食材對應
- 預估風險：鈉、鉀、磷、糖、脂肪、蛋白質
- 是否採用


## v6 菜名取得流程

為避免菜單名稱完全憑空產生，建議先人工或程式整理外部來源摘要，再使用 `scripts/suggest_recipe_names.py` 產出候選菜名。

### recipe_sources.json 範例

```json
[
  {
    "source_type": "TasteAtlas",
    "source_name": "TasteAtlas",
    "region": "Peru / Japan",
    "dish_or_style": "Nikkei citrus seafood",
    "flavor_notes": ["citrus", "pepper", "herbs"],
    "techniques": ["marinate", "quick sear"],
    "risk_notes": ["avoid high sodium sauce", "control seafood protein portion"]
  }
]
```

### 指令

```bash
python scripts/suggest_recipe_names.py recipe_sources.json --patient ckd_non_dialysis --output candidate_recipe_names.json
```

### 使用限制

- 只能擷取料理概念、風味方向、技法與搭配邏輯。
- 不可複製來源完整食譜。
- 菜名、食材重量與調味必須依個案重新設計。
- CKD、高血鉀、水腫、寡尿個案需優先控制蛋白質、鈉、鉀、磷與水分。
