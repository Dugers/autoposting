from aiohttp import ClientSession
import asyncio
from data import VK_TOKEN


async def parse_posts(group_name):
    async with ClientSession() as session:
        async with session.get(f"https://api.vk.com/method/wall.get?domain={group_name}&count=100&access_token={VK_TOKEN}&v=5.131") as res:                                              
            res = await res.json()
            posts = res['response']['items']
    content = []
    for post in posts:
        try:
            data_list = post['attachments']
            for data in data_list:
                data_type = data['type']
                if data_type == "video":
                    # async with ClientSession() as session:
                    #     async with session.get(f"https://api.vk.com/method/video.get?videos={data['video']['owner_id']}_{data['video']['id']}&access_token={VK_TOKEN}&v=5.131") as video_url:
                    #         video_url = await video_url.json()
                    #         video_url = video_url['response']['items'][0]['player']
                    #         with youtube_dl.YoutubeDL(params={'outtmpl': f"video/{post['id']}_{data['video']['id']}.mp4"}) as ydl:
                    #             ydl.download([video_url])
                    #             content.append([post['id'], data['video']['id'] ,'video', f"video/{post['id']}_{data['video']['id']}.mp4"])
                    continue
                if data_type == "photo":
                    photo_url = data['photo']['sizes'][-1]['url']
                    content.append([post['id'], data['photo']['id'] , "photo", photo_url])
        except:
            continue
    return content


async def parse_group_info(group_name_or_id):
    try:
        async with ClientSession() as session:
            async with session.get(f"https://api.vk.com/method/groups.getById?group_id={group_name_or_id}&access_token={VK_TOKEN}&v=5.131") as res:
                res = await res.json()
                res = res['response'][0]
                return [res['id'], res['name'], res['screen_name']]
    except KeyError:
        return False