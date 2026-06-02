import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { JobService, Job } from '../services/job.service';

@Component({
  selector: 'app-job-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './job-list.component.html',
  styleUrl: './job-list.component.scss'
})
export class JobListComponent implements OnInit {
  jobs: Job[] = [];
  loading = false;
  error: string | null = null;

  constructor(
    private jobService: JobService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadJobs();
  }

  loadJobs(): void {
    this.loading = true;
    this.error = null;
    this.cdr.detectChanges();
    
    this.jobService.getJobs().subscribe({
      next: (data) => {
        console.log('Datos recibidos del backend:', data);
        this.jobs = data;
        this.loading = false;
        console.log('Jobs asignados:', this.jobs);
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'Error al cargar las vacantes. Por favor, intenta nuevamente.';
        this.loading = false;
        console.error('Error loading jobs:', err);
        this.cdr.detectChanges();
      }
    });
  }
}
