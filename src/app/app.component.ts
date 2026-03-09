import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize } from 'rxjs/operators';

interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  username: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  private readonly fb = inject(FormBuilder);
  private readonly http = inject(HttpClient);

  isLoading = false;
  showPassword = false;
  errorMessage = '';

  readonly loginForm = this.fb.nonNullable.group({
    username: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]]
  });

  get usernameControl() {
    return this.loginForm.controls.username;
  }

  get passwordControl() {
    return this.loginForm.controls.password;
  }

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

  submit(): void {
    if (this.loginForm.invalid || this.isLoading) {
      this.loginForm.markAllAsTouched();
      return;
    }

    const { username, password } = this.loginForm.getRawValue();
    const normalizedUsername = username.trim().toLowerCase();

    if (!normalizedUsername) {
      this.loginForm.controls.username.setErrors({ required: true });
      this.loginForm.controls.username.markAsTouched();
      return;
    }

    this.errorMessage = '';
    this.isLoading = true;

    this.http
      .post<LoginResponse>('/api/v1/auth/login', {
        username: normalizedUsername,
        password
      })
      .pipe(finalize(() => (this.isLoading = false)))
      .subscribe({
        next: (response) => {
          localStorage.setItem('auth.access_token', response.access_token);
          localStorage.setItem('auth.user_id', response.user_id);
          localStorage.setItem('auth.username', response.username);
        },
        error: (error) => {
          if (error?.status === 401) {
            this.errorMessage = 'Usuário ou senha incorretos';
            return;
          }
          this.errorMessage = 'Sistema indisponível, tente mais tarde';
        }
      });
  }
}
