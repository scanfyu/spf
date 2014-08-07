import ptf
import numpy as np
#from ptf import *
#class ptfstore?

def dump_model(fname, model):
    f = open(fname, 'w+')

    f.write("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n" % \
        (model.user_count, model.item_count, model.K, model.MF, model.trust, \
        model.iat, model.intercept, model.undirected, model.binary, model.sorec))

    user_mapping = ''
    for user in model.users:
        user_mapping += ' %d:%d' % (user, model.users[user])
    f.write("%s\n" % user_mapping.strip())
    
    item_mapping = ''
    for item in model.items:
        if not isinstance(item, basestring):
            item_mapping += ' %d:%d' % (item, model.items[item])
        else:
            item_mapping += ' %s:%d' % (item, model.items[item])
    f.write("%s\n" % item_mapping.strip())

    f.close()

def dump(fname, model, params):
    f = open(fname, 'w+')

    # intercepts
    if model.intercept:
        intercepts = ''
        for i in params.inter:
            intercepts += ' %.5e' % i
        f.write("%s\n" % intercepts.strip())

    # eta
    if model.trust and model.iat:
        f.write("%.5e\n" % params.eta)

    # tau
    if model.trust or model.iat:
        tau = ''
        for row in params.tau.rows:
            for col in params.tau.rows[row]:
                tau += ' %d:%d:%.5e' % (row,col,params.tau.rows[row][col])
        f.write("%s\n" % tau.strip())

    # theta
    if model.MF or model.iat:
        row_id = 0
        for row in params.theta:
            r = 'U%d' % row_id
            for val in row:
                r += " %.5e" % val
            f.write("%s\n" % r)
            row_id += 1

    # beta
    if model.MF or model.iat:
        row_id = 0
        for row in params.beta:
            r = 'I%d' % row_id
            for val in row:
                r += " %.5e" % val
            f.write("%s\n" % r.strip())
            row_id += 1
    
    f.close()

#print ptf.parameters

def load_model(fname):
    f = open(fname, 'r')

    user_count, item_count, K, MF, trust, iat, intercept, undirected, binary, sorec = \
        [int(token) for token in f.readline().strip().split(',')]

    user_mapping = {}
    for token in f.readline().strip().split(' '):
        a,b = token.split(':')
        user_mapping[int(a)] = int(b)
    
    item_mapping = {}
    for token in f.readline().strip().split(' '):
        a,b = token.split(':')
        if a.startswith('f'):
            item_mapping[a] = int(b)
        else:
            item_mapping[int(a)] = int(b)

    model = ptf.model_settings(K, MF, trust, iat, intercept, user_mapping, item_mapping, undirected, binary, sorec)
    
    f.close()
    return model

def load(fname, model, readonly=True, priors=False, data=False):
    f = open(fname, 'r')

    print "  in load"    
    params = ptf.parameters(model, readonly, priors, data)

    # itercepts
    if model.intercept:
        i = 0
        for intercept in f.readline().strip().split(' '):
            if i >= model.item_count:
                continue
            params.inter[i] = float(intercept)
            i += 1
        print "INTERCEPT (ave %f)" % (sum(params.inter) / len(params.inter))

    # eta
    if model.trust and model.iat:
        params.eta = float(f.readline().strip())
        print "ETA", params.eta

    # tau
    if model.trust or model.iat:
        count = 0.0
        val = 0.0
        for tau in f.readline().strip().split(' '):
            if tau.strip() == '':
                continue
            user, friend, trust = tau.split(':')
            count += 1
            val += float(trust)
            #print user, friend, trust
            params.tau.rows[int(user)][int(friend)] = float(trust)
        print "TAU (ave # %f, ave val %f)" % (count/model.user_count, val/count)#count / model.user_count, val / count)

    # theta
    if model.MF or model.iat:
        print "THETA"
        params.theta = np.zeros((model.user_count, model.K))
        params.beta = np.zeros((model.item_count, model.K))
        aves = np.zeros(model.K)
        for user in xrange(model.user_count):
            i = 0
            L = f.readline()
            #for val in [float(v) for v in f.readline().strip().split(' ')]:
            for val in [float(v) for v in L.strip().split(' ')[1:]]:
                params.theta[user,i] = val
                aves[i] += val
                i += 1
        print "aves: ", (aves / model.user_count)
        
        # beta
        print "BETA"
        aves = np.zeros(model.K)
        for item in xrange(model.item_count):
            i = 0
            L = f.readline()
            #print L
            #for val in [float(v) for v in f.readline().strip().split(' ')]:
            for val in [float(v) for v in L.strip().split(' ')[1:]]:
                params.beta[item,i] = val
                aves[i] += val
                i += 1
        print "aves: ", (aves / model.user_count)
    
    f.close()

    return params
