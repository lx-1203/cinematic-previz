"""Read-only validation of the 分镜总览 / 生成任务 XLSX layout.

Custom user templates take precedence; this checker covers the default layout,
not wording quality, picture correctness, sentence boundaries or user approval.
"""
import argparse
import json
import pathlib
import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile

GUIDANCE_HEADERS = ['叙事任务与动作表演', '景别机位与构图', '完整旁白与声音', '运镜与焦点', '风格色调与光影', '切点与承接']
LEGACY_HEADERS = {'任务与情绪节拍', '景别、机位与镜头', '起幅→落幅构图与空间', '动作与表演', '运镜、焦点与节奏', '台词与声音', '必要分镜设计'}
ID_HEADERS = {'镜号与时间', '镜号／时间', '镜号/时间'}
PROMPT_HEADERS = {'当前完整视频规划词', '当前完整视频提示词', '当前完整视频词'}
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
OVERVIEW = '分镜总览'
TASKS = '生成任务'
OVERVIEW_HEADERS = ['镜号与时间', '生成包ID', '画面与表演', '运镜与承接', '台词与音效', '关键预览', '提示词', '状态与缺项']
TASK_HEADERS = ['包号与时间', '所含镜号', '平台／模式／时长', '实际素材引用', '当前完整视频词', '审核与执行状态']


class Formula(str):
    """Distinguish an actual spreadsheet formula from a typed imitation."""


def read_xlsx(path, preserve_formulas=False):
    tables = {}
    with zipfile.ZipFile(path) as archive:
        strings = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            strings = [''.join(t.text or '' for t in item.findall('.//s:t', NS)) for item in ET.fromstring(archive.read('xl/sharedStrings.xml')).findall('s:si', NS)]
        rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))}
        for sh in ET.fromstring(archive.read('xl/workbook.xml')).findall('s:sheets/s:sheet', NS):
            target = rels[sh.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
            member = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            rows = {}
            for row in ET.fromstring(archive.read(member)).findall('s:sheetData/s:row', NS):
                values = []
                for cell in row.findall('s:c', NS):
                    letters = re.match(r'[A-Z]+', cell.get('r'))[0]
                    column = 0
                    for letter in letters:
                        column = column * 26 + ord(letter) - 64
                    value = cell.find('s:v', NS)
                    formula = cell.find('s:f', NS)
                    text = value.text or '' if value is not None else ''
                    if cell.get('t') == 's':
                        text = strings[int(text)]
                    elif cell.get('t') == 'inlineStr':
                        text = ''.join(t.text or '' for t in cell.findall('.//s:t', NS))
                    if formula is not None and (preserve_formulas or sh.get('name') in {OVERVIEW, TASKS}):
                        text = Formula('=' + (formula.text or ''))
                    values.extend([''] * max(0, column - len(values)))
                    values[column - 1] = text
                rows[int(row.get('r'))] = values
            tables[sh.get('name')] = rows
    return tables


def validate(tables):
    if OVERVIEW in tables or TASKS in tables:
        return validate_overview(tables)
    errors, headers, shots = [], {}, {}
    for name in ['逐镜脚本', '提示词指导']:
        if name not in tables:
            errors.append({'code': 'SHEET_MISSING', 'sheet': name})
            continue
        rows = tables[name]
        header_row = next((r for r, values in sorted(rows.items()) if values and values[0] in ID_HEADERS), None)
        if header_row is None:
            errors.append({'code': 'HEADER_MISSING', 'sheet': name})
            continue
        headers[name] = rows[header_row]
        body = [(r, v) for r, v in sorted(rows.items()) if r > header_row and v and str(v[0]).strip()]
        shots[name] = [re.split(r'[\s／/]+', str(v[0]).strip())[0] for _, v in body]
        if not body:
            errors.append({'code': 'SHOTS_EMPTY', 'sheet': name})
        if len(set(shots[name])) != len(shots[name]):
            errors.append({'code': 'SHOT_DUPLICATE', 'sheet': name})
        if name == '逐镜脚本':
            normalized = ['镜号与时间' if h in ID_HEADERS else '当前完整视频规划词' if h in PROMPT_HEADERS else h for h in headers[name] if h]
            expected = ['镜号与时间', '场次与人物阶段', '当前完整视频规划词', '首帧', '人物参考', '场景参考', '表情参考', '物品参考', '生成设置与状态', '审阅意见']
            if normalized != expected:
                errors.append({'code': 'MAIN_HEADERS', 'expected': expected})
            forbidden = set(GUIDANCE_HEADERS) | LEGACY_HEADERS
            found = sorted(set(headers[name]) & forbidden)
            if found:
                errors.append({'code': 'MAIN_GUIDANCE_COLUMNS', 'headers': found})
            prompt = [i for i, title in enumerate(headers[name]) if title in PROMPT_HEADERS]
            if len(prompt) != 1:
                errors.append({'code': 'MAIN_PROMPT_COLUMN'})
            elif any(len(v) <= prompt[0] or not str(v[prompt[0]]).strip() for _, v in body):
                errors.append({'code': 'PROMPT_EMPTY'})
        else:
            if [v for v in headers[name][1:] if v] != GUIDANCE_HEADERS:
                errors.append({'code': 'GUIDANCE_HEADERS', 'expected': GUIDANCE_HEADERS})
            if any(len(v) < 7 or any(not str(x).strip() for x in v[1:7]) for _, v in body):
                errors.append({'code': 'GUIDANCE_EMPTY'})
    if len(shots) == 2 and shots['逐镜脚本'] != shots['提示词指导']:
        errors.append({'code': 'SHOT_MAPPING'})
    return {'status': 'valid' if not errors else 'invalid', 'errors': errors, 'shots': len(shots.get('逐镜脚本', [])), 'scope': 'Default sheet layout, header placement, nonempty design and ordered shot IDs; semantic and media checks remain separate.'}


def identifier(value):
    return str(value).splitlines()[0].strip() if value else ''


def task_rows(tables):
    from validate_production_timing import body
    return body(tables.get(TASKS, {}), {TASK_HEADERS[0]})


def validate_overview(tables):
    from validate_production_timing import body, cell, interval
    from validate_prompt_format import SHOT, bounds

    errors = []

    def error(code, **details):
        errors.append(dict(code=code, **details))

    if set(tables) != {OVERVIEW, TASKS}:
        error('SHEET_SET', expected=[OVERVIEW, TASKS])
    for name, expected in [(OVERVIEW, OVERVIEW_HEADERS), (TASKS, TASK_HEADERS)]:
        rows = tables.get(name, {})
        header = next((r for r, v in sorted(rows.items()) if v and v[0] == expected[0]), None)
        if header is None or rows[header] != expected:
            error('SHEET_HEADERS', sheet=name, expected=expected)

    overview = body(tables.get(OVERVIEW, {}), {OVERVIEW_HEADERS[0]})
    tasks = task_rows(tables)
    shot_ids = [identifier(v[0]) for _, v in overview]
    package_ids = [identifier(v[0]) for _, v in tasks]
    for ids, name in [(shot_ids, OVERVIEW), (package_ids, TASKS)]:
        if not ids or not all(ids) or len(ids) != len(set(ids)):
            error('ROW_IDS', sheet=name)
    owners = {}
    ordered = []
    for row, values in tasks:
        package = identifier(values[0])
        members = str(cell(values, 1)).split()
        if not members or any(not str(cell(values, i)).strip() for i in range(2, 6)):
            error('TASK_FIELDS', package=package)
        if isinstance(cell(values, 4), Formula):
            error('TASK_PROMPT_NOT_LITERAL', package=package)
        prompt = str(cell(values, 4)).replace('\r\n', '\n')
        ranges = [bounds(m['time']) for m in SHOT.finditer(prompt)]
        if len(ranges) != len(members):
            error('TASK_SHOT_COUNT', package=package)
        package_range = interval(values[0])
        for i, shot in enumerate(members):
            relative = ranges[i] if i < len(ranges) else None
            global_range = tuple(package_range[0] + t for t in relative) if package_range and relative else None
            owners[shot] = (package, row, global_range)
        ordered.extend(members)
    if shot_ids != ordered:
        error('SHOT_MAPPING')
    for (row, values), shot in zip(overview, shot_ids):
        owner = owners.get(shot)
        if owner is None:
            continue
        package, task_row, global_range = owner
        if cell(values, 1) != package:
            error('SHOT_PACKAGE', row=row)
        formula = cell(values, 6)
        if not isinstance(formula, Formula) or formula != f"='{TASKS}'!$E${task_row}":
            error('MAIN_PROMPT_REFERENCE', row=row, package=package)
        actual_range = interval(values[0])
        if not global_range or not actual_range or any(abs(a - b) > 1e-6 for a, b in zip(actual_range, global_range)):
            error('SHOT_TIME', row=row)
        if any(not str(cell(values, i)).strip() for i in (2, 3, 4, 7)):
            error('OVERVIEW_FIELDS', row=row)
    return {'status': 'invalid' if errors else 'valid', 'errors': errors,
            'shots': len(overview), 'packages': len(tasks)}


def validate_delivery(tables, prompt_mode='multi_shot', check_timing=True, segment_seconds=15,
                      reading_evidence=None):
    """Check layout, prose, package timing and recorded reading evidence."""
    from validate_prompt_format import validate_workbook
    report = validate(tables)
    prompts = validate_workbook(tables, prompt_mode)
    report['errors'].extend(prompts['errors'])
    report['status'] = 'invalid' if report['errors'] else 'valid'
    report['prompt_format'] = {'status': prompts['status'], 'prompts': prompts['prompts']}
    if check_timing:
        from validate_production_timing import validate as validate_timing
        timing = validate_timing(tables, segment_seconds, prompt_mode, reading_evidence)
        report['errors'].extend(timing['errors'])
        report['production_timing'] = {k: v for k, v in timing.items() if k != 'errors'}
    report['status'] = 'invalid' if report['errors'] else 'valid'
    report['scope'] = 'Layout, prose, package timing and recorded reading evidence; semantics, real recordings, bindings, approval and platform support remain separate.'
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xlsx', type=pathlib.Path)
    parser.add_argument('--mode', choices=['multi_shot', 'single_shot'], default='multi_shot')
    parser.add_argument('--segment-seconds', type=float, default=15)
    parser.add_argument('--reading-evidence', type=pathlib.Path)
    parser.add_argument('--legacy', action='store_true', help='Check an existing pre-overview workbook')
    args = parser.parse_args()
    try:
        tables = read_xlsx(args.xlsx)
        if not args.legacy and set(tables) != {OVERVIEW, TASKS}:
            report = validate_overview(tables)
        else:
            evidence = None
            if OVERVIEW in tables and TASKS in tables:
                path = args.reading_evidence or args.xlsx.with_name('reading-evidence.json')
                if path.exists():
                    evidence = json.loads(path.read_text(encoding='utf-8-sig'))
            report = validate_delivery(tables, args.mode, segment_seconds=args.segment_seconds,
                                       reading_evidence=evidence)
    except (OSError, ValueError, KeyError, IndexError, ET.ParseError, zipfile.BadZipFile) as exc:
        print(json.dumps({'status': 'unreadable', 'error': str(exc)}, ensure_ascii=True))
        return 2
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0 if not report['errors'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
