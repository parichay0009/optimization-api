import itertools
import time
import json
import random
import statistics

from flask import Flask,jsonify,request


app = Flask(__name__)

def f(x):
    return x**2

def naive(lists, m, f):
    Maximum = 0
    products = itertools.product(*lists)
    products_list = list(products)
    for prod in products_list:
        k = [f(item) for item in prod]
        total = sum(k) % m
        if  total > Maximum:
            Maximum = total
    return Maximum

def efficient(lists, m, f):
    # Here i am using dynamic programming approch to store results at every elemets of lists and using that sum for
    # the next element also i am using property of mod example (123+321) mod 11 = 4 is same as (123 mod 11) + (321 mod 11)
    # which is 2 + 2 = 4 mod 11 = 4 which is the same as (123+321) mod 11

    fun = f
    dp = []
    for i in lists:
        tmp_list = []
        for j in i:
            if dp == []:
                tmp_list.append(fun(j)%m)
            else:
                for k in dp:
                    # here i am adding new elements(from lists) with previously computed sum stored
                    tmp_list.append(((fun(j)%m) + k)%m)
        dp = tmp_list
    return max(dp)



@app.route('/optimize/naive',methods=['GET'])
def naive_api(request=request):
    """
    :param lists: List of lists with values to choose from.
    :param m: Quotient of modulo operator.
    :param f: Function to map x to f.
    :return: Maximum
    """
    query_parameters = request.args
    lists = query_parameters.get('lists',None)
    fun = query_parameters.get('f',None)
    m = query_parameters.get('m',None)
    if lists == None or m == None or f==None:
        return jsonify(message="Parameters not provided."), 404
    if fun != "f":
        return jsonify(message="Function name not valid."), 400
    try:
        lists = list(json.loads(lists))
    except:
        return jsonify(message="lists param is not valid list type."), 400
    try:
        m = int(m)
    except:
        return jsonify(message="m param is not valid integer type."), 400

    Maximum = naive(lists,m,f)
    
    return dict({"Maximum":Maximum}),200

@app.route('/optimize/efficient',methods=['GET'])
def efficient_api(request=request):
    """
    :param lists: List of lists with values to choose from.
    :param m: Quotient of modulo operator.
    :param f: Function to map x to f.
    :return: Maximum
    """
    query_parameters = request.args
    lists = query_parameters.get('lists',None)
    fun = query_parameters.get('f',None)
    m = query_parameters.get('m',None)
    if lists == None or m == None or f==None:
        return jsonify(message="Parameters not provided."), 404
    if fun != "f":
        return jsonify(message="Function name not valid."), 400
    Maximum = 0
    try:
        lists = list(json.loads(lists))
    except:
        return jsonify(message="lists param is not valid list type."), 400
    try:
        m = int(m)
    except:
        return jsonify(message="m param is not valid integer type."), 400
    
    Maximum = efficient(lists,m,f)
    
    return dict({"Maximum":Maximum}),200

@app.route('/benchmark/naive',methods=['GET'])
def benchmark_naive(request=request):
    """
    :param num_lists: Length of lists.
    :param num_elements: Length of every element in list.
    :param replications: Number of times procedure has to repeat.
    :return: Maximum
    """

    query_parameters = request.args
    num_lists = query_parameters.get('num_lists',None)
    num_elements = query_parameters.get('num_elements',None)
    replications = query_parameters.get('replications',None)
    if num_lists == None or num_elements == None or replications==None:
        return jsonify(message="Parameters not provided."), 404
    
    try:
        num_lists = int(num_lists)
    except:
        return jsonify(message="num_lists param is not valid integer type."), 400
    
    try:
        num_elements = int(num_elements)
    except:
        return jsonify(message="num_elements param is not valid integer type."), 400
    
    try:
        replications = int(replications)
    except:
        return jsonify(message="replications param is not valid integer type."), 400
    times = []
    for repeat in range(replications):
        lists = []
        for list_x in range(num_lists):
            lists.append(random.sample(range(1, 500), num_elements))
        start_time = time.time()
        naive(lists,30,f)
        total_time = time.time() - start_time
        times.append(total_time)
    mean = statistics.mean(times)
    return dict({"Mean":mean}),200



@app.route('/benchmark/efficient',methods=['GET'])
def benchmark_efficient(request=request):
    """
    :param num_lists: Length of lists.
    :param num_elements: Length of every element in list.
    :param replications: Number of times procedure has to repeat.
    :return: Maximum
    """

    query_parameters = request.args
    num_lists = query_parameters.get('num_lists',None)
    num_elements = query_parameters.get('num_elements',None)
    replications = query_parameters.get('replications',None)
    if num_lists == None or num_elements == None or replications==None:
        return jsonify(message="Parameters not provided."), 404
    
    try:
        num_lists = int(num_lists)
    except:
        return jsonify(message="num_lists param is not valid integer type."), 400
    
    try:
        num_elements = int(num_elements)
    except:
        return jsonify(message="num_elements param is not valid integer type."), 400
    
    try:
        replications = int(replications)
    except:
        return jsonify(message="replications param is not valid integer type."), 400
    times = []
    for repeat in range(replications):
        lists = []
        for list_x in range(num_lists):
            lists.append(random.sample(range(1, 500), num_elements))
        start_time = time.time()
        efficient(lists,30,f)
        total_time = time.time() - start_time
        times.append(total_time)
    mean = statistics.mean(times)
    return dict({"Mean":mean}),200


@app.route('/performance',methods=['GET'])
def performance(request=request):
    """
    :param num_lists: Length of lists.
    :return: Json object
    """
    query_parameters = request.args
    num_lists = query_parameters.get('num_lists',None)
    if num_lists == None:
        return jsonify(message="Parameters not provided."), 404
    try:
        num_lists = int(num_lists)
    except:
        return jsonify(message="num_lists param is not valid integer type."), 400
    
    performance = dict()

    naive_x = []
    naive_y = []

    efficient_x = []
    efficient_y = []
    for list_x in range(num_lists):
        lists = []
        for list_y in range(list_x+1):
            lists.append(random.sample(range(1, 500), 10))
        navie_start_time = time.time()
        naive(lists,random.randint(1,50),f)
        navie_total_time = time.time() - navie_start_time
        naive_x.append(list_x+1)
        naive_y.append(navie_total_time)

        start_time = time.time()
        efficient(lists,random.randint(1,50),f)
        total_time = time.time() - start_time
        efficient_x.append(list_x+1)
        efficient_y.append(total_time)
    performance = {"navie":{"x":naive_x,"y":naive_y},"efficient":{"x":efficient_x,"y":efficient_y}}
    return performance,200




if __name__ == '__main__':

    app.run(host='0.0.0.0',port = 5001, debug = True)