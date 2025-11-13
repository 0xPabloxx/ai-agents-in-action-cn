#!/usr/bin/env python3
"""
PDF to Text Converter - Chapter by Chapter
处理 PDF 文件并按章节分割保存为文本文件
"""

import os
import re
import sys
from pathlib import Path

try:
    import pymupdf  # PyMuPDF
except ImportError:
    print("错误: 需要安装 PyMuPDF")
    print("请运行: pip install pymupdf")
    sys.exit(1)


def extract_text_from_pdf(pdf_path):
    """从 PDF 提取所有文本"""
    doc = pymupdf.open(pdf_path)
    full_text = []

    print(f"正在处理 PDF: {pdf_path}")
    print(f"总页数: {len(doc)}")

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        full_text.append({
            'page': page_num + 1,
            'text': text
        })
        if (page_num + 1) % 10 == 0:
            print(f"已处理 {page_num + 1}/{len(doc)} 页...")

    doc.close()
    return full_text


def split_by_chapters(pages_text):
    """将文本按章节分割"""
    chapters = []
    current_chapter = {
        'number': 0,
        'title': 'Front Matter',
        'content': '',
        'start_page': 1
    }

    # 常见的章节标题模式
    chapter_patterns = [
        r'^Chapter\s+(\d+)[:\s]+(.+)$',
        r'^CHAPTER\s+(\d+)[:\s]+(.+)$',
        r'^第\s*([一二三四五六七八九十\d]+)\s*章[:\s]+(.+)$',
        r'^\d+\s+(.+)$',  # 数字开头的章节
    ]

    for page_info in pages_text:
        page_num = page_info['page']
        text = page_info['text']
        lines = text.split('\n')

        for i, line in enumerate(lines):
            line = line.strip()

            # 检查是否是章节标题
            is_chapter = False
            for pattern in chapter_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    # 保存当前章节
                    if current_chapter['content'].strip():
                        chapters.append(current_chapter.copy())

                    # 开始新章节
                    if len(match.groups()) >= 2:
                        chapter_num = match.group(1)
                        chapter_title = match.group(2).strip()
                    else:
                        chapter_num = str(len(chapters) + 1)
                        chapter_title = match.group(1).strip() if match.groups() else line

                    current_chapter = {
                        'number': chapter_num,
                        'title': chapter_title,
                        'content': '',
                        'start_page': page_num
                    }
                    is_chapter = True
                    print(f"发现章节: Chapter {chapter_num} - {chapter_title} (Page {page_num})")
                    break

            # 如果不是章节标题,添加到当前章节内容
            if not is_chapter:
                current_chapter['content'] += line + '\n'

    # 保存最后一个章节
    if current_chapter['content'].strip():
        chapters.append(current_chapter)

    return chapters


def save_chapters(chapters, output_dir):
    """保存章节到单独的文件"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    print(f"\n共找到 {len(chapters)} 个章节")
    print(f"保存到目录: {output_dir}\n")

    for chapter in chapters:
        if chapter['number'] == 0:
            filename = f"00_front_matter.txt"
        else:
            # 清理标题用于文件名
            safe_title = re.sub(r'[^\w\s-]', '', chapter['title'])
            safe_title = re.sub(r'\s+', '_', safe_title)[:50]
            filename = f"chapter{chapter['number']}_{safe_title}.txt"

        filepath = output_path / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Chapter {chapter['number']}: {chapter['title']}\n")
            f.write(f"Starting Page: {chapter['start_page']}\n")
            f.write("=" * 80 + "\n\n")
            f.write(chapter['content'])

        print(f"✓ 已保存: {filename} ({len(chapter['content'])} 字符)")


def main():
    # 设置路径
    translation_dir = Path("/home/pablo/projects/translation")
    pdf_files = list(translation_dir.glob("*.pdf"))

    if not pdf_files:
        print("未找到 PDF 文件")
        return

    # 处理每个 PDF 文件
    for pdf_file in pdf_files:
        print(f"\n{'='*80}")
        print(f"处理文件: {pdf_file.name}")
        print(f"{'='*80}\n")

        # 提取文本
        pages_text = extract_text_from_pdf(pdf_file)

        # 按章节分割
        chapters = split_by_chapters(pages_text)

        # 保存章节
        output_dir = translation_dir / f"{pdf_file.stem}_chapters"
        save_chapters(chapters, output_dir)

        print(f"\n✓ 完成处理: {pdf_file.name}\n")


if __name__ == "__main__":
    main()
