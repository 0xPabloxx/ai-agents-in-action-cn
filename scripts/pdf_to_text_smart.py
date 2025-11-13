#!/usr/bin/env python3
"""
智能 PDF 转文本工具 - 使用 PDF 书签/目录进行章节分割
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

try:
    import pymupdf
except ImportError:
    print("错误: 需要安装 PyMuPDF")
    print("请运行: pip install pymupdf")
    sys.exit(1)


def get_toc_from_pdf(pdf_path):
    """从 PDF 获取目录(Table of Contents)"""
    doc = pymupdf.open(pdf_path)
    toc = doc.get_toc()
    doc.close()
    return toc


def extract_chapters_using_toc(pdf_path):
    """使用 TOC 信息提取章节"""
    doc = pymupdf.open(pdf_path)
    toc = doc.get_toc()

    print(f"PDF 文件: {pdf_path}")
    print(f"总页数: {len(doc)}")
    print(f"TOC 条目数: {len(toc)}\n")

    if not toc:
        print("警告: PDF 没有书签/目录信息,将使用备用方法...")
        return extract_chapters_fallback(pdf_path)

    # 解析 TOC 结构
    # TOC 格式: [level, title, page_number]
    chapters = []

    for i, (level, title, page_num) in enumerate(toc):
        # 只处理顶层章节 (level 1 或包含 "Chapter" 的条目)
        if level == 1 or re.search(r'chapter\s+\d+', title, re.IGNORECASE):
            # 确定章节结束页
            end_page = len(doc)
            for j in range(i + 1, len(toc)):
                next_level, next_title, next_page = toc[j]
                if next_level <= level:
                    end_page = next_page - 1
                    break

            chapters.append({
                'title': title.strip(),
                'start_page': page_num,
                'end_page': end_page,
                'level': level
            })

            print(f"发现章节: {title} (页 {page_num}-{end_page})")

    # 提取每个章节的文本
    chapter_data = []
    for idx, chapter in enumerate(chapters):
        print(f"\n提取章节 {idx + 1}/{len(chapters)}: {chapter['title']}")

        content = []
        for page_num in range(chapter['start_page'] - 1, min(chapter['end_page'], len(doc))):
            page = doc[page_num]
            text = page.get_text()
            content.append(text)

            if (page_num + 1) % 20 == 0:
                print(f"  已处理 {page_num + 1 - (chapter['start_page'] - 1)} 页...")

        chapter_data.append({
            'number': idx + 1,
            'title': chapter['title'],
            'start_page': chapter['start_page'],
            'end_page': chapter['end_page'],
            'content': '\n'.join(content)
        })

    doc.close()
    return chapter_data


def extract_chapters_fallback(pdf_path):
    """备用方法: 基于文本模式识别章节"""
    doc = pymupdf.open(pdf_path)

    # 第一遍: 扫描所有页面,查找章节标题
    chapter_locations = []

    print("扫描 PDF 查找章节标题...")

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        blocks = page.get_text("dict")["blocks"]

        # 查找大字体的章节标题
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_content = span["text"].strip()
                        font_size = span["size"]

                        # 检测章节标题: 大字体 + 包含 "Chapter" 或数字开头
                        if font_size > 14:  # 章节标题通常字体较大
                            if re.match(r'^(Chapter|CHAPTER)\s+\d+', text_content):
                                chapter_locations.append({
                                    'page': page_num + 1,
                                    'title': text_content,
                                    'font_size': font_size
                                })
                                print(f"发现章节: {text_content} (页 {page_num + 1})")

        if (page_num + 1) % 50 == 0:
            print(f"已扫描 {page_num + 1}/{len(doc)} 页...")

    # 第二遍: 提取章节内容
    chapters = []
    for i, loc in enumerate(chapter_locations):
        start_page = loc['page']
        end_page = chapter_locations[i + 1]['page'] - 1 if i + 1 < len(chapter_locations) else len(doc)

        print(f"\n提取: {loc['title']} (页 {start_page}-{end_page})")

        content = []
        for page_num in range(start_page - 1, end_page):
            page = doc[page_num]
            text = page.get_text()
            content.append(text)

        chapters.append({
            'number': i + 1,
            'title': loc['title'],
            'start_page': start_page,
            'end_page': end_page,
            'content': '\n'.join(content)
        })

    doc.close()
    return chapters


def save_chapters(chapters, output_dir, pdf_name):
    """保存章节到文件"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    print(f"\n{'='*80}")
    print(f"共提取 {len(chapters)} 个章节")
    print(f"保存到: {output_dir}")
    print(f"{'='*80}\n")

    for chapter in chapters:
        # 清理文件名
        safe_title = re.sub(r'[^\w\s-]', '', chapter['title'])
        safe_title = re.sub(r'\s+', '_', safe_title)[:80]

        filename = f"chapter{chapter['number']:02d}_{safe_title}.txt"
        filepath = output_path / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{'='*80}\n")
            f.write(f"{chapter['title']}\n")
            f.write(f"{'='*80}\n")
            f.write(f"PDF: {pdf_name}\n")
            f.write(f"页码: {chapter['start_page']} - {chapter['end_page']}\n")
            f.write(f"{'='*80}\n\n")
            f.write(chapter['content'])

        word_count = len(chapter['content'].split())
        print(f"✓ {filename}")
        print(f"  页数: {chapter['end_page'] - chapter['start_page'] + 1}, "
              f"字符: {len(chapter['content'])}, "
              f"单词: {word_count}\n")


def main():
    # 设置路径
    translation_dir = Path("/home/pablo/projects/translation")
    pdf_files = list(translation_dir.glob("*.pdf"))

    if not pdf_files:
        print("未找到 PDF 文件")
        return

    # 处理每个 PDF
    for pdf_file in pdf_files:
        print(f"\n{'='*80}")
        print(f"处理: {pdf_file.name}")
        print(f"{'='*80}\n")

        try:
            # 提取章节
            chapters = extract_chapters_using_toc(pdf_file)

            if not chapters:
                print("\n未找到章节,跳过此文件")
                continue

            # 保存章节
            output_dir = translation_dir / f"{pdf_file.stem}_chapters_smart"
            save_chapters(chapters, output_dir, pdf_file.name)

            print(f"\n✓ 完成: {pdf_file.name}\n")

        except Exception as e:
            print(f"\n✗ 处理失败: {e}\n")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
