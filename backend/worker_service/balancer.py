from random import randint,choice
import datetime
import uuid
from entities.worker import Worker,resolver

all_workers = []
all_orders = []


class balancer():
    def __init__(self):
        self.G_t = []
        self.uuid_dict = {}

    def add_graph(self,wor:Worker):
        for p in wor.parameters_declaration:
            self.G_t.append((p,wor.id))

    def add_to_uuid_dict(self,wor:Worker):
        self.uuid_dict[wor.id] = wor

    for wor in all_workers:
        add_graph(wor)
        add_to_uuid_dict(wor)

# start = datetime.datetime.now()

    def balance_order(ord,graphlist,parameter_values):
        grph = []
        for g in graphlist:
            if g[0].name in [x.name for x in ord.parameters]:
                grph.append(g)
        pworkers = {}
        for g in grph:
            try:
                pworkers[g[1]].append(g[0])
            except:
                pworkers[g[1]] = [g[0]]

        for g in pworkers.copy().items():
            if len(g[1]) < len(ord.params):
                pworkers.pop(g[0])

        for p in ord.parameters:
            for g in pworkers.copy().items():
                if p.name not in g[1].name:
                    pworkers.pop(g[0])
        
        for g in pworkers.copy().items():
            if not resolver.resolve(g[0].parameters_expression,parameter_values):
                pworkers.pop(g[0])
        scored_workers = []
        for wor in pworkers:
            scored_workers.append((wor,len(wor.parameters_declaration) + len(wor.orders)))
        return sorted(scored_workers, key=lambda item:item[1])[0][0]

def assign_work(wor:Worker):
    ...

# print(datetime.datetime.now() - start)