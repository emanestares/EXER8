# Author : Frederick Emmanuel S. Estares
# Description : K Means Clustering
# Date : November 19 2023

# import tkinter for filedialog
# import math for euclidean distance computation
from tkinter import filedialog
import customtkinter as tk
import math
import random

attributeList = []
vectorList = []
vectors = []
isFirstLine = True

def inputNumbers(char):
    return char.isdigit()

def run():
    attr1Index = attributeList.index(attribute1Drop.get())
    attr2Index = attributeList.index(attribute2Drop.get())
    nClusters = noOfClusterInput.get()
    currentCentroids = []
    previousCentroids = []
    isFirstCentroid = True
    clusterIndex = 0
    index = 0
    minDistance = 0
    distance = 0
    centroid = 0
    x = 0
    y = 0

    if attr1Index == attr2Index:
        print("Attributes 1 and 2 cannot be the same")
        return 0

    for i in range(0, int(nClusters)):
        centroid = vectorList[random.randint(0, len(vectorList))][0]
        currentCentroids.append([float(centroid[attr1Index]), float(centroid[attr2Index])])
        previousCentroids.append(0)
    
    while previousCentroids != currentCentroids:
        for vector in vectorList:
            clusterIndex = 0
            minDistance = 0
            distance = 0
            index = 0
            isFirstCentroid = True
            for centroid in currentCentroids:
                distance = (float(vector[0][attr1Index]) - float(centroid[0]))**2
                distance += ((float(vector[0][attr2Index]) - float(centroid[1])))**2
                distance = math.sqrt(distance)

                if isFirstCentroid:
                    minDistance = distance
                    isFirstCentroid = False

                if distance < minDistance:
                    minDistance = distance
                    clusterIndex = index
                index +=1
            vector[1] = clusterIndex

        for i in range(0, int(nClusters)):
            index = 0
            x = 0
            y = 0
            for vector in vectorList:
                if i == vector[1]:
                    x += float(vector[0][attr1Index])
                    y += float(vector[0][attr2Index])
                    index +=1
            x = x/ index
            y = y/ index

            previousCentroids[i] = currentCentroids[i]
            currentCentroids[i] = [x, y]

    print(currentCentroids)


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

root = tk.CTk()
root.title("K-Means Clustering")
# root.iconbitmap("./icon.ico")

#GUI using ctkinter
tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")

#title label
titleLabel = tk.CTkLabel(root, text="K MEANS CLUSTERING", text_color = "white", font = ("Helvetica", 35))
titleLabel.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)

#data elements
dataFrame = tk.CTkFrame(root, height=200, width=250)
dataFrame.grid(row = 1, column = 0, padx = 10, pady = 2)

centroidsFrame = tk.CTkScrollableFrame(root, height=300, width=280)
centroidsFrame.grid(row = 3, column = 0, padx = 10, pady = 2)

#scatter plot
plotFrame = tk.CTkFrame(root, height=500, width=250)
plotFrame.grid(row = 1, column = 1, rowspan = 3, padx = 10, pady = 2)

attr1var = tk.StringVar(value=attributeList[0])
attribute1Label = tk.CTkLabel(dataFrame, text = "Select Attribute 1", text_color= "white", font =("Helvetica", 15))
attribute1Label.grid(row = 0, column = 0)
attribute1Drop = tk.CTkComboBox(dataFrame, values = attributeList, variable=attr1var)
attribute1Drop.grid(row = 0, column = 1)

attr2var = tk.StringVar(value=attributeList[1])
attribute2Label = tk.CTkLabel(dataFrame, text = "Select Attribute 2", text_color= "white", font =("Helvetica", 15))
attribute2Label.grid(row = 1, column = 0, padx = 5, pady = 5)
attribute2Drop = tk.CTkComboBox(dataFrame, values = attributeList, variable=attr2var)
attribute2Drop.grid(row = 1, column = 1, padx = 5, pady = 5)

validation = dataFrame.register(inputNumbers)
noOfClusterLabel = tk.CTkLabel(dataFrame, text = "Enter N Clusters", text_color= "white", font =("Helvetica", 15))
noOfClusterLabel.grid(row = 2, column = 0, padx = 5, pady = 5)
noOfClusterInput = tk.CTkEntry(dataFrame, validate = "key", validatecommand = (validation, '%S'))
noOfClusterInput.grid(row = 2, column = 1, padx = 5, pady = 5)

runButton = tk.CTkButton(dataFrame, text = "RUN", command=run)
runButton.grid(row = 3, column = 0, padx = 5, pady = 5)
resetButton = tk.CTkButton(dataFrame, text = "RESET")
resetButton.grid(row = 3, column = 1, padx = 5, pady = 5)

centroidsLabel = tk.CTkLabel(root, text = "Centroids And Clusters", text_color= "white", font =("Helvetica", 15))
centroidsLabel.grid(row = 2, column = 0, padx = 2, pady = 5)

scatterPlotLabel = tk.CTkLabel(plotFrame, text = "K-Means Scatter Plot", text_color= "white", font =("Helvetica", 15))
scatterPlotLabel.grid(row = 0, column = 0, padx = 5, pady = 5)

#mainloop
root.mainloop()