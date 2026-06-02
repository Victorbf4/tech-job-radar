import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Job {
  id?: string;
  title: string;
  company: string;
  min_salary?: string | null;
  max_salary?: string | null;
  currency?: string | null;
  years_of_experience?: number | null;
  english_level?: string | null;
  modality?: string | null;
  original_url?: string;
  created_at?: string;
  technologies?: Technology[];
}

export interface Technology {
  id: string;
  name: string;
}

@Injectable({
  providedIn: 'root'
})
export class JobService {
  private apiUrl = 'http://localhost:8000/api/jobs';

  constructor(private http: HttpClient) {}

  getJobs(): Observable<Job[]> {
    return this.http.get<Job[]>(this.apiUrl);
  }
}
