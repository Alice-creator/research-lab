from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

def _parse_iso_z(s: str) -> datetime:   
        return datetime.fromisoformat(s.replace("Z", "+00:00"))

class Review(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    title: str
    rating: int = Field(ge=1, le=5)
    body: str
    review_date: str
    reviewer_name: str
    product_url: str
    picture_urls: List[str]
    product_id: str     
    
    @classmethod
    def from_judgeme(cls, item: dict, *, product_url_input: str, product_id: str) -> "Review":
        """
        Map a Judge.me review dict -> Review model

        - review_date <- created_at
        - body <- body (fallback: stripped body_html)
        - picture_urls <- only originals
        - product_url <- absolute; prefer item.product_url_with_utm -> product_url -> input URL
        """
        # body
        body = item.get("body")

        # rating (clamp to 1..5)
        rating = int(item.get("rating") or 1)

        # pictures (originals only)
        originals = [
            p.get("original")
            for p in (item.get("pictures_urls") or [])
            if isinstance(p, dict) and p.get("original")
        ]

        return cls(
            title=(item.get("title") or "").strip(),
            rating=rating,
            body=body,
            review_date= _parse_iso_z(item.get("created_at")).strftime("%d/%m/%Y"),
            reviewer_name=(item.get("reviewer_name") or "").strip(),
            product_url=product_url_input,
            picture_urls=originals,
            product_id=str(product_id),
        )
