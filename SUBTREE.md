# Git Subtree Workflow: Anatomica & Parent Repository

This repository ([https://github.com/Ricky-zzz/Anatomica.git](https://github.com/Ricky-zzz/Anatomica.git)) is mirrored with the parent `chansey` repository via `git subtree`.

---

## Quick Reference Commands (Run from parent repository root)

### Push Updates to Standalone Repo
```powershell
git add anatomica/
git commit -m "feat(anatomica): update description"
git subtree push --prefix=anatomica anatomica-origin main
```

### Pull Updates from Standalone Repo
```powershell
git subtree pull --prefix=anatomica anatomica-origin main --squash -m "sync: pull updates from standalone Anatomica repo"
```

### History Mismatch Recovery (`split` method)
```powershell
git subtree split --prefix=anatomica -b anatomica-sync
git push anatomica-origin anatomica-sync:main
git branch -D anatomica-sync
```

### Pre-Push Checklist
- [ ] No `.env` committed
- [ ] No `.venv/` committed
- [ ] No `results/arm1/*.png` or `results/arm2/*.png` committed (only `.gitkeep`)
- [ ] No `assets/flame/*.pkl` committed
