# Codex 審查指南

這個 repository 是 Python Twitch 聊天室機器人，會監聽 Twitch EventSub 聊天訊息，並使用 OpenAI Responses API 產生簡短的公開回覆。

審查這個 repo 的變更時，請使用這份指南。

## 審查語言

- 請使用繁體中文撰寫 review comment。
- 優先指出具體風險、bug、行為退化、缺少測試或安全性問題。
- 除非會影響正確性、可維護性或使用者安全，否則避免只針對風格提出建議。

## 高風險區域

- Secret 絕不能被提交、記錄到 log、印出，或寫進範例：
  - `OPENAI_API_KEY`
  - `TWITCH_TOKEN`
  - `TWITCH_CLIENT_SECRET`
  - `.env`
  - `prompt/system_prompt.txt`
  - 本機 token/cache 檔案
- Twitch 驗證相關變更必須保留以下項目的關係：
  - `TWITCH_TOKEN`
  - `TWITCH_BOT_ID`
  - `TWITCH_OWNER_ID`
  - 必要 scopes：`user:read:chat` 和 `user:write:chat`
- 公開聊天室回覆必須避免洗版：
  - 保持全域冷卻與單一使用者冷卻行為正確
  - 保留指令、網址、過長訊息與黑名單使用者的忽略規則
  - 讓回覆機率與強制觸發行為保持容易理解
- LLM 輸出必須受到限制：
  - 保留 `MAX_INPUT_LENGTH` 和 `MAX_REPLY_LENGTH`
  - 避免讓 prompt injection 更容易成功的變更
  - 避免在回覆中暴露私有 prompt 或環境資料

## Python 審查清單

- 確認新的環境變數同時記錄在 `.env.example` 和 `README.md`。
- 檢查數值型環境變數是否有清楚的失敗訊息或安全預設值。
- 檢查網路呼叫是否設定 timeout，且錯誤訊息是否有助於排查。
- 檢查 Twitch EventSub handler 是否沒有不必要地阻塞。
- 檢查使用者可見的回覆行為是否足夠可預測，方便除錯。
- 優先提出小範圍、局部修正，避免大規模重寫。

## GitHub Actions 審查清單

- 確認 workflow 權限沒有超過實際需要。
- 可行時，優先使用固定 action 版本或穩定 tag，避免使用會移動的分支。
- 不要透過 log、PR comment、命令輸出或 debug flag 暴露 secrets。
- 確認 PR 自動化不會建立重複 pull request，也不會造成 workflow 遞迴觸發。

## 文件期望

- 如果行為有變更，請更新 `README.md`。
- 如果設定有變更，請更新 `.env.example`。
- 如果 prompt 設定方式有變更，請更新 `prompt/system_prompt.txt.example`。
- 不要記錄真實 secrets 或只存在本機的值。

## 本機驗證

可行時，執行範圍最小且相關的檢查：

```bash
python -m py_compile main.py
```

如果已安裝 dependencies，且變更會影響執行期行為，請優先做聚焦的手動檢查，避免提出範圍過大的推測性變更。
