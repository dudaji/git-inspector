This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, Setup environment variable in .env.local

```bash
cp ./.env.example ./.env.local
```

Copy environment variable values from [Notion](https://www.notion.so/dudaji/2024-07-08-Gemini-API-Developer-competition-b45d57ce7e934f1c8748db9f5450ca58?pvs=4#e7d975f39ba54bf590d159d7501da987)

Second, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Hosting Web on Firebase

```bash
firebase deploy --only hosting:git-inspector
```

## Emulate and Deploy cloud function on Firebase
### Env 설정
[안내](https://www.notion.so/dudaji/2024-07-08-Gemini-API-Developer-competition-b45d57ce7e934f1c8748db9f5450ca58?pvs=4#3924a8550b9d4e8fbb5e41d91789abdb)에 따라 `.env` 파일을 생성합니다.
### Emulate
1. venv 설정
    ```bash
    cd functions
    python -m venv venv
    ./venv/bin/pip3 install -r requirements.txt
    ```
1. Emulator 실행

    ```bash
    # frontend 폴더로 이동
    firebase emulators:start --only functions
    ---
    # 정상적으로 실행되면 아래와 같은 로그가 나오고, 해당 주소로 요청보낼 수 있음
    functions[us-central1-analyzer]: http function initialized (http://127.0.0.1:5001/gpu-brokerage/us-central1/analyzer).
    ```
1. curl로 테스트
    ```bash
    curl -X POST http://127.0.0.1:5001/gpu-brokerage/us-central1/analyzer -d '{"repoUrl": "https://github.com/rjwharry/coin-dashboard.git", "branchName": "main", "directory": ""}' -H "Content-Type: application/json" | jq
    ```
### Deploy
```bash
firebase deploy --only functions
```