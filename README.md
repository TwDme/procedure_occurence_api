To start just run docker

docker-compose build
docker-compose up

I have included just portion of the data as csv

To test endpoints
curl -X POST http://localhost:5000/unique-persons -H "Content-Type: application/json" -d '{"days": 100000}'
curl -X POST http://localhost:5000/unique-providers-by-procedure-type -H "Content-Type: application/json" -d '{"procedure_type": 2000212}'



 

