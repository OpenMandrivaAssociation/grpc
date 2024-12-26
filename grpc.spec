# We need to use C++17 to link against the system abseil-cpp, or we get linker
# errors.
%global cpp_std 20

%define devname                 %mklibname %{name} -d

%bcond_without python

%if %{with python}
# Allow the python module to not link to libpython
%define _disable_ld_no_undefined 1
%endif

Name:           grpc
Version:        1.69.0
Release:        1
Summary:        Modern, open source, high-performance remote procedure call (RPC) framework
License:        ASL 2.0
Group:          System/Libraries
URL:            https://www.grpc.io
Source0:        https://github.com/grpc/grpc/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz
Source2:	https://github.com/census-instrumentation/opencensus-proto/archive/refs/heads/master.tar.gz
#Patch0:		grpc-1.62.1-protobuf-26.0.patch
Patch13:        grpc-1.53.2-grpc_build-cli-always-and-install-cli.patch
#Patch15:	grpc-1.43.0-system-gtest.patch
BuildRequires:  cmake
BuildRequires:  cmake(absl)
BuildRequires:  gcc-c++
BuildRequires:  protobuf-compiler
BuildRequires:  gperftools-devel
BuildRequires:  ninja
BuildRequires:  pkgconfig(benchmark)
BuildRequires:  pkgconfig(protobuf) >= 3.12.0
BuildRequires:  pkgconfig(openssl) > 1.1
BuildRequires:  pkgconfig(libcares)
BuildRequires:  pkgconfig(libsystemd)
#BuildRequires:  pkgconfig(gflags)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(zlib)
%if %{with python}
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-cython
%endif

%description
gRPC is a modern open source high performance RPC framework that can run in any
environment. It can efficiently connect services in and across data centers
with pluggable support for load balancing, tracing, health checking and
authentication. It is also applicable in last mile of distributed computing to
connect devices, mobile applications and browsers to backend services.

The main usage scenarios:

* Efficiently connecting polyglot services in microservices style architecture
* Connecting mobile devices, browser clients to backend services
* Generating efficient client libraries

Core Features that make it awesome:

* Idiomatic client libraries in 10 languages
* Highly efficient on wire and with a simple service definition framework
* Bi-directional streaming with http/2 based transport
* Pluggable auth, tracing, load balancing and health checking

#------------------------------------------------

%package        plugins
Summary:        gRPC protocol buffers compiler plugins
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       protobuf-compiler

%description    plugins
Plugins to the protocol buffers compiler to generate gRPC sources.

#------------------------------------------------

%package        cli
Summary:        gRPC protocol buffers cli
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}

%description    cli
Plugins to the protocol buffers compiler to generate gRPC sources.

#------------------------------------------------

%if %{with python}
%package -n     python-grpcio
Summary:        Python3 language bindings for grpc, remote procedure call (RPC) framework
Group:          Development/Python
Requires:       %{name} = %{version}-%{release}
%{?python_provide:%python_provide python-grpcio}

%description -n python-grpcio
Python3 bindings for gRPC library.
%endif

#------------------------------------------------

%prep
%autosetup -a1 -p1
tar xf %{S:1}
tar xf %{S:2}

# Remove bundled googletest
#sed -i -e '/\(gtest\|gmock\)-all.cc/d' CMakeLists.txt
#rm -rf third_party/googletest/
#mkdir -p third_party/googletest/google{test,mock}/include
rm -rf third_party/googletest
mv googletest-* third_party/googletest
rm -rf third_party/opencensus-proto
mv opencensus-proto-master third_party/opencensus-proto

# Do not DL opencensus-proto
ln -s $(pwd)/opencensus-proto-*/src third_party/opencensus-proto/src

# Remove bundled xxhash
rm -rvf third_party/xxhash
sed -i -e 's/\(_gRPC_XXHASH_INCLUDE_DIR\s\+\)\".*\"/\1"${CMAKE_INSTALL_INCLUDEDIR}"/' cmake/xxhash.cmake

# Remove Android sources and examples
rm -rvf examples/android src/android

# Drop the NodeJS example’s package-lock.json file, which will hopefully keep
# us from having bugs filed due to CVE’s in its (unpackaged) recursive
# dependencies.
rm -rvf examples/node/package-lock.json

# Remove unwanted .gitignore files, generally in examples. One could argue that
# a sample .gitignore file is part of the example, but, well, we’re not going
# to do that.
find . -type f -name .gitignore -print -delete

# We need to adjust the C++ standard to avoid abseil-related linker errors. For
# the main C++ build, we can use CMAKE_CXX_STANDARD. For extensions, examples,
# etc., we must patch.
sed -r -i 's/(std=c\+\+)1[1,4]/\1%{cpp_std}/g' \
    setup.py Rakefile \
    examples/cpp/*/Makefile \
    examples/cpp/*/CMakeLists.txt \
    tools/run_tests/artifacts/artifact_targets.py \
    tools/distrib/python/grpcio_tools/setup.py

%build
export CXXFLAGS="%{build_cxxflags} -Wno-deprecated-declarations -std=gnu++%{cpp_std}"
export LDFLAGS="%{build_ldflags} -Wno-deprecated-declarations -std=gnu++%{cpp_std}"
%cmake -GNinja                            \
       -DCMAKE_CXX_STANDARD=%{cpp_std}    \
       -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
       -DgRPC_INSTALL=ON                  \
       -DgRPC_INSTALL_LIBDIR:PATH="%{_lib}" \
       -DgRPC_INSTALL_CMAKEDIR:PATH="%{_libdir}/cmake/grpc" \
       -DgRPC_BUILD_TESTS:BOOL=ON         \
       -DgRPC_ABSL_PROVIDER=package       \
       -DgRPC_BENCHMARK_PROVIDER=package  \
       -DgRPC_CARES_PROVIDER=package      \
       -DgRPC_PROTOBUF_PROVIDER=package   \
       -DgRPC_RE2_PROVIDER=package        \
       -DgRPC_SSL_PROVIDER=package        \
       -DgRPC_ZLIB_PROVIDER=package       \
       -DZLIB_LIBRARY=%{_libdir}/libz.so
export LD_LIBRARY_PATH=$(pwd):$LD_LIBRARY_PATH
%ninja_build
cd ..

%if %{with python}
# build python module
export GRPC_PYTHON_BUILD_WITH_CYTHON=True
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=True
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=True
export GRPC_PYTHON_BUILD_SYSTEM_CARES=True
export GRPC_PYTHON_BUILD_SYSTEM_RE2=True
export GRPC_PYTHON_BUILD_SYSTEM_ABSL=True
%py_build
%endif

%install
%ninja_install -C build

%if %{with python}
%py_install
%endif

# We don't currently ship opentelemetry and therefore the plugin doesn't get
# built -- but its pkgconfig file (dragging in dependencies) is installed
# anyway. Remove it.
# FIXME get rid of this line if and when we package opentelemetry and add
# it as a dependency.
rm -f %{buildroot}%{_libdir}/pkgconfig/grpcpp_otel_plugin.pc

%libpackages -d

cat >%{specpartsdir}/%{devname}.specpart <<EOF
%%%package -n     %{devname}
Summary:        gRPC library development files
Group:          Development/C++
Requires:       %{name}-cli = %{EVRD}
Requires:       %{name}-plugins = %{EVRD}
Provides:       %{name}-devel = %{EVRD}
EOF

for i in $LIBPACKAGES; do
	echo "Requires:	%{mklibname $i} = %{EVRD}" >>%{specpartsdir}/%{devname}.specpart
done

cat >>%{specpartsdir}/%{devname}.specpart <<EOF
%%%description -n %{devname}
Development headers and files for gRPC libraries.

%%%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/grpc/
%{_includedir}/grpc/
%{_includedir}/grpc++/
%{_includedir}/grpcpp/
EOF

%files
%doc README.md
%license LICENSE
%{_datadir}/grpc/

%files cli
%doc README.md
%license LICENSE
%{_bindir}/grpc_cli

%files plugins
%doc README.md
%license LICENSE
%{_bindir}/grpc_*_plugin

%if %{with python}
%files -n python-grpcio
%license LICENSE
%{python_sitearch}/grpc/
%{python_sitearch}/grpcio-%{version}*.*-info
%endif
