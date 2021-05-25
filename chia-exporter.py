import sys
import random
import time
import socket
from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram
from prometheus_client.utils import INF

hostname = socket.gethostname()



#TIME_CHECKING_PROOFS = Summary('time_checking_proofs', 'Time spent checking each proof')
NUMBER_OF_CHALLENGES = Counter('number_of_challenges', "Number of challenges verified", ['host'])
ELIGIBLE_PLOTS = Counter('eligible_plots', 'Number of eligible plots for a specific challenge', ['host'])
PROOFS_FOUND = Counter('proofs_found', 'Number of proofs found for a specific challengee', ['host'])
DURATION = Histogram(
    'check_duration',
    'Time to check challenge',
    ['host'],
    buckets=(.005, .01, .025, .05, .075, .1, .25, .5, .75, 1.0, 2.5, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0, 28.0, 30.0, INF)
)
TOTAL_PLOTS = Gauge('total_plots', 'Total number of plots', ['host'])


def parse_log(line):
  if("eligible" in line):
    decomposed=line.split("chia.harvester.harvester: INFO")[1].strip().split()
    eligible, challenge, proofs, duration, plots = decomposed[0], decomposed[6],  decomposed[8], decomposed[11], decomposed[14]
    NUMBER_OF_CHALLENGES.labels(host=hostname).inc(1)
    ELIGIBLE_PLOTS.labels(host=hostname).inc(int(eligible))
    PROOFS_FOUND.labels(host=hostname).inc(int(proofs))
    DURATION.labels(host=hostname).observe(float(duration))
    TOTAL_PLOTS.labels(host=hostname).set(int(plots))

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9092)

    k = 0
    try:
        buff = ''
        while True:
            buff += sys.stdin.read(1)
            if buff.endswith('\n'):
                parse_log(buff[:-1])
                buff = ''
                k = k + 1
    except KeyboardInterrupt:
       sys.stdout.flush()
       pass
    print(k)
