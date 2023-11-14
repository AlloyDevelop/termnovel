from dataclasses import dataclass
from typing import List

import aiohttp

CONSUMET_API = "https://api.consumet.org/light-novels/readlightnovels"

@dataclass
class SearchResult:
    id: str 
    title: str 
    url: str 
    image: str 

@dataclass
class Chapter:
    """
    This is for LightNovel dataclass
    """
    id: str 
    title: str 
    url: str 

@dataclass
class LightNovel:
    id: str 
    title: str 
    url: str 
    image: str 
    author: str 
    genres: List[str]
    rating: float 
    views: int
    description: str 
    status: str 
    pages: int 
    chapters: List[Chapter]

@dataclass
class ChapterContent:
    novelTitle: str 
    chapterTitle: str
    text: str

async def get_search(query: str) -> SearchResult | None:
    """
    Send a GET request to CONSUMET_API and fetch the result.

    :param: `query: str` Must not contain spaces, should be formatted for a url parameter
    :return: class(SearchResult)
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(CONSUMET_API + "/" + query) as r:
            if r.status != 200:
                return None
    
            chunk = await r.json()
            data: List[SearchResult] = []

            # Return None if the JSON content does not match the fields 
            # of SearchResult.
            try:
                for item in chunk["results"]:
                    data.append(SearchResult(**item))
            except Exception as e:
                print(f"{e}")
                return None 
            return data

async def get_info(id: str):
    """
    Send a GET request to CONSUMET_API/info and fetch details about a specific light novel.

    The ID should be fetched from get_search(...) method
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(CONSUMET_API + "/info?id=" + id) as r:
            if r.status != 200:
                return None 
    
            chunk = await r.json()
            data: LightNovel = None

            # Return None if the JSON content does not match the fields 
            # of LightNovel.
            try:
                data = LightNovel(**chunk)
            except Exception:
                return None 
            return data

async def get_read(chapter_id: str):
    """
    Send a GET request to CONSUMET_API/info and fetch details about a specific light novel.

    The ID should be fetched from get_info(...) method
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(CONSUMET_API + "/read?chapterId=" + chapter_id) as r:
            if r.status != 200:
                return None
    
            chunk = await r.json()
            data: ChapterContent = None

            # Return None if the JSON content does not match the fields 
            # of ChapterContent.
            try:
                data = ChapterContent(**chunk)
            except Exception:
                return None 
            return data