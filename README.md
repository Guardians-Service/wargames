# 🛡️ Guardians-Service wargames

**Guardians-Service wargames**는 Guardians 팀이 개발한 다양한 보안 워게임을 모아놓은 저장소입니다.  
각 워게임은 독립적인 디렉토리로 구성되어 있으며, 자동화된 CI/CD 파이프라인을 통해 효율적으로 배포됩니다.

## 📁 워게임 구조

저장소에는 다음과 같은 워게임 디렉토리들이 포함되어 있습니다:

- `BruteForceLAB-Easy`
- `CRYPTOLAB-Caesar`
- `CRYPTOLAB-XOR`
- `FileUpload-Webshell`
- `FormatStringLAB-Easy`
- `LFI-Easy`
- `RCELAB-Easy`
- `RSA-High`
- `SQLI-Easy`
- `SQLI-Medium`
- `SSTILAB-Medium`
- `STEGANO-Easy`
- `XSSLAB-Cookie`
- `XSSLAB-Easy`
- `XSSLAB-Medium`

각 디렉토리는 해당 워게임의 `Dockerfile`, `.upload-include` 파일, 소스 코드 등을 포함합니다.

## ⚙️ GitHub Actions 기반 CI/CD 파이프라인

이 저장소는 GitHub Actions를 통해 다음과 같은 자동화 프로세스를 수행합니다:


1. **변경 감지**
   - `push` 발생 시 변경된 파일을 기준으로 **최상위 워게임 디렉토리**를 자동 감지합니다.
   - `.github/**`, `README.md` 변경만 있는 경우 배포 대상에서 제외됩니다.

2. **Docker 이미지 빌드 및 GHCR 푸시**
   - 변경된 디렉토리에 `Dockerfile`이 존재하는 경우에만 빌드를 수행합니다.
   - 이미지 태그는 디렉토리 이름을 사용합니다.
   - `ghcr.io/guardians-service/wargames:<디렉토리명>` 형식으로 ECR에 푸시됩니다.

3. **문제 파일 ZIP 생성 및 GCS 업로드**
   - `.upload-include`에 명시된 파일만을 포함해 ZIP 파일로 압축합니다.
   - `.upload-include`파일이 존재하는 경우에만 ZIP 파일을 생성합니다.
   - 압축된 파일은 `gs://guardians-dev/guardians-wargames/<디렉토리명>.zip` 경로로 업로드됩니다.

> 해당 워크플로우는 `.github/workflows` 디렉토리의 `Deploy CTF Problems` 워크플로우로 관리됩니다.

## 🧪 워게임 실행 방법

각 워게임은 아래와 같이 Docker를 통해 실행할 수 있습니다:

```bash
docker run -p 8000:8000 ghcr.io/guardians-service/wargames:<디렉토리명>
```

예시:

```bash
docker run -p 8000:8000 ghcr.io/guardians-service/wargames/BruteForceLAB-Easy
```

> 각 워게임은 내부적으로 8000번 포트를 사용하므로, 외부 포트도 8000으로 매핑해야 정상적으로 웹 접근이 가능합니다.

## 🤝 기여 방법

Guardians 팀은 외부 기여를 환영합니다.  
새로운 워게임을 추가하거나 기존 워게임을 개선하고 싶다면 다음 절차를 따라 주세요:

1. 새로운 워게임 디렉토리를 생성하거나 기존 디렉토리를 수정합니다.
2. 실행이 필요한 경우 Dockerfile을 추가합니다.
3. 문제 파일 배포가 필요한 경우 `.upload-include` 파일을 작성합니다. `.upload-include` 파일을 해당 디렉토리에 생성하여 압축 포함 대상 파일을 지정합니다.
4. 변경 사항을 커밋하고 GitHub에 push합니다.
5. GitHub에 푸시하면 자동으로 CI/CD 파이프라인이 실행됩니다.
