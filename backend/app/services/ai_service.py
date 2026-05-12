from __future__ import annotations

from google import genai
from google.genai import types

from app.core.settings import get_settings
from app.schemas.job import JobExtractedData
from app.services.gemini_prompt import GEMINI_SYSTEM_PROMPT


settings = get_settings()

# Inicializamos el cliente moderno de Google GenAI
client = genai.Client(api_key=settings.gemini_api_key)


async def extract_job_data(job_text: str) -> JobExtractedData:
    prompt = f"""{GEMINI_SYSTEM_PROMPT}

        TEXTO DE LA OFERTA (input):
        {job_text}
        """

    # Usamos el método asíncrono del nuevo SDK
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",  # Cambiamos a 2.0-flash para evitar conflictos de versión
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=JobExtractedData,
        ),
    )

    parsed = getattr(response, "parsed", None)
    if parsed is not None:
        print("Parsed:")
        print(parsed)
        if isinstance(parsed, JobExtractedData):
            print("Is JobExtractedData")
            return JobExtractedData.model_validate(parsed.model_dump())
        return JobExtractedData.model_validate(parsed)
    
    if not response.text:
        raise ValueError("Gemini returned an empty response")
        
    return JobExtractedData.model_validate_json(response.text)
