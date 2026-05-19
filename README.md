# Twitch GPT Chat Bot

這是一個使用 TwitchIO EventSub 監聽 Twitch 聊天室，並透過 OpenAI Responses API 產生簡短回覆的直播聊天室機器人。

## 功能

- 監聽指定 Twitch 頻道的聊天室訊息。
- 使用 OpenAI 模型產生符合直播聊天室語氣的短回覆。
- 可設定是否每則訊息都回覆，或依機率回覆。
- 支援全域與單一使用者冷卻時間，避免洗版。
- 可忽略指令、網址、過長訊息與黑名單使用者。
- 可用 LLM 做二次判斷，決定訊息是否值得公開回覆。
- 啟動時會驗證 Twitch token scope，以及 token 使用者是否符合 `TWITCH_BOT_ID`。

## 專案結構

```text
.
├── main.py                         # Bot 主程式
├── .env.example                    # 可提交到 Git 的環境變數範例
├── .gitignore                      # 忽略本機密鑰與私人 prompt
└── prompt/
    ├── system_prompt.txt.example   # 可提交到 Git 的 prompt 範例
    └── system_prompt.txt           # 實際 prompt，預設不提交
```

## 必要條件

- Python 3.10 以上
- Twitch 開發者應用程式的 Client ID
- Twitch OAuth token，至少需要以下 scopes：
  - `user:read:chat`
  - `user:write:chat`
- OpenAI API key

## 安裝

建議使用 virtual environment：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 初始化設定

複製範例設定檔：

```bash
cp .env.example .env
cp prompt/system_prompt.txt.example prompt/system_prompt.txt
```

接著編輯 `.env`，填入實際密鑰與 Twitch 帳號資訊。

## 環境變數

### OpenAI

| 變數 | 說明 | 取得方式 |
| --- | --- | --- |
| `OPENAI_API_KEY` | OpenAI API key。 | 到 [OpenAI Platform API keys](https://platform.openai.com/api-keys) 建立 key。 |
| `OPENAI_MODEL` | 主要回覆模型，例如 `gpt-4.1-mini` 或其他可用 Responses API 的模型。 | 到 [OpenAI Models](https://platform.openai.com/docs/models) 查可用 model id，或用 Models API 列出帳號可用模型。 |
| `LLM_REPLY_FILTER_ENABLED` | 是否啟用 LLM 回覆判斷器。`true`/`false`。 | 自行決定；想省 token 或降低延遲可設 `false`。 |
| `LLM_REPLY_FILTER_MODEL` | 回覆判斷器使用的模型。 | 同 `OPENAI_MODEL`，通常可選較快、較便宜的模型。 |
| `PROMPT_PATH` | system prompt 檔案路徑，預設為 `prompt/system_prompt.txt`。 | 本機檔案路徑；初始化時可由 `prompt/system_prompt.txt.example` 複製。 |

### Twitch

| 變數 | 說明 | 取得方式 |
| --- | --- | --- |
| `TWITCH_TOKEN` | Bot 帳號的 OAuth user access token，可包含或不包含 `oauth:` 前綴。 | 建議用 Twitch CLI：`twitch token --user-token --scopes "user:read:chat user:write:chat"`。Twitch chat EventSub 讀取訊息需要 `user:read:chat`，發送聊天訊息需要 `user:write:chat`。 |
| `TWITCH_CLIENT_ID` | Twitch Developer Console 應用程式的 Client ID。 | 到 [Twitch Developer Console](https://dev.twitch.tv/console/apps) 建立或選擇 app，複製 Client ID。 |
| `TWITCH_CLIENT_SECRET` | 目前程式可讀取但不是 token 登入的主要必填項；若未使用 client secret flow 可留空或註解。 | 在 Twitch Developer Console 的 app 頁面產生。不要提交到 Git。 |
| `TWITCH_BOT_ID` | Bot 帳號的 Twitch user ID，必須與 `TWITCH_TOKEN` 所屬帳號一致。 | 用 Twitch Helix Get Users 查 bot 帳號 login，回傳的 `id` 即 user ID。 |
| `TWITCH_OWNER_ID` | 要監聽的頻道擁有者 Twitch user ID。這個值實際決定 EventSub 監聽哪個頻道。 | 用 Twitch Helix Get Users 查目標頻道 login，回傳的 `id` 即 user ID。 |
| `TWITCH_CHANNEL` | 頻道登入名稱，目前主要用於 log 顯示。 | Twitch 頻道網址最後一段，例如 `https://www.twitch.tv/topa_1120` 的 login 是 `topa_1120`。 |
| `TWITCH_BOT_NICK` | Bot 暱稱，目前主要用於 console log 顯示；Twitch 實際發話帳號由 `TWITCH_TOKEN` 決定。 | 自行設定，建議填容易辨識的 bot 顯示名稱。 |

查 Twitch user ID 可以使用 Helix Get Users API：

```bash
curl -H "Client-ID: <TWITCH_CLIENT_ID>" \
  -H "Authorization: Bearer <TWITCH_TOKEN_WITHOUT_OAUTH_PREFIX>" \
  "https://api.twitch.tv/helix/users?login=<twitch_login>"
```

回傳 JSON 中的 `data[0].id` 就是 `TWITCH_BOT_ID` 或 `TWITCH_OWNER_ID` 要填的值。

### 回覆策略

| 變數 | 說明 | 取得方式 |
| --- | --- | --- |
| `ALWAYS_REPLY` | `true` 時通過忽略規則與冷卻後都會回覆。 | 自行決定。正式直播建議先用 `false` 或拉高冷卻時間。 |
| `REPLY_PROBABILITY` | `ALWAYS_REPLY=false` 時的隨機回覆機率，例如 `0.25`。 | 自行設定，範圍建議 `0.0` 到 `1.0`。 |
| `GLOBAL_COOLDOWN_SECONDS` | Bot 兩次公開回覆之間的全域冷卻秒數。 | 自行設定，正式直播建議不要太低。 |
| `USER_COOLDOWN_SECONDS` | 同一使用者兩次被回覆之間的冷卻秒數。 | 自行設定，用來避免單一觀眾連續觸發 bot。 |
| `MAX_INPUT_LENGTH` | 超過此長度的聊天室訊息會被忽略。 | 自行設定，短一點可降低 prompt injection 和成本風險。 |
| `MAX_REPLY_LENGTH` | GPT 回覆超過此長度會被截斷。 | 自行設定，建議符合聊天室可讀性。 |

## Twitch 設定重點

`TWITCH_BOT_ID` 和 `TWITCH_OWNER_ID` 很容易混淆：

- `TWITCH_BOT_ID` 是「誰來發話」。
- `TWITCH_OWNER_ID` 是「監聽誰的聊天室」。
- `TWITCH_TOKEN` 必須屬於 `TWITCH_BOT_ID` 這個帳號。
- 如果 bot 要在自己的頻道回覆，`TWITCH_BOT_ID` 和 `TWITCH_OWNER_ID` 可以相同。
- 如果 bot 要替另一個頻道回覆，`TWITCH_BOT_ID` 是 bot 帳號，`TWITCH_OWNER_ID` 是被監聽的直播主帳號。

## 執行

確認 `.env` 和 `prompt/system_prompt.txt` 都已建立後：

```bash
python main.py
```

啟動成功時會看到類似輸出：

```text
Logged in as <bot nick or bot id>
Connected to channel: <channel name>
Always reply: <true/false>
Reply probability: <number>
LLM reply filter enabled: <true/false>
```

## 回覆流程

1. 收到 Twitch 聊天室訊息。
2. 如果訊息來自 bot 自己，直接忽略。
3. 記錄聊天室訊息到 console。
4. 忽略空訊息、黑名單、過長訊息、指令和網址。
5. 檢查全域與使用者冷卻時間。
6. 若訊息包含強制觸發詞，直接進入回覆流程。
7. 否則依 `ALWAYS_REPLY` 或 `REPLY_PROBABILITY` 決定是否回覆。
8. 若啟用 `LLM_REPLY_FILTER_ENABLED`，先讓 LLM 判斷是否值得回覆。
9. 使用 `prompt/system_prompt.txt` 和聊天室訊息產生 GPT 回覆。
10. 發送 `@username <reply>` 到 Twitch 聊天室。

## 常見問題

### `TWITCH_BOT_ID 與 TWITCH_TOKEN 使用者不一致`

代表 `TWITCH_TOKEN` 不是 `TWITCH_BOT_ID` 這個帳號產生的。請重新產生 bot 帳號的 token，或修正 `TWITCH_BOT_ID`。

### `TWITCH_TOKEN 缺少必要 scope`

重新產生 Twitch OAuth token，並確認包含：

```text
user:read:chat
user:write:chat
```

### `找不到 prompt 檔案`

請建立 `prompt/system_prompt.txt`：

```bash
cp prompt/system_prompt.txt.example prompt/system_prompt.txt
```

### Bot 沒有在預期頻道回覆

請優先檢查 `TWITCH_OWNER_ID`。目前程式實際監聽頻道是由 `TWITCH_OWNER_ID` 決定，不是 `TWITCH_CHANNEL`。
