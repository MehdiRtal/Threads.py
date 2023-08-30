import httpx
import urllib.parse
import json
import re
from instagrapi import Client

from .utils import get_media_id_from_url


class Threads:
    def __init__(self, proxy: str = None):
        self._client = httpx.Client(proxies=f"http://{proxy}" if proxy else None)
        self._instagrapi = Client(proxy=f"http://{proxy}" if proxy else None)
        self.session_id = None
        self.fb_dtsg = None

    def login(self, username: str = None, password: str = None, session_id: str = None):
        if username and password:
            try:
                self._instagrapi.login(username=username, password=password)
            except:
                raise Exception("Login failed")
            self.session_id = self._instagrapi.sessionid
        elif session_id:
            self.session_id = session_id
        self._client.cookies = {
            "sessionid": self.session_id
        }
    
    def _refresh_fb_dtsg(self):
        if not self.fb_dtsg:
            r = self._client.get("https://www.threads.net/404")
            try:
                self.fb_dtsg = re.search(r'"token":"(.+?)"', r.text).group(1)
            except:
                raise Exception("Login failed")

    def edit_profile(self, name: str, bio: str, avatar: str):
        if not self._instagrapi.sessionid:
            self._instagrapi.login_by_sessionid(self._client.cookies["sessionid"])
        self._instagrapi.account_edit(full_name=name, biography=bio)
        self._instagrapi.account_change_picture(avatar)

    def like(self, url: str):
        self._refresh_fb_dtsg()
        
        body = f"variables={urllib.parse.quote(json.dumps({'media_id': get_media_id_from_url(url)}))}&fb_dtsg={self.fb_dtsg}&doc_id=6163527303756305"
        r = self._client.post(
            "https://www.threads.net/api/graphql",
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data=body
        )
        if r.status_code != 200:
            raise Exception("Like failed")
    
    def follow(self, username: str):
        self._refresh_fb_dtsg()
        
        user_id = self._instagrapi.user_id_from_username(username)

        body = f"variables={urllib.parse.quote(json.dumps({'target_user_id': user_id}))}&fb_dtsg={self.fb_dtsg}&doc_id=6240353742756860"
        r = self._client.post(
            "https://www.threads.net/api/graphql",
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data=body
        )
        if r.status_code != 200:
            raise Exception("Follow failed")

    def repost(self, url: str):
        self._refresh_fb_dtsg()
        
        body = f"variables={urllib.parse.quote(json.dumps({'media_id': get_media_id_from_url(url)}))}&fb_dtsg={self.fb_dtsg}&doc_id=6590225731000123"
        r = self._client.post(
            "https://www.threads.net/api/graphql",
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data=body
        )
        if r.status_code != 200:
            raise Exception("Repost failed")