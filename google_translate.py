import asyncio
import functools
import logging
import os
import re
import sys
from typing import List
from tqdm import tqdm

import httpx
import langcodes
from more_itertools import chunked

GOOGLE_API_KEY = "AIzaSyDMx3Lf9EGMyve9EArG0IJ__FkJYJ5MPBQ"
URL = f"https://translation.googleapis.com/language/translate/v2?key={GOOGLE_API_KEY}"
GOOGLE_SUPPORTED_LANGUAGES = None


@functools.cache
def get_supported_languages() -> List[str]:
    global GOOGLE_SUPPORTED_LANGUAGES
    if GOOGLE_SUPPORTED_LANGUAGES:
        return GOOGLE_SUPPORTED_LANGUAGES
    else:
        # Get the supported languages from Google
        url = "https://translation.googleapis.com/language/translate/v2/languages"
        params = {"key": GOOGLE_API_KEY}
        response = httpx.get(url, params=params)
        data = response.json()
        GOOGLE_SUPPORTED_LANGUAGES = [d["language"] for d in data["data"]["languages"]]
        return GOOGLE_SUPPORTED_LANGUAGES


async def batch_translate_texts(
    texts: List[str], source_language_code: str, target_language_code: str
) -> List[str]:
    supported_languages = get_supported_languages()
    if target_language_code not in supported_languages:
        target_language_code = langcodes.closest_supported_match(
            target_language_code, supported_languages
        )
        if not target_language_code:
            raise ValueError(
                f"Language code {target_language_code} is not supported by Google Translate."
            )

    if (
        source_language_code not in supported_languages
        and source_language_code != "auto"
    ):
        source_language_code = langcodes.closest_supported_match(
            source_language_code, supported_languages
        )
        if not source_language_code:
            raise ValueError(
                f"Language code {source_language_code} is not supported by Google Translate."
            )

    if source_language_code == target_language_code:
        return texts

    translations = []
    for chunk in chunked(
        texts, 128
    ):  # Google Translate API has a limit of 128 texts per request
        if source_language_code == "auto":
            payload = {
                "q": chunk,
                "target": target_language_code,
            }
        else:
            payload = {
                "source": source_language_code,
                "q": chunk,
                "target": target_language_code,
            }
        async with httpx.AsyncClient() as client:
            response = await client.post(URL, json=payload)
            data = response.json()
            translations.extend(
                [d["translatedText"] for d in data["data"]["translations"]]
            )

    return translations


async def translate_text(text, source_language_code, target_language_code):
    texts = re.split(r"(\n+)", text)
    input_texts = [text for text in texts if text.strip()]
    translatons = await batch_translate_texts(
        input_texts, source_language_code, target_language_code
    )

    output_texts = []
    for text in texts:
        if text.strip():
            output_texts.append(translatons.pop(0))
        else:
            output_texts.append(text)

    return "".join(output_texts)


if __name__ == "__main__":
    source_language_code = sys.argv[1]
    target_language_code = sys.argv[2]

    for batch in tqdm(chunked(sys.stdin, 100)):
        batch = [line.strip() for line in batch]
        results = asyncio.run(
            batch_translate_texts(batch, source_language_code, target_language_code)
        )
        for result in results:
            print(result)
