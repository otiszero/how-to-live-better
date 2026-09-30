# -*- coding: utf-8 -*-
"""把上游《高性价比人生指南》逐条翻译成越南语，写入 translations/vi/。

用法：
    python translate.py --repo /path/to/HowToLiveBetter            # 全部节
    python translate.py 1 2 --repo /path/to/HowToLiveBetter        # 只翻某几节
    python translate.py --repo ... --check                         # 只统计待翻条数，不调用 API

需要环境变量 ANTHROPIC_API_KEY 和 `pip install anthropic`。

缓存：translations/vi/.cache.json，键是「源文本块的 sha256」，值是译文。
上游没改的块直接复用，所以每天定时跑只会翻上游变动的那几条。
译文块必须通过结构校验（结构键、成本标签行、链接与原文一致），不通过就重试，
仍失败则该节不写盘并报错，绝不落一个 build.py 解析不了的文件。
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "translations" / "vi"
CACHE_FILE = OUT_DIR / ".cache.json"
DEFAULT_MODEL = "claude-sonnet-5-5"

FIELD_RE = re.compile(r"^-\s*(成本|说人话|收益|证据等级|来源|备注)：", re.M)
TAG_RE = re.compile(r"^<!--\s*成本标签:.*?-->\s*$", re.M)
URL_RE = re.compile(r"https?://[^\s<>)）]+")

SYSTEM = """Bạn là biên dịch viên Trung → Việt cho cuốn sách «高性价比人生指南» (khuyên nhủ đời sống, y tế, pháp lý, tài chính, dựa trên bằng chứng).
Bạn nhận MỘT khối markdown (phần dẫn nhập hoặc một mục `### N. ...`) và trả về đúng khối đó đã dịch sang tiếng Việt. Chỉ trả về khối markdown, không giải thích, không bọc trong ```.

Quy tắc cấu trúc (script sẽ parse bằng regex, sai là hỏng):
1. Giữ NGUYÊN từng ký tự: dòng `[← 回总目录](../README.md)` và mọi dòng `<!-- 成本标签: ... -->` (giá trị 钱=0 时间=少 … giữ tiếng Trung).
2. Giữ nguyên tiền tố khóa + dấu hai chấm toàn-rộng: `- 成本：` `- 说人话：` `- 收益：` `- 证据等级：` `- 来源：` `- 备注：`. Chỉ dịch phần giá trị phía sau. `- 证据等级：A` giữ nguyên chữ cái.
3. Tiêu đề `# N. tên` và `### N. tiêu đề`: giữ số và định dạng, dịch tên/tiêu đề.
4. Giữ nguyên URL, `<https://...>`, tên tài liệu/tạp chí/bài báo tiếng Anh trong mục 来源, số liệu, %, đơn vị, `**đậm**`, `\\*`. Chú thích tiếng Trung trong 来源 thì dịch.
5. Tiền: giữ số, 元 → "NDT" (lần đầu "nhân dân tệ (NDT)"). Không quy đổi sang VND.
6. Thuật ngữ y khoa/thống kê dùng tiếng Việt chuẩn (随机分组试验 = thử nghiệm ngẫu nhiên có đối chứng; 死亡率 = tỷ lệ tử vong). Tên tổ chức giữ viết tắt quen thuộc (WHO, NHTSA, CDC).
7. Giọng đơn giản, thẳng, đời thường như bản gốc, nhất là phần 说人话. Không thêm, không bớt, không bình luận."""


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_chunks(text):
    """按 `### ` 切块：第 0 块是标题+导语，其余每块一条建议。拼回去必须与原文逐字相同。"""
    parts = re.split(r"(?m)^(?=### )", text)
    return parts


def structure_errors(src, dst):
    """返回译文相对原文的结构问题列表，空表示通过。"""
    errs = []
    if FIELD_RE.findall(src) != FIELD_RE.findall(dst):
        errs.append("结构键序列不一致")
    if TAG_RE.findall(src) != TAG_RE.findall(dst):
        errs.append("成本标签行被改动")
    if sorted(URL_RE.findall(src)) != sorted(URL_RE.findall(dst)):
        errs.append("链接集合不一致")
    for ln in src.split("\n"):
        if ln.startswith("[← "):
            if ln not in dst.split("\n"):
                errs.append("回目录行被改动")
    if re.match(r"^###\s+\d+\.", src) and not re.match(r"^###\s+\d+\.\s*\S", dst):
        errs.append("### 标题格式错误")
    m1 = re.match(r"^###\s+(\d+)\.", src)
    m2 = re.match(r"^###\s+(\d+)\.", dst)
    if m1 and (not m2 or m1.group(1) != m2.group(1)):
        errs.append("条目编号不一致")
    return errs


def call_model(client, model, chunk):
    msg = client.messages.create(
        model=model, max_tokens=8000, system=SYSTEM,
        messages=[{"role": "user", "content": chunk}])
    return "".join(b.text for b in msg.content if b.type == "text")


def translate_chunk(client, model, chunk, retries=2):
    last = []
    for _ in range(retries + 1):
        out = call_model(client, model, chunk)
        # 块间空行由拼接保证一致：保持与原块相同的结尾换行数
        out = out.strip("\n") + "\n" * (len(chunk) - len(chunk.rstrip("\n")))
        last = structure_errors(chunk, out)
        if not last:
            return out
    raise RuntimeError("译文结构校验失败：%s\n--- 原文开头 ---\n%s" % ("、".join(last), chunk[:120]))


def main():
    ap = argparse.ArgumentParser(description="逐条翻译上游书稿为越南语")
    ap.add_argument("sections", nargs="*", help="节号；缺省或 all 表示全部")
    ap.add_argument("--repo", default=os.environ.get("HLTB_REPO"), help="上游仓库目录")
    ap.add_argument("--model", default=os.environ.get("HLTB_MODEL", DEFAULT_MODEL))
    ap.add_argument("--check", action="store_true", help="只统计待翻块数，不调用 API")
    args = ap.parse_args()
    if not args.repo:
        raise SystemExit("请用 --repo 或 HLTB_REPO 指定上游仓库目录")

    book = Path(args.repo) / "book"
    files = sorted(book.glob("[0-9][0-9]-*.md"))
    if args.sections and not any(a.lower() == "all" for a in args.sections):
        want = {int(a) for a in args.sections}
        files = [f for f in files if int(f.name[:2]) in want]
    if not files:
        raise SystemExit("找不到要翻译的节")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cache = json.loads(CACHE_FILE.read_text(encoding="utf-8")) if CACHE_FILE.exists() else {}

    todo = sum(1 for f in files for c in split_chunks(f.read_text(encoding="utf-8"))
               if c.strip() and sha(c) not in cache)
    print("待翻 %d 块（%d 节）" % (todo, len(files)))
    if args.check:
        return

    client = None
    if todo:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit("缺少 ANTHROPIC_API_KEY")
        import anthropic
        client = anthropic.Anthropic()

    for f in files:
        chunks = split_chunks(f.read_text(encoding="utf-8"))
        out_parts = []
        for c in chunks:
            if not c.strip():
                out_parts.append(c)
                continue
            key = sha(c)
            if key not in cache:
                cache[key] = translate_chunk(client, args.model, c)
                # 每翻完一块就落盘缓存，中途失败重跑不会白花钱
                CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")
            out_parts.append(cache[key])
        (OUT_DIR / f.name).write_text("".join(out_parts), encoding="utf-8")
        print("已写入 %s" % f.name)


if __name__ == "__main__":
    sys.exit(main())
