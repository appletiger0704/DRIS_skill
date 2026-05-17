# DRIS_skill

泛用型營養菜單設計 Skill，支援慢性腎臟病、高血壓、高血脂、糖尿病、體重控制、營養不良與運動員菜單設計。

## 目前主要 skill

- `general-meal-planner/`

## 版本重點

- 將原本腎臟病專用菜單 skill 擴充為泛用開菜單 skill。
- 午餐與晚餐強制採用：1 份主食、1 份主菜、3 份副菜。
- 每道料理需具備至少 5 種以上食材或調味元素。
- 每道料理需提供料理方式、調味方式與疾病/運動族群提醒。
- 補強台灣國人膳食營養素參考攝取量第八版 DRIs 的維生素目標欄位。
- 保留 Excel / Python pipeline：食材搜尋、DRIs 目標設定、菜單寫入、LibreOffice 重算、營養結果讀取。

## 目錄

```text
general-meal-planner/
  SKILL.md
  references/
  assets/
  scripts/
```

## 注意

`assets/DRIs_template.xlsx` 是標準 DRIs Excel 範本，菜單產出時需寫入該範本並用 LibreOffice 重新計算公式。
