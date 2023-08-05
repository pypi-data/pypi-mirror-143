import base64
from re import findall
from sys import exc_info

import httpx
from httpx import AsyncClient
from nonebot import get_driver
from nonebot.log import logger

from .config import Config

plugin_config = Config.parse_obj(get_driver().config.dict())

proxies = plugin_config.setu_proxy
if proxies:
    logger.info(f"使用自定代理 {proxies}")
else:
    proxies = None


save = plugin_config.setu_save
if save == "webdav":
    from .save_to_webdav import save_img
elif save == "local":
    from .save_to_local import save_img
else:
    save = None


reverse_proxy = plugin_config.setu_reverse_proxy
if reverse_proxy:
    logger.info(f"使用自定反向代理 {reverse_proxy}")
else:
    reverse_proxy = "i.pixiv.re"
error = "Error:"


async def get_setu(keyword="", r18=False) -> list:
    """获取色图并返回一堆东西

    Args:
        keyword (str, optional): 关键词. Defaults to "".
        r18 (bool, optional): 是否r18. Defaults to False.

    Returns:
        list[0]: base64编码图片或"Error:"
        list[1]: 图片信息或错误详情
        list[2]: 获取到图片 True, 否则 False
    """
    async with AsyncClient() as client:
        req_url = "https://api.lolicon.app/setu/v2"
        params = {
            "keyword": keyword,
            "r18": 1 if r18 else 0,
            "size": "regular",
            "proxy": reverse_proxy,
        }
        try:
            res = await client.get(req_url, params=params, timeout=120)
            logger.debug(res.json())
        except httpx.HTTPError as e:
            logger.warning(e)
            return [error, f"API异常{e}", False]
        try:
            setu_title = res.json()["data"][0]["title"]
            setu_url = res.json()["data"][0]["urls"]["regular"]
            content = await down_pic(setu_url)
            setu_pid = res.json()["data"][0]["pid"]
            setu_author = res.json()["data"][0]["author"]
            p = res.json()["data"][0]["p"]

            base64 = convert_b64(content)
            data, pic = "", ""
            # 保存图片
            if save:
                try:
                    save_img(content, pid=setu_pid, p=p, r18=r18)
                except Exception:
                    logger.warning(f"{exc_info()[0]}, {exc_info()[1]}")

            if type(base64) == str:
                pic = "[CQ:image,file=base64://" + base64 + "]"
                data = f"\n标题: {setu_title}\n" f"pic: {setu_pid}\n" f"画师: {setu_author}"

            return [pic, data, True, setu_url]
        except httpx.ProxyError as e:
            logger.warning(e)
            return [error, f"代理错误: {e} {exc_info()[0]}, {exc_info()[1]}", False]
        except IndexError as e:
            logger.warning(e)
            return [error, f"图库中没有搜到关于{keyword}的图。", False]


async def down_pic(url):
    async with AsyncClient(proxies=proxies) as client:  # type: ignore
        headers = {
            "Referer": "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }
        re = await client.get(url=url, headers=headers, timeout=120)
        if re.status_code == 200:
            logger.debug("成功获取图片")
            return re.content
        else:
            logger.error(f"获取图片失败: {re.status_code}")
            return re.status_code


def convert_b64(content) -> str:
    ba = str(base64.b64encode(content))
    pic = findall(r"\'([^\"]*)\'", ba)[0].replace("'", "")
    return pic
