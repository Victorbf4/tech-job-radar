from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.job import Job
from app.models.technology import Technology
from app.schemas.job import JobCreateRequest, JobResponse, JobScrapeRequest
from app.services.ai_service import extract_job_data
from app.services.scraper_service import scrape_text_from_url


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    tech: Optional[str] = None,
    min_salary: Optional[int] = None,
    company: Optional[str] = None,
    currency: Optional[str] = None,
    modality: Optional[str] = None,
) -> List[Job]:
    stmt = select(Job).options(selectinload(Job.technologies))

    if min_salary is not None:
        stmt = stmt.where(Job.min_salary >= min_salary)

    if tech is not None:
        normalized_tech = tech.strip()
        if normalized_tech:
            stmt = (
                stmt.join(Job.technologies)
                .where(func.lower(Technology.name) == normalized_tech.lower())
                .distinct()
            )

    if company is not None:
        normalized_company = company.strip()
        if normalized_company:
            stmt = stmt.where(Job.company.ilike(f'%{company}%'))

    if currency is not None:
        normalized_currency = currency.strip()
        if normalized_currency:
            stmt = stmt.where(func.lower(Job.currency) == normalized_currency.lower())

    if modality is not None:
        normalized_modality = modality.strip()
        if normalized_modality:
            stmt = stmt.where(func.lower(Job.modality) == normalized_modality.lower())

    stmt = stmt.offset(skip).limit(limit)
    result = await session.execute(stmt)
    return list(result.scalars().all())


@router.post("/extract")
async def extract_job(request: JobCreateRequest, session: AsyncSession = Depends(get_db)):
    try:
        extracted = await extract_job_data(request.text)
        print("Sin errores - Extracción completada")
        print(extracted)
    except (ValidationError, Exception) as exc:
        print("Error extracting job")
        raise HTTPException(
            status_code=422,
            detail=(
                "No se pudo extraer información válida. Es posible que el sitio haya bloqueado la lectura, "
                "no sea una vacante de TI, o falten tecnologías clave."
            ),
        ) from exc

    job = Job(
        title=extracted.title,
        company=extracted.company,
        min_salary=extracted.min_salary,
        max_salary=extracted.max_salary,
        currency=extracted.currency,
        years_of_experience=extracted.years_of_experience,
        english_level=extracted.english_level,
        modality=extracted.modality,
        original_url=request.original_url,
    )

    session.add(job)

    for tech_name in extracted.technologies:
        normalized = tech_name.strip()
        if not normalized:
            continue

        stmt = select(Technology).where(func.lower(Technology.name) == normalized.lower())
        result = await session.execute(stmt)
        technology = result.scalar_one_or_none()

        if technology is None:
            technology = Technology(name=normalized)
            session.add(technology)

        job.technologies.append(technology)

    await session.commit()
    await session.refresh(job)

    return {
        "id": str(job.id),
        "title": job.title,
        "company": job.company,
        "min_salary": job.min_salary,
        "max_salary": job.max_salary,
        "currency": job.currency,
        "years_of_experience": job.years_of_experience,
        "english_level": job.english_level,
        "modality": job.modality,
        "technologies": [t.name for t in job.technologies],
        "created_at": job.created_at.isoformat() if job.created_at else None,
    }

@router.post("/scrape")
async def scrape_job(request: JobScrapeRequest, session: AsyncSession = Depends(get_db)):
    text = await scrape_text_from_url(request.url)
    print("🛑 TEXTO EXTRAÍDO POR BEAUTIFULSOUP:")
    print(text)
    text_request = JobCreateRequest(text=text, original_url=request.url)
    return await extract_job(text_request, session)