import os
import boto3
import json
from dotenv import load_dotenv

load_dotenv()

# AWS設定（.envから取得）
region = os.getenv("AWS_REGION", "us-east-1")
model_id = os.getenv("BEDROCK_MODEL_ID")
bedrock = boto3.client("bedrock-runtime", region_name=region)

def ask_bedrock(prompt: str) -> str:
    """
    Bedrock（Claudeなど）に質問して返答を得る関数
    """
    body = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.7
    }

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )
        result = json.loads(response['body'].read())
        return result["content"][0]["text"]
    except Exception as e:
        return f"[エラー] Bedrock呼び出しに失敗しました: {e}"
