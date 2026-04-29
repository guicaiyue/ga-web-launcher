"""启动自举：自动初始化 GenericAgent"""
from core.paths import GA_ROOT
from core.utils import run_cmd


def ensure_generic_agent():
    """确保 GenericAgent 存在，不存在则自动 clone 并初始化基础文件"""
    if GA_ROOT.exists():
        return {"ok": True, "status": "exists", "path": str(GA_ROOT)}

    print("[Bootstrap] GenericAgent not found, cloning...")
    GA_ROOT.parent.mkdir(parents=True, exist_ok=True)
    repo_url = "https://github.com/lsdefine/GenericAgent.git"
    result = run_cmd(
        ["git", "clone", "--depth", "1", repo_url, str(GA_ROOT)],
        cwd=GA_ROOT.parent,
        timeout=120,
    )

    if result.returncode != 0:
        return {
            "ok": False,
            "error": f"Clone failed: {result.stderr.strip() or result.stdout.strip()}",
        }

    template = GA_ROOT / "mykey_template.py"
    mykey = GA_ROOT / "mykey.py"
    if template.exists() and not mykey.exists():
        mykey.write_text(template.read_text("utf-8"), "utf-8")
        print(f"[Bootstrap] Created {mykey} from template")

    return {"ok": True, "status": "cloned", "path": str(GA_ROOT)}


__all__ = ["ensure_generic_agent"]
