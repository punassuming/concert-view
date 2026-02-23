import json
import logging
from typing import Any

from app.models.layout import (
    Layout,
    LayoutSlot,
    LayoutSuggestionRequest,
    LayoutSuggestionResponse,
)
from app.services.layout_service import generate_grid_layout, generate_pip_layout

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are a video layout designer for a multi-camera concert view application. "
    "Given a feed count and desired style, return a JSON object with two keys: "
    '"layout" (an object with "name" (string), "slots" (array of objects with '
    '"feed_id", "x", "y", "width", "height" where x/y/width/height are floats 0-1), '
    '"output_width" (int), "output_height" (int)) and "description" (string). '
    "Return ONLY valid JSON, no markdown."
)


def _build_user_prompt(request: LayoutSuggestionRequest) -> str:
    return (
        f"Create a {request.style} layout for {request.feed_count} camera feeds "
        f"at a live concert. Return JSON only."
    )


def _parse_ai_response(raw: str, request: LayoutSuggestionRequest) -> LayoutSuggestionResponse:
    """Parse the AI JSON response into a LayoutSuggestionResponse."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    data: dict[str, Any] = json.loads(text)
    layout_data = data.get("layout", data)
    slots = [LayoutSlot(**s) for s in layout_data.get("slots", [])]
    layout = Layout(
        name=layout_data.get("name", f"{request.style} layout"),
        slots=slots,
        output_width=layout_data.get("output_width", 1920),
        output_height=layout_data.get("output_height", 1080),
    )
    return LayoutSuggestionResponse(
        layout=layout,
        description=data.get("description", "AI-generated layout"),
    )


async def _try_openai(request: LayoutSuggestionRequest, api_key: str) -> LayoutSuggestionResponse:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(request)},
        ],
        temperature=0.7,
    )
    raw = response.choices[0].message.content or ""
    return _parse_ai_response(raw, request)


async def _try_gemini(request: LayoutSuggestionRequest, api_key: str) -> LayoutSuggestionResponse:
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"{_SYSTEM_PROMPT}\n\n{_build_user_prompt(request)}"
    response = await model.generate_content_async(prompt)
    raw = response.text or ""
    return _parse_ai_response(raw, request)


def _fallback(request: LayoutSuggestionRequest) -> LayoutSuggestionResponse:
    """Use built-in layout generators when no AI keys are available."""
    if request.style == "pip":
        layout = generate_pip_layout(request.feed_count, name=f"PiP – {request.feed_count} feeds")
        desc = "Picture-in-picture layout generated locally."
    else:
        layout = generate_grid_layout(request.feed_count, name=f"Grid – {request.feed_count} feeds")
        desc = "Grid layout generated locally (no AI keys configured)."
    return LayoutSuggestionResponse(layout=layout, description=desc)


async def get_layout_suggestion(
    request: LayoutSuggestionRequest,
    openai_key: str = "",
    gemini_key: str = "",
) -> LayoutSuggestionResponse:
    """Try AI providers in order, falling back to built-in generators."""
    if openai_key:
        try:
            return await _try_openai(request, openai_key)
        except Exception:
            logger.warning("OpenAI layout suggestion failed, trying next provider", exc_info=True)

    if gemini_key:
        try:
            return await _try_gemini(request, gemini_key)
        except Exception:
            logger.warning("Gemini layout suggestion failed, using fallback", exc_info=True)

    return _fallback(request)
