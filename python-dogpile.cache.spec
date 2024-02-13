#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (sdist contains prebuilt html)
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	A caching front-end based on the Dogpile lock
Summary(pl.UTF-8):	Frontend z pamięcią podręczną oparty na blokadzie Dogpile
Name:		python-dogpile.cache
# keep 0.9.x here for python2 support
Version:	0.9.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/dogpile.cache/
Source0:	https://files.pythonhosted.org/packages/source/d/dogpile.cache/dogpile.cache-%{version}.tar.gz
# Source0-md5:	ab35b826ca17477ab0db3dd76227e8aa
Patch0:		dogpile.cache-mock.patch
Patch1:		dogpile.cache-pytest.patch
URL:		https://pypi.org/project/dogpile.cache/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-Mako
BuildRequires:	python-decorator >= 4.0.0
BuildRequires:	python-futures
BuildRequires:	python-mock
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Mako
BuildRequires:	python3-decorator >= 4.0.0
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-Mako
BuildRequires:	python-changelog
BuildRequires:	python-decorator
BuildRequires:	python-sphinx-paramlinks
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dogpile consists of two subsystems, one building on top of the other.

dogpile provides the concept of a "dogpile lock", a control structure
which allows a single thread of execution to be selected as the
"creator" of some resource, while allowing other threads of execution
to refer to the previous version of this resource as the creation
proceeds; if there is no previous version, then those threads block
until the object is available.

dogpile.cache is a caching API which provides a generic interface to
caching backends of any variety, and additionally provides API hooks
which integrate these cache backends with the locking mechanism of
dogpile.

%description -l pl.UTF-8
Dogpile składa się z dwóch podsystemów, jeden jest zbudowany na
drugim.

dogpile udostępnia koncept "blokady dogpile" - struktury sterującej,
pozwalającej na wybór jednego z wątków jako "twórcy" jakiegoś zasobu,
podczas gdy pozostałe wątki odwołują się do poprzedniej wersji zasobu
w miarę procesu tworzenia; jeśli nie ma poprzedniej wersji, wątki te
blokują się do czasu dostępności obiektu.

dogpile.cache to API z pamięcią podręczną, zapewniające ogólny
interfejs do dowolnych backendów pamięci podręcznej oraz uchwyty API
integrujące te backendy z mechanizmem blokującym dogpile.

%package -n python3-dogpile.cache
Summary:	A caching front-end based on the Dogpile lock
Summary(pl.UTF-8):	Frontend z pamięcią podręczną oparty na blokadzie Dogpile
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-dogpile.cache
Dogpile consists of two subsystems, one building on top of the other.

dogpile provides the concept of a "dogpile lock", a control structure
which allows a single thread of execution to be selected as the
"creator" of some resource, while allowing other threads of execution
to refer to the previous version of this resource as the creation
proceeds; if there is no previous version, then those threads block
until the object is available.

dogpile.cache is a caching API which provides a generic interface to
caching backends of any variety, and additionally provides API hooks
which integrate these cache backends with the locking mechanism of
dogpile.

%description -n python3-dogpile.cache -l pl.UTF-8
Dogpile składa się z dwóch podsystemów, jeden jest zbudowany na
drugim.

dogpile udostępnia koncept "blokady dogpile" - struktury sterującej,
pozwalającej na wybór jednego z wątków jako "twórcy" jakiegoś zasobu,
podczas gdy pozostałe wątki odwołują się do poprzedniej wersji zasobu
w miarę procesu tworzenia; jeśli nie ma poprzedniej wersji, wątki te
blokują się do czasu dostępności obiektu.

dogpile.cache to API z pamięcią podręczną, zapewniające ogólny
interfejs do dowolnych backendów pamięci podręcznej oraz uchwyty API
integrujące te backendy z mechanizmem blokującym dogpile.

%package apidocs
Summary:	API documentation for Python dogpile.cache module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona dogpile.cache
Group:		Documentation

%description apidocs
API documentation for Python dogpile.cache module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona dogpile.cache.

%prep
%setup -q -n dogpile.cache-%{version}
%patch0 -p1
%patch1 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests -k 'not test_dbm_backend and not test_memcached_backend and not test_redis_backend'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests -k 'not test_dbm_backend and not test_memcached_backend and not test_redis_backend'
%endif
%endif

%if %{with doc}
sphinx-build-2 -b html docs/build docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/dogpile
%{py_sitescriptdir}/dogpile.cache-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-dogpile.cache
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/dogpile
%{py3_sitescriptdir}/dogpile.cache-%{version}-py*.egg-info
%endif

%files apidocs
%defattr(644,root,root,755)
%doc docs/{_static,*.html,*.js}
