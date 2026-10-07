# Paper Includes — Cross References

# English

- Figure 1: `paper/figures/pipeline.mmd`
- Table 1: `paper/tables/main_results.tex`
- Table 2: `paper/tables/deltas.tex`

When rendering to LaTeX, use:

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=\linewidth]{paper/figures/pipeline.pdf}
    \caption{Scar Memory Agent — conceptual pipeline.}
    \label{fig:pipeline}
\end{figure}

\input{paper/tables/main_results.tex}
\input{paper/tables/deltas.tex}
