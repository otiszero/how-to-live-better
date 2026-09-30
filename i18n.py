# -*- coding: utf-8 -*-
"""build.py 用到的全部界面文案。

正文里的结构键（成本 / 说人话 / 收益 / 证据等级 / 来源 / 备注、成本标签里的
钱=0 时间=少 …）在任何语言的源文件中都保持中文原样，因为性价比档位要靠它们计算；
这里只负责「显示成什么」。新增语言：复制 vi 那一块，逐项翻译即可。

zh 一块必须与原版 build.py 里的硬编码文案逐字一致，这样中文产物不会因重构而变化。
"""

LANGS = {
    "zh": {
        "html_lang": "zh-CN",
        "title": "高性价比人生指南",
        "scope_all": "全书 %d 节",
        "scope_some": "第 %s 节",
        "scope_join": "、",
        "meta_desc": "《高性价比人生指南》%s，共 %d 条建议，"
                     "每条标注成本、收益、证据等级（A/B/C）与原始文献链接。单文件、零依赖、可离线阅读。",
        "jump_label": "跳转到某一节",
        "f_all": "全部",
        "f_a": "只看 A 级",
        "f_plain": "只看说人话",
        "search_ph": "搜索标题、说人话、收益…",
        "theme": "明/暗",
        "count_fmt": "%d / %d 条",
        "unit": "条",
        "sec_count": "%d 条",
        "empty": "没有匹配的条目",
        "top_title": "回到顶部",
        "grade_badge": "%s 级",
        "ratio_badge": "性价比 %s",
        "ratio_names": {"极高": "极高", "高": "高", "一般": "一般"},
        "tag_names": {"口径": "口径", "钱": "钱", "时间": "时间", "毅力": "毅力", "收益": "收益"},
        "tag_values": {},  # 空 = 原样显示
        "row_names": {"成本": "成本", "收益": "收益", "备注": "备注"},
        "src_label": "来源",
        "src_count": "（%d 条文献）",
        "src_credit": "数据来源：",
        "src_license": "（Unlicense，公有领域）",
        "src_rev": "，数据截至 ",
        "rev_date": "（%s）",
        "footer": "%s。<br>"
                  "「说人话」「收益」等栏目为原文摘录，未作改写；本页共 %d 条，"
                  "A 级 %d 条、B 级 %d 条、C 级 %d 条，含 %d 条文献外链。<br>"
                  "单文件自包含，不引用任何外部资源（正文中的文献链接除外），可离线阅读。"
                  "由 build.py 生成。",
        "out_name": "高性价比人生指南_%s.html",
        "out_sec": "第%d节",
        "css_extra": "",
    },
    "vi": {
        "html_lang": "vi",
        "title": "Cẩm nang sống đáng tiền",
        "scope_all": "Toàn bộ %d phần",
        "scope_some": "Phần %s",
        "scope_join": ", ",
        "meta_desc": "Bản tiếng Việt của «高性价比人生指南» (%s), gồm %d lời khuyên, "
                     "mỗi lời khuyên ghi rõ chi phí, lợi ích, mức bằng chứng (A/B/C) và liên kết tài liệu gốc. "
                     "Một file duy nhất, không phụ thuộc, đọc được offline.",
        "jump_label": "Nhảy đến một phần",
        "f_all": "Tất cả",
        "f_a": "Chỉ bằng chứng A",
        "f_plain": "Chỉ xem “nói dễ hiểu”",
        "search_ph": "Tìm tiêu đề, nói dễ hiểu, lợi ích…",
        "theme": "Sáng/Tối",
        "count_fmt": "%d / %d mục",
        "unit": "mục",
        "sec_count": "%d mục",
        "empty": "Không có mục nào khớp",
        "top_title": "Lên đầu trang",
        "grade_badge": "Bằng chứng %s",
        "ratio_badge": "Đáng tiền: %s",
        "ratio_names": {"极高": "rất cao", "高": "cao", "一般": "vừa"},
        "tag_names": {"口径": "Thước đo", "钱": "Tiền", "时间": "Thời gian", "毅力": "Ý chí", "收益": "Lợi ích"},
        "tag_values": {
            "口径": {"自由": "tự do", "金钱": "tiền", "死亡率": "tử vong", "时间": "thời gian"},
            "钱": {"0": "0", "少": "ít", "多": "nhiều"},
            "时间": {"少": "ít", "中": "vừa", "多": "nhiều"},
            "毅力": {"否": "không cần", "些": "một chút", "是": "cần nhiều"},
            "收益": {"大": "lớn", "中": "vừa", "小": "nhỏ"},
        },
        "row_names": {"成本": "Chi phí", "收益": "Lợi ích", "备注": "Ghi chú"},
        "src_label": "Nguồn",
        "src_count": " (%d tài liệu)",
        "src_credit": "Nguồn dữ liệu: ",
        "src_license": " (Unlicense, phạm vi công cộng; bản tiếng Việt do máy dịch)",
        "src_rev": ", dữ liệu đến ",
        "rev_date": " (%s)",
        "footer": "%s.<br>"
                  "Trang này có %d lời khuyên: %d mức A, %d mức B, %d mức C, kèm %d liên kết tài liệu. "
                  "Nội dung là bản dịch tiếng Việt của bản gốc tiếng Trung; khi cần chính xác "
                  "(số liệu, thuật ngữ y khoa) hãy đối chiếu bản gốc và tài liệu trong mục Nguồn.<br>"
                  "Một file tự chứa, không tải tài nguyên ngoài (trừ liên kết tài liệu trong nội dung), "
                  "đọc được offline. Tạo bởi build.py.",
        "out_name": "cam-nang-song-dang-tien_%s.html",
        "out_sec": "phan%d",
        # 越南语标签比汉字长，栏目标签列要加宽
        "css_extra": ".f{grid-template-columns:78px 1fr}"
                     "@media (max-width:820px){.f{grid-template-columns:64px 1fr}}"
                     "@media (max-width:520px){.f{grid-template-columns:1fr;gap:2px}}",
    },
}
