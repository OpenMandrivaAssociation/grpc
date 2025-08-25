# We need to use C++17 to link against the system abseil-cpp, or we get linker
# errors.
%global cpp_std 20

%define devname                 %mklibname %{name} -d

%bcond_without python

%if %{with python}
# Allow the python module to not link to libpython
%define _disable_ld_no_undefined 1
%endif

%global s1_name abseil-cpp
%global s1_commit 76bb24329e8bf5f39704eb10d21b9a80befa7c81
%global s1_shortcommit %(c=%{s1_commit}; echo ${c:0:7})

%global s2_name benchmark
%global s2_commit 12235e24652fc7f809373e7c11a5f73c5763fc4c
%global s2_shortcommit %(c=%{s2_commit}; echo ${c:0:7})

%global s3_name bloaty
%global s3_commit 60209eb1ccc34d5deefb002d1b7f37545204f7f2
%global s3_shortcommit %(c=%{s3_commit}; echo ${c:0:7})

%global s4_name boringssl
%global s4_commit c63fadbde60a2224c22189d14c4001bbd2a3a629
%global s4_shortcommit %(c=%{s4_commit}; echo ${c:0:7})

%global s5_name data-plane-api
%global s5_commit 4de3c74cf21a9958c1cf26d8993c55c6e0d28b49
%global s5_shortcommit %(c=%{s5_commit}; echo ${c:0:7})

%global s6_name googleapis
%global s6_commit fe8ba054ad4f7eca946c2d14a63c3f07c0b586a0
%global s6_shortcommit %(c=%{s6_commit}; echo ${c:0:7})

%global s7_name googletest
%global s7_commit 52eb8108c5bdec04579160ae17225d66034bd723
%global s7_shortcommit %(c=%{s7_commit}; echo ${c:0:7})

%global s8_name opencensus-proto
%global s8_commit 4aa53e15cbf1a47bc9087e6cfdca214c1eea4e89
%global s8_shortcommit %(c=%{s8_commit}; echo ${c:0:7})

%global s9_name opentelemetry-proto
%global s9_commit 60fa8754d890b5c55949a8c68dcfd7ab5c2395df
%global s9_shortcommit %(c=%{s9_commit}; echo ${c:0:7})

%global s10_name protobuf
%global s10_commit 74211c0dfc2777318ab53c2cd2c317a2ef9012de
%global s10_shortcommit %(c=%{s10_commit}; echo ${c:0:7})

%global s11_name protoc-gen-validate
%global s11_commit 7b06248484ceeaa947e93ca2747eccf336a88ecc
%global s11_shortcommit %(c=%{s11_commit}; echo ${c:0:7})

%global s12_name re2
%global s12_commit 0c5616df9c0aaa44c9440d87422012423d91c7d1
%global s12_shortcommit %(c=%{s12_commit}; echo ${c:0:7})

%global s13_name xds
%global s13_commit 3a472e524827f72d1ad621c4983dd5af54c46776
%global s13_shortcommit %(c=%{s13_commit}; echo ${c:0:7})

%global s14_name zlib
%global s14_commit f1f503da85d52e56aae11557b4d79a42bcaa2b86
%global s14_shortcommit %(c=%{s14_commit}; echo ${c:0:7})

Name:           grpc
Version:        1.74.0
Release:        2
Summary:        Modern, open source, high-performance remote procedure call (RPC) framework
License:        ASL 2.0
Group:          System/Libraries
URL:            https://www.grpc.io
Source0:        https://github.com/grpc/grpc/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/abseil/%{s1_name}/archive/%{s1_commit}/%{s1_name}-%{s1_shortcommit}.tar.gz
Source2:        https://github.com/google/%{s2_name}/archive/%{s2_commit}/%{s2_name}-%{s2_shortcommit}.tar.gz
Source3:        https://github.com/google/%{s3_name}/archive/%{s3_commit}/%{s3_name}-%{s3_shortcommit}.tar.gz
Source4:        https://github.com/google/%{s4_name}/archive/%{s4_commit}/%{s4_name}-%{s4_shortcommit}.tar.gz
Source5:        https://github.com/envoyproxy/%{s5_name}/archive/%{s5_commit}/%{s5_name}-%{s5_shortcommit}.tar.gz
Source6:        https://github.com/googleapis/%{s6_name}/archive/%{s6_commit}/%{s6_name}-%{s6_shortcommit}.tar.gz
Source7:        https://github.com/google/%{s7_name}/archive/%{s7_commit}/%{s7_name}-%{s7_shortcommit}.tar.gz
Source8:        https://github.com/census-instrumentation/%{s8_name}/archive/%{s8_commit}/%{s8_name}-%{s8_shortcommit}.tar.gz
Source9:        https://github.com/open-telemetry/%{s9_name}/archive/%{s9_commit}/%{s9_name}-%{s9_shortcommit}.tar.gz
Source10:       https://github.com/protocolbuffers/%{s10_name}/archive/%{s10_commit}/%{s10_name}-%{s10_shortcommit}.tar.gz
Source11:        https://github.com/bufbuild/%{s11_name}/archive/%{s11_commit}/%{s11_name}-%{s11_shortcommit}.tar.gz
Source12:        https://github.com/google/%{s12_name}/archive/%{s12_commit}/%{s12_name}-%{s12_shortcommit}.tar.gz
Source13:        https://github.com/cncf/%{s13_name}/archive/%{s13_commit}/%{s13_name}-%{s13_shortcommit}.tar.gz
Source14:        https://github.com/madler/%{s14_name}/archive/%{s14_commit}/%{s14_name}-%{s14_shortcommit}.tar.gz
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

# Remove bundled googletest
#sed -i -e '/\(gtest\|gmock\)-all.cc/d' CMakeLists.txt
#rm -rf third_party/googletest/
#mkdir -p third_party/googletest/google{test,mock}/include
cd third_party
tar xf %{S:1}
tar xf %{S:2}
tar xf %{S:3}
tar xf %{S:4}
tar xf %{S:5}
tar xf %{S:6}
tar xf %{S:7}
tar xf %{S:8}
tar xf %{S:9}
tar xf %{S:10}
tar xf %{S:11}
tar xf %{S:12}
tar xf %{S:13}
tar xf %{S:14}
for i in googletest opencensus-proto xds protoc-gen-validate googleapis; do
	rm -rf $i
	mv $i-* $i
done
rm -rf envoy-api
mv data-plane-api-* envoy-api
cd ..

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
%if "%{cpp_std}" != "17"
sed -i -e 's,c++17,c++%{cpp_std},g' setup.py
%endif
export GRPC_PYTHON_BUILD_WITH_CYTHON=True
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=True
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=True
export GRPC_PYTHON_BUILD_SYSTEM_CARES=True
export GRPC_PYTHON_BUILD_SYSTEM_RE2=True
export GRPC_PYTHON_BUILD_SYSTEM_ABSL=True
# Sadly the build system is very much messed up and
# passes -std=c++20 even to C files, which makes clang
# throw a fatal error while gcc throws a warning
export CC=gcc
export CXX=g++
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
