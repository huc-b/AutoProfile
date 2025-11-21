import requests
import datetime
import os

# ---------------- 配置区域 ----------------
# 天气城市，支持拼音，如 Beijing, Shanghai, Shenzhen
CITY = "Beijing" 
# ----------------------------------------

def get_beijing_time():
    """获取北京时间 (UTC+8)"""
    utc_now = datetime.datetime.utcnow()
    beijing_time = utc_now + datetime.timedelta(hours=8)
    return beijing_time.strftime("%Y-%m-%d %H:%M:%S"), beijing_time.strftime("%Y-%m-%d")

def get_quote():
    """抓取每日名言"""
    try:
        url = "https://api.quotable.io/random?tags=technology,programming"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return f"**“{data['content']}”**\n\n— *{data['author']}*"
    except Exception as e:
        print(f"Quote Error: {e}")
    return "**“Talk is cheap. Show me the code.”**\n\n— *Linus Torvalds*"

def get_hacker_news():
    """抓取 Hacker News 前 5 条热点"""
    news_content = ""
    try:
        # 获取前 5 个 ID
        top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        ids = requests.get(top_url, timeout=10).json()[:5]
        
        for idx, story_id in enumerate(ids, 1):
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story = requests.get(story_url, timeout=5).json()
            title = story.get('title', 'No Title')
            link = story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
            # 拼接成列表格式
            news_content += f"{idx}. [{title}]({link})\n"
            
    except Exception as e:
        print(f"News Error: {e}")
        news_content = "暂时无法获取新闻数据，请稍后再试。"
    
    return news_content

def update_readme():
    """组装所有数据并写入 README.md"""
    current_time, current_date = get_beijing_time()
    quote = get_quote()
    news = get_hacker_news()
    
    # 生成 Markdown 内容
    # 技巧：使用 wttr.in 生成天气图片，无需 API Key
    md_content = f"""
# 👨‍💻 My Personal Dashboard

这里是我的自动化仪表盘，每天由 **GitHub Actions** 自动更新。

<div align="center">

| 📅 北京时间 | 🌤️ 今日天气 |
| :---: | :---: |
| **{current_time}** | <img src="https://wttr.in/{CITY}?format=%c+%t+%w&m" height="25"> |

</div>

---

### 📰 Hacker News 热点 (Top 5)
{news}

---

### 💡 每日一句
{quote}

---
<div align="right">
  Last Automated Update: {current_time} <br>
  <i>Powered by Python & GitHub Actions</i>
</div>
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(md_content)

if __name__ == "__main__":
    update_readme()
    print("Dashboard updated successfully!")
