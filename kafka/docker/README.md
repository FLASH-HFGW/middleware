### How to access HFGW data produced @ LNF

- You do **not** need to clone the repository.
- Copy the `docker-compose.yml` to your local machine.
- Ask for an **access key** and save it in a private folder on your local machine  
  (be sure **not** to commit it or store it in publicly accessible locations).
- The access key must have **user-only permissions**, e.g.:  
  `chmod 600 hfgw_lnf`
- Edit the `docker-compose.yml` and update the path to your access key  
  (e.g. `/Users/mazzitel/.ssh/hfgw_lnf`, `/home/mazzitel/.ssh/hfgw_lnf`, etc.).
- Run the docker container:  
  `docker compose up -d`
- Monitor the data flow:  
  `docker logs ssh-kafka-consumer -f`
- If you want to customize the script, download `receiver.py`, modify it,  
  and uncomment in the `docker-compose.yml` the line:  
  `- ./receiver.py:/app/receiver.py`
- If you prefer to access raw data **without Docker**, it is possible to create an SSH tunnel:
  - Temporary tunnel:  
    `ssh -L 9092:localhost:9092 user@server_kafka` ex `ssh -N -L 9092:localhost:9092 portfw@131.154.99.229 -i hfgw_lnf `
  - Permanent tunnel:  
    https://github.com/CYGNUS-RD/middleware/tree/master/conf/sshtunnel/client  
  - Then write your own script connecting to Kafka at:  
    `localhost:9092`

