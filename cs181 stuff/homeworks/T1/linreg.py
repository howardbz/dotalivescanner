#####################
# CS 181, Spring 2019
# Homework 1, Problem 3
#
##################

import csv
import numpy as np
import matplotlib.pyplot as plt

csv_filename = 'data/year-sunspots-republicans.csv'
years  = []
republican_counts = []
sunspot_counts = []

with open(csv_filename, 'r') as csv_fh:

    # Parse as a CSV file.
    reader = csv.reader(csv_fh)

    # Skip the header line.
    next(reader, None)

    # Loop over the file.
    for row in reader:

        # Store the data.
        years.append(float(row[0]))
        sunspot_counts.append(float(row[1]))
        republican_counts.append(float(row[2]))

# Turn the data into numpy arrays.
years  = np.array(years)
republican_counts = np.array(republican_counts)
sunspot_counts = np.array(sunspot_counts)
last_year = 1985

# Plot the data.
plt.figure(1)
plt.plot(years, republican_counts, 'o')
plt.xlabel("Year")
plt.ylabel("Number of Republicans in Congress")
plt.figure(2)
plt.plot(years, sunspot_counts, 'o')
plt.xlabel("Year")
plt.ylabel("Number of Sunspots")
plt.figure(3)
plt.plot(sunspot_counts[years<last_year], republican_counts[years<last_year], 'o')
plt.xlabel("Number of Sunspots")
plt.ylabel("Number of Republicans in Congress")
plt.show()

# Create the simplest basis, with just the time and an offset.
X = np.vstack((np.ones(years.shape), years)).T

# TODO: basis functions

# def basis_a, basis_b, basis_c, basis_d

X_base = np.ones(years.shape)

def basis_a(years, base):
    a_base = base
    for i in range(1,6):
        a_base = np.vstack((a_base, np.power(years, i)))
    return a_base.T
        
def basis_b(years, base):
    b_base = base
    for i in range(1960, 2011, 5):
        b_base = np.vstack((b_base, np.exp(-(years-i)**2/25)))
    return b_base.T

def basis_c(years, base):
    c_base = base
    for i in range(1,6):
        c_base = np.vstack((c_base, np.cos(years/i)))
    return c_base.T

def basis_d(years, base):
    d_base = base
    for i in range(1,26):
        d_base = np.vstack((d_base, np.cos(years/i)))
    return d_base.T

# Nothing fancy for outputs.
Y = republican_counts

# Find the regression weights using the Moore-Penrose pseudoinverse.
w = np.linalg.solve(np.dot(X.T, X) , np.dot(X.T, Y))

# Compute the regression line on a grid of inputs.
# DO NOT CHANGE grid_years!!!!!
grid_years = np.linspace(1960, 2005, 200)
grid_sunspots = np.linspace(min(sunspot_counts), max(sunspot_counts), 200)

grid_X = np.vstack((np.ones(grid_years.shape), grid_years))
grid_Yhat  = np.dot(grid_X.T, w)

grid_base = np.ones(grid_years.shape)

# helper functions
def find_w(X, Y):
    return np.linalg.solve(np.dot(X.T, X), np.dot(X.T, Y))

def find_grid_X(basis_grid):
    return np.vstack((np.ones(grid_years.shape), basis_grid.T))
# find_grid_X(basis_a(grid_years))

def find_grid_Yhat(grid_X, w):
    return np.vstack((np.dot(grid_X.T, w)))

# TODO: plot and report sum of squared error for each basis
# def square_error
def squared_error(X, Y, w):
    return np.sum((Y - np.dot(X, w))**2/2)

# Plot the data and the regression line.
plt.plot(years, republican_counts, 'o', grid_years, grid_Yhat, '-')
plt.xlabel("Year")
plt.ylabel("Number of Republicans in Congress")
plt.show()

gridx_1a = basis_a(grid_years, grid_base)
gridx_1b = basis_b(grid_years, grid_base)
gridx_1c = basis_c(grid_years, grid_base)
gridx_1d = basis_d(grid_years, grid_base)

gridx_3a = basis_a(grid_sunspots, np.ones(grid_sunspots.shape))
gridx_3b = basis_b(grid_sunspots, np.ones(grid_sunspots.shape))
gridx_3c = basis_c(grid_sunspots, np.ones(grid_sunspots.shape))
gridx_3d = basis_d(grid_sunspots, np.ones(grid_sunspots.shape))

plt.figure(1)
plt.plot(years, republican_counts, 'o', grid_years, 
         find_grid_Yhat(gridx_1a.T, find_w(basis_a(years, X_base), Y)), '-')
plt.xlabel("Year")
plt.ylabel("Number of Republicans in Congress")
plt.show()

print("1a error", squared_error(basis_a(years, X_base), republican_counts, 
                                find_w(basis_a(years, X_base), Y)))

plt.figure(2)
plt.plot(years, republican_counts, 'o', grid_years, 
         find_grid_Yhat(gridx_1b.T, find_w(basis_b(years, X_base), Y)), '-')
plt.xlabel("Year")
plt.ylabel("Number of Republicans in Congress")
plt.show()

print("1b error", squared_error(basis_b(years, X_base), republican_counts, 
                                find_w(basis_b(years, X_base), Y)))

plt.figure(3)
plt.plot(years, republican_counts, 'o', grid_years, 
         find_grid_Yhat(gridx_1c.T, find_w(basis_c(years, X_base), Y)), '-')
plt.xlabel("Year")
plt.ylabel("Number of Republicans in Congress")
plt.show()

print("1c error", squared_error(basis_c(years, X_base), republican_counts, 
                                find_w(basis_c(years, X_base), Y)))

plt.figure(4)
plt.plot(years, republican_counts, 'o', grid_years, 
         find_grid_Yhat(gridx_1d.T, find_w(basis_d(years, X_base), Y)), '-')
plt.xlabel("Year")
plt.ylabel("Number of Republicans in Congress")
plt.show()

print("1d error", squared_error(basis_d(years, X_base), republican_counts, 
                                find_w(basis_d(years, X_base), Y)))

sunspot_counts = sunspot_counts[years<last_year]
republican_counts = republican_counts[years<last_year]

plt.figure(5)
plt.plot(sunspot_counts, republican_counts, 'o', grid_sunspots, 
         find_grid_Yhat(gridx_3a.T, find_w(basis_a(sunspot_counts, 
         np.ones(sunspot_counts.shape)), republican_counts)), '-')
plt.xlabel("Sunspots")
plt.ylabel("Republicans")
plt.show()

x_s = sunspot_counts
y_s = np.ones(sunspot_counts.shape)

print("3a error", squared_error(basis_a(x_s, y_s), republican_counts, 
                                find_w(basis_a(x_s, y_s), republican_counts)))

plt.figure(6)
plt.plot(sunspot_counts, republican_counts, 'o', grid_sunspots, 
         find_grid_Yhat(gridx_3c.T, find_w(basis_c(sunspot_counts, 
         np.ones(sunspot_counts.shape)), republican_counts)), '-')
plt.xlabel("Sunspots")
plt.ylabel("Republicans")
plt.show()

print("3c error", squared_error(basis_c(x_s, y_s), republican_counts, 
                                find_w(basis_c(x_s, y_s), republican_counts)))

plt.figure(7)
plt.plot(sunspot_counts, republican_counts, 'o', grid_sunspots, 
         find_grid_Yhat(gridx_3d.T, find_w(basis_d(sunspot_counts, 
         np.ones(sunspot_counts.shape)), republican_counts)), '-')
plt.xlabel("Sunspots")
plt.ylabel("Republicans")
plt.show()

print("3d error", squared_error(basis_d(x_s, y_s), republican_counts, 
                                find_w(basis_d(x_s, y_s), republican_counts)))


# plt.figure(#)
# plt.plot(x, y, 'o', gridx, gridy, '-')
# plt.xlabel
# plt.ylabel
# plt.show()

# individual plots


