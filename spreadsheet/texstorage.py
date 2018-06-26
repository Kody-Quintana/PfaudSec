line_graph_tex = [
r"""
\Large
\begin{center}
\begin{tikzpicture}[trim axis left, trim axis right]% Line graph, use for data over time
	\begin{axis}
		[ymin=0,
		%ytick distance=1,
		title=\fontsize{25}{25}\selectfont\color{pfgrey}{
""",
# Title goes here
r"""
                },
		tick label style={/pgf/number format/assume math mode},
		every axis plot/.append style={ultra thick},
		ymajorgrids,
		bar width={0.06\textwidth},
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
		nodes near coords={\pgfmathfloatifflags{\pgfplotspointmeta}{0}{}{\pgfmathprintnumber{\pgfplotspointmeta}}},
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
		ymin=0,
		title=\fontsize{25}{25}\selectfont\color{pfgrey}{
""",
# Title goes here                
r""" - \monthyeardate\today},
		tick label style={/pgf/number format/assume math mode},
		every axis plot/.append style={ultra thick},
		ymajorgrids,
		bar width={0.06\textwidth},
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
			{\pgfmathprintnumber{\pgfplotspointmeta}}},
		nodes near coords align={south},
		nodes near coords style={font=\Large,/pgf/number format/assume math mode},
		every node near coord/.append style={xshift=0pt,yshift=-24pt,anchor=south,font=\color{white}\Large}]
		coordinates{
""",
# Coordinates go here
r"""
		};
	\end{axis}
\end{tikzpicture}
\end{center}
"""
]
