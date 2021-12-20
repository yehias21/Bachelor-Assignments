cmake_minimum_required(VERSION 3.20)
project(semaphores)

set(CMAKE_CXX_STANDARD 20)

add_executable(semaphores main.cpp)
target_link_libraries(semaphores pthread)
