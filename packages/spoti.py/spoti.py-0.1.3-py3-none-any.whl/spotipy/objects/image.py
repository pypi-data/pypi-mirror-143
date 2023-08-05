# Future
from __future__ import annotations

# My stuff
from spotipy.typings.objects import ImageData


__all__ = (
    "Image",
)


class Image:

    def __init__(self, data: ImageData) -> None:
        self.url = data["url"]
        self.width = data["width"]
        self.height = data["height"]

    def __repr__(self) -> str:
        return f"<spotipy.Image url='<{self.url}>', width={self.width}, height={self.height}>"
