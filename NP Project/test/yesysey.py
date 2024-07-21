# 원본 딕셔너리 리스트
enabling_contents = [
    {"name": "chapter_name1", "content_file": ["file1", "file2"]},
    {"name": "chapter_name2", "content_file": ["file3", "file4", "file5"]}
]

closing_contents = [
    {"name": "chapter_name1", "content_file": ["file1", "file2"]},
    {"name": "chapter_name2", "content_file": ["file3", "file4", "file5"]}
]

# 두 리스트를 합침
combined_contents = enabling_contents + closing_contents

# 결과 출력
print(combined_contents)
