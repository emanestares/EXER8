# Author : Frederick Emmanuel S. Estares
# Description : K Means Clustering
# Date : November 19 2023

# import matplotlib modules for scatter plot
# import math for euclidean distance computation
# import random for initializing the centroids
# import customtkinter for GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import customtkinter as tk
import matplotlib.pyplot as plt
import math
import random

# initial lists for reading the data from wine.csv
attributeList = []
vectorList = []
vectors = []
isFirstLine = True

# initializing the customtkinter
root = tk.CTk()
root.title("K-Means Clustering")
root.iconbitmap("./wine.ico")

# initializing matplotlib
fig, ax = plt.subplots()

# exits the app
def quitApp():
    tk.CTk.quit(root)

# resets the app and the plot
def reset():
    attribute1Drop.set("Alcohol")
    attribute2Drop.set("Malic_Acid")
    noOfClusterInput.delete(0, 'end')

    for widget in centroidsFrame.winfo_children():
        widget.destroy()
    
    ax.clear()
    canvas.draw()

# restricts the input for number of clusters to integer
def inputNumbers(char):
    return char.isdigit()

# executes the algorithm and plots the clustering
def run():
    # initializes all of the variables and lists needed
    centroidLabel = 0
    vectorLabel = 0
    vectorString = ""
    ax.clear()

    attr1Index = attributeList.index(attribute1Drop.get())
    attr2Index = attributeList.index(attribute2Drop.get())
    nClusters = noOfClusterInput.get()
    currentCentroids = []
    previousCentroids = []
    tempXList = []
    tempYList = []
    isFirstCentroid = True
    clusterIndex = 0
    index = 0
    minDistance = 0
    distance = 0
    centroid = 0
    x = 0
    y = 0

    # if attributes 1 and 2 are equal, prompts the user and exits the function
    if attr1Index == attr2Index:
        print("Attributes 1 and 2 cannot be the same")
        return 0

    # labels the x and y axis of the plot
    plt.xlabel(attribute1Drop.get())
    plt.ylabel(attribute2Drop.get())

    # initializes the random n centroids
    for i in range(0, int(nClusters)):
        centroid = vectorList[random.randint(0, len(vectorList))][0]
        currentCentroids.append([float(centroid[attr1Index]), float(centroid[attr2Index])])
        previousCentroids.append(0)
    
    # main loop: while the current centroid is not the same with previous
    while previousCentroids != currentCentroids:
        # for every feature vectors
        for vector in vectorList:
            clusterIndex = 0
            minDistance = 0
            distance = 0
            index = 0
            isFirstCentroid = True

            # gets the distance from each centroids
            for centroid in currentCentroids:
                distance = (float(vector[0][attr1Index]) - float(centroid[0]))**2
                distance += ((float(vector[0][attr2Index]) - float(centroid[1])))**2
                distance = math.sqrt(distance)

                # if this is the first centroid, sets minDistance to distance
                if isFirstCentroid:
                    minDistance = distance
                    isFirstCentroid = False

                # if distance is less than the minDistance
                # sets minDistance to distance
                # sets the clusterIndex to current index
                if distance < minDistance:
                    minDistance = distance
                    clusterIndex = index
                index +=1
            # labels the current vector with the clusterIndex
            vector[1] = clusterIndex

        # updating the centroids
        for i in range(0, int(nClusters)):
            index = 0
            x = 0
            y = 0

            # gets the average x and y of vectors that inside the cluster
            # sets the previous cluster to the current cluster
            # sets the currentcluster to the averages
            for vector in vectorList:
                if i == vector[1]:
                    x += float(vector[0][attr1Index])
                    y += float(vector[0][attr2Index])
                    index +=1
            x = x/ index
            y = y/ index

            previousCentroids[i] = currentCentroids[i]
            currentCentroids[i] = [x, y]

    # clears the centroid Frame
    for widget in centroidsFrame.winfo_children():
        widget.destroy()

    # opening output.csv
    outputFile = open("output.csv", "w")

    # drawing the plot
    # plotting the centroids
    # for every cluster, gets the x and y values of feature vectors
    # plotting the vectors

    # writing for output.txt
    for i in range(0, int(nClusters)):
        centroidLabel = tk.CTkLabel(centroidsFrame, text= "Centroid " + str(i), text_color="Cyan")
        centroidLabel.pack()
        tempXList = []
        tempYList = []

        outputFile.write("Centroid " + str(i) + " (" + str(currentCentroids[i][0]) + ", " + str(currentCentroids[i][1]) + ")\n")

        for vector in vectorList:
            if i == vector[1]:
                outputFile.write("[" + vector[0][attr1Index] + ", " + vector[0][attr2Index] + "]\n")

                tempXList.append(float(vector[0][attr1Index]))
                tempYList.append(float(vector[0][attr2Index]))
                vectorString = "[" + vector[0][attr1Index] + "," + vector[0][attr2Index] + "]"
                vectorLabel = tk.CTkLabel(centroidsFrame, text = vectorString)
                vectorLabel.pack()
        ax.plot(float(currentCentroids[i][0]), float(currentCentroids[i][1]), marker="X", markersize = 10, markeredgecolor="black")
        ax.scatter(tempXList, tempYList)
        canvas.draw()

    # closing the output.csv
    outputFile.close()
# reads the contents of wine.csv
# gets the attribute list
# gets the feature vectors
inputFile = open("wine.csv", "r")
for line in inputFile:
    vectors = []
    if isFirstLine:
        attributeList = line[:-1].split(",")
        isFirstLine = False
    else:
        vectors.append(line[:-1].split(","))
        vectors.append(0)
        vectorList.append(vectors)
inputFile.close()

#GUI using ctkinter
tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")

#title label
titleLabel = tk.CTkLabel(root, text="K MEANS CLUSTERING", text_color = "white", font = ("Helvetica", 35))
titleLabel.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)

#data elements
dataFrame = tk.CTkFrame(root, height=200, width=250)
dataFrame.grid(row = 1, column = 0, padx = 10, pady = 2)

# centroids and vectors
centroidsFrame = tk.CTkScrollableFrame(root, height=300, width=280)
centroidsFrame.grid(row = 3, column = 0, padx = 10, pady = 2)

#scatter plot
plotFrame = tk.CTkFrame(root, height=500, width=250)
plotFrame.grid(row = 1, column = 1, rowspan = 3, padx = 10, pady = 2)

# attribute 1 dropdown
attr1var = tk.StringVar(value=attributeList[0])
attribute1Label = tk.CTkLabel(dataFrame, text = "Select Attribute 1", text_color= "white", font =("Helvetica", 15))
attribute1Label.grid(row = 0, column = 0)
attribute1Drop = tk.CTkComboBox(dataFrame, values = attributeList, variable=attr1var)
attribute1Drop.grid(row = 0, column = 1)

# attribute 2 dropdown
attr2var = tk.StringVar(value=attributeList[1])
attribute2Label = tk.CTkLabel(dataFrame, text = "Select Attribute 2", text_color= "white", font =("Helvetica", 15))
attribute2Label.grid(row = 1, column = 0, padx = 5, pady = 5)
attribute2Drop = tk.CTkComboBox(dataFrame, values = attributeList, variable=attr2var)
attribute2Drop.grid(row = 1, column = 1, padx = 5, pady = 5)

# number of clusters input and validation
validation = dataFrame.register(inputNumbers)
noOfClusterLabel = tk.CTkLabel(dataFrame, text = "Enter N Clusters", text_color= "white", font =("Helvetica", 15))
noOfClusterLabel.grid(row = 2, column = 0, padx = 5, pady = 5)
noOfClusterInput = tk.CTkEntry(dataFrame, validate = "key", validatecommand = (validation, '%S'))
noOfClusterInput.grid(row = 2, column = 1, padx = 5, pady = 5)

# run button: executes run function
runButton = tk.CTkButton(dataFrame, text = "RUN", command=run)
runButton.grid(row = 3, column = 0, padx = 5, pady = 5)

# reset button: executes the reset function
resetButton = tk.CTkButton(dataFrame, text = "RESET", command=reset)
resetButton.grid(row = 3, column = 1, padx = 5, pady = 5)

# labeling
centroidsLabel = tk.CTkLabel(root, text = "Centroids And Clusters", text_color= "white", font =("Helvetica", 15))
centroidsLabel.grid(row = 2, column = 0, padx = 2, pady = 5)

scatterPlotLabel = tk.CTkLabel(plotFrame, text = "K-Means Scatter Plot", text_color= "white", font =("Helvetica", 15))
scatterPlotLabel.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)

# creating the canvas for plotting
canvas = FigureCanvasTkAgg(fig, master = plotFrame)
canvas.get_tk_widget().grid(row = 1, column= 0, columnspan=2)

# creating and placing the toolbar
toolbar = NavigationToolbar2Tk(canvas, plotFrame, pack_toolbar=False)
toolbar.update()
toolbar.grid(row = 2, column = 0, sticky = "w")

# quit button
quitButton = tk.CTkButton(plotFrame, text = "EXIT", command = quitApp)
quitButton.grid(row = 2, column = 1, sticky = "e")

#mainloop
root.mainloop()