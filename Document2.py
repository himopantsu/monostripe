import discord
import glob
from discord.ext import commands,tasks
import gspread
import random  # おみくじで使用
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import pandas as pd
import datetime
import os
import urllib.request, urllib.error
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import timedelta
import cv2
import io
from PIL import Image

bot_token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()  # 接続に使用するオブジェクト

def uranai(url):
	html = urllib.request.urlopen(url)
	soup = BeautifulSoup(html)
	df2 = pd.DataFrame(soup.find_all("a"))
	bbbb = str(df2[0][17])
	bbb = bbbb.split("「")
	bbb = bbb[1].split("」")
	bbb = bbb[0]

	df = pd.DataFrame(soup.find_all("td"))
	test = str(df[0][1])
	n = test.split("=")

	df4 = pd.DataFrame(soup.find_all("p"))
	test2 = str(df4[0][4])
	mm = test2.split("=")
	mmm = mm[0].split(">")[1].split("<")[0].split("。")

	ccc = str(soup.find_all("meta")[7]).split("=")
	ddd = ccc[1][1:-10]
	
	list = []
	list.append(n[3].split(" ")[0][1:-1])
	list.append(n[6].split(" ")[0][1:-1])
	list.append(n[9].split(" ")[0][1:-1])
	list.append(n[12].split(" ")[0][1:-1])
	list.append(bbb)
	return list,ddd


@client.event
async def on_ready():
	"""起動時に通知してくれる処理"""
	print('ログインしました')
	print(client.user.name)  # ボットの名前
	print(client.user.id)  # ボットのID
	print(discord.__version__)  # discord.pyのバージョン
	print('------')
	
@client.event
async def on_message(message):
	"""メッセージを処理"""
	if message.author.bot:  # ボットのメッセージをハネる
		return
	
	elif message.attachments:
		headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
		request = urllib.request.Request(url=str(message.attachments[0].url),headers=headers)
		f = io.BytesIO(urllib.request.urlopen(request).read())
		
		validation_img = Image.open("horntale_necklace.png")
		validation_grayimg = validation_img.convert('L')
		validation_array = np.asarray(validation_grayimg)
		
		img = Image.open(f)
		grayimg = img.convert('L')
		input_array = np.asarray(grayimg)
		custom_cascade = cv2.CascadeClassifier('cascade.xml')
		custom_rect = custom_cascade.detectMultiScale(grayimg, scaleFactor=1.07, minNeighbors=2, minSize=(1, 1))
		
		
		#match_result = cv2.matchTemplate(input_array,validation_array,cv2.TM_CCOEFF_NORMED)
		#threshold = 0.5
		#loc=np.where(match_result >= threshold)
		
		if len(custom_rect) == 0:
			return
		else: await message.channel.send(f"あるよ")
	
	elif message.content == "('o')ｷｬｧｧｧｧｧｧｧｧｧｧｧｧｧｧｧｧｧｧwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww":
		await message.channel.send(f"うるせえぞタピオカ")
		
	elif message.content == "!やるじゃん":
		await message.channel.send(f"ありがとう")
		
	elif message.content == "!えっち":
		await message.channel.send(f'きゃー！{message.author.mention}さんのえっち！！', file=discord.File("4ba65a1c.jpg"))
		
	elif message.content == "!ハンバーグ":
		await message.channel.send(f"ハンバアアアアアアアアアアアアアアアアアアアアアアアアアアアグ！！！！！！")
	
	elif message.content == "!やってないじゃん":
		await message.channel.send(f"ごめんなさい")
		
	elif message.content == "!ゆきやこんこ":
		await message.channel.send(f"⛄雪や⛄\n\n❄❅❆❄❅❆❄❅❆❄\n▉▉▉ ◥◣　　 ▉▉▉ \n　　▉ 　　◢◤ 　　▉ \n▉▉▉ ◢▉◤　 ▉▉▉ \n❄❅❆❄❅❆❄❅❆❄\n\n🚽ケツから🚽\n\n💩💩💩💩💩💩💩💩\n　▉\n▉▉▉▉◥◣　　▉▉▉\n▉　◢◤　　◢◤　　▉\n　◢◤　◢▉◤　▉▉▉\n💩💩💩💩💩💩💩💩")
		
	elif message.content == "juruli":
		await message.channel.send(f"そのキャラはキャラデリしました")
		
	elif message.content == "!おみくじ":
		# Embedを使ったメッセージ送信 と ランダムで要素を選択
		embed = discord.Embed(title="おみくじ", description=f"{message.author.mention}さんの今日の運勢は！",color=0x2ECC69)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="[運勢] ", value=random.choice(('大吉', '吉', '凶', '大凶')), inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!ダイス":
		embed = discord.Embed(title="ダイス", description=f"{message.author.mention}さんの結果",color=0x2ECC69)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="[結果] ", value=random.randint(0,100), inline=False)
		await message.channel.send(embed=embed)
		
	elif message.content == "!ダイレクトメッセージ":
		# ダイレクトメッセージ送信
		dm = await message.author.create_dm()
		await dm.send(f"{message.author.mention}さんにダイレクトメッセージ")

	elif message.content == "!おひつじ座":
		url = "https://fortune.yahoo.co.jp/12astro/aries"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!おうし座":
		url = "https://fortune.yahoo.co.jp/12astro/taurus"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!ふたご座":
		url = "https://fortune.yahoo.co.jp/12astro/gemini"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!かに座":
		url = "https://fortune.yahoo.co.jp/12astro/cancer"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!しし座":
		url = "https://fortune.yahoo.co.jp/12astro/leo"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!おとめ座":
		url = "https://fortune.yahoo.co.jp/12astro/virgo"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!てんびん座":
		url = "https://fortune.yahoo.co.jp/12astro/libra"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!さそり座":
		url = "https://fortune.yahoo.co.jp/12astro/scorpio"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!いて座":
		url = "https://fortune.yahoo.co.jp/12astro/sagittarius"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!やぎ座":
		url = "https://fortune.yahoo.co.jp/12astro/capricorn"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!みずがめ座":
		url = "https://fortune.yahoo.co.jp/12astro/aquarius"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

	elif message.content == "!うお座":
		url = "https://fortune.yahoo.co.jp/12astro/pisces"
		kekka,ddd = uranai(url)
		embed = discord.Embed(title="星座占い", description=f"{message.author.mention}さんの今日の運勢は！",color=0x00FF00)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="総合運",value=kekka[0],inline=False)
		embed.add_field(name="恋愛運",value=kekka[1],inline=False)
		embed.add_field(name="金運",value=kekka[2],inline=False)
		embed.add_field(name="仕事運",value=kekka[3],inline=False)
		embed.add_field(name="コメント",value=kekka[4],inline=False)
		embed.add_field(name="====",value=ddd,inline=False)
		await message.channel.send(embed=embed)

client.run(bot_token)
