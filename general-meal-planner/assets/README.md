# Assets

此資料夾應放置 skill 執行所需的大型資料檔。

## 必要檔案

- `DRIs_template.xlsx`
  - 標準台灣第八版 DRIs Excel 範本。
  - `write_menu.py` 會將菜單寫入 `計算` sheet。
  - `set_dris_targets.py` 會將個案目標寫入 `與DRIs比較` sheet。
  - 寫入後必須使用 `recalc.py` 透過 LibreOffice 重算公式。

- `food_database_index.json`
  - 食品成分資料庫索引。
  - `search_food.py` 會用它搜尋資料庫正式食材名稱。

- `common_ingredients.json`
  - 常用食材俗名與資料庫名稱 mapping。

## 注意

目前透過 ChatGPT GitHub connector 推送時，主要適合寫入 UTF-8 文字檔；大型二進位 `.xlsx` 與完整食品索引需由本機或 Codex/Claude Code 以 git push 補上。

本次對話產出的完整 skill 壓縮檔為：`general-meal-planner-v2.skill`，可由本地解壓後將 `assets/` 內檔案補入此 repo。
