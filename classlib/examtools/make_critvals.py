#!/usr/bin/env python3
import argparse
from pathlib import Path
import random


def fmt(x: float, digits: int, mode: str) -> str:
    if mode == "sig":
        s = f"{x:.{digits}g}"
        if "e" in s or "E" in s:
            return s

        core = s.replace(".", "").replace("-", "")
        sig_count = len(core.lstrip("0"))

        if sig_count < digits:
            if "." not in s:
                s += "."
            s += "0" * (digits - sig_count)

        return s

    return f"{x:.{digits}f}"


def parse_csv_floats(s: str):
    return [float(tok.strip()) for tok in s.split(",") if tok.strip()]


def parse_csv_ints(s: str):
    return [int(tok.strip()) for tok in s.split(",") if tok.strip()]


def unique_preserve(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            out.append(x)
            seen.add(x)
    return out


def main():
    p = argparse.ArgumentParser()

    p.add_argument("--out", default="build/critvals.tex")
    p.add_argument("--digits", type=int, default=3)
    p.add_argument(
        "--caption",
        default=r"Upper quantiles: $q_\alpha$ satisfies $\Prob(X>q_\alpha)=\alpha$",
    )

    p.add_argument(
        "--alphas",
        default="0.99,0.975,0.95,0.9,0.1,0.05,0.025,0.01",
    )

    p.add_argument("--t-df", default="")
    p.add_argument("--chi-df", default="")
    p.add_argument("--f-dfn", default="")
    p.add_argument("--f-dfd", default="")
    p.add_argument("--n", type=int, default=0)

    p.add_argument("--t-bait", default="0")
    p.add_argument("--chi-bait", default="0")
    p.add_argument("--f-dfn-bait", default="0")
    p.add_argument("--f-dfd-bait", default="0")
    p.add_argument("--bait-include-target", action="store_true")

    p.add_argument("--shuffle", action="store_true")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--fmt", choices=["dec", "sig"], default="sig")

    args = p.parse_args()

    import scipy.stats as st

    alphas = parse_csv_floats(args.alphas)
    alphas = sorted(unique_preserve(alphas), reverse=True)

    split_at = 0.5
    left_alphas = [a for a in alphas if a >= split_at]
    right_alphas = [a for a in alphas if a < split_at]

    if not left_alphas or not right_alphas:
        m = len(alphas) // 2
        left_alphas, right_alphas = alphas[:m], alphas[m:]

    t_dfs = parse_csv_ints(args.t_df) if args.t_df.strip() else []
    chi_dfs = parse_csv_ints(args.chi_df) if args.chi_df.strip() else []
    f_dfns = parse_csv_ints(args.f_dfn) if args.f_dfn.strip() else []
    f_dfds = parse_csv_ints(args.f_dfd) if args.f_dfd.strip() else []

    if args.n > 0:
        t_target = args.n - 1
        chi_target = 2 * args.n
        f_dfn_target = 1
        f_dfd_target = args.n - 1

        t_offsets = parse_csv_ints(args.t_bait) if args.t_bait.strip() else [0]
        chi_offsets = parse_csv_ints(args.chi_bait) if args.chi_bait.strip() else [0]
        f_dfn_offsets = parse_csv_ints(args.f_dfn_bait) if args.f_dfn_bait.strip() else [0]
        f_dfd_offsets = parse_csv_ints(args.f_dfd_bait) if args.f_dfd_bait.strip() else [0]

        t_from_n = [t_target + k for k in t_offsets if (t_target + k) >= 1]
        chi_from_n = [chi_target + k for k in chi_offsets if (chi_target + k) >= 1]
        f_dfn_from_n = [f_dfn_target + k for k in f_dfn_offsets if (f_dfn_target + k) >= 1]
        f_dfd_from_n = [f_dfd_target + k for k in f_dfd_offsets if (f_dfd_target + k) >= 1]

        if not t_dfs:
            t_dfs = t_from_n
        elif args.bait_include_target and t_target not in t_dfs:
            t_dfs.append(t_target)

        if not chi_dfs:
            chi_dfs = chi_from_n
        elif args.bait_include_target and chi_target not in chi_dfs:
            chi_dfs.append(chi_target)

        if not f_dfns:
            f_dfns = f_dfn_from_n
        elif args.bait_include_target and f_dfn_target not in f_dfns:
            f_dfns.append(f_dfn_target)

        if not f_dfds:
            f_dfds = f_dfd_from_n
        elif args.bait_include_target and f_dfd_target not in f_dfds:
            f_dfds.append(f_dfd_target)

    t_dfs = sorted(unique_preserve(t_dfs))
    chi_dfs = sorted(unique_preserve(chi_dfs))
    f_dfns = sorted(unique_preserve(f_dfns))
    f_dfds = sorted(unique_preserve(f_dfds))

    if args.shuffle:
        rng = random.Random(None if args.seed == 0 else args.seed)
        rng.shuffle(t_dfs)
        rng.shuffle(chi_dfs)
        rng.shuffle(f_dfns)
        rng.shuffle(f_dfds)

    colspec = (
        "rl"
        + ("c" * len(left_alphas))
        + r"@{\hspace{0.6em}}|@{\hspace{0.6em}}"
        + ("c" * len(right_alphas))
    )

    def header_row():
        hL = " & ".join([rf"${a:g}$" for a in left_alphas])
        hR = " & ".join([rf"${a:g}$" for a in right_alphas])
        return r"$X$ & $\alpha$ & " + hL + " & " + hR + r" \\"

    def row_vals(dist_func):
        left_vals = [dist_func(a) for a in left_alphas]
        right_vals = [dist_func(a) for a in right_alphas]
        return left_vals, right_vals

    def row_line(dist, label, left_vals, right_vals):
        L = " & ".join(fmt(v, args.digits, args.fmt) for v in left_vals)
        R = " & ".join(fmt(v, args.digits, args.fmt) for v in right_vals)
        return dist + " & " + label + " & " + L + " & " + R + r" \\"

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append(r"\begin{center}")
    lines.append(r"\small")
    if args.caption.strip():
        lines.append(r"\textbf{" + args.caption + r"}")
        lines.append("")
    lines.append(r"\begin{tabular}{" + colspec + r"}")

    lines.append(header_row())
    lines.append(r"\toprule")

    zL, zR = row_vals(lambda a: st.norm.isf(a))
    lines.append(row_line(r"$\mathrm{Norm}(0,1)$", r"$z_\alpha$", zL, zR))

    if t_dfs or chi_dfs or (f_dfns and f_dfds):
        lines.append(r"\midrule")

    for i, nu in enumerate(t_dfs):
        tL, tR = row_vals(lambda a, nu=nu: st.t.isf(a, nu))
        dist = r"$t_\nu$" if i == 0 else r"{}"
        lines.append(row_line(dist, rf"$t_{{{nu},\alpha}}$", tL, tR))

    if t_dfs and (chi_dfs or (f_dfns and f_dfds)):
        lines.append(r"\midrule")

    for i, nu in enumerate(chi_dfs):
        cL, cR = row_vals(lambda a, nu=nu: st.chi2.isf(a, nu))
        dist = r"$\chi^2_\nu$" if i == 0 else r"{}"
        lines.append(row_line(dist, rf"$\chi^2_{{{nu},\alpha}}$", cL, cR))

    if chi_dfs and f_dfns and f_dfds:
        lines.append(r"\midrule")

    f_first = True
    for dfn in f_dfns:
        for dfd in f_dfds:
            fL, fR = row_vals(lambda a, dfn=dfn, dfd=dfd: st.f.isf(a, dfn, dfd))
            dist = r"$F_{d_1,d_2}$" if f_first else r"{}"
            lines.append(row_line(dist, rf"$F_{{{dfn},{dfd};\alpha}}$", fL, fR))
            f_first = False

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{center}")
    lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
