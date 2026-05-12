from __future__ import annotations

import asyncio

from app.services.ai_service import extract_job_data


TEST_JOB_TEXT = (
    "Estamos buscando un Senior Backend Developer para unirse a nuestro equipo en Bluetab. "
    "Necesitas al menos 4 años de experiencia trabajando con Python y bases de datos relacionales "
    "como PostgreSQL. Es indispensable tener nivel de inglés B2/C1. El rango salarial es de "
    "3500 a 5000 USD mensuales. Modalidad 100% remota. Valoramos conocimientos en AWS y Docker."
)


async def main() -> None:
    result = await extract_job_data(TEST_JOB_TEXT)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
