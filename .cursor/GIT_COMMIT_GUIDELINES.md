# Git Commit Guidelines

## 防止 Co-authored-by 自动添加

### 已配置的保护措施

项目已配置以下 Git 设置来防止不必要的内容被添加到 commit message：

```bash
# 在项目 .git/config 中已设置
[commit]
    cleanup = strip    # 自动清理空行和注释
    verbose = true     # 显示详细的 diff
```

### 提交时的注意事项

1. **使用命令行提交时**
   ```bash
   # 推荐方式：直接使用 -m
   git commit -m "你的提交信息"
   
   # 避免使用可能添加额外信息的方式
   # ❌ 不要使用 --trailer 选项
   git commit --trailer "Co-authored-by: xxx"
   ```

2. **检查提交信息**
   ```bash
   # 提交前预览
   git commit --dry-run -m "你的信息"
   
   # 查看最后一次提交
   git log -1 --pretty=full
   ```

3. **如果不小心添加了 Co-authored-by**
   ```bash
   # 修改最后一次提交
   git commit --amend
   # 在编辑器中删除 Co-authored-by 行
   
   # 或者直接重写 message
   git commit --amend -m "新的提交信息"
   ```

### 永久性清理历史记录

如果历史中已经有了 Co-authored-by，使用以下命令清理：

```bash
# 清理所有 Co-authored-by 记录
git filter-branch --msg-filter 'sed "/^Co-authored-by: Cursor/d"' -- --all

# 清理备份
git for-each-ref --format='delete %(refname)' refs/original/ | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 强制推送（警告：这会重写历史）
git push --force origin main
```

### 为什么会出现 Co-authored-by

可能的原因：
1. Cursor IDE 可能有自动添加 co-author 的功能
2. 某些 Git GUI 工具会自动添加
3. 使用了带有 `--trailer` 参数的 git commit 命令

### 解决方案

- ✅ 已配置 `commit.cleanup = strip` 自动清理
- ✅ 使用简单的 `git commit -m "message"` 命令
- ✅ 避免使用 Cursor 的某些提交功能（如果它们会自动添加）
- ✅ 提交前检查 commit message

### 验证配置

```bash
# 查看当前配置
git config --local --list | grep commit

# 应该看到
# commit.cleanup=strip
# commit.verbose=true
```

## 提交最佳实践

1. **清晰的提交信息**
   ```
   feat: Add new feature
   fix: Fix bug in component
   docs: Update documentation
   refactor: Refactor code structure
   ```

2. **避免包含**
   - 空行（在消息末尾）
   - 注释行（以 # 开头）
   - 不相关的 trailers（Co-authored-by, Signed-off-by 等，除非必要）

3. **提交前检查**
   ```bash
   git status
   git diff --staged
   git commit -m "your message" --dry-run
   ```

---

**记住：简单明了的提交信息是最好的！**
