# 老杨走了，我不维护了(大哭中)


## 编译应用
### 1. 编译应用的前提
1. 编译前，请确保已经安装好 **python3.10**
2. 安装 `uv`
3. 进入项目根目录
    ```bash
    cd E:\PROJECT_Python\auto_excal
    ```
4. 使用 `uv` 同步依赖和构建依赖
   ```bash
   uv sync --group build
   ```
5. 至此，环境搭建完成，可以开始编译了
### 2. 编译应用
1. **构建可执行文件**：
   ```bash
   uv run cxfreeze build
   ```
2. **生成 zip 发布包**：
   ```bash
   uv run python zip.py --build-dir build/AutoExcal --output-dir dist --artifact-name AutoExcal-1.3.0-windows-amd64.zip --upx upx.exe
   ```
3. **构建结果**：构建后会生成 `build/AutoExcal`，zip 包位于 `dist/` 目录。
### 3. 运行应用
开发环境直接运行：

```bash
uv run python main.py
```

### 4. 更新与下载

- 项目仓库：`https://github.com/UF4OVER/auto_excal`
- 发布页：`https://github.com/UF4OVER/auto_excal/releases`
- 最新版入口：`https://github.com/UF4OVER/auto_excal/releases/latest`

只要后续继续发布到 GitHub Releases，用户就还能通过上述链接继续下载更新版本。

### 5. GitHub Actions 自动构建与发布

项目已内置工作流：`.github/workflows/release.yml`

当推送 tag 时，会自动：

1. 使用 `uv` 安装依赖
2. 使用 `cx_Freeze` 构建 Windows 可执行文件
3. 使用 `zip.py` 生成 zip 发布包
4. 按 tag 对应 commit 的提交信息创建 GitHub Release
5. 上传 zip 作为 Release 资产

本次版本发布约定：

```bash
git add .
git commit -m "feat(release): migrate build pipeline to uv and pyproject"
git tag 1.3.0
git push origin HEAD
git push origin 1.3.0
```

Release 名称和 tag 为 `1.3.0`，正文使用该 tag 对应提交的 commit message。

