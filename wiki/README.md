# 인프라 도감

정적 HTML·CSS·JavaScript 앱입니다. 항목 데이터는 `data/`의 JSON 파일에서 관리하고 `site/wikidata.js`로 합쳐 배포합니다.

## 빌드

```sh
python3 wiki/build.py
```

## 로컬 실행

저장소 루트에서 다음 명령을 실행한 뒤 `http://localhost:8000/wiki/site/`에 접속합니다.

```sh
python3 -m http.server 8000
```

설치와 오프라인 사용에는 HTTPS 또는 localhost가 필요합니다. 모바일 Chrome에서는 앱 메뉴의 **앱 설치** 또는 **홈 화면에 추가**를 선택할 수 있습니다.

## GitHub Pages 배포

`.github/workflows/deploy-pages.yml`이 `main` 변경 또는 수동 실행으로 `wiki/site/`를 빌드하고 배포합니다. 저장소 Settings → Pages에서 Build and deployment의 Source를 **GitHub Actions**로 한 번 설정해야 합니다.

GitHub의 `github-pages` environment에 다음 변수 또는 secret을 설정하면 빌드가 `site/firebase-config.js`의 `window.FIREBASE_CONFIG`에 반영합니다: `FIREBASE_API_KEY`, `FIREBASE_APP_ID`, `FIREBASE_AUTH_DOMAIN`, `FIREBASE_DATABASE_URL`, `FIREBASE_PROJECT_ID`, `FIREBASE_STORAGE_BUCKET`, `FIREBASE_MESSAGING_SENDER_ID`, `FIREBASE_MEASUREMENT_ID`. 앱 코드에서 Firebase를 초기화할 때 이 객체를 사용하면 됩니다.

Firebase 웹 API 키와 App ID는 브라우저에 전달되므로 배포 후 누구나 볼 수 있습니다. 이 값은 Firebase 웹 설정으로만 사용하고 서비스 계정 키나 관리자 비밀키는 등록하지 마세요. 데이터베이스 접근은 인증, 보안 규칙, App Check로 제한해야 합니다.