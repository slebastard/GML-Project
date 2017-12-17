import numpy as np
from tqdm import tqdm

def EXP3(G, U, eta, gamma, T):
    # nodes of G must be ordered and separated by 1 [0 1 2 ...], [0 2 3] is forbidden
    V = list(G.nodes())
    t = 0
    u = np.array([0 if not n in U else 1/len(U) for n in V])
    q = (1/len(V))*np.ones((T+1, len(V)))
    p = np.zeros((T, len(V)))
    losses = np.zeros((T,))
    for t in tqdm(range(T), desc="Simulating EXP3"):
        p[t] = (1-gamma)*q[t]+gamma*u
        draw = np.random.multinomial(1, p[t])
        It = V[np.argmax(draw)]
        
        # observe
        loss = {action: G.node[action]['arm'].sample()/sum([p[t][pred] for pred in G.predecessors(action)]) for action in G.successors(It)}
        losses[t] = G.node[It]['arm'].sample()
        q[t+1] = np.array([q[t][i]*np.exp(-eta*loss[i]) if i in loss else q[t][i] for i in V])
        q[t+1] = 1/(sum(q[t+1]))*q[t+1]
    return q[-1], losses