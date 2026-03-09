import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn,
  Validators
} from '@angular/forms';
import { finalize } from 'rxjs/operators';

interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  username: string;
}

const usernameOrEmailValidator: ValidatorFn = (
  control: AbstractControl
): ValidationErrors | null => {
  const rawValue = control.value;
  const value = typeof rawValue === 'string' ? rawValue.trim() : '';

  if (!value) {
    return null;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const usernameRegex = /^[a-zA-Z0-9._-]{3,50}$/;

  if (emailRegex.test(value) || usernameRegex.test(value)) {
    return null;
  }

  return { usernameOrEmail: true };
};

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
  toastMessage = '';
  toastType: 'success' | 'error' = 'error';
  private toastTimeoutId: ReturnType<typeof setTimeout> | null = null;

  readonly loginForm = this.fb.nonNullable.group({
    username: ['', [Validators.required, usernameOrEmailValidator]],
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

  private showToast(message: string, type: 'success' | 'error'): void {
    this.toastMessage = message;
    this.toastType = type;

    if (this.toastTimeoutId) {
      clearTimeout(this.toastTimeoutId);
    }

    this.toastTimeoutId = setTimeout(() => {
      this.toastMessage = '';
      this.toastTimeoutId = null;
    }, 4000);
  }

  submit(): void {
    if (this.loginForm.invalid || this.isLoading) {
      this.loginForm.markAllAsTouched();
      return;
    }

    const { username, password } = this.loginForm.getRawValue();
    const normalizedUsername = username.trim();

    if (!normalizedUsername) {
      this.loginForm.controls.username.setErrors({ required: true });
      this.loginForm.controls.username.markAsTouched();
      return;
    }

    this.errorMessage = '';
    this.toastMessage = '';
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
          this.showToast('Login realizado com sucesso', 'success');
        },
        error: (error) => {
          if (error?.status === 401) {
            this.errorMessage = 'Usuário ou senha incorretos';
            this.showToast(this.errorMessage, 'error');
            return;
          }
          this.errorMessage = 'Sistema indisponível, tente mais tarde';
          this.showToast(this.errorMessage, 'error');
        }
      });
  }
}
