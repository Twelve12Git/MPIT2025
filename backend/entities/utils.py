from worker import Worker, WorkerParameterDescription
from order import Order
from uuid import UUID

ParameterName_t = str
WorkerId_t = UUID

G_t = list[
    tuple[ParameterName_t, WorkerId_t | ParameterName_t] # worker - leaf
]

graph = [
    # ("param1", "param2"),
    ("param2", "dd7b9413-00fb-45b2-80b6-0c86f80e2bbd")
]

def get_candidates(names: list[ParameterName_t], g: G_t) -> list[WorkerId_t]:
    # g - only for Parameter -> Worker relations
    candidates = []
    # add relation with rest parameters
    g.extend([(names[0], other) for other in names[1:]])
