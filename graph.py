import matplotlib.pyplot,matplotlib.animation

pyp = matplotlib.pyplot
anime = matplotlib.animation
shape = pyp.figure()
shaplot = shape.add_subplot(1, 1, 1)

def animation(x):
    data = open("./cpu.txt").readlines()

    l = []

    for value in data:
        if len(value) > 1:
            l.append(float(value))
    
    shaplot.clear()
    shaplot.plot(l)
    pyp.title(label="CPU Util.")
graph = anime.FuncAnimation(shape, animation, interval=1000)

pyp.show()