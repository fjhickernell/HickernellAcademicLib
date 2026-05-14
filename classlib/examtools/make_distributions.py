#!/usr/bin/env python3

import sys
from pathlib import Path

OUTPUT = Path("build/distributions.tex")

DISTRIBUTIONS = {
    "binomial": {
        "name": r"Binomial --- $\Bin(n,p)$",
        "space": r"\{0,1,\ldots,n\}",
        "rho": r"\binom{n}{x}\,p^x(1-p)^{n-x}",
        "mu": r"np",
        "var": r"np(1-p)",
    },
    "chi-squared": {
        "name": r"Chi-squared --- $\chi^2_\nu$",
        "space": r"(0,\infty)",
        "rho": r"\frac{1}{2^{\nu/2}\Gamma(\nu/2)}x^{\nu/2-1}e^{-x/2}",
        "mu": r"\nu",
        "var": r"2\nu",
    },
    "exponential": {
        "name": r"Exponential --- $\Exp(\lambda)$",
        "space": r"[0,\infty)",
        "rho": r"\lambda e^{-\lambda x}",
        "mu": r"\frac{1}{\lambda}",
        "var": r"\frac{1}{\lambda^2}",
    },
    "geometric": {
        "name": r"Geometric --- $\Geom(p)$",
        "space": r"\{1,2,\ldots\}",
        "rho": r"p(1-p)^{x-1}",
        "mu": r"\frac{1}{p}",
        "var": r"\frac{1-p}{p^2}",
    },
    "normal": {
        "name": r"Normal --- $\Norm(\mu,\sigma^2)$",
        "space": r"(-\infty,\infty)",
        "rho": r"\frac{\exp\bigl(-(x-\mu)^2/(2\sigma^2)\bigr)}{\sigma\sqrt{2\pi}}",
        "mu": r"\mu",
        "var": r"\sigma^2",
    },
    "poisson": {
        "name": r"Poisson --- $\Poisson(\lambda)$",
        "space": r"\{0,1,2,\ldots\}",
        "rho": r"\frac{\lambda^x \exp(-\lambda)}{x!}",
        "mu": r"\lambda",
        "var": r"\lambda",
    },
    "student-t": {
        "name": r"Student's $t$ --- $t_\nu$",
        "space": r"(-\infty,\infty)",
        "rho": r"\frac{\Gamma((\nu+1)/2)}{\sqrt{\nu\pi}\Gamma(\nu/2)}\left(1+\frac{x^2}{\nu}\right)^{-(\nu+1)/2}",
        "mu": r"0 \ (\nu>1)",
        "var": r"\frac{\nu}{\nu-2} \ (\nu>2)",
    },
    "uniform": {
        "name": r"Uniform --- $\Unif[a,b]$",
        "space": r"[a,b]",
        "rho": r"\frac{1}{b-a}",
        "mu": r"\frac{a+b}{2}",
        "var": r"\frac{(b-a)^2}{12}",
    },
}

def main():
    selected = sys.argv[1:]
    selected = sorted(selected)
    if not selected:
        raise SystemExit("Specify distributions")

    OUTPUT.parent.mkdir(exist_ok=True)

    with OUTPUT.open("w") as f:
        f.write(r"\begin{center}" + "\n")
        f.write(r"\small" + "\n")
        f.write(r"\begin{tabular}{" + "\n")
        f.write("c" + "\n")
        f.write(">{$ \\displaystyle}c<{$}" + "\n")
        f.write(">{$ \\displaystyle}c<{$}" + "\n")
        f.write(">{$ \\displaystyle}c<{$}" + "\n")
        f.write(">{$ \\displaystyle}c<{$}" + "\n")
        f.write("}" + "\n")

        f.write(
            r"Distribution & \text{Sample Space} & \varrho(x) & \mu & \sigma^2 \\"
            + "\n"
        )
        f.write(r"\toprule" + "\n")

        for dist in selected:
            d = DISTRIBUTIONS[dist]
            f.write(
                f"{d['name']} & {d['space']} & {d['rho']} & {d['mu']} & {d['var']} \\\\\n"
            )

        f.write(r"\bottomrule" + "\n")
        f.write(r"\end{tabular}" + "\n")
        f.write(r"\end{center}" + "\n")

    print(f"Wrote {OUTPUT}")

if __name__ == "__main__":
    main()

