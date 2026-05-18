# DRIS Excel structure

正式 DRIS Excel 必須從原始範本複製後修改，不可重建 workbook。

## 必要 sheet

- `台灣食品成分表2020版`
- `計算`
- `與DRIs比較`
- `菜單`
- `食物EX設計`
- `使用說明`
- `常用食材庫`
- `採購單`

## 寫入位置

### `計算` sheet

- `D3`：菜單名稱。
- `A6:A90`：餐別，例如 `1早餐`、`2午餐`、`3晚餐`。
- `B6:B90`：菜餚名稱。
- `C6:C90`：食材俗稱。
- `D6:D90`：食品成分表正式樣品名稱。
- `H6:H90`：可食重量，單位公克。

`E:G` 與 `I:DH` 原則上保留原公式，不可覆蓋。

### `與DRIs比較` sheet

- `A4:DF4`：個案 DRIS 或治療目標。
- `B12:DF12`：全天營養量結果。

## 完整性要求

正式 Excel 可能包含 drawings、comments、printerSettings、styles、theme、sharedStrings、calcChain、relationship files、docProps 等內部元件。產出前需檢查 ZIP/XML 結構與重要 sheet 是否完整。
