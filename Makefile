

.PHONY: data build

# downloads data
data:
	docker-compose run app kaggle datasets download -p data/ --unzip bahramjannesarr/goodreads-book-datasets-10m

# builds docker image
build:
	docker-compose build


clean:
	docker-compose run app rm data/*