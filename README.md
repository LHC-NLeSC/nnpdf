# buildmaster
Converts paper data into NNPDF standards. 
 
## Project summary and aim

The aim of `buildmaster` is to provide a systematic mechanism to
create a master copy of the experimental data used in the NNPDF fits.

This program requires `libnnpdf` and uses the CommonData structures defined there.

### Release and Tag policy

The code is tagged and released when a major and stable status is achieved. 
Tags and releases do not necessarily follows the NNPDF releases.

### New data implementation rules

Given a new data implementation request:

1. 2 developers are assigned

2. Each developer implements the data independently, without pushing its local branch to github

3. When both implementations are ready, each developers open a pull request with his own version

4. A referee is assigned, the referee must be a core developer

5. The referee reads and run the code, check for code and data bugs and, decides the best implementation.

### Code development policy/rules

Developers must never commit code structure modifications to master. The development pattern should follow these rules:
- Open an issue explaining your bug or feature request. If you report a bug, post information to reproduce it.
- The resolution of issues must be performed in a new branch through a pull request.
- If you have already a local version of the code that you would like to merge in the master, open a pull request.
- The pull request must be reviewed by at least 2 core developers.

### Code style

Originally the code of this library was written at the beginning of
2012 so at that time C++11 was not used as default. Developers are
invited to implement new experiments using clean C++11 features.

### Continuous integration (CI)

CI is actually not implemented in the current repository..

### Testing

Testing is actually not implemented in the current repository.

## Installation

`buildmaster` depends on the following libraries:

- libnnpdf

please ensure to have the dependencies correctly installed and in your
PATH before installing libnnpdf.

In order to compile just type `make`.

## Documentation

### Running the code

In order to generate a master copy of all experimental data run the
`buildmaster` program. This program will create for each dataset:
- DATA_<exp>.dat are generated and placed in the results folder
- SYSTYPE_<exp>_NULL.dat are generated and placed in results/systypes
After generating these files the user can copy them to the `nnpdfcpp/data/commondata` folder.

### Code documentation

In order to implement a new dataset the developer has to:

1. Create input files in `rawdata/<exp>`, where `<exp>` is the name of
the new dataset and must coincide with the `apfelcomb` and `applgrid`
definitions. The input files are raw data files obtained from papers
(copy/paste) or from the HEPDATA website. The user has the freedom to
select his preferred format, but csv or plain text are the recommended
formats.

2. Create a new class with the dataset name in `inc` (*.h) and
`filters` (*.cc) following the patter of other datasets, i.e. in the
header create a
```c++
static const dataInfoRaw MY_NEW_DATATSET_INFO = {
int, // number of data points
int, // number of systematics
string, // the set name
string, // the process type (check apfelcomb documentation) }
```
followed by a new class which inherits from libnnpdf `NNPDF::CommonData`:
```c++
class MY_NEW_DATASET_CLASSFilter: public CommonData {
public: MY_NEW_DATASET_CLASSFilter(MY_NEW_DATASET_INFO) { ReadData(); }
private:
	void ReadData();
}
```
in the C++ file you implement the `void ReadData()` method.

4. The previous class must read from rawdata all the required
information about the data, and fill the attributes of the CommonData
class in `libnnpdf`. The required entries are:
- the kinematic information: fKin1, fKin2, fKin3
- the data: fData
- the statistical uncer.: fStat
- the systematic uncer.: fSys

5. Edit `src/buildmaster.cc` by including the header file of the new
dataset and by pushing back to the `target` object a new instance of
the class created in step 2. Namely:
```c++
target.push_back(new MY_NEW_DATASET_CLASSFilter());
```

### Layout documentation

For specifications about data please check the `nnpdfcpp` repository in `data/doc`.

