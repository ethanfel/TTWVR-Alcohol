# SPDX-License-Identifier: GPL-3.0-only
WINCXX ?= i686-w64-mingw32-g++
OPENXR_HEADERS ?= /usr/include/openxr
FLAGS := -std=c++17 -Wall -Wextra -Werror -O2
RUNTIME := build/TTWVRPhysicalCanteen.dll
HEADERS := $(wildcard src/*.h)
TESTS := build/test-Projection build/test-Balance build/test-DrinkTiming

.PHONY: package test
package: $(RUNTIME)
	python3 -B alcohol/package.py

build:
	mkdir -p $@

$(RUNTIME): src/Plugin.cpp src/Tracking.cpp $(HEADERS) | build
	$(WINCXX) $(FLAGS) -I$(OPENXR_HEADERS) -static -shared -s src/Plugin.cpp src/Tracking.cpp -o $@

build/test-%: tests/%.cpp $(HEADERS) | build
	$(CXX) $(FLAGS) -I$(OPENXR_HEADERS) $< -o $@

test: $(TESTS)
	./build/test-Projection
	./build/test-Balance
	./build/test-DrinkTiming
	python3 -B tests/test_alcohol.py
