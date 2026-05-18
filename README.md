# DRIS_skill

泛用型營養菜單設計 Skill，支援慢性腎臟病、高血壓、高血脂、糖尿病、體重控制、營養不良與運動員菜單設計。

## 目前主要 skill

- `general-meal-planner/`

## 版本重點

- 將原本腎臟病專用菜單 skill 擴充為泛用開菜單 skill。
- 午餐與晚餐強制採用：1 份主食、1 份主菜、3 份副菜。
- 每道料理需具備至少 2 種主要食材與 3 種以上調味／低鈉增味元素；若疾病限制無法達成，需明確註記原因。
- 每道料理需提供料理方式、調味方式與疾病/運動族群提醒。
- 補強台灣國人膳食營養素參考攝取量第八版 DRIs 的維生素目標欄位。
- 保留 Excel / Python pipeline：食材搜尋、DRIs 目標設定、菜單寫入、LibreOffice 重算、營養結果讀取。
- 菜色設計可參考 TasteAtlas、Gastronomixs 與 The World's 50 Best Restaurants 的料理概念，但需依個案疾病限制重新客製化。

## 目錄

```text
general-meal-planner/
  SKILL.md
  recipe_lookup_workflow.txt
  reference/
  assets/
  scripts/
  examples/
```

## reference 資料夾命名規則

正式資料夾名稱統一使用：

```text
general-meal-planner/reference/
```

不要再建立下列錯誤或舊版資料夾名稱：

```text
general-meal-planner/rederence/
general-meal-planner/references/
```

原因：

- `rederence` 是拼字錯誤。
- `references` 是早期 README 說明中的舊命名。
- v6 之後統一使用 `reference/`，避免 skill 與 scripts 找錯路徑。

## 注意

`assets/DRIs_template.xlsx` 是標準 DRIs Excel 範本，菜單產出時需寫入該範本並用 LibreOffice 重新計算公式。
