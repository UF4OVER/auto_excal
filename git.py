# 获取某个git仓库的所有提交记录

# git.py
from git import Repo

def get_all_commits(repo_path):
    repo = Repo(repo_path)
    commits = list(repo.iter_commits('master'))  # 假设主分支是 'main'，如果是 'master'，请改为 'master'
    for commit in commits:
        # print(f"Commit: {commit.hexsha}")
        print(f"Author: {commit.author.name} <{commit.author.email}>")
        # print(f"Date: {commit.authored_date}")
        print(f"Message: {commit.message}")
        print("-" * 40)

if __name__ == "__main__":
    repo_path = r"E:\python\auto_excal_new\siui"  # 替换为你的 Git 仓库路径
    get_all_commits(repo_path)