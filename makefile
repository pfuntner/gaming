all: .run


.build: dockerfile history waiter.py
	docker build -f Dockerfile -t iyt_history .
	touch .build

kill:
	-docker kill history
	-docker rm -f history

.run: kill .build
	docker run --dns 8.8.8.8 --dns 8.8.4.4 --hostname history --detach --name history iyt_history
	touch .run
	@echo
	@echo "Now run: docker exec -it history bash"

clean: kill
	-docker rmi -f iyt_history
	rm -frv .build .run
