import os

enabling_list = []
read_file_list = []

enabling_list_path = os.path.join(os.getcwd(), 'enabling_list')

# 해당 폴더 내 모든 폴더 추출
for item in os.listdir(enabling_list_path):
    sub_folder = os.path.join(enabling_list_path, item)

    # 폴더 여부 확인
    if os.path.isdir(sub_folder):
        enabling_list.append(item)  # 폴더 이름 추가

        # 폴더 내 파일 읽기
        files_in_folder = []
        for filename in os.listdir(sub_folder):
            file_path = os.path.join(sub_folder, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    files_in_folder.append(f.readlines())
        
        read_file_list.append(files_in_folder)  # 폴더 내 파일 내용 추가

print("Enabling List:", enabling_list)
print("Read File List:")
for i, files in enumerate(read_file_list):
    print(f"Folder '{enabling_list[i]}' files:")
    for file_content in files:
        print(file_content)
