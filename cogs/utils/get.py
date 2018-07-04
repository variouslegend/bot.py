import aiohttp,json
import os,random

async def random_gif(tag):
	request=str("https://api.giphy.com/v1/gifs/random?api_key=zyPrj7wXqesqCX3v2l7mW5gH02YwVEmV&tag="+tag+"&rating=R")
	data= await aiohttp.get(request)
	data= await data.json()
	gif_url=data['data']['image_mp4_url']
	return gif_url

async def chuck_joke():
	request=str("http://api.icndb.com/jokes/random")
	data= await aiohttp.get(request)
	data= await data.json()
	joke=data['value']['joke']
	return joke

async def insult():
	request=str("https://insult.mattbas.org/api/insult.json")
	data= await aiohttp.get(request)
	data= await data.json()
	insult=data['insult']
	return insult

async def compliment():
	request="https://spreadsheets.google.com/feeds/list/1eEa2ra2yHBXVZ_ctH4J15tFSGEu-VTSunsrvaCAV598/od6/public/values?alt=json"
	data= await aiohttp.get(request)
	data= await data.json()
	entry=random.choice(data['feed']['entry'])
	return entry['title']['$t']
