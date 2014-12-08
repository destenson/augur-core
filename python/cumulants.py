#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cumulant tensors and statistics.  Semi-compatible with Serpent.

"""
from __future__ import division

def array(size):
    # Emulates Serpent arrays.  Multidimensional arrays have the following
    # syntax in Serpent:
    #
    #     x = array(W)
    #     i = 0
    #     while i < W:
    #         x[i] = array(H)
    #         i += 1
    #
    # Args:
    #   size (int): number of elements in the array
    #   typecode (char): data type the array will hold (default: float)
    #
    a = [0] * size
    return(a)

def mean(u, size):
    # Calculates the arithmetic mean.
    #
    # Args:
    #   u: numeric array (vector)
    #   size (int): number of elements in u
    #
    m = 0
    i = 0
    while i < size:
        m += u[i]
        i += 1
    m /= size
    return(m)

def dot(u, v, size):
    # Calculates the dot (inner) product of vectors.
    #
    # Args:
    #   u: numeric array (vector)
    #   v: numeric array (vector)
    #   size (int): number of elements in u
    #
    prod = 0
    i = 0
    while i < size:
        prod += u[i] * v[i]
        i += 1
    return(prod)

def outer(u, v, size):
    # Calculates the outer product of vectors.
    #
    # Args:
    #   u: numeric array (vector)
    #   v: numeric array (vector)
    #   size (int): number of elements in u
    #
    prod = array(size)
    i = 0
    while i < size:
        prod[i] = array(size)
        j = 0
        while j < size:
            prod[i][j] += u[i] * v[j]
            j += 1
        i += 1
    return(prod)

def transpose(a, m, n):
    # m: # rows in a
    # n: # colunms in a
    at = array(n)
    i = 0
    while i < n:
        at[i] = array(m)
        i += 1
    i = 0
    while i < m:
        j = 0
        while j < n:
            at[j][i] = a[i][j]
            j += 1
        i += 1
    return(at)

def matrix_multiply(a, b, am, bm, an, bn):
    # am: # rows in a
    # bm: # rows in b
    # an: # columns in a
    # bn: # columns in b
    cm = am
    cn = bn
    c = array(cm)
    if bn > 1:
        i = 0
        while i < cm:
            c[i] = array(cn)
            i += 1
    i = 0
    while i < cm:
        j = 0
        while j < cn:
            k = 0
            while k < an:
                if bn == 1:
                    c[i] += a[i][k] * b[k]
                else:
                    c[i][j] += a[i][k] * b[k][j]
                k += 1
            j += 1
        i += 1
    return(c)

def kron(u, v, size):
    # Calculates the Kronecker product.
    #
    # Args:
    #   u: numeric array (vector)
    #   v: numeric array (vector)
    #   size (int): number of elements in u
    #
    prod = array(size**2)
    i = 0
    while i < size:
        j = 0
        while j < size:
            prod[size*i + j] += u[i] * v[j]
            j += 1
        i += 1
    return(prod)

def cov(data, rows, cols, unbias):
    # Covariance matrix (second cumulant).
    #
    # Args:
    #   data: two-dimensional data matrix (signals = columns, samples = rows)
    #   rows: number of rows (samples per signal) in the data matrix
    #   cols: number of columns (signals) in the data matrix
    #
    tensor = array(cols)
    i = 0
    while i < cols:
        j = 0
        tensor[i] = array(cols)
        while j < cols:
            u = 0
            row = 0
            while row < rows:
                i_mean = 0
                j_mean = 0
                r = 0
                while r < rows:
                    i_mean += data[r][i]
                    j_mean += data[r][j]
                    r += 1
                i_mean /= rows
                j_mean /= rows
                i_center = data[row][i] - i_mean
                j_center = data[row][j] - j_mean
                u += i_center * j_center
                row += 1
            tensor[i][j] = u / (rows - unbias)
            j += 1
        i += 1
    return(tensor)

def coskew(data, rows, cols, unbias):
    # Block-unfolded third cumulant tensor.
    #
    # Args:
    #   data: two-dimensional data matrix (signals = columns, samples = rows)
    #   rows: number of rows (samples per signal) in the data matrix
    #   cols: number of columns (signals) in the data matrix
    #
    tensor = array(cols)
    k = 0
    while k < cols:
        face = array(cols)
        i = 0
        while i < cols:
            j = 0
            face[i] = array(cols)
            while j < cols:
                u = 0
                row = 0
                while row < rows:
                    i_mean = 0
                    j_mean = 0
                    k_mean = 0
                    r = 0
                    while r < rows:
                        i_mean += data[r][i]
                        j_mean += data[r][j]
                        k_mean += data[r][k]
                        r += 1
                    i_mean /= rows
                    j_mean /= rows
                    k_mean /= rows
                    i_center = data[row][i] - i_mean
                    j_center = data[row][j] - j_mean
                    k_center = data[row][k] - k_mean
                    u += i_center * j_center * k_center
                    row += 1
                face[i][j] = u / (rows - unbias)
                j += 1
            tensor[k] = face
            i += 1
        k += 1
    return(tensor)

def cokurt(data, rows, cols, unbias):
    # Block-unfolded fourth cumulant tensor.
    #
    # Args:
    #   data: two-dimensional data matrix (signals = columns, samples = rows)
    #   rows: number of rows (samples per signal) in the data matrix
    #   cols: number of columns (signals) in the data matrix
    #
    tensor = array(cols)
    l = 0
    while l < cols:
        block = array(cols)
        k = 0
        while k < cols:
            face = array(cols)
            i = 0
            while i < cols:
                j = 0
                face[i] = array(cols)
                while j < cols:
                    u = 0
                    row = 0
                    while row < rows:
                        i_mean = 0
                        j_mean = 0
                        k_mean = 0
                        l_mean = 0
                        r = 0
                        while r < rows:
                            i_mean += data[r][i]
                            j_mean += data[r][j]
                            k_mean += data[r][k]
                            l_mean += data[r][l]
                            r += 1
                        i_mean /= rows
                        j_mean /= rows
                        k_mean /= rows
                        l_mean /= rows
                        i_center = data[row][i] - i_mean
                        j_center = data[row][j] - j_mean
                        k_center = data[row][k] - k_mean
                        l_center = data[row][l] - l_mean
                        u += i_center * j_center * k_center * l_center
                        row += 1
                    face[i][j] = u / (rows - unbias)
                    j += 1
                block[k] = face
                i += 1
            tensor[l] = block
            k += 1
        l += 1
    return(tensor)

def coskewness(data, w):
    S = matrix_multiply(matrix_multiply(transpose(w), coskew(data)), kron(w, w))
    return(S)

def cokurtosis(data, w):
    S = matrix_multiply(matrix_multiply(transpose(w), cokurt(data)), kron(kron(w, w), w))
    return(S)