clean:
	rm -rf __pycache__ sources/__pycache__ houses.csv weights.pkl

describe:
	@python sources/describe.py

scatter:
	@python sources/scatter_plot.py

histogram:
	@python sources/histogram.py

pair:
	@python sources/pair_plot.py

install:
	python -r requirements.txt

run:
	@python sources/logreg_train.py
	@python sources/logreg_predict.py --model-file weights.pkl --verbose

# TODO units tests for describe and the accuracy with pytest