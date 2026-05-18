# Troubleshooting

## Excel 顯示檔案損毀

回到原始 `DRIs_template.xlsx` 重新產生，不要在損毀檔上繼續修補。檢查 ZIP/XML、relationship、content types、worksheet XML 是否完整。

## 公式沒有更新

使用 LibreOffice headless 重算：

```bash
python scripts/recalc.py output.xlsx
```

若環境沒有 LibreOffice，開啟 Excel 後執行重新計算。

## 食材查不到

先用 `search_food.py` 查詢正式食品名稱；若仍找不到，改用食品成分表中最接近且可解釋的替代項。

```bash
python scripts/search_food.py 雞胸肉
```

## 餐別排序錯誤

`write_menu.py` 會依排序權重寫入，若仍錯誤，檢查 menu JSON 的 `meal` 欄位是否為 `1早餐`、`2午餐`、`3晚餐` 等範本代碼。
