## Chia Harvester Monitoring ###

Very quick and dirty Harvester monitoring (including the local harvester when running a full node).

Setup:

1) Enable INFO level logging in ~/.chia/mainnet/config/config.yml and restart your harvester
2) `pip3 install prometheus-client` wherever you want to run this
3) Pipe the Harvester log into the chia-exporter.py. I run the harvester in a container so it looks like this (run under `screen`):

```docker exec -it chia-harvester-1.1.1 tail -F /root/.chia/mainnet/log/debug.log | python3 chia-exporter.py```

4) Start scraping the exporter metrics with Prometheus (see reference prometheus.yml config).
5) Import the JSON dashboard into Grafana.

![Dashboard screenshot](dashboard-screenshot.png?raw=true "Dashboard Screenshot")
