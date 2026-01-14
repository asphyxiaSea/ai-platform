{
  "openapi": "3.0.3",
  "info": {
    "title": "paddleocr API",
    "description": "调用paddleocr模型",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://oa1.gxlky.com.cn"
    }
  ],
  "paths": {
    "/paddleocr/predict": {
      "post": {
        "operationId": "paddleocr",
        "summary": "输入图像或PDF调用模型推理，输出结构化信息。",
        "requestBody": {
          "required": true,
          "content": {
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "required": ["files"],
                "properties": {
                   "file": {
                    "type": "string",
                    "format": "binary",
                    "description": "PDF 或图片文件（一次仅支持一个文件）"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "模型回复",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "content": {
                      "type": "object",
                      "additionalProperties": true
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
  }
}