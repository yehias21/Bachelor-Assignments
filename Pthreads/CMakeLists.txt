cmake_minimum_required(VERSION 3.20)
project(Pthreads)

set(CMAKE_CXX_STANDARD 14)
#set(CMAKE_CXX_FLAGS "-pthread")  matMultThread.c
add_executable(Pthreads  mergeSortthread.c)
target_link_libraries(Pthreads pthread)