clean:
	rm -rf __pycache__ sources/__pycache__ houses.csv weights.pkl

install:
	python -r requirements.txt

run:
	@python sources/logreg_train.py
	@python sources/logreg_predict.py --model-file weights.pkl --verbose

# TODO units tests for describe and the accuracy with pytest