#include <pybind11/pybind11.h>
#include <pybind11/iostream.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/numpy.h>

#include <cmath>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <list>
#include <string>
#include <vector>

#include "../include/qureg.hpp"
#include "../include/mpi_env.hpp"
#include "../include/rng_utils.hpp"

// Extra feature. It can be included optionally.
#if 1
#include "../include/qaoa_features.hpp"
#endif

#ifdef INTELQS_HAS_MPI
#include <mpi.h>
#endif

//////////////////////////////////////////////////////////////////////////////

namespace py = pybind11;
using Environment = iqs::mpi::Environment;

namespace iqs {

//////////////////////////////////////////////////////////////////////////////

void EnvInit()
{ Environment::Init(); }

void EnvFinalize()
{ Environment::Finalize(); }

void EnvFinalizeDummyRanks()
{
  if (Environment::GetSharedInstance()->IsUsefulRank()==false)
  {
      Environment::Finalize();
      return;
  }
}

//////////////////////////////////////////////////////////////////////////////
// PYBIND CODE for the Intel Quantum Simulator library
//////////////////////////////////////////////////////////////////////////////

PYBIND11_MODULE(intelqs_py, m)
{
    m.doc() = "pybind11 wrap for the Intel Quantum Simulator";


//////////////////////////////////////////////////////////////////////////////
// Init & Finalize for HPC
//////////////////////////////////////////////////////////////////////////////
    m.def("EnvInit", &EnvInit, "Initialize the MPI environment of Intel-QS for HPC resource allocation");
    m.def("EnvFinalize", &EnvFinalize, "Finalize the MPI environemtn fo Intel-QS");
    m.def("EnvFinalizeDummyRanks", &EnvFinalizeDummyRanks, "Finalize the dummy ranks of the MPI environment");

//////////////////////////////////////////////////////////////////////////////
// Utilities
//////////////////////////////////////////////////////////////////////////////

    // Random Number Generator
    py::class_<iqs::RandomNumberGenerator<double>>(m, "RandomNumberGenerator")
        .def(py::init<>())
        .def("GetSeed", &iqs::RandomNumberGenerator<double>::GetSeed)
        .def("SetSeedStreamPtrs", &iqs::RandomNumberGenerator<double>::SetSeedStreamPtrs)
        .def("SkipeAhead", &iqs::RandomNumberGenerator<double>::SkipAhead)
        .def("UniformRandomNumbers", &iqs::RandomNumberGenerator<double>::UniformRandomNumbers)
        .def("GaussianRandomNumbers", &iqs::RandomNumberGenerator<double>::GaussianRandomNumbers)
        .def("RandomIntegersInRange", &iqs::RandomNumberGenerator<double>::RandomIntegersInRange)
        .def("GetUniformRandomNumbers",
             [](iqs::RandomNumberGenerator<double> &rng, std::size_t size,
                double a, double b, std::string shared) {
                std::vector<double> random_values(size);
                rng.UniformRandomNumbers(random_values.data(), size, a, b, shared);
                return random_values;
             }, "Return an array of 'size' random number from the uniform distribution [a,b[.")
#ifdef WITH_MPI_AND_MKL
        .def("SetRndStreamPtrs", &iqs::RandomNumberGenerator<double>::SetRndStreamPtrs)
#endif
        .def("__repr__", []() { return "<RandomNumberGenerator specialized for MKL.>"; } );


    // Chi Matrix 4x4
    py::class_<iqs::ChiMatrix<ComplexDP, 4, 32>>(m, "CM4x4", py::buffer_protocol())
        .def(py::init<>())
        .def(py::init<>())
        // Access element:
        .def("__getitem__", [](const iqs::ChiMatrix<ComplexDP,4,32> &a, std::pair<py::ssize_t, py::ssize_t> i, int column) {
             if (i.first > 4) throw py::index_error();
             if (i.second > 4) throw py::index_error();
std::cout << "ciao\n";
             return a(i.first, i.second);
             }, py::is_operator())
        // Set element:
        .def("__setitem__", [](iqs::ChiMatrix<ComplexDP,4,32> &a, std::pair<py::ssize_t, py::ssize_t> i, ComplexDP value) {
             if (i.first > 4) throw py::index_error();
             if (i.second > 4) throw py::index_error();
             a(i.first, i.second) = value;
             }, py::is_operator())
#if 0
        .def_buffer([](iqs::ChiMatrix<ComplexDP,4,32> &m) -> py::buffer_info {
            return py::buffer_info(
                m.GetPtrToData(),                      /* Pointer to buffer */
                sizeof(ComplexDP),                     /* Size of one scalar */
                py::format_descriptor<ComplexDP>::format(), /* Python struct-style format descriptor */
                std::size_t(2),                                      /* Number of dimensions */
                { 4, 4 },                 /* Buffer dimensions */
                { 4*sizeof(ComplexDP), 4 });             /* Strides (in bytes) for each index */
        })
#endif
#if 0
        .def("ApplyChannel",
             [](QubitRegister<ComplexDP> &a, unsigned qubit,
                py::array_t<ComplexDP, py::array::c_style | py::array::forcecast> matrix ) {
               py::buffer_info buf = matrix.request();
               if (buf.ndim != 2)
                   throw std::runtime_error("Number of dimensions must be two.");
               if (buf.shape[0] != 4 || buf.shape[1] != 4)
                   throw std::runtime_error("The shape of the chi-matrix is not 4x4.");
               // Create and initialize the custom chi-matrix used by Intel QS.
               ComplexDP *ptr = (ComplexDP *) buf.ptr;
               CM4x4<ComplexDP> m;
               m(0,0)=ptr[0];  m(0,1)=ptr[1];  m(0,2)=ptr[2];  m(0,3)=ptr[3];
               m(1,0)=ptr[4];  m(1,1)=ptr[5];  m(1,2)=ptr[6];  m(1,3)=ptr[7];
               m(2,0)=ptr[8];  m(2,1)=ptr[9];  m(2,2)=ptr[10]; m(2,3)=ptr[11];
               m(3,0)=ptr[12]; m(3,1)=ptr[13]; m(3,2)=ptr[14]; m(3,3)=ptr[15];
               a.ApplyChannel(qubit, m);
             }, "Apply 1-qubit channel provided via its chi-matrix.")
#endif
        .def("SolveEigenSystem", &iqs::ChiMatrix<ComplexDP,4,32>::SolveEigenSystem)
        .def("Print", &iqs::ChiMatrix<ComplexDP,4,32>::Print)
        .def("__repr__", []() { return "<ChiMatrix for 1-qubit channel>"; } );

    // Chi Matrix 16x16
    py::class_<iqs::ChiMatrix<ComplexDP,16,32>>(m, "CM16x16")
        .def(py::init<>())
        .def(py::init<>())
        // Access element:
        .def("__getitem__", [](const iqs::ChiMatrix<ComplexDP,16,32> &a, std::pair<py::ssize_t, py::ssize_t> i, int column) {
             if (i.first > 16) throw py::index_error();
             if (i.second > 16) throw py::index_error();
             return a(i.first, i.second);
             }, py::is_operator())
        // Set element:
        .def("__setitem__", [](iqs::ChiMatrix<ComplexDP,16,32> &a, std::pair<py::ssize_t, py::ssize_t> i, ComplexDP value) {
             if (i.first > 16) throw py::index_error();
             if (i.second > 16) throw py::index_error();
             a(i.first, i.second) = value;
             }, py::is_operator())
        .def("SolveEigenSystem", &iqs::ChiMatrix<ComplexDP,16,32>::SolveEigenSystem)
        .def("Print", &iqs::ChiMatrix<ComplexDP,16,32>::Print)
        .def("__repr__", []() { return "<ChiMatrix for 2-qubit channel>"; } );

//////////////////////////////////////////////////////////////////////////////
// Intel-QS
//////////////////////////////////////////////////////////////////////////////

    // Intel Quantum Simulator
    // Notice that to use std::cout in the C++ code, one needs to redirect the output streams.
    // https://pybind11.readthedocs.io/en/stable/advanced/pycpp/utilities.html
//    py::class_<QubitRegister<ComplexDP>, shared_ptr< QubitRegister<ComplexDP> >>(m, "QubitRegister")
    py::class_< QubitRegister<ComplexDP> >(m, "QubitRegister", py::buffer_protocol(), py::dynamic_attr())
        .def(py::init<> ())
        .def(py::init<const QubitRegister<ComplexDP> &>())	// copy constructor
        .def(py::init<std::size_t , std::string , std::size_t, std::size_t> ())
        // Information on the internal representation:
        .def("NumQubits", &QubitRegister<ComplexDP>::NumQubits)
        .def("GlobalSize", &QubitRegister<ComplexDP>::GlobalSize)
        .def("LocalSize" , &QubitRegister<ComplexDP>::LocalSize )
        // Access element:
        .def("__getitem__", [](const QubitRegister<ComplexDP> &a, std::size_t index) {
             if (index >= a.LocalSize()) throw py::index_error();
             return a[index];
             }, py::is_operator())
        // Set element:
        .def("__setitem__", [](QubitRegister<ComplexDP> &a, std::size_t index, ComplexDP value) {
             if (index >= a.LocalSize()) throw py::index_error();
             a[index] = value;
             }, py::is_operator())
        // Numpy buffer protocol
        // See https://pybind11.readthedocs.io/en/stable/advanced/pycpp/numpy.html
        .def_buffer([](QubitRegister<ComplexDP> &reg) -> py::buffer_info {
            return py::buffer_info(
                reg.RawState(),                            /* Pointer to buffer */
                sizeof(ComplexDP),                          /* Size of one scalar */
                py::format_descriptor<ComplexDP>::format(), /* Python struct-style format descriptor */
                1,                                      /* Number of dimensions */
                { reg.LocalSize() },                 /* Buffer dimensions */
                { sizeof(ComplexDP) });             /* Strides (in bytes) for each index */
        })
        // One-qubit gates:
        .def("ApplyRotationX", &QubitRegister<ComplexDP>::ApplyRotationX)
        .def("ApplyRotationY", &QubitRegister<ComplexDP>::ApplyRotationY)
        .def("ApplyRotationZ", &QubitRegister<ComplexDP>::ApplyRotationZ)
        .def("ApplyPauliX", &QubitRegister<ComplexDP>::ApplyPauliX)
        .def("ApplyPauliY", &QubitRegister<ComplexDP>::ApplyPauliY)
        .def("ApplyPauliZ", &QubitRegister<ComplexDP>::ApplyPauliZ)
        .def("ApplyPauliSqrtX", &QubitRegister<ComplexDP>::ApplyPauliSqrtX)
        .def("ApplyPauliSqrtY", &QubitRegister<ComplexDP>::ApplyPauliSqrtY)
        .def("ApplyPauliSqrtZ", &QubitRegister<ComplexDP>::ApplyPauliSqrtZ)
        .def("ApplyT", &QubitRegister<ComplexDP>::ApplyT)
        .def("ApplyHadamard", &QubitRegister<ComplexDP>::ApplyHadamard)
        // Two-qubit gates:
        .def("ApplySwap", &QubitRegister<ComplexDP>::ApplySwap)
        .def("ApplyCRotationX", &QubitRegister<ComplexDP>::ApplyCRotationX)
        .def("ApplyCRotationY", &QubitRegister<ComplexDP>::ApplyCRotationY)
        .def("ApplyCRotationZ", &QubitRegister<ComplexDP>::ApplyCRotationZ)
        .def("ApplyCPauliX", &QubitRegister<ComplexDP>::ApplyCPauliX)
        .def("ApplyCPauliY", &QubitRegister<ComplexDP>::ApplyCPauliY)
        .def("ApplyCPauliZ", &QubitRegister<ComplexDP>::ApplyCPauliZ)
        .def("ApplyCPauliSqrtZ", &QubitRegister<ComplexDP>::ApplyCPauliSqrtZ)
        .def("ApplyCHadamard", &QubitRegister<ComplexDP>::ApplyCHadamard)
        // Custom 1-qubit gate and controlled 2-qubit gates:
        .def("Apply1QubitGate",
             [](QubitRegister<ComplexDP> &a, unsigned qubit,
                py::array_t<ComplexDP, py::array::c_style | py::array::forcecast> matrix ) {
               py::buffer_info buf = matrix.request();
               if (buf.ndim != 2)
                   throw std::runtime_error("Number of dimensions must be two.");
               if (buf.shape[0] != 2 || buf.shape[1] != 2)
                   throw std::runtime_error("Input shape is not 2x2.");
               // Create and initialize the custom tiny-matrix used by Intel QS.
               ComplexDP *ptr = (ComplexDP *) buf.ptr;
               TM2x2<ComplexDP> m;
               m(0,0)=ptr[0];
               m(0,1)=ptr[1];
               m(1,0)=ptr[2];
               m(1,1)=ptr[3];
               a.Apply1QubitGate(qubit, m);
             }, "Apply custom 1-qubit gate.")
        .def("ApplyControlled1QubitGate",
             [](QubitRegister<ComplexDP> &a, unsigned control, unsigned qubit,
                py::array_t<ComplexDP, py::array::c_style | py::array::forcecast> matrix ) {
               py::buffer_info buf = matrix.request();
               if (buf.ndim != 2)
                   throw std::runtime_error("Number of dimensions must be two.");
               if (buf.shape[0] != 2 || buf.shape[1] != 2)
                   throw std::runtime_error("The shape of the unitary-matrix is not 2x2.");
               // Create and initialize the custom tiny-matrix used by Intel QS.
               ComplexDP *ptr = (ComplexDP *) buf.ptr;
               TM2x2<ComplexDP> m;
               m(0,0)=ptr[0];
               m(0,1)=ptr[1];
               m(1,0)=ptr[2];
               m(1,1)=ptr[3];
               a.ApplyControlled1QubitGate(control, qubit, m);
             }, "Apply custom controlled-1-qubit gate.")
        // Apply 1-qubit and 2-qubit channel.
        .def("GetOverallSignOfChannels", &QubitRegister<ComplexDP>::GetOverallSignOfChannels)
#if 1
        .def("ApplyChannel",
             [](QubitRegister<ComplexDP> &a, unsigned qubit, iqs::ChiMatrix<ComplexDP,4,32> chi) {
               a.ApplyChannel(qubit, chi);
             }, "Apply 1-qubit channel provided via its chi-matrix.")
        .def("ApplyChannel",
             [](QubitRegister<ComplexDP> &a, unsigned qubit1, unsigned qubit2,
                iqs::ChiMatrix<ComplexDP,16,32> chi) {
               a.ApplyChannel(qubit1, qubit2, chi);
             }, "Apply 2-qubit channel provided via its chi-matrix.")
#else
        .def("ApplyChannel",
             [](QubitRegister<ComplexDP> &a, unsigned qubit,
                py::array_t<ComplexDP, py::array::c_style | py::array::forcecast> matrix ) {
               py::buffer_info buf = matrix.request();
               if (buf.ndim != 2)
                   throw std::runtime_error("Number of dimensions must be two.");
               if (buf.shape[0] != 4 || buf.shape[1] != 4)
                   throw std::runtime_error("The shape of the chi-matrix is not 4x4.");
               // Create and initialize the custom chi-matrix used by Intel QS.
               ComplexDP *ptr = (ComplexDP *) buf.ptr;
               CM4x4<ComplexDP> m;
               m(0,0)=ptr[0];  m(0,1)=ptr[1];  m(0,2)=ptr[2];  m(0,3)=ptr[3];
               m(1,0)=ptr[4];  m(1,1)=ptr[5];  m(1,2)=ptr[6];  m(1,3)=ptr[7];
               m(2,0)=ptr[8];  m(2,1)=ptr[9];  m(2,2)=ptr[10]; m(2,3)=ptr[11];
               m(3,0)=ptr[12]; m(3,1)=ptr[13]; m(3,2)=ptr[14]; m(3,3)=ptr[15];
               a.ApplyChannel(qubit, m);
             }, "Apply 1-qubit channel provided via its chi-matrix.")
        .def("ApplyChannel",
             [](QubitRegister<ComplexDP> &a, unsigned qubit1, unsigned qubit2,
                py::array_t<ComplexDP, py::array::c_style | py::array::forcecast> matrix ) {
               py::buffer_info buf = matrix.request();
               if (buf.ndim != 2)
                   throw std::runtime_error("Number of dimensions must be two.");
               if (buf.shape[0] != 16 || buf.shape[1] != 16)
                   throw std::runtime_error("The shape of the chi-matrix is not 16x16.");
               // Create and initialize the custom chi-matrix used by Intel QS.
               ComplexDP *ptr = (ComplexDP *) buf.ptr;
               CM16x16<ComplexDP> m;
               int index = 0;
               for (int i=0; i<16; ++i)
               for (int j=0; j<16; ++j)
               {
                   m(i,j)=ptr[index];
                   index += 1;
               }
               a.ApplyChannel(qubit1, qubit2, m);
             }, "Apply 1-qubit channel provided via its chi-matrix.")
#endif
        // Three-qubit gates:
        .def("ApplyToffoli", &QubitRegister<ComplexDP>::ApplyToffoli)
        // State initialization:
        .def("Initialize",
               (void (QubitRegister<ComplexDP>::*)(std::string, std::size_t ))
                 &QubitRegister<ComplexDP>::Initialize)
        //Enable Specialization
        .def("TurnOnSpecialize", &QubitRegister<ComplexDP>::TurnOnSpecialize)
        .def("TurnOffSpecialize", &QubitRegister<ComplexDP>::TurnOffSpecialize)
        .def("TurnOnSpecializeV2", &QubitRegister<ComplexDP>::TurnOnSpecializeV2)
        .def("TurnOffSpecializeV2", &QubitRegister<ComplexDP>::TurnOffSpecializeV2)
        // Associate the random number generator and set its seed.
        .def("ResetRngPtr", &QubitRegister<ComplexDP>::ResetRngPtr)
        .def("SetRngPtr", &QubitRegister<ComplexDP>::SetRngPtr)
        .def("SetSeedRngPtr", &QubitRegister<ComplexDP>::SetSeedRngPtr)
        // State measurement and collapse:
        .def("GetProbability", &QubitRegister<ComplexDP>::GetProbability)
        .def("CollapseQubit", &QubitRegister<ComplexDP>::CollapseQubit)
          // Recall that the collapse selects: 'false'=|0> , 'true'=|1>
        .def("Normalize", &QubitRegister<ComplexDP>::Normalize)
        .def("ExpectationValue", &QubitRegister<ComplexDP>::ExpectationValue)
        // Other quantum operations:
        .def("ComputeNorm", &QubitRegister<ComplexDP>::ComputeNorm)
        .def("ComputeOverlap", &QubitRegister<ComplexDP>::ComputeOverlap)
        // Noisy simulation
        .def("GetT1", &QubitRegister<ComplexDP>::GetT1)
        .def("GetT2", &QubitRegister<ComplexDP>::GetT2)
        .def("GetTphi", &QubitRegister<ComplexDP>::GetTphi)
        .def("SetNoiseTimescales", &QubitRegister<ComplexDP>::SetNoiseTimescales)
        .def("ApplyNoiseGate", &QubitRegister<ComplexDP>::ApplyNoiseGate)
        // Utility functions:
        .def("Print",
             [](QubitRegister<ComplexDP> &a, std::string description) {
               py::scoped_ostream_redirect stream(
               std::cout,                               // std::ostream&
               py::module::import("sys").attr("stdout") // Python output
               );
               std::vector<size_t> qubits = {};
               std::cout << "<<the output has been redirected to the terminal>>\n";
               a.Print(description, qubits);
             }, "Print the quantum state with an initial description.");


//////////////////////////////////////////////////////////////////////////////
// Extra features: QAOA circuits
//////////////////////////////////////////////////////////////////////////////

#ifdef QAOA_EXTRA_FEATURES_HPP
    m.def("InitializeVectorAsMaxCutCostFunction",
          &qaoa::InitializeVectorAsMaxCutCostFunction<ComplexDP>,
          "Use IQS vector to store a large real vector and not as a quantum state.");

    m.def("InitializeVectorAsWeightedMaxCutCostFunction",
          &qaoa::InitializeVectorAsWeightedMaxCutCostFunction<ComplexDP>,
          "Use IQS vector to store a large real vector and not as a quantum state.");

    m.def("ImplementQaoaLayerBasedOnCostFunction",
          &qaoa::ImplementQaoaLayerBasedOnCostFunction<ComplexDP>,
          "Implement exp(-i gamma C)|psi>.");

    m.def("GetExpectationValueFromCostFunction",
          &qaoa::GetExpectationValueFromCostFunction<ComplexDP>,
          "Get expectation value from the cost function.");

    m.def("GetExpectationValueSquaredFromCostFunction",
          &qaoa::GetExpectationValueSquaredFromCostFunction<ComplexDP>,
          "Get expectation value squared from the cost function.");

    m.def("GetHistogramFromCostFunction",
          &qaoa::GetHistogramFromCostFunction<ComplexDP>,
          "Get histogram instead of just the expectation value.");
        
    m.def("GetHistogramFromCostFunctionWithWeightsRounded",
          &qaoa::GetHistogramFromCostFunctionWithWeightsRounded<ComplexDP>,
          "Get histogram instead of just the expectation value for a weighted graph, with all cut values rounded down.");
    
    m.def("GetHistogramFromCostFunctionWithWeightsBinned",
          &qaoa::GetHistogramFromCostFunctionWithWeightsBinned<ComplexDP>,
          "Get histogram instead of just the expectation value for a weighted graph, with specified bin width.");
#endif


//////////////////////////////////////////////////////////////////////////////
// MPI Features
//////////////////////////////////////////////////////////////////////////////
    py::class_<Environment>(m, "MPIEnvironment")
        .def(py::init<>())
        .def_static("GetRank", &Environment::GetRank)
        .def_static("IsUsefulRank", &Environment::IsUsefulRank)
        .def_static("GetSizeWorldComm",
             []() {
               int world_size = 1;
#ifdef INTELQS_HAS_MPI
               MPI_Comm_size(MPI_COMM_WORLD, &world_size);
#endif
               return world_size;
             }, "Number of processes when the MPI environment was first created.")
        .def_static("GetPoolRank", &Environment::GetPoolRank)
        .def_static("GetStateRank", &Environment::GetStateRank)
        .def_static("GetPoolSize", &Environment::GetPoolSize)
        .def_static("GetStateSize", &Environment::GetStateSize)

        .def_static("GetNumRanksPerNode", &Environment::GetNumRanksPerNode)
        .def_static("GetNumNodes", &Environment::GetNumNodes)
        .def_static("GetStateId", &Environment::GetStateId)
        .def_static("GetNumStates", &Environment::GetNumStates)

        .def_static("Barrier", &iqs::mpi::Barrier)
        .def_static("PoolBarrier", &iqs::mpi::PoolBarrier)
        .def_static("StateBarrier", &iqs::mpi::StateBarrier)

        .def_static("IncoherentSumOverAllStatesOfPool", &Environment::IncoherentSumOverAllStatesOfPool<double>)
        .def_static("UpdateStateComm", &Environment::UpdateStateComm);

}

//////////////////////////////////////////////////////////////////////////////

} // end namespace iqs

