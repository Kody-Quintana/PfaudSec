line_graph_tex = [
r"""
\Large
\begin{center}
\begin{tikzpicture}[trim axis left, trim axis right]% Line graph, use for data over time
	\begin{axis}
		[ymin=0,
                yticklabel style={/pgf/number format/precision=3, /pgf/number format/fixed},
		%ytick distance=1,
		title=\fontsize{25}{25}\selectfont\color{pfgrey}{
""",
# Title goes here
r"""
                },
		tick label style={/pgf/number format/assume math mode},
		every axis plot/.append style={ultra thick},
		ymajorgrids,
		bar width=1,%{0.06\textwidth},
		legend style={
			at={(0.5,-0.2)},
			anchor=north,
			legend columns=-1},
		ylabel={},
		symbolic x coords={
""",
#Symbolic x coords go here
r"""},
		xtick=data,
""",
#ytick distance here (must be set to 1 for values less than 6, otherwise non whole numbers will be used)
r"""nodes near coords,
		nodes near coords align={vertical},
		x tick label style={rotate=35, anchor=north east},]
	\addplot [draw=pfblue,
		nodes near coords={\pgfmathfloatifflags{\pgfplotspointmeta}{0}{}{\pgfmathprintnumber[fixed]{\pgfplotspointmeta}}},
		nodes near coords align={horizontal},
		nodes near coords style={font=\Large,/pgf/number format/assume math mode}]
		coordinates{
""",
#Coordinates go here
r"""
		};
	\end{axis}
\end{tikzpicture}
\end{center}
"""
]

percent_line_graph_tex = [
r"""
\Large
\begin{center}
\begin{tikzpicture}[trim axis left, trim axis right]% Line graph, use for data over time
	\begin{axis}
		[ymin=0,
                yticklabel style={/pgf/number format/precision=3, /pgf/number format/fixed},
		%ytick distance=1,
		title=\fontsize{25}{25}\selectfont\color{pfgrey}{
""",
# Title goes here
r"""
                },
		tick label style={/pgf/number format/assume math mode},
		every axis plot/.append style={ultra thick},
		ymajorgrids,
		bar width=1,%{0.06\textwidth},
		legend style={
			at={(0.5,-0.2)},
			anchor=north,
			legend columns=-1},
		ylabel={},
		symbolic x coords={
""",
#Symbolic x coords go here
r"""},
		xtick=data,
		yticklabel={\pgfmathprintnumber[fixed]\tick\%},
""",
#ytick distance here (must be set to 1 for values less than 6, otherwise non whole numbers will be used)
r"""nodes near coords,
		nodes near coords align={vertical},
		x tick label style={rotate=35, anchor=north east},]
	\addplot [draw=pfblue,
		nodes near coords={\pgfmathfloatifflags{\pgfplotspointmeta}{0}{}{\pgfmathprintnumber[fixed]{\pgfplotspointmeta}\%}},
                %nodes near coords=\pgfmathprintnumber[fixed]{\pgfplotspointmeta}\%
		nodes near coords align={horizontal},
		nodes near coords style={font=\Large,/pgf/number format/assume math mode}]
		coordinates{
""",
#Coordinates go here
r"""
		};
	\end{axis}
\end{tikzpicture}
\end{center}
"""
]


bar_graph_tex = [
r"""
\Large
\begin{center}
\begin{tikzpicture}[trim axis left, trim axis right]% Bar graph, use for current month's values
	\begin{axis}
		[ybar,
                yticklabel style={/pgf/number format/precision=3, /pgf/number format/fixed},
		ymin=0,
		title=\fontsize{25}{25}\selectfont\color{pfgrey}{
""",
# Title goes here                
r"""},
		tick label style={/pgf/number format/assume math mode},
		every axis plot/.append style={ultra thick},
		ymajorgrids,
		bar width={0.04\textwidth},
		legend style={
			at={(0.5,-0.2)},
			anchor=north,
			legend columns=-1},
		ylabel={},
		symbolic x coords={
""",
#Symbolic x coords go here
r"""},
		xtick=data,
""",
#ytick distance here (must be set to 1 for values less than 6, otherwise non whole numbers will be used)
r"""nodes near coords,
		nodes near coords align={vertical},
		x tick label style={rotate=25,anchor=north east},]
	\addplot [fill=pfblue,
		draw=none,
		nodes near coords={
			\pgfmathfloatifflags
			{\pgfplotspointmeta}{0}{}
			{\pgfmathprintnumber[fixed]{\pgfplotspointmeta}}},
		nodes near coords align={south},
		nodes near coords style={font=\Large,/pgf/number format/assume math mode},
		every node near coord/.append style={xshift=0pt,yshift=-24pt,anchor=south,font=\color{white}\Large}]
		coordinates{
""",
# Coordinates go here
r"""
		};
	\end{axis}
% Pareto line
	\begin{axis}
		[ymin=0,
		ymax=100,
		tick label style={/pgf/number format/assume math mode},
		every axis plot/.append style={ultra thick},
		ytick style={draw=none},
		%bar width={0.06\textwidth},
		legend style={
			at={(0.5,-0.2)},
			anchor=north,
			legend columns=-1},
		ylabel={},
		xtick=data,
		xticklabels={,,},
		yticklabel={\pgfmathprintnumber[fixed]\tick\%},
		xtick style={draw=none},
		%nodes near coords,
		%nodes near coords align={vertical},
		yticklabel pos=right,
		y tick label style={},
		x tick label style={},]
	\addplot [draw=orange,
		nodes near coords={}
]
		coordinates{""",

# pareto coords go here

r"""};
	\end{axis}
\end{tikzpicture}
\end{center}
"""
]




latex_table = [
r"""\renewcommand{\baselinestretch}{1.05}
\begin{center}
\LARGE
\keepXColumns
%\newcolumntype{s}{>{\hsize=.7\hsize}X}%TODO do this in python
\begin{tabularx}{\textwidth}{""",
#| Y@{} | s@{} | Y@{} | Y@{} | Y@{} | Y@{} |
r"""}
\multicolumn{""",
#num columns
r"""}{c}{\fontsize{25}{25}\selectfont\color{pfgrey}{""",
#Warranties Claims - \monthyeardate\today
r"""}}\\
\hline""",
#\textbf{Label1} &\textbf{Label2} &\textbf{Label3} &\textbf{Label4} &\textbf{Label5}
r"""\\
\hline
\endfirsthead% all the lines above this will be repeated on every page
\multicolumn{""",
#num columns
r"""}{c}{\fontsize{25}{25}\selectfont\color{pfgrey}{""",
#Warranties Claims - \monthyeardate\today (cont.)
r"""}}\\
\hline
""",
#\textbf{Label1} &\textbf{Label2} &\textbf{Label3} &\textbf{Label4} &\textbf{Label5}
r"""\\
\hline
\endhead% all the lines above this will be repeated on every page
""",
#Color Cell & Color Cell &sdfkjh  & asdfkjh & \\
#\hline
#Color Cell & Color Cell &sdfkjh  & asdfkjh & \\
#\hline
#Color Cell & Color Cell &sdfkjh  & asdfkjh & \\
#\hline
#Color Cell & Color Cell & ksfkjh djhsdfkjh 343 4kj dfsdfkjh  & asdfkjh & \\
#\hline
#Color Cell & Color Cell &sdfkjh  & asdfkjh & \\
#\hline
#Color Cell & Color Cell &sdfkjh  & asdfkjh & \\
#\hline
#Color Cell & slfkjsal;kdfj kdjflksj dsfj  &sdfkjh  & asdfkjh & \\
#\hline
#Color Cell & Color Cell &sdfkjh  & asdfkjh & \\
#\hline
r"""
\end{tabularx}
\end{center}
"""
]
