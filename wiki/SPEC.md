# IT 인프라 위키 — 콘텐츠 작성 스펙 (모든 작성 에이전트 공통)

## 목적
독자는 Eddie — IT SOX/ITGC 매니저(개발자 출신, SAP BASIS·인프라 경험 있음). 클라우드 기반(AWS, Kubernetes 등) 회사로 이직하며,
**어떤 회사에 가더라도 그 회사의 업무 flow를 빠르게 이해**하기 위한 개인용 검색 위키를 만든다.
그는 "비유 + 구체 예시 + 도식"으로 설명받는 것을 선호하며, 이해가 안 되면 더 쉬운 버전을 요구한다.
각 항목은 (1) 기술을 아주 쉽고 상세하게 설명하고 (2) **ITGC(SOX) · 금감원(전자금융감독규정 등) · ISMS-P** 세 관점의 통제 포인트를 함께 담는다.

## 출력 형식
- 순수 JSON 파일. 최상위는 객체:
```json
{
  "category": "aws-core",
  "categoryLabel": "AWS 핵심 서비스",
  "entries": [ ...Entry ]
}
```
- 파일은 여러 개로 나눠 써도 된다 (권장: 파일당 10~15개 항목). 파일명: `<category>-1.json`, `<category>-2.json` ...
- **반드시 유효한 JSON**. 문자열 안의 줄바꿈은 `\n`, 따옴표는 `\"`. 후행 콤마 금지. 주석 금지.
- 한국어로 작성. 기술 용어는 한국어 뒤에 영문 병기 (예: "가용 영역(Availability Zone, AZ)").

## Entry 스키마 (모든 필드 필수, 없으면 빈 배열/빈 문자열)
```json
{
  "id": "aws-ec2",                       // 영문 소문자-하이픈, 전체 위키에서 유일. 접두어는 카테고리 약어 사용
  "title": "EC2",                        // 짧은 제목 (한국어 or 널리 쓰는 영문)
  "titleEn": "Amazon Elastic Compute Cloud",
  "aliases": ["가상서버", "인스턴스", "VM"],   // 검색용 동의어·약어·한글표기. 3~8개. 실무자들이 실제 부르는 말 포함
  "tags": ["compute", "iaas"],
  "level": "기초|중급|심화",
  "oneLiner": "한 문장 정의 (40자 내외)",
  "analogy": "일상 비유 2~4문장. '~와 같다' 형태로. 반드시 채운다.",
  "explanation": "핵심 설명 (HTML 조각). <p>, <ul><li>, <strong>, <code> 만 사용. 4~8문단 분량. 개념 → 왜 필요한가 → 구성요소 → 동작 원리 순.",
  "howItWorks": "동작 순서를 단계별로 (HTML <ol><li>). 실제 요청/데이터가 어떻게 흐르는지.",
  "example": "실무 예시 (HTML). 가상의 핀테크/커머스 회사 시나리오 1개 + 실제 명령어/설정/코드 <pre><code> 1~2개. 코드 안 HTML 특수문자는 &lt; &gt; &amp; 로 이스케이프.",
  "diagram": "인라인 SVG 문자열 또는 빈 문자열 (아래 규칙)",
  "keyTerms": [ {"term": "AMI", "meaning": "한 줄 설명"} ],   // 4~10개
  "pitfalls": ["실무에서 흔한 오해·실수 3~6개"],
  "audit": {
    "itgc": ["SOX ITGC 관점 통제 포인트. 도메인 명시: [접근] [변경] [운영] [ITAC] 접두어 사용. 3~6개"],
    "fss": ["금감원/전자금융감독규정·전자금융거래법·클라우드 이용 가이드 관점. 관련 조항 번호가 확실할 때만 표기(예: 전자금융감독규정 제14조의2 클라우드컴퓨팅서비스 이용절차). 2~5개"],
    "isms": ["ISMS-P 인증기준 관점. 기준 번호가 확실할 때만 표기(예: 2.5.1 사용자 계정 관리, 2.6.1 네트워크 접근, 2.9.1 변경관리, 2.10.x 시스템 및 서비스 보안관리). 2~5개"],
    "evidence": ["감사인이 요청할 증빙 목록: 어떤 화면/로그/설정 export를 어디서 뽑는지 구체적으로. 3~6개"],
    "auditorQuestions": ["현업 담당자에게 실제로 던질 질문 3~6개 (인터뷰용)"],
    "controlExample": "이 기술에 대한 통제 활동 기술문(control description) 예시 1~2문장. 예: '운영 EKS 클러스터의 cluster-admin 권한은 플랫폼팀 3인으로 제한되며, 분기별로 RBAC 바인딩을 리뷰하고 승인 기록을 보관한다.'"
  },
  "related": ["aws-vpc", "k8s-pod"],     // 다른 항목 id. 같은 카테고리 + 아래 '전체 ID 목록'의 다른 카테고리 id 자유 참조. 3~8개
  "learnMore": ["공식 문서 제목 (URL 없이 이름만, 또는 확실한 공식 URL)"]
}
```

## 문체 규칙
- 쉬운 말 우선. 어려운 개념은 "쉽게 말하면 ~" 문장을 한 번 더 넣는다.
- 추상 설명 후 반드시 **구체 숫자/이름이 있는 예시** (예: "결제 API 서버 3대가 ap-northeast-2a/2c에 나뉘어 있고 ...").
- 감사 관점은 "무엇이 통제 대상 자산인지 → 누가 어떻게 접근/변경하는지 → 그 기록이 어디 남는지" 흐름으로.
- 각 항목이 독립적으로 읽혀야 한다 (다른 항목을 안 읽었다고 가정).
- 현재(2026년) 실무에서 통용되는 최신 상태 기준으로 쓴다. 폐기·변경된 명칭은 "구 명칭"으로 병기.

## SVG 도식 규칙 (diagram 필드)
- 항목의 **절반 이상**에 도식을 넣는다. 아키텍처·흐름·관계가 있는 항목은 필수.
- `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 260" font-family="system-ui, sans-serif" font-size="13">` 로 시작. width/height 속성 없음(viewBox만).
- 색: 선/글자는 `stroke="currentColor"` / `fill="currentColor"`. 박스 채움은 `fill="var(--dg-box)"`, 강조 박스 `fill="var(--dg-accent)"`, 배경 없음. 다른 색 하드코딩 금지 (다크/라이트 모드 공용).
- 텍스트는 `<text>`로, 12~14px, 박스 안에서 넘치지 않게 짧게. 화살표는 `<line>`/`<path>` + `marker-end="url(#ar)"`, marker는 svg 안 `<defs>`에 정의 (id는 항목마다 `ar` 그대로 써도 됨).
- 요소 수 15~40개 정도의 단순 도식. 복잡하면 두 개 도식으로 나누지 말고 하나로 요약.
- JSON 문자열에 넣을 때 큰따옴표는 모두 `\"` 로 이스케이프하거나, SVG 속성에 작은따옴표를 사용해도 된다(권장: 작은따옴표).

## 전체 ID 목록(카테고리 접두어) — related 참조용
카테고리와 접두어: aws-core(aws-), aws-security(awssec-), aws-data(awsdata-), k8s(k8s-), cicd(cicd-), iac(iac-), observability(obs-), network(net-), security(sec-), database(db-), app-architecture(app-), onprem(onprem-), platform-itsm(plat-), ai-data(ai-), compliance(comp-).
다른 카테고리 항목을 related로 걸 때는 가장 대표적인 id를 추측해 써라 (예: k8s-pod, k8s-rbac, k8s-ingress, aws-vpc, aws-iam(=awssec-iam), awssec-cloudtrail, awssec-kms, cicd-github-actions, cicd-argocd, iac-terraform, obs-prometheus, obs-grafana, net-tls, net-dns, sec-sso-oidc, sec-vault, sec-pam, db-postgresql, db-kafka, app-msa, onprem-sap-basis, plat-change-management, ai-rag, comp-sox-itgc, comp-fss-egfs, comp-isms-p). 병합 단계에서 존재하지 않는 id는 자동 제거되므로 부담 없이 참조하라.

## 분량
- 항목당 본문(explanation+howItWorks+example) 합계 한국어 1,200~2,500자. 짧게 쓰지 말 것. 토큰을 아끼지 말 것.
- 카테고리당 항목 수는 에이전트 프롬프트에 명시.
