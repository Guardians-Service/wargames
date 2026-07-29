# 🛡️ Guardians Wargames

**Guardians Wargames**는 BeeGuardians 팀이 개발한 다양한 보안 워게임을 모아놓은 저장소입니다.  
각 워게임은 독립적인 디렉토리로 구성되어 있으며, 자동화된 CI/CD 파이프라인을 통해 효율적으로 배포됩니다.

## 📁 워게임 구조

저장소에는 다음과 같은 워게임 디렉토리들이 포함되어 있습니다:

- `BruteForceLAB-Easy`
- `CRYPTOLAB-Caesar`
- `CRYPTOLAB-XOR`
- `DESERIALIZELAB-Medium`
- `FileUpload-Webshell`
- `FormatStringLAB-Easy`
- `IDOR-Easy`
- `JWTLAB-Medium`
- `LFI-Easy`
- `NOSQLI-Easy`
- `RCELAB-Easy`
- `RSA-High`
- `SQLI-Easy`
- `SQLI-Medium`
- `SSRF-Medium`
- `SSTILAB-Medium`
- `STEGANO-Easy`
- `XSSLAB-Cookie`
- `XSSLAB-Easy`
- `XSSLAB-Medium`

각 디렉토리는 해당 워게임의 `Dockerfile`, `.upload-include` 파일, 소스 코드 등을 포함합니다.

## ⚙️ GitHub Actions 기반 CI/CD 파이프라인

이 저장소는 GitHub Actions를 통해 다음과 같은 자동화 프로세스를 수행합니다:

1. **변경 감지 및 필터링** (2026-07-29부터 자동화됨 — 더 이상 커밋 메시지에 디렉토리명을 적을 필요 없음)
   - `git diff`로 변경된 최상위 디렉토리를 자동으로 감지합니다.
   - 그중 `Dockerfile`이 실제로 존재하는 디렉토리만 빌드 대상으로 필터링합니다 (`.github/` 같은 무관한 폴더가 실수로 걸려도 안전하게 건너뜀).

2. **Docker 이미지 빌드 및 ECR 푸시**
   - 각 워게임 디렉토리의 `Dockerfile`을 이용해 Docker 이미지를 빌드합니다.
   - 빌드된 이미지는 `public.ecr.aws/i7t0x0a1/gaurdians/wargames:<디렉토리명>` 형식으로 ECR에 푸시됩니다.

3. **파일 압축 및 S3 업로드**
   - `.upload-include`에 명시된 파일만을 포함해 ZIP 파일로 압축합니다.
   - 압축된 파일은 `s3://s3-guardians-dev/wargame_zips/` 경로로 업로드됩니다.

> 해당 워크플로우는 `.github/workflows` 디렉토리의 `Deploy CTF Problems` 워크플로우로 관리됩니다.

## 🧪 워게임 실행 방법

각 워게임은 아래와 같이 Docker를 통해 실행할 수 있습니다:

```bash
docker run -p 8000:8000 public.ecr.aws/i7t0x0a1/gaurdians/wargames:<디렉토리명>
```

예시:

```bash
docker run -p 8000:8000 public.ecr.aws/i7t0x0a1/gaurdians/wargames/BruteForceLAB-Easy
```

> 각 워게임은 내부적으로 8000번 포트를 사용하므로, 외부 포트도 8000으로 매핑해야 정상적으로 웹 접근이 가능합니다.

## 🤝 기여 방법

BeeGuardians 팀은 외부 기여를 환영합니다.  
새로운 워게임을 추가하거나 기존 워게임을 개선하고 싶다면 다음 절차를 따라 주세요:

1. 워게임 디렉토리를 생성하거나 수정합니다 (`Dockerfile`은 반드시 포함, 8000번 포트 사용).
2. `.upload-include` 파일을 해당 디렉토리에 생성하여 압축 포함 대상 파일을 지정합니다.
3. GitHub에 푸시하면 자동으로 CI/CD 파이프라인이 실행됩니다 (커밋 메시지에 디렉토리명을 별도로 적을 필요 없음).