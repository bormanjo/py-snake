{
 "nbformat": 4,
 "nbformat_minor": 2,
 "metadata": {
  "language_info": {
   "name": "python",
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "version": "3.7.6-final"
  },
  "orig_nbformat": 2,
  "file_extension": ".py",
  "mimetype": "text/x-python",
  "name": "python",
  "npconvert_exporter": "python",
  "pygments_lexer": "ipython3",
  "version": 3,
  "kernelspec": {
   "name": "python37664bitpy37condaec647e71318c47208e190ff375d64cd6",
   "display_name": "Python 3.7.6 64-bit ('py37': conda)"
  }
 },
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "clist = snake.FixedList('hello world', capacity=5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": "['h', 'e', 'l', 'l', 'o']"
     },
     "metadata": {},
     "execution_count": 3
    }
   ],
   "source": [
    "clist"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": "'o'"
     },
     "metadata": {},
     "execution_count": 4
    }
   ],
   "source": [
    "clist.add(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": "[10, 'h', 'e', 'l', 'l']"
     },
     "metadata": {},
     "execution_count": 5
    }
   ],
   "source": [
    "clist"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "output_type": "stream",
     "name": "stdout",
     "text": "10\nh\ne\nl\nl\n"
    }
   ],
   "source": [
    "for i in clist:\n",
    "    print(i)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": "'e'"
     },
     "metadata": {},
     "execution_count": 9
    }
   ],
   "source": [
    "clist.add('10')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": "<snake.FixedList at 0x126d2fd6fc8>"
     },
     "metadata": {},
     "execution_count": 10
    }
   ],
   "source": [
    "clist"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": "'b'"
     },
     "metadata": {},
     "execution_count": 10
    }
   ],
   "source": [
    "['a', 'b'].pop()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ]
}