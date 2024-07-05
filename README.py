import tweepy
import openai

# 设置Twitter API密钥
consumer_key = 'YOUR_TWITTER_CONSUMER_KEY'
consumer_secret = 'YOUR_TWITTER_CONSUMER_SECRET'
access_token = 'YOUR_TWITTER_ACCESS_TOKEN'
access_token_secret = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

# 设置OpenAI API密钥
openai.api_key = 'YOUR_OPENAI_API_KEY'

# 认证并初始化Twitter API客户端
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# 定义自动回复函数
def auto_reply(tweet):
    # 使用OpenAI生成回复
    response = openai.Completion.create(
        engine="text-davinci-003",  # 或者使用 "gpt-4" 引擎
        prompt=f"回复这条推文: {tweet.text}",
        max_tokens=50
    )
    reply_text = response.choices[0].text.strip()
    
    # 发送回复
    api.update_status(
        status=f"@{tweet.user.screen_name} {reply_text}",
        in_reply_to_status_id=tweet.id
    )

# 监控账户的mentions
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        auto_reply(status)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# 开始流式监听
myStream.filter(track=['@YourTwitterHandle'])  # 替换为你的Twitter用户名

