clean:
	rm -rf __pycache__ sources/__pycache__

install:
	python -r requirements.txt

# TODO run rule with logtrain and logpredict
# TODO units tests for describe and the accuracy