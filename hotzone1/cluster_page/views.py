from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from sklearn.cluster import DBSCAN
from hotzoneData.models import *
from datetime import date, timedelta
import numpy as np
import math


# Create your views here.
@login_required
def clusterOptionView(request, disease):
    context = {}
    context['disease'] = Disease.objects.get(pk=disease)
    return render(request, 'cluster_option.html', context)

@login_required
def clusterView(request, disease):
    if 'distance' not in request.GET or 'distance' not in request.GET or 'distance' not in request.GET:
        return HttpResponseRedirect('/cluster/disease/' + str(disease))
    D = request.GET['distance']
    T = request.GET['time']
    C = request.GET['size']

    rawData = []
    disease = Disease.objects.get(pk=disease)
    cases = Case.objects.filter(disease=disease)
    for case in cases:
        placesVisited = CasePlace.objects.filter(case=case.pk)
        for placeVisited in placesVisited:
            place = placeVisited.place
            date_from = placeVisited.date_from
            date_to = placeVisited.date_to
            day_diff = date_to - date_from
            day_start = date_from - date(2020, 1, 1)
            if day_diff.days == 0:
                rawData.append([place.x_coor, place.y_coor, day_start.days, case.case_number])
                continue
            for i in range(day_diff.days):
                rawData.append([place.x_coor, place.y_coor, day_start.days+i, case.case_number])
    clusters = cluster(np.array(rawData), D, T, C)
    context = {}
    context['clusters'] = clusters
    context['disease'] = disease
    return render(request, 'cluster_view.html', context)


def cluster(vector_4d, distance, time, minimum_cluster):
    params = {"space_eps": int(distance), "time_eps": int(time)}
    db = DBSCAN(eps=1, min_samples=int(minimum_cluster)-1, metric=custom_metric, metric_params=params).fit_predict(vector_4d)

    unique_labels = set(db)
    total_clusters = len(unique_labels) if -1 not in unique_labels else len(unique_labels) -1

    total_noise = list(db).count(-1)

    clusters = []

    for k in unique_labels:
        if k != -1:
            labels_k = db == k
            cluster_k = vector_4d[labels_k]

            currCluster = []
            for pt in cluster_k:
                currCluster.append({
                    "x_coor": pt[0],
                    "y_coor": pt[1],
                    "date": date(2020,1,1) + timedelta(days=pt[2].item()),
                    "caseNo": pt[3]
                })
            if len(currCluster) > 0:
                clusters.append(currCluster)

    return clusters

def custom_metric(q, p, space_eps, time_eps):
    dist = 0
    for i in range(2):
        dist += (q[i] - p[i])**2
    spatial_dist = math.sqrt(dist)

    time_dist = math.sqrt((q[2]-p[2])**2)

    if time_dist/time_eps <= 1 and spatial_dist/space_eps <=1 and p[3] != q[3]:
        return 1
    else:
        return 2
