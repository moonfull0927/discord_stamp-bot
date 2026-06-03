import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'ログインしました: {bot.user}')

@bot.command()
async def スタンプ数を教えて(ctx):
    await ctx.send("サーバー全体のスタンプを集計中だよ！ちょっと待ね...")
    target_user = ctx.author
    total_reactions = 0

    for channel in ctx.guild.text_channels:
        permissions = channel.permissions_for(ctx.guild.me)
        if not permissions.read_message_history:
            continue
        try:
            async for message in channel.history(limit=200):
                if message.author == target_user:
                    for reaction in message.reactions:
                        total_reactions += reaction.count
        except discord.Forbidden:
            continue
        except Exception as e:
            continue

    await ctx.send(f"{target_user.mention} さんがこれまでに送信したメッセージには、合計で **{total_reactions}個** のスタンプが付いています！")

# ⚠️ トークンはここには書かず、サーバー側の設定から読み込むように変更しました
bot.run(os.environ.get("DISCORD_TOKEN"))
