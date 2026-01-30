# Copilot 使用说明（针对本仓库）

目标：帮助 AI 编程代理快速理解本项目的架构、关键约定、常用运行/调试命令与常见集成点，便于生成准确、可运行的代码改动。

## 快速一览
- 应用类型：FastAPI 服务，入口为 [main.py](../main.py)。
- 路由：主要路由在 [app/api/router/files_extract.py](../app/api/router/files_extract.py)，对外暴露 `/ai-platform/files/parse` 接口。
- 业务分层：
  - 路由层：解析表单、校验 schema、构建 `TaskConfig`（见 [app/domain/task_config_factory.py](../app/domain/task_config_factory.py)）。
  - 服务层：`app/service/extract_service.py` 根据 `TaskMode` 分派到 `marker_service` 或 `paddle_service`。
  - 域层（domain）：Schema 构建、`FileItem`、marker/paddle 纯逻辑（参见 `app/domain/` 下文件）。
  - 基础设施/集成：与本地 Ollama（HTTP）通信在 [app/infra/ollama.py](../app/infra/ollama.py)；OpenAI-compatible client 封装在 [app/infra/openai.py](../app/infra/openai.py)（其 base_url 指向本地 Ollama）。

## 关键概念与约定（必须遵守）
- Schema 输入：路由接收一个 JSON 字符串，格式由 `SchemaPayload` 定义（见 [app/api/router/files_extract.py](../app/api/router/files_extract.py)）。代码通过 `app/domain/build_schema.get_schema_model` 将其动态转换为 `pydantic.BaseModel`。
- TaskConfig：通过 `TaskConfig_factory` 构建，包含 `schema`, `model`, `task_mode`, `preprocess` / `postprocess` 等（见 [app/domain/task_config_factory.py](../app/domain/task_config_factory.py)）。
- 两条主线：
  - `FILESTOTEXTBYMARKER`：通过 `app/infra/marker_client.py` 取文本，`app/domain/marker.py` 负责配置与纯逻辑（见 [app/service/marker_service.py](../app/service/marker_service.py)）。
  - `FILESTOTEXTBYPADDLE`：通过 `app/infra/paddle_client.py` 取文本并做后处理（见 [app/service/paddle_service.py](../app/service/paddle_service.py)）。
- LLM 格式化输出：项目依赖 Ollama 的 `format` 参数把模型输出直接映射为 JSON schema（见 [app/infra/ollama.py](../app/infra/ollama.py)），请求格式必须与 `schema.model_json_schema()` 配合。
- 错误处理：LLM / 请求错误会抛出 `fastapi.HTTPException`（HTTP 502）；schema 解析错误会抛出 400。
- 返回值约定：`marker_service` 与 `paddle_service` 通常返回结果列表，但当前实现会取 `results[0]`（注意：这个设计是明确的，修改时请确认调用端预期）。

## 常用运行 / 本地调试步骤
- 安装依赖：使用仓内的 `requirements.txt`。

  ```bash
  python -m pip install -r requirements.txt
  ```

- 本地启动 FastAPI（开发模式 - 自动重载）：

  ```bash
  python main.py
  # 或
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

- 必备外部服务：
  - 本地 Ollama HTTP 服务（默认期望在 `http://localhost:8001`），项目使用它作为推理后端（见 [app/infra/ollama.py](../app/infra/ollama.py) 与 [app/infra/openai.py](../app/infra/openai.py)）。

## 接口示例（用于测试/生成示例代码）
- POST /ai-platform/files/parse （multipart/form-data）字段说明：
  - `schema`：字符串化的 JSON，满足 `SchemaPayload`（包含 `schema_name` 与 `fields`）。
  - `system_prompt`（可选）：覆盖 `TaskConfig.system_prompt`。
  - `preprocess` / `postprocess`（可选）：字符串化 JSON，用于 PDF 前/后处理。
  - `files`：要上传的文件列表（支持 PDF 特殊前处理）。

示例 cURL：

```bash
curl -X POST "http://localhost:8000/ai-platform/files/parse" \
  -F 'schema={"schema_name":"MySchema","fields":[{"name":"title","type":"str","description":"标题"}]}' \
  -F "files=@/path/to/doc.pdf" \
  -H "Content-Type: multipart/form-data"
```

## 代码生成 / 修改注意事项（为 Copilot 指令定制）
- 对于 schema 操作，优先调用现有的 `get_schema_model`（[app/domain/build_schema.py](../app/domain/build_schema.py)），不要在路由里重复拼接 Pydantic 模型。
- 当修改 LLM 调用流程时，请保持 [app/infra/ollama.py](../app/infra/ollama.py) 的请求格式（`format: schema.model_json_schema()`），这样服务端会返回可被 `schema.model_validate_json` 解析的字符串。
- PDF 与 OCR：PDF 的前处理逻辑集中在 [app/domain/preprocess.py](../app/domain/preprocess.py)（服务层触发）；有关 paddle/marker 的外部抽取在 [app/infra/paddle_client.py](../app/infra/paddle_client.py)、[app/infra/marker_client.py](../app/infra/marker_client.py)。修改前务必检查 `preprocess` / `postprocess` 的 JSON 结构。
- 返回模型：服务层函数通常返回 `pydantic.BaseModel` 实例或列表。自动化测试或代码生成时，遵循现有返回值（不要随意把返回改为原始 dict，除非同步更新调用方）。

## 同步 / 异步 约定（重要）

本项目对同步与异步有明确约定，修改或新增代码时请严格遵守：

- **网络与外部服务（异步）**: 所有对外 HTTP / RPC 调用必须使用异步客户端（`httpx.AsyncClient`），并以 `async def` 暴露。示例文件：[app/infra/ollama.py](../app/infra/ollama.py)、[app/infra/paddle_client.py](../app/infra/paddle_client.py)、[app/infra/marker_client.py](../app/infra/marker_client.py)。
- **LLM 调用（异步）**: 同步 SDK 请包成异步封装（`asyncio.to_thread`）或直接使用异步 HTTP。统一入口为 [app/infra/llm_client.py](../app/infra/llm_client.py)，使用 `await structured_output(...)`。示例：[app/infra/ollama.py](../app/infra/ollama.py), [app/infra/openai.py](../app/infra/openai.py)。
- **文件上传/下载 与 FastAPI 接口（异步）**: 路由层使用 `UploadFile.read()`、返回流等均为异步，路由函数应为 `async def`。示例：[app/api/router/files_extract.py](../app/api/router/files_extract.py)。
- **PDF 页数解析（线程池）**: `pypdf.PdfReader` 等 CPU / blocking 操作应放入线程池（`asyncio.to_thread`）。已实现例子：[app/service/extract_service.py](../app/service/extract_service.py)。
- **域模型 / 业务算法 / 文本处理（同步）**: 领域模型与纯 CPU 算法（如文本后处理、processor 列表构造）保持同步实现，调用方在需要将阻塞操作放在线程或在异步函数中 `await` 对应的 async wrapper。示例目录：[app/domain/](../app/domain/)。
- **服务层（异步）**: service 层负责 orchestration，应采用 `async def` 并 `await` 下游异步调用（例：[app/service/extract_service.py](../app/service/extract_service.py)，[app/service/marker_service.py](../app/service/marker_service.py)，[app/service/paddle_service.py](../app/service/paddle_service.py)）。

举例：

 - 异步服务函数示例：

```python
async def paddle_services(...):
  text = await domain.paddle.extract_file(file_item=fi)
  result = await llm_client.structured_output(...)
```

 - 同步域函数示例（保留同步实现）：

```python
class Marker:
  def to_processor_list(self) -> list[str]:
    # 同步逻辑
    ...
```

约定小结：网络/IO/LLM/Upload 都 async；域模型/算法保持 sync；阻塞库（PDF/CPU heavy）走线程池。

## 参考文件（快速跳转）
- 应用入口：[main.py](../main.py)
- 路由：[app/api/router/files_extract.py](../app/api/router/files_extract.py)
- TaskConfig：[app/domain/task_config_factory.py](../app/domain/task_config_factory.py)
- Schema 构建：[app/domain/build_schema.py](../app/domain/build_schema.py)
- Marker/paddle 服务：[app/service/marker_service.py](../app/service/marker_service.py), [app/service/paddle_service.py](../app/service/paddle_service.py)
- Ollama / OpenAI wrappers：[app/infra/ollama.py](../app/infra/ollama.py), [app/infra/openai.py](../app/infra/openai.py)

---
如果有你认为缺失或不准确的细节，请指出具体文件或场景，我会基于实际代码把本文档进一步精炼。
