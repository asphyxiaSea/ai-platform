{
  "openapi": "3.0.3",
  "info": {
    "title": "ai-platform",
    "description": "ai-platform",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://oa1.gxlky.com.cn"
    }
  ],
  "paths": {
    "/ai-platform/files/parse": {
      "post": {
        "operationId": "FilesParse",
        "summary": "输入图像或PDF调用模型推理，输出结构化信息。",
        "requestBody": {
          "required": true,
          "content": {
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "required": ["schema","files"],
                "properties": {
                  "system_prompt": {
                    "type": "string"
                  },
                  "schema": {
                    "type": "string"
                  },
                  "preprocess": {
                    "type": "string"
                  },
                  "postprocess": {
                    "type": "string"
                  },
                "files": {
                    "type": "array",
                    "items":{
                       "type": "string",
                       "format": "binary"
                     }
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