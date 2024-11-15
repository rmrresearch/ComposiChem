cmake_minimum_required(VERSION 3.14)

## Set Project and Version
project(composichem VERSION "0.0.1" LANGUAGES NONE)

## Get CMaize and Common NWChemEx CMake infrastructure
include(cmake/get_nwx_cmake.cmake)
include(nwx_versions)
include(get_cmaize)

## Paths ##
set(${PROJECT_NAME}_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src/python")
set(${PROJECT_NAME}_TESTS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/tests/python")

## Options ##
cmaize_option_list(
    BUILD_TESTING ON "Should the tests be built?"
    INTEGRATION_TESTING ON "Should we build the integration tests?"
)

## Find or build dependencies ##
cmaize_find_or_build_dependency(
    simde
    URL github.com/NWChemEx/SimDE
    VERSION master
    BUILD_TARGET simde
    FIND_TARGET nwx::simde
    CMAKE_ARGS BUILD_TESTING=OFF
)

## Add libraries ##
add_library(${PROJECT_NAME} INTERFACE)
target_link_libraries(${PROJECT_NAME} INTERFACE simde)

## Build tests ##
if("${BUILD_TESTING}")
    include(CTest)
    include(nwx_pybind11)

    nwx_pybind11_tests(
        ${PROJECT_NAME}_unit_tests
        "${${PROJECT_NAME}_TESTS_DIR}/unit_tests/test_composichem.py"
        SUBMODULES simde chemist pluginplay parallelzone
    )

    if("${INTEGRATION_TESTING}")

        cmaize_find_or_build_dependency(
            nwchemex
            URL github.com/NWChemEx/NWChemEx
            BUILD_TARGET nwchemex
            FIND_TARGET nwx::nwchemex
            CMAKE_ARGS BUILD_TESTING=OFF
        )

        nwx_pybind11_tests(
            ${PROJECT_NAME}_integration_test
            "${${PROJECT_NAME}_TESTS_DIR}/integration_tests/test_composichem.py"
            SUBMODULES nwchemex chemcache friendzone simde chemist pluginplay 
                       parallelzone
        )
    endif()

endif()

install(
    DIRECTORY "${${PROJECT_NAME}_SRC_DIR}/composichem"
    DESTINATION "${NWX_MODULE_DIRECTORY}"
)