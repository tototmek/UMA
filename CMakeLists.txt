cmake_minimum_required(VERSION 3.1.0)
project(Environment)
set (CMAKE_CXX_STANDARD 17)

execute_process(
  COMMAND python3 -m pybind11 --cmakedir
  OUTPUT_VARIABLE pybind11_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
find_package(pybind11 CONFIG REQUIRED)
include_directories(pybind11)

add_compile_options(-Wall -Wextra -pedantic -Werror)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ../)

include_directories(include)

pybind11_add_module(engine 
    src/engine_binding.cpp
    src/engine.cpp
    src/track.cpp
    src/critic.cpp
    src/environment.cpp)