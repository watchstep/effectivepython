#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2019 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Reproduce book environment
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# Write all output to a temporary directory
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1
numbers = [93, 86, 11, 68, 70]
numbers.sort()
print(numbers)


# Example 2
class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'

tools = [
    Tool('level', 3.5),
    Tool('hammer', 1.25),
    Tool('screwdriver', 0.5),
    Tool('chisel', 0.25),
]


# Example 3
try:
    tools.sort()
except:
    logging.exception('Expected')
else:
    assert False


# Example 4
print('Unsorted:', repr(tools))
tools.sort(key=lambda x: x.name)
print('\nSorted:  ', tools)


# Example 5
tools.sort(key=lambda x: x.weight)
print('By weight:', tools)


# Example 6
places = ['home', 'work', 'New York', 'Paris']
places.sort()
print('Case sensitive:  ', places)
places.sort(key=lambda x: x.lower())
print('Case insensitive:', places)


# Example 7
power_tools = [
    Tool('drill', 4),
    Tool('circular saw', 5),
    Tool('jackhammer', 40),
    Tool('sander', 4),
]


# Example 8
saw = (5, 'circular saw')
jackhammer = (40, 'jackhammer')
assert not (jackhammer < saw)  # Matches expectations
# tuple (sort에 필요한 __lt__ 정의 들어가 있음)
# 각 index에 해당하는 원소를 한 번에 하나씩 비교 

# Example 9
drill = (4, 'drill')
sander = (4, 'sander')
assert drill[0] == sander[0]  # Same weight
assert drill[1] < sander[1]   # Alphabetically less
assert drill < sander         # Thus, drill comes first
# 첫 번째 위치의 값이 서로 같으면
# tuple의 비교 메서드는 두 번째 서로 비교하는 방식
# 두 번째도 같으면 세 번째 비교 반복


# Example 10
power_tools.sort(key=lambda x: (x.weight, x.name)) # 먼저 weight로 정렬하고, 그 후 name으로 정렬
print(power_tools)


# Example 11
power_tools.sort(key=lambda x: (x.weight, x.name),
                 reverse=True)  # Makes all criteria descending
print(power_tools)


# Example 12
power_tools.sort(key=lambda x: (-x.weight, x.name)) # 숫자인 경우 - 연산자 사용해서 정렬 순서 혼합 가능
print(power_tools)


# Example 13
try:
    power_tools.sort(key=lambda x: (x.weight, -x.name),
                     reverse=True)
except:
    logging.exception('Expected')
else:
    assert False


# Example 14
power_tools.sort(key=lambda x: x.name)   # Name ascending

power_tools.sort(key=lambda x: x.weight, # Weight descending
                 reverse=True)

print(power_tools)


# Example 15
power_tools.sort(key=lambda x: x.name)
print(power_tools)


# Example 16
power_tools.sort(key=lambda x: x.weight,
                 reverse=True)
print(power_tools)

# key 함수에 tuple 반환하면 여러 정렬 기준을 하나로 엮을 수 있음
# 단항 부호 반전 연산자 (-)를 사용하면 부호를 바꿀 수 있는 타입이 정렬 기준인 경우
# 정렬 순서를 반대로 바꿀 수 있음

# 부호를 바꿀 수 없는 타입의 경우 여러 정렬 기준을 조합하려면
# 각 정렬 기준마다 reverse 값으로 정렬 순서를 지정하면서 sort 메서드 여러 번 사용해야 함
# 정렬 기준의 우선순위가 점점 높아지는 순서로 sort 호출해야함
# e.g weight 내림차순 정렬 후 name에 의해 오름차순 정렬하고 싶으면
# name 오름차순 정렬 후 weight 내림차순 정렬해야함 