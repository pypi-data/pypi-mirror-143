# Description
Natorbs is a utility for post-processing the results of quantum-chemical
calculations. It computes natural/natural spin-density orbitals based
on canonical unrestricted (UHF-type) orbitals resulting from HF or DFT
calculations. It can also compute natural orbitals for chemical
valence (NOCVs) based on the orbitals of a molecule and its constituing
fragments.

The program was created in response to the demand in the course of our
own studies on the electronic structure of open-shell systems,
transition-metal complexes in particular.  By generating
natural/spin orbitals one can immediately identify the orbitals
carrying unpaired electrons among, possibly, hundreds of orbitals,
most of which are empty or describe closed shells. Such a diagnosis
tool is particularly valuable for complicated electronic structure
(broken-symmetry solutions / antiferromagnetic coupling /
biradicals and multiradicals).
It could be useful, however, to facilitate interpretation of
any open-shell UHF-type calculations.

Natorbs works with a number of quantum-chemical programs and was
created with the aim of being independent software.  It reads the
input data (geometry and MOs) either using
[the cclib library](http://cclib.sourceforge.net) or via
[Molden format](http://www.cmbi.ru.nl/molden).  It saves the output
data (the desired flavour of natural orbitals) in Molden format, so
that like Molden or Gabedit can read these orbitals for
visualization. Note that natorbs reconstructs the overlap integrals of
the atomic basis functions from the provided molecular orbitals
(exactly if all the virtuals are provided or approximately otherwise).

# License
Program Natorbs is made available free of charge under the terms of
the terms of the 3-clause BSD license.  
Copyright 2021 Uniwersytet Jagielloñski, Dr hab. Mariusz Radoñ
For details, see attached file LICENSE.txt .

# Installation
Natorbs requires Python3, numpy, and cclib (tested with version 1.6.1).
The documentation is provided in the form of man page on Unix-like systems.

Determine the installation prefix, e.g. /usr/local or $HOME/.local,
which will be referred to as PREFIX. You need root priviliges to
natorbs install system-wide.

It is recommended to remove the previous version before installing a
new one.

Use the following shell command to install natorbs  
    python3 setup.py install --prefix=<prefix>  
Replace <prefix> by your desired installation prefix, e.g. /usr/local
or $HOME/.local (you need root priviliges to install the program
system-wide).

Make sure that <prefix>/bin location is listed in your PATH
variable. If you would like to access the documentatoon provided (man
page), also make sure that <prefix>/share/man is listed in your
MANPATH variable.

#Using
Call the program with --help / -h option
    natorbs -h
or use the provided man page
    man natorbs
for the usage info and the list of options.

#Recommended Citation
M. Radoñ, <i>Natorbs v1.0</i>, Jagiellonian University, Krakow, Poland, 2021; available from https://tungsten.ch.uj.edu.pl/~mradon/natorbs

#Further Information
Definitions of natural/natural-spin orbitals can be found
in quantum-chemistry literature. Basically,
they are defined as eigenvectors of
one-particle density or spin-density matrix, respectively. The
connection between spin-unrestricted orbitals and natural orbitals is
explained in the seminal paper:
* A. Amos and G. Hall, Proc. Roy. Soc. A, 1961, 263, 483, doi: 10.1098/rspa.1961.0175.

For description of the NOCV method see the following paper:
* M. Mitoraj and A. Michalak, J. Mol. Model., 2007, 13, 347,
  doi: 10.1007/s00894-006-0149-4.
The pairing property of NOCVs:
* M. Radon Theor. Chem. Acc., 2008, 120, 337,
  doi: 10.1007/s00214-008-0428-5.

Some applications of programs Natorbs, mainly its NOCV
stuff, can be found in the following papers:
* M. Radon, E. Broclawik, J. Chem. Theory Comput., 2007, 3, 728-734,
  doi 10.1021/ct600363a;
* M. Radon, P. Kozyra, A. Stepniewski, J. Datka, E. Broclawik,
  Can. J. Chem., 2013, 91, 538-543, doi: 10.1139/cjc-2012-0536;
* P. Kozyra, M. Radon, J. Datka E. Broclawik Struct. Chem., 2012, 23,
  1349-1356, doi: 10.1007/s11224-012-0050-y;
* K. Gora-Marek, A. Stepniewski, M. Radon, E. Broclawik,
  Phys. Chem. Chem. Phys., 2014, 16, 24089-24098,
  doi: 10.1039/C4CP03350G;
* E. Broclawik, A. Stepniewski, M. Radon, J. Inorg. Biochem., 2014,
  136, 147-153, doi 10.1016/j.jinorgbio.2014.01.010.
