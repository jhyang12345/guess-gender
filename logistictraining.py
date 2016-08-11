from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import math, copy, random

def separate(comments):
    x = []
    y = []
    for comment in comments:
        newx = {}
        for key in comment:
            if key != '_id' and key != 'gender':
                newx[key] = comment[key]
            elif key == 'gender':
                if comment['gender'] == 'male':
                    y.append(1)
                elif comment['gender'] == 'female':
                    y.append(0)
        x.append(newx)
    return (x, y)

def logistic(x):
    return 1.0 / (1 + math.exp(-x))

def g(x, theta):
    ret = 0
    ret += theta['theta0']
    for key in x.keys():
        if key == '_id':
            continue
        elif type(x[key]) == dict:
            for key2 in x[key].keys():
                ret += (x[key][key2] * theta[key][key2])
        else:
            ret += (x[key] * theta[key])
    return ret

def nexttheta(theta, alpha, x, y):
    m = len(y)
    newtheta = copy.deepcopy(theta)
    val = 0
    for i in range(m):
        val += (h(x[i], theta) - y[i])
    newtheta['theta0'] = theta['theta0'] - alpha * val / m
    for key in theta.keys():
        if key == '_id' or key == 'gender' or key == 'theta0':
            continue
        elif type(theta[key]) == dict:
            for key2 in theta[key].keys():
                val = 0
                for i in range(m):
                    val += (h(x[i], theta) - y[i]) * x[i][key][key2]
            #    print(val)
                newtheta[key][key2] = theta[key][key2] - alpha * val / m
        else:
            val = 0
            for i in range(m):
                val += (h(x[i], theta) - y[i]) * x[i][key]
            #print(val)
            newtheta[key] = theta[key] - alpha * val / m
    return newtheta

def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def h(x, theta):
    return logistic(g(x, theta))#both row vectors

def cost(theta, x, y):
    m = len(y)
    J = 0
    for i in range(m):
        J += (y[i] * math.log(h(x[i], theta)) + (1 - y[i]) * math.log(1 - h(x[i], theta)))
    J = - J / m
    return J

def main():
    print("Starting training.")
    try:
        c = MongoClient(host='localhost', port=27017)
    except ConnectionFailure as e:
        sys.stderr.write("Connecion failed.")
        sys.exit(1)
    dbh = c['commentdb']
    men = dbh.trainingsample.find({'gender': 'male'})
    women = dbh.trainingsample.find({'gender': 'female'})
    total = dbh.trainingsample.find({})

#    print(separate([men[0]]))
    theta = dbh.theta.find({})[0]
#
    alphas = [100, 10, 1, 0.3, 0.1, 0.03]
    x, y = separate(total)
    print(cost(theta, x, y))
    i = 0
    originalcost = cost(theta, x, y)
    for _ in range(10000):
        print("Current learning rate:", alphas[i])
        newtheta = nexttheta(theta, alphas[i], x, y)
        if cost(newtheta, x, y) > originalcost:
            i += 1
            if i < len(alphas):
                continue
            else:
                print("Theta found:", theta)
                break
        theta = newtheta
        originalcost = cost(theta, x, y)
        print(originalcost)
        for key in theta:
            dbh.theta.update({}, {'$set': {key: theta[key]}})
    print(theta)

"""    dbh.theta.delete_many({})
    theta = {}
    theta['theta0'] = 0
    for key in men[0].keys():
        if key == '_id' or key == 'gender':
            continue
        print(key, men[0][key])
        theta[key] = 0
        if type(men[0][key]) == dict:
            theta[key] = {}
            for x in men[0][key]:
                theta[key][x] = 0
    print(theta)
    dbh.theta.insert(theta)
"""


if __name__ == '__main__':
    main()
