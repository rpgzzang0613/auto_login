from PIL import Image
from slack_sdk import WebClient
import os

def send_slack_msg(msg):
    oauth_token = os.getenv("SLACK_BOT_OAUTH_TOKEN")
    channel = os.getenv("SLACK_CHANNEL")
    
    client = WebClient(oauth_token)
    response = client.chat_postMessage(channel = channel, text = msg)
    
    return response

def convert_image(original_img):
    img_rgb = original_img.convert("RGB")
    
    width, height = img_rgb.size
    darkest_color = (255, 255, 255)
    
    # 흰색(255, 255, 255)부터 시작해서 이미지에서 가장 진한색 찾기
    for y in range(height):
        for x in range(width):
            r, g, b = img_rgb.getpixel((x, y))
            intensity = r + g + b
            if intensity < sum(darkest_color):
                darkest_color = (r, g, b)
    
    # 원본과 크기가 같은 흰색 이미지 생성
    new_img = Image.new("RGB", (width, height), (255, 255, 255))
    
    # 원본 이미지 동일픽셀위치의 색상이 가장 진한놈만 검정색으로 찍음
    for y in range(height):
        for x in range(width):
            r, g, b = img_rgb.getpixel((x, y))
            if (r, g, b) == darkest_color:
                new_img.putpixel((x, y), (0, 0, 0))
    
    return new_img
