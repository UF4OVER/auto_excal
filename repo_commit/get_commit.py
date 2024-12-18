# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : upper_computer
#  @Time    : 2025 - 01-11 20:56
#  @FileName: get_commit.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
import git

path = r'E:\python\upper_computer'
repo = git.Repo(path)

commits = list(repo.iter_commits())

for commit in commits:
    author = commit.author
    commit_data = commit.committed_datetime
    message = commit.message

    print(f"提交人: {author.name}")
    print(f"提交时间: {commit_data}")
    print(f"提交信息: {message}")

