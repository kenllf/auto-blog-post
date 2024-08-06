#!/bin/bash

# 配置变量
title="测试标题"
content="这是测试内容"
mp3_url="https://example.com/audio.mp3"

# JSON 数据
json_data='{
    "platform": "toutiao",
    "title": "'"$title"'",
    "content": "'"$content"'",
    "mp3Url": "'"$mp3_url"'"
}'

# 发送请求
echo "$json_data" | curl -v -X POST http://localhost:8000/publish \
     -H "Content-Type: application/json" \
     --data-binary @-