#!/usr/bin/env python3
"""Merge category JSON files into one wiki data bundle, validating as we go."""
import json, glob, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'site')
os.makedirs(OUT, exist_ok=True)

CATEGORY_ORDER = [
    ('aws-core',        'AWS 핵심', 'AWS 컴퓨팅·네트워크·스토리지'),
    ('aws-security',    'AWS 보안·IAM', 'AWS 계정·권한·보안 서비스'),
    ('aws-data',        'AWS 데이터·운영', 'AWS DB·통합·운영관리'),
    ('k8s',             'Kubernetes', '컨테이너 오케스트레이션(EKS 포함)'),
    ('cicd',            'CI/CD·GitOps', '컨테이너 빌드·배포 파이프라인'),
    ('iac',             'IaC·자동화', 'Terraform 등 코드형 인프라'),
    ('observability',   '관측성·SRE', '모니터링·로그·장애대응'),
    ('network',         '네트워크', '프로토콜·엣지·서비스 메시'),
    ('security',        '보안·계정권한', 'IAM·비밀관리·보안운영'),
    ('database',        'DB·스토리지', '데이터베이스·메시징·백업'),
    ('app-architecture','앱 아키텍처', '애플리케이션 설계·개발 실무'),
    ('onprem',          '온프레미스', '엔터프라이즈 시스템·하이브리드'),
    ('platform-itsm',   '플랫폼·ITSM', '변경관리·협업도구·멀티클라우드'),
    ('ai-data',         'AI·데이터', 'AI 인프라·데이터 플랫폼'),
    ('compliance',      '규제·감사', 'SOX/ITGC·금감원·ISMS-P'),
]

REQUIRED = ['id','title','oneLiner','explanation']
AUDIT_KEYS = ['itgc','fss','isms','evidence','auditorQuestions','controlExample']

entries = []
seen = {}
problems = []
cat_labels = {}

for cat, short, desc in CATEGORY_ORDER:
    files = sorted(glob.glob(os.path.join(DATA, f'{cat}-*.json')))
    if not files:
        problems.append(f'NO FILES for category {cat}')
        continue
    for f in files:
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            problems.append(f'{os.path.basename(f)}: invalid JSON {e}')
            continue
        cat_labels.setdefault(cat, d.get('categoryLabel') or short)
        for e in d.get('entries', []):
            missing = [k for k in REQUIRED if not e.get(k)]
            if missing:
                problems.append(f"{os.path.basename(f)}: {e.get('id','?')} missing {missing}")
                continue
            eid = e['id']
            if eid in seen:
                problems.append(f"duplicate id {eid} ({seen[eid]} / {os.path.basename(f)}) — skipped")
                continue
            seen[eid] = os.path.basename(f)
            a = e.get('audit') or {}
            e['audit'] = {k: (a.get(k) if a.get(k) else ([] if k != 'controlExample' else '')) for k in AUDIT_KEYS}
            e['cat'] = cat
            e.setdefault('titleEn','')
            e.setdefault('aliases',[])
            e.setdefault('tags',[])
            e.setdefault('level','중급')
            e.setdefault('analogy','')
            e.setdefault('howItWorks','')
            e.setdefault('example','')
            e.setdefault('diagram','')
            e.setdefault('keyTerms',[])
            e.setdefault('pitfalls',[])
            e.setdefault('related',[])
            e.setdefault('learnMore',[])
            entries.append(e)

ids = set(seen)
# prune dangling related links
dangling = 0
for e in entries:
    rel = [r for r in e['related'] if r in ids and r != e['id']]
    dangling += len(e['related']) - len(rel)
    e['related'] = rel

# backlinks: make related symmetric-ish (add reverse links, capped)
back = {e['id']: set() for e in entries}
for e in entries:
    for r in e['related']:
        back[r].add(e['id'])
for e in entries:
    extra = [b for b in sorted(back[e['id']]) if b not in e['related']]
    e['related'] = e['related'] + extra[:max(0, 10 - len(e['related']))]

cats = [{'id': c, 'short': s, 'desc': d, 'label': cat_labels.get(c, s),
         'count': sum(1 for e in entries if e['cat'] == c)}
        for c, s, d in CATEGORY_ORDER if any(e['cat'] == c for e in entries)]

bundle = {'categories': cats, 'entries': entries}
payload = json.dumps(bundle, ensure_ascii=False, separators=(',', ':'))
with open(os.path.join(OUT, 'wikidata.js'), 'w', encoding='utf-8') as fh:
    fh.write('window.WIKI=' + payload + ';')

firebase_fields = {
    'apiKey': 'FIREBASE_API_KEY',
    'appId': 'FIREBASE_APP_ID',
    'authDomain': 'FIREBASE_AUTH_DOMAIN',
    'databaseURL': 'FIREBASE_DATABASE_URL',
    'projectId': 'FIREBASE_PROJECT_ID',
    'storageBucket': 'FIREBASE_STORAGE_BUCKET',
    'messagingSenderId': 'FIREBASE_MESSAGING_SENDER_ID',
    'measurementId': 'FIREBASE_MEASUREMENT_ID',
}
firebase_config = {key: os.environ.get(env_name, '') for key, env_name in firebase_fields.items()}
with open(os.path.join(OUT, 'firebase-config.js'), 'w', encoding='utf-8') as fh:
    fh.write('window.FIREBASE_CONFIG = Object.freeze(')
    fh.write(json.dumps(firebase_config, ensure_ascii=False, separators=(',', ':')))
    fh.write(');\n')

print(f'entries: {len(entries)}')
print(f'categories: {len(cats)}')
for c in cats:
    print(f"  {c['id']:18s} {c['count']:3d}  {c['label']}")
print(f'dangling related pruned: {dangling}')
print(f'bundle size: {len(payload)/1024/1024:.2f} MB')
print(f'entries with diagram: {sum(1 for e in entries if e["diagram"].strip())}')
print(f'entries with audit.itgc: {sum(1 for e in entries if e["audit"]["itgc"])}')
if problems:
    print('\nPROBLEMS (%d):' % len(problems))
    for p in problems[:40]:
        print(' -', p)
else:
    print('\nno problems')
