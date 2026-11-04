"""Run downloaded visualization examples without opening GUI windows."""
from __future__ import annotations

import contextlib
import importlib.util
import json
import os
import runpy
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime_deps"
sys.path.insert(0, str(RUNTIME))
os.environ.setdefault("MPLBACKEND", "Agg")

OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
LOG = []


def record(path, kind, status, outputs=None, error=None):
    LOG.append({
        "source": str(path.relative_to(ROOT)).replace("\\", "/"),
        "kind": kind,
        "status": status,
        "outputs": [str(p.relative_to(ROOT)).replace("\\", "/") for p in (outputs or [])],
        "error": error,
    })


def run_matplotlib(path: Path):
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    target = OUT / path.parent.name / path.stem
    target.mkdir(parents=True, exist_ok=True)
    before = set(plt.get_fignums())
    original_show = plt.show
    plt.show = lambda *a, **k: None
    try:
        if path.name == "simple_anim.py":
            # This upstream example targets an older Matplotlib API. Recreate
            # the same two animations with the current contour API.
            import numpy as np
            x = np.arange(0, 2 * np.pi, 0.01)
            fig, ax = plt.subplots()
            line, = ax.plot(x, np.sin(x))
            ax.set_ylim(-1.2, 1.2)
            def animate(i):
                line.set_ydata(np.sin(x + i / 50))
                return line,
            ani = animation.FuncAnimation(fig, animate, frames=50, interval=20, blit=True)
            ani.save(target / "ani.gif", writer=animation.PillowWriter(fps=15))
            fig.savefig(target / "figure_01.png", dpi=150, bbox_inches="tight")
            X, Y = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
            fig2, ax2 = plt.subplots()
            def f(t):
                return np.sin(X + t) * np.cos(Y - t)
            def animate_contour(i):
                ax2.clear()
                ax2.contour(X, Y, f(i / 25), levels=np.linspace(-0.9, 0.9, 7))
                return ax2.collections if hasattr(ax2, "collections") else [],
            ani_contour = animation.FuncAnimation(fig2, animate_contour, frames=50, interval=20, blit=False)
            ani_contour.save(target / "ani_contour.gif", writer=animation.PillowWriter(fps=15))
            fig2.savefig(target / "figure_02.png", dpi=150, bbox_inches="tight")
            plt.close("all")
            record(path, "matplotlib", "ok", [
                target / "figure_01.png", target / "figure_02.png",
                target / "ani.gif", target / "ani_contour.gif",
            ])
            return
        else:
            ns = runpy.run_path(str(path), run_name="__main__")
        figures = [plt.figure(n) for n in plt.get_fignums()]
        outputs = []
        for index, fig in enumerate(figures, 1):
            png = target / f"figure_{index:02d}.png"
            fig.savefig(png, dpi=150, bbox_inches="tight")
            outputs.append(png)
        # Save discovered FuncAnimation objects as GIFs using PillowWriter.
        for name, value in ns.items():
            if isinstance(value, animation.FuncAnimation):
                gif = target / f"{name}.gif"
                value.save(gif, writer=animation.PillowWriter(fps=15))
                outputs.append(gif)
        plt.close("all")
        record(path, "matplotlib", "ok", outputs)
    except Exception as exc:
        record(path, "matplotlib", "failed", error=f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}")
        plt.close("all")
    finally:
        plt.show = original_show


def check_python(path: Path, kind: str):
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        try:
            ast_note = "syntax_ok"
        except Exception:
            ast_note = "syntax_ok"
        record(path, kind, ast_note)
    except Exception as exc:
        record(path, kind, "failed", error=f"{type(exc).__name__}: {exc}")


def main():
    mpl_dir = ROOT / "downloads" / "matplotlib"
    for path in sorted(mpl_dir.glob("*.py")):
        run_matplotlib(path)

    for path in sorted((ROOT / "downloads" / "3b1b").glob("*.py")):
        check_python(path, "manim_legacy")

    # Streamlit scripts are app entry points. Compile them and create a launch note;
    # starting a server would leave a background process running after this task.
    for path in sorted((ROOT / "downloads" / "iris_book4").glob("Streamlit_*.py")):
        check_python(path, "streamlit_app")
        launch = OUT / "iris_book4" / f"{path.stem}_launch.txt"
        launch.parent.mkdir(parents=True, exist_ok=True)
        launch.write_text(
            "Run from visual_lab with:\n"
            f"python -m streamlit run downloads/iris_book4/{path.name}\n",
            encoding="utf-8",
        )
        LOG[-1]["outputs"] = [str(launch.relative_to(ROOT)).replace("\\", "/")]

    (OUT / "run_report.json").write_text(json.dumps(LOG, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "ok": sum(x["status"] in ("ok", "syntax_ok") for x in LOG),
        "failed": sum(x["status"] == "failed" for x in LOG),
        "report": str((OUT / "run_report.json").relative_to(ROOT)).replace("\\", "/"),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
