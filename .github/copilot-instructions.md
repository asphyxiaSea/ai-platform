# Copilot 使用说明（针对本仓库）

目标：帮助 AI 编程代理快速理解本项目的架构、关键约定、常用运行/调试命令与常见集成点，便于生成准确、可运行的代码改动。

## 快速一览
- 应用类型：FastAPI 服务，入口为 [main.py](main.py)。
- 路由：主要路由在 [router/files_extract.py](router/files_extract.py)，对外暴露 `/ai-platform/files/parse` 接口。
- 业务分层：
  - 路由层：解析表单、校验 schema、构建 `TaskConfig`（见 [domain/task_config_factory.py](domain/task_config_factory.py)）。
  - 服务层：`service/extract_service.py` 根据 `TaskMode` 分派到 `marker_service` 或 `paddle_service`。
  - 域层（domain）：Schema 构建、`FileItem`、marker/paddle 文本抽取逻辑（参见 `domain/` 下文件）。
  - 工具/集成：与本地 Ollama（HTTP）通信在 [util/ollama.py](util/ollama.py)；也有一个基于 OpenAI-compatible client 的封装在 [util/openai.py](util/openai.py)（其 base_url 指向本地 Ollama）。

## 关键概念与约定（必须遵守）
- Schema 输入：路由接收一个 JSON 字符串，格式由 `SchemaPayload` 定义（见 [router/files_extract.py](router/files_extract.py)）。代码通过 `domain/build_schema.get_schema_model` 将其动态转换为 `pydantic.BaseModel`。
- TaskConfig：通过 `TaskConfig_factory` 构建，包含 `schema`, `model`, `task_mode`, `preprocess` / `postprocess` 等（见 [domain/task_config_factory.py](domain/task_config_factory.py)）。
- 两条主线：
  - `FILESTOTEXTBYMARKER`：使用 `domain/marker.py` 的标注器把文件转为文本，再发送给 LLM（见 [service/marker_service.py](service/marker_service.py)）。
  - `FILESTOTEXTBYPADDLE`：使用 PaddleOCR/解析（`domain/paddle.py`）转文本并做后处理（见 [service/paddle_service.py](service/paddle_service.py)）。
- LLM 格式化输出：项目依赖 Ollama 的 `format` 参数把模型输出直接映射为 JSON schema（见 [util/ollama.py](util/ollama.py)），请求格式必须与 `schema.model_json_schema()` 配合。
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
  - 本地 Ollama HTTP 服务（默认期望在 `http://localhost:8001`），项目使用它作为推理后端（见 [util/ollama.py](util/ollama.py) 与 [util/openai.py](util/openai.py)）。

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
- 对于 schema 操作，优先调用现有的 `get_schema_model`（[domain/build_schema.py](domain/build_schema.py)），不要在路由里重复拼接 Pydantic 模型。
- 当修改 LLM 调用流程时，请保持 `util/ollama.py` 的请求格式（`format: schema.model_json_schema()`），这样服务端会返回可被 `schema.model_validate_json` 解析的字符串。
- PDF 与 OCR：PDF 的前处理逻辑集中在 [domain/preprocess.py](domain/preprocess.py)（路由层触发）；有关 paddle 的抽取在 [domain/paddle.py](domain/paddle.py)。修改前务必检查 `preprocess` / `postprocess` 的 JSON 结构。
- 返回模型：服务层函数通常返回 `pydantic.BaseModel` 实例或列表。自动化测试或代码生成时，遵循现有返回值（不要随意把返回改为原始 dict，除非同步更新调用方）。

## 参考文件（快速跳转）
- 应用入口：[main.py](main.py)
- 路由：[router/files_extract.py](router/files_extract.py)
- TaskConfig：[domain/task_config_factory.py](domain/task_config_factory.py)
- Schema 构建：[domain/build_schema.py](domain/build_schema.py)
- Marker/paddle 服务：[service/marker_service.py](service/marker_service.py), [service/paddle_service.py](service/paddle_service.py)
- Ollama / OpenAI wrappers：[util/ollama.py](util/ollama.py), [util/openai.py](util/openai.py)

---
如果有你认为缺失或不准确的细节，请指出具体文件或场景，我会基于实际代码把本文档进一步精炼。
