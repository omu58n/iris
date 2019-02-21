from django.shortcuts import render, get_object_or_404
from .models import Iris
from .forms import IrisForm
from django.shortcuts import redirect
from sklearn import datasets
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def input(request):
    if request.method == "POST":
        form = IrisForm(request.POST)
        if form.is_valid():
            iris = form.save()
            return redirect('output', pk=iris.pk)
    else:
        form = IrisForm()
    return render(request, 'irisclass/input.html', {'form': form})

def output(request, pk):
    iris = get_object_or_404(Iris, pk=pk)
    irises = datasets.load_iris()
    clf = svm.LinearSVC()
    clf.fit(irises.data, irises.target)
    predict = clf.predict([[iris.sepalLength, iris.sepalWidth, iris.petalLength, iris.petalWidth]])
    if predict == 0:
        result = 'Iris-setosa'
    elif predict == 1:
        result = 'Iris-versicolor'
    else:
        result = 'Iris-virginica'
    return render(request, 'irisclass/output.html', {'iris': iris, 'result': result})

def figure(request):
    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    sns.set_palette('Set1')
    df = sns.load_dataset('iris')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for sp in set(df.species):
        df_species = df[df['species'] == sp]
        ax.scatter(data=df_species, x='sepal_length', y='sepal_width', label='species')
    ax.legend(loc='lower right')

    ax.set_xlabel('length [cm]')
    ax.set_ylabel('width [cm]')
    plt.savefig('out.png')

    canvas = FigureCanvas(fig)
    buf = cStringIO.StringIO()
    canvas.print_png(buf)
    data = buf.getvalue()

    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    
    return response
