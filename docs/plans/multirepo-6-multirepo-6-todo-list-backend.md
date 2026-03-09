# Technical Plan: MULTIREPO-6

## Summary
Implementar autenticação completa de login entre Angular e Python, reutilizando a estrutura existente de rotas/componentes no frontend e endpoint/serviço de auth no backend, com JWT, validações de UX, CORS e proteção básica contra brute force.
Sub-task focus: MULTIREPO-6 -  Implementação de Tela de Login (Angular + Python)
Apply only changes needed for this sub-task. Avoid duplicating unrelated scope.
No prior sub-task dependency context.

## Complexity: high

## Estimated Hours: 14

## Steps

### 1. Implementar tela de login no frontend com validação em tempo real
Substituir o conteúdo base atual por formulário de login centralizado com campos de usuário/e-mail e senha, toggle de visibilidade, botão Entrar e link Esqueci minha senha. Aplicar validações reativas (obrigatório, formato de e-mail quando aplicável), estado de loading no botão e bloqueio de submit quando inválido.
Scoped to sub-task MULTIREPO-6:  Implementação de Tela de Login (Angular + Python).
Files: [Todo-list-frontend] src/app/app.component.ts, [Todo-list-frontend] src/app/app.component.html, [Todo-list-frontend] src/app/app.component.css

### 2. Consolidar contrato de autenticação existente
Mapear o fluxo real já presente de autenticação no backend (endpoint, schema, serviço e utilitários de segurança) para confirmar se o POST /api/v1/auth/login já existe, quais campos são aceitos (username/email), e quais claims JWT são emitidas. Esse passo reduz risco de duplicar lógica e define o contrato exato que o frontend deve consumir.
Scoped to sub-task MULTIREPO-6:  Implementação de Tela de Login (Angular + Python).
Files: [todo-list-backend] app/api/v1/endpoints/auth.py, [todo-list-backend] app/schemas/auth.py, [todo-list-backend] app/services/auth.py, [todo-list-backend] app/core/security.py, [todo-list-backend] app/api/v1/router.py, [Todo-list-frontend] package-lock.json, [todo-list-backend] app/api/deps.py

## Risks
- Ausência de política de segurança final para armazenamento do JWT (HttpOnly cookie vs LocalStorage) pode exigir retrabalho.
- Rate limiting pode introduzir impacto em testes automatizados e ambiente local se não houver bypass/configuração por ambiente.
- Sem protótipo Figma anexado, há risco de desalinhamento visual no layout final da tela de login.
- Mudanças no contrato de login (username/email) podem quebrar integrações existentes se não houver compatibilidade retroativa.

## Acceptance Criteria
- [ ] POST /api/v1/auth/login retorna 200 com JWT válido (claims sub, exp, iat) para credenciais corretas.
- [ ] POST /api/v1/auth/login retorna 401 para credenciais incorretas sem expor detalhes sensíveis.
- [ ] Senha é validada apenas via hash seguro (bcrypt/argon2), sem armazenamento em texto plano.
- [ ] CORS permite somente origens configuradas e bloqueia origens não autorizadas.
- [ ] Endpoint de login possui proteção contra brute force com comportamento previsível por ambiente.
- [ ] Tela de login exibe campos obrigatórios, toggle de senha, botão Entrar com loading e link Esqueci minha senha.
- [ ] Botão Entrar permanece desabilitado enquanto o formulário estiver inválido.
- [ ] Frontend apresenta feedback visual claro para erros 401 e 500.
- [ ] Após login com sucesso, usuário é redirecionado para área restrita e sessão permanece válida após refresh quando token ainda não expirou.