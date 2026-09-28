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