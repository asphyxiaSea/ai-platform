# Copilot 使用说明（针对本仓库）

目标：帮助 AI 编程代理快速理解当前项目结构、关键约定与运行方式，确保生成的改动可落地。

## 快速一览
- 应用类型：FastAPI 服务，入口 [main.py](../main.py)。
- 路由：
  - 文件解析：[app/api/router/files_parse_router.py](../app/api/router/files_parse_router.py) 提供 `/ai-platform/files/parse`。
  - LLM 多模态：[app/api/router/llm_router.py](../app/api/router/llm_router.py) 提供 `/ai-platform/llm/multimodal`。
  - 语音转写：[app/api/router/voice_transcribe.py](../app/api/router/voice_transcribe.py) 提供 `/ai-platform/voice/transcribe`。
- 分层约定：
  - 路由层：解析表单、校验 schema、构建各自的 TaskConfig。
  - 服务层：`files_parse_service`/`llm_service`/`transcribe_service` 负责流程编排与任务分发。
  - 域层：Schema 构建、`FileItem`、文本处理、Marker 配置、提示词构造等纯逻辑。
  - 基础设施层：外部服务与 LLM 访问（httpx/OpenAI SDK）。

## 关键概念与约定（必须遵守）
- Schema 输入：路由接收 JSON 字符串（`SchemaPayload`），通过 `get_schema_model` 动态构建 `pydantic.BaseModel`。
- TaskConfig：三类配置在 [app/domain/task_config_factory.py](../app/domain/task_config_factory.py)。
  - FilesTaskConfig：包含 `task_mode`、`preprocess`、`postprocess`、`marker` 等。
  - LLMTaskConfig：包含 `task_mode`、`model`、`vl_model`、`system_prompt` 等。
  - VoiceTaskConfig：包含 `task_mode`、`model_key` 等。
- 文件处理链：
  - `FILESTOTEXTBYMARKER`：Marker 抽取文本 → LLM 结构化输出。
  - `FILESTOTEXTBYPADDLE`：Paddle 抽取文本 → 文本后处理 → LLM 结构化输出。
- LLM 提示词构造：放在 [app/domain/capabilities/llm/build_llm_prompte.py](../app/domain/capabilities/llm/build_llm_prompte.py)，只构造 `messages`，不做 IO。
- LLM 调用：统一通过 [app/infra/llm_client.py](../app/infra/llm_client.py) 的 `structured_output`/`raw_output`。
- 错误处理：统一异常基类为 `AppError`，FastAPI 中间件统一格式化响应。
- 返回值：服务层返回 `{"results": list[BaseModel]}`（不要随意改为 dict 或单对象）。

## 外部服务与 URL 统一配置
- 所有外部 URL 统一在 [app/infra/url_config.py](../app/infra/url_config.py)。
- Marker/Paddle/LLM 均从该配置读取，不在业务代码里硬编码 URL。

## 常用运行 / 本地调试
- 安装依赖：`python -m pip install -r requirements.txt`
- 启动服务：
  - `python main.py`
  - 或 `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

## 接口示例
- POST `/ai-platform/files/parse`（multipart/form-data）：
  - `schema`：字符串化 JSON（`schema_name` + `fields`）
  - `system_prompt`（可选）
  - `preprocess` / `postprocess`（可选，字符串化 JSON）
  - `files`：上传文件列表
- POST `/ai-platform/llm/multimodal`（multipart/form-data）：
  - `schema`：字符串化 JSON（`schema_name` + `fields`）
  - `system_prompt`（可选）
  - `files`：上传文件列表
- POST `/ai-platform/voice/transcribe`（multipart/form-data）：
  - `file`：上传音频文件
  - `model_key`（可选）

## 同步 / 异步 约定（重要）
- **外部 HTTP / LLM 调用**：使用 `httpx.AsyncClient`，函数必须是 `async def`。
- **OpenAI SDK**：同步 SDK 必须用 `asyncio.to_thread` 包装。
- **PDF 解析**：`pypdf.PdfReader` 必须放线程池（`asyncio.to_thread`）。
- **域层逻辑**：纯同步逻辑，不直接做 IO。
- **路由与服务层**：统一异步，`await` 下游调用。

## 参考文件（快速跳转）
- 入口：[main.py](../main.py)
- 路由：[app/api/router/files_parse_router.py](../app/api/router/files_parse_router.py)
- Schema 构建：[app/domain/resources/build_schema.py](../app/domain/resources/build_schema.py)
- TaskConfig：[app/domain/task_config_factory.py](../app/domain/task_config_factory.py)
- 服务层：[app/service/files_parse_service.py](../app/service/files_parse_service.py)
- LLM 提示词构造：[app/domain/capabilities/llm/build_llm_prompte.py](../app/domain/capabilities/llm/build_llm_prompte.py)
- LLM 客户端：[app/infra/llm_client.py](../app/infra/llm_client.py)
- URL 配置：[app/infra/url_config.py](../app/infra/url_config.py)

---
如发现文档与代码不一致，请指出具体文件或行为场景。
