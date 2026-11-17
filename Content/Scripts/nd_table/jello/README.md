# <p align="center">🟢🟡🔴 Jello 🔴🟡🟢</p>

<p align="center">
    <a href="https://github.com/codereport/jello/issues" alt="contributions welcome">
        <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat" /></a>
    <a href="https://lbesson.mit-license.org/" alt="MIT license">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" /></a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-3-ff69b4.svg"/></a>
    <a href="https://github.com/codereport?tab=followers" alt="GitHub followers">
        <img src="https://img.shields.io/github/followers/codereport.svg?style=social&label=Follow" /></a>
    <a href="https://GitHub.com/codereport/jello/stargazers/" alt="GitHub stars">
        <img src="https://img.shields.io/github/stars/codereport/jello.svg?style=social&label=Star" /></a>
    <a href="https://twitter.com/code_report" alt="Twitter">
        <img src="https://img.shields.io/twitter/follow/code_report.svg?style=social&label=@code_report" /></a>
</p>

## Description

A Python script for wrapping the Jellyfish (a fork of Jelly) executable so you can more easily play with the language.

![image](https://github.com/codereport/jello/assets/36027403/26c99f84-36a2-4857-b0f0-1b8f5bd4eef9)

## Links

### Jelly(fish) Links

* [Jelly GitHub Repo](https://github.com/DennisMitchell/jellylanguage/)
* [Jelly Online Interpreter](https://jellyballs.github.io/)
* [Jellyfish Repo 🪼](https://github.com/codereport/jellyfish)

### Livestreams

* [Jello LiveStream I](https://youtube.com/live/jM7UCu220CU)
* [Jello LiveStream II](https://www.youtube.com/watch?v=nnskDAOHRCU)
* [Jello LiveStream III](https://www.youtube.com/watch?v=zOB5D_NgVJU&t)
* [Jello LiveStream IV (Top 10)](https://www.youtube.com/watch?v=XkLsy_I_H6w)
* [Jello LiveStream V (PWC)](https://www.youtube.com/watch?v=tNaZykHHHWs)
* [Jello LiveStream VI (`bits`, `keep`, `cuts.md`, `--find-by-example`)](https://www.youtube.com/watch?v=RAUbKNeA2LA)
* [Jello LiveStream VII (`maxs`, `cuts`, Combinators i.e. `Φ.₂`)](https://www.youtube.com/watch?v=AHLe0wfiu3s)

### YouTube Videos

* [BQN vs Jelly](https://www.youtube.com/watch?v=k9BNn39gWiM)

## Chain Patterns

### Special Chain Names

* **LCC:** [Leading Constant Chain](https://github.com/DennisMitchell/jellylanguage/wiki/Tutorial#whats-the-starting-value)
* **LDC:** Leading Dyadic Chain (described in the first bullet [here](https://github.com/DennisMitchell/jellylanguage/wiki/Tutorial#43dyadic-chains))
* **JL:** Just use Left Arg (as `v`)

### Monadic Chains

**Q: What makes my chain monadic?** <br>
A: If you only pass it one argument (aka `ω`)

|       | Chain pattern | New `v` value | Chain Type |     Name     |  IC   |  SC   |
| :---: | :-----------: | :-----------: | :--------: | :----------: | :---: | :---: |
|   1   |   `+ F ...`   |   `v+F(ω)`    |   `2-1`    | `dyad-monad` |   S   |   Φ   |
|   2   |   `+ 1 ...`   |     `v+1`     |   `2-0`    | `dyad–nilad` |   d   |   Δ   |
|   3   |   `1 + ...`   |     `1+v`     |   `0-2`    | `nilad-dyad` |   d   |   D   |
|   4   |    `+ ...`    |     `v+ω`     |    `2`     |    `dyad`    |   W   |   Σ   |
|   5   |    `F ...`    |    `F(v)`     |    `1`     |   `monad`    |   m   |   B   |

* IC = Initial Combinator
* SC = Subsequent Combinator
* m  = Monadic function application
* d  = Dyadic function application

### Dyadic Chains

**Q: What makes my chain dyadic?** <br>
A: If you pass it two arguments (aka `λ` and `ρ`)

|       | Chain pattern | New `v` value | Chain Type |       Name        |  IC   |  SC   |
| :---: | :-----------: | :-----------: | :--------: | :---------------: | :---: | :---: |
|   1   |  `+ × 1 ...`  |  `(v+ρ)×1`*   |  `2-2-0`   | `dyad-dyad-nilad` |       |       |
|   2   |   `+ × ...`   |   `v+(λ×ρ)`   |   `2-2`    |    `dyad-dyad`    |  Φ₁   |  Φ₁   |
|   3   |   `+ 1 ...`   |     `v+1`     |   `2-0`    |   `dyad-nilad`    |  Kd   |   ε   |
|   4   |   `1 + ...`   |     `1+v`     |   `0-2`    |   `nilad-dyad`    |  πd   |   E   |
|   5   |    `+ ...`    |     `v+ρ`     |    `2`     |      `dyad`       |   d   |  ε'   |
|   6   |    `F ...`    |    `F(v)`     |    `1`     |      `monad`      |  Km   |  B₁   |

## Combinator Table (WIP)

| Combinator | Chain Spelling |
| :--------: | :------------: |
|     S      | `2-1` monadic  |
|     B₁     |  `2-1` dyadic  |
|     E      |
|     ε      |

## Examples

### Example 1 (from [Section 1](https://github.com/DennisMitchell/jellylanguage/wiki/Tutorial#1tacit-programming))

`+H` can be called monadically or dyadically, and is a `2-1` chain.
* If called monadically, its a `2-1` monadic train, aka the `S` combinator.
* If called dyadically, it is a `JL`+`5`+`6`, which ends up being the `B₁` combinator.

### Example 2 (from [Section 4.2](https://github.com/DennisMitchell/jellylanguage/wiki/Tutorial#42monadic-chains))

`+²×` can be called **monadically** or dyadically, and it is a `2-1-2` chain.
* If called monadically, `S` forms a monadic function, that is then used in `Σ`
* If called dyadically, the `2-1` is the `B₁` combinator, and then used in a `Φ₁` where the left dyadic function is `⊢`.

### Example 3 (from [Section 4.3](https://github.com/DennisMitchell/jellylanguage/wiki/Tutorial#43dyadic-chains))

`+×÷H` can be called monadically and **dyadically**, and it is a `2-2-2-1` chain.
* If called monadically, apply `W` is applied, then evalaate the `2-2` part as repeated (or 2) `S` combinators, and then the `2-1` chain at the end matches the `S` combinator.
* If called dyadically, we have a LDC, which means the `2-2-2` forms the `Φ₁` which yield a binary function that is then used in the sits inside a `B₁` along with the final monadic operation.

### Example 4 (Top 10 #3.1 extended — longest increasing run across `iota`s)

`iota flat < prior : + * r . scan maxr add1` (Jelly atoms: `RF<ṕð+×ṛµ\Ṁ‘`) is a `1-1-2-q-s-2-2-2-s-q-1-1` chain, called **monadically**.
* On `[2,4,3]` it returns `4`: `iota` gives `[[1,2],[1,2,3,4],[1,2,3]]`, `flat` concatenates to `[1,2,1,2,3,4,1,2,3]`, `< prior` flags strictly-increasing steps (`[1,0,1,1,1,0,1,1]`), and `: + * r . scan maxr add1` reduces that mask to the longest run plus one.
* The chain collapses to `BBBB`: a row-1 `B` fuses `iota` and `flat`, a row-3 `B` lifts that through an `h₁` over `<`+`prior` (quick), a row-5 `B` joins the left tree to a `Φ₁` over `+ * r` lifted by another `h₁` through `scan` (quick) across `:`, and a row-7 `B` joins everything to the `.` subchain `maxr add1`.
* This is the [Top 10 #3.1](https://www.youtube.com/watch?v=XkLsy_I_H6w) algorithm fronted with `iota flat`, so it generalises from a flat list of integers to a list of lengths.
