import os
rootDir = os.path.dirname(os.path.abspath(__file__))
readmeFile = os.path.join(rootDir, "README.md")
# 제외할 카테고리
excludeCategories = ["Books", ".git", ".obsidian"]
# 미분류 카테고리
specialCategory = "Unclassified-Unwritten"
specialCategoryDisplayName = "미분류/작성중인 글"  # 미분류 카테고리 표시명

# 고정 내용 
fixedContent = """
# TIL
배운 것을 키워드 별로 간결하게 정리한 마크다운 모음입니다.
옵시디언을 사용해 마크다운 문서를 작성하고 [obsidian git](https://github.com/Vinzent03/obsidian-git) 플러그인으로 자동 커밋과 동기화를 진행합니다.
Github Actions를 사용해서 현재 문서 `README.md`에 카테고리별로 글을 분류하여 갱신하게끔 했습니다.
전체적인 스타일은 [Josh Branchaud의 til](https://github.com/jbranchaud/til)을 참고했습니다.
*총 {totalPosts}개의 글*
"""

# 카테고리별 고정 내용
categoryTemplate = "### {category}\n{posts}\n"

def getPostLinks(category):
    categoryPath = os.path.join(rootDir, category)
    posts = []
    
    # 링크 목록 생성
    for post in os.listdir(categoryPath):
        postPath = os.path.join(categoryPath, post)
        if os.path.isfile(postPath):
            postName = os.path.splitext(post)[0]
            postLink = f"- [{postName}](https://github.com/river20s/TIL/blob/main/{category}/{post})"
            posts.append(postLink)
    
    return "\n".join(posts)

def countPostsAndUpdateReadme():
    categories = {}
    totalPosts = 0
    
    # 카테고리 폴더별로 파일 수 카운트
    for category in os.listdir(rootDir):
        categoryPath = os.path.join(rootDir, category)
        if os.path.isdir(categoryPath) and category not in excludeCategories:
            postLinks = getPostLinks(category)
            postCount = len(postLinks.splitlines())
            if postCount > 0:
                categories[category] = postLinks
                totalPosts += postCount
    
    # README 업데이트
    with open(readmeFile, "w", encoding="utf-8") as readme:
        # 고정 내용 작성
        readme.write(fixedContent.format(totalPosts=totalPosts))
        
        # 미분류 카테고리(Unclassified-Unwritten)를 먼저 표시
        if specialCategory in categories:
            special_posts = categories.pop(specialCategory)
            readme.write(categoryTemplate.format(
                category=specialCategoryDisplayName, 
                posts=special_posts
            ))
        
        # 나머지 카테고리들 처리 (알파벳 순 정렬)
        for category in sorted(categories.keys()):
            readme.write(categoryTemplate.format(
                category=category, 
                posts=categories[category]
            ))
        
        # 고정된 하단 내용 작성
        readme.write("""
### 📖 Books
- [성공과 실패를 결정하는 1%의 네트워크 관리](https://github.com/river20s/TIL/tree/main/Books/HowNetworksWork#readme)
- [가상 면접 사례로 배우는 대규모 시스템 설계 기초](https://github.com/river20s/TIL/tree/main/Books/System%20Design%20Interview)
""")

if __name__ == "__main__":
    countPostsAndUpdateReadme()