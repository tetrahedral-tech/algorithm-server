import matplotlib.dates as md
from plots import colors  #Dont change it to import colors or import .colors ... won't work

def style_plots(figure, plt, interval):
	axes = figure.get_axes()

	for axis in axes:
		axis.tick_params(color=colors.outline(), labelcolor=colors.outline())
		for spine in axis.spines.values():
			spine.set_edgecolor(colors.outline())

		if interval >= 10080:
			xfmt = md.DateFormatter('%Y')
		elif interval >= 1440:
			xfmt = md.DateFormatter('%y/%m')
		elif interval >= 240:
			xfmt = md.DateFormatter('%m/%d')
		elif interval >= 15:
			xfmt = md.DateFormatter('%d')
		else:
			xfmt = md.DateFormatter('%H')

		axis.xaxis.set_major_formatter(formatter=xfmt)

	plt.tight_layout()
