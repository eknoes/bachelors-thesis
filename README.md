# Bachelor's Thesis of Sönke Huster
**Enhancements for MACsec providing transparent Layer-2 encryption**

This repository contains all materials for my thesis.
The thesis itself as PDF is [here](thesis/thesis.pdf).

## Conclusion
The goal of this thesis was to develop a transparent fragmentation solution while using MACsec to mitigate the problems of a decreased MTU.
It is required to not mitigate the problem by the use of jumbo frames or fragmentation in upper layers.
Three established fragmentation processes in computer networks were presented.
Two general approaches for the given problem were deduced and discussed.
The approach of fragmenting MPDU turned out to be vulnerable, so the approach of fragmenting SDU was choosen.
To optimize this solution a concatenation scheme was developed.
The fragmentation solution was implemented in C for the linux kernel.
The concatenation scheme was not implemented.
The implemented algorithm in MACsec was then evaluated regarding performance and security.
For evaluation of performance the implementation was deployed to two physical machines.
The results of this evaluation were compared to the solution of using jumbo frames, which is considered as an optimal solution.
Here, the proposed solution appeared to be successful, as the performance results were just slightly below the results of the optimum.
Furthermore, the security evaluation showed that the proposed solution is secure.

The solution of fragmenting SDU solves the problem of a decreased MTU when using MACsec.
It performs well---as the evaluation showed---and maintains the security which is established by MACsec.
The developed improvement of a concatenation process appeared to be an optimization, which could be implemented and evaluated by future work.
Moreover, the field of other improvements and optimizations for MACsec can be researched.
The behavior when using Jumbo Frames seems to be an interesting topic which can be investigated, as the evaluation detected some notable deviations from expected behavior.

## Repo Information
The thesis itself is written in LaTeX, the source files are in the `thesis/` directory.

The implementation can be found in `macsec/`, the scripts for evaluation are in `evaluation/` and a small test environment can be setup with the files contained in `test/` and [Vagrant](https://vagrantup.com).

Each directory contains its own README file.

* LaTeX Source: [Thesis](thesis/README.md)
* Fast Test environment for development: [Test](test/README.md)
* Modified macsec module: [Implementation](macsec/README.md)
* Evaluation scripts and measurements: [Evaluation](evaluation/README.md)
