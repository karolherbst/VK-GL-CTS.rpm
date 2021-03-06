Name:           VK-GL-CTS
Version:        1.2.3.3
Release:        100
Summary:        Official Khronos CTS for OpenGL and Vulkan

# check PACKAGES inside external/fetch_sources.py
%global AMBER_VER a40bef4dba98d2d80b48e5a940d8574fbfceb197
%global GLSLANG_VER b5f003d7a3ece37db45578a8a3140b370036fc64
%global SPIRV_HEADERS_VER f8bf11a0253a32375c32cad92c841237b96696c0
%global SPIRV_TOOLS_VER d2b486219495594f2e5d0e8d457fc234a3460b3b

%global AMBER_SRC amber-%{AMBER_VER}.tar.gz
%global GLSLANG_SRC glslang-%{GLSLANG_VER}.tar.gz
%global SPIRV_HEADERS_SRC spirv-headers-%{SPIRV_HEADERS_VER}.tar.gz
%global SPIRV_TOOLS_SRC spirv-tools-%{SPIRV_TOOLS_VER}.tar.gz

License:        ASL 2.0 and BSD and GPLv3+
URL:            https://github.com/KhronosGroup/VK-GL-CTS
Source0:        https://github.com/KhronosGroup/%{name}/archive/vulkan-cts-%{version}.tar.gz
Source1:        https://github.com/google/amber/archive/%{AMBER_VER}.tar.gz#/%{AMBER_SRC}
Source2:        https://github.com/KhronosGroup/glslang/archive/%{GLSLANG_VER}.tar.gz#/%{GLSLANG_SRC}
Source3:        https://github.com/KhronosGroup/SPIRV-Headers/archive/%{SPIRV_HEADERS_VER}.tar.gz#/%{SPIRV_HEADERS_SRC}
Source4:        https://github.com/KhronosGroup/SPIRV-Tools/archive/%{SPIRV_TOOLS_VER}.tar.gz#/%{SPIRV_TOOLS_SRC}

Patch0:         0001-make-system-installs-possible.patch

BuildRequires:  cmake >= 2.8.2
BuildRequires:  gcc
BuildRequires:  gcc-c++
%if 0%{?fedora}
Requires:       gmock
BuildRequires:  gmock-devel
%endif
Requires:       libglvnd
BuildRequires:  libglvnd-devel
Requires:       libpng
BuildRequires:  libpng-devel
Requires:       libwayland-client
Requires:       libwayland-cursor
Requires:       libwayland-egl
Requires:       libwayland-server
Requires:       libxcb
BuildRequires:  libxcb-devel
BuildRequires:  python3
BuildRequires:  make
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  wayland-devel
Requires:       zlib
BuildRequires:  zlib-devel

%description
VK-GL-CTS is the official confromance test suite for OpenGL and Vulkan

%prep
%autosetup -p1 -n %{name}-vulkan-cts-%{version}

mkdir -p external/amber/src
pushd external/amber/src
  tar xf %{SOURCE1} --strip 1
popd
mkdir -p external/glslang/src
pushd external/glslang/src
  tar xf %{SOURCE2} --strip 1
popd
mkdir -p external/spirv-headers/src
pushd external/spirv-headers/src
  tar xf %{SOURCE3} --strip 1
popd
mkdir -p external/spirv-tools/src
pushd external/spirv-tools/src
  tar xf %{SOURCE4} --strip 1
popd

rm -rf build
mkdir build

%build
pushd build
  %cmake ../ \
    -DCMAKE_BUILD_TYPE:STRING=Debug \
    -DBUILD_SHARED_LIBS:BOOL=OFF
  make VERBOSE=1 %{?_smp_mflags}
popd

%install
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_datadir}/%{name}/gl_cts/data
mkdir -p %{buildroot}/%{_datadir}/%{name}/mustpass/vulkan

pushd build
  cp executor/testlog-to-csv %{buildroot}/%{_bindir}/
  cp executor/testlog-to-xml %{buildroot}/%{_bindir}/
  cp external/openglcts/modules/glcts %{buildroot}/%{_bindir}/
  cp external/vulkancts/modules/vulkan/deqp-vk %{buildroot}/%{_bindir}/
popd
# the gtf tests have no relevance anymore
find external/openglcts/data/mustpass/ -type f -iname *gtf* -delete
cp -r external/openglcts/data/mustpass/* %{buildroot}/%{_datadir}/%{name}/mustpass/
cp -r external/vulkancts/mustpass/* %{buildroot}/%{_datadir}/%{name}/mustpass/vulkan/
cp -r external/openglcts/data/gl* %{buildroot}/%{_datadir}/%{name}/gl_cts/data
cp -r external/vulkancts/data/vulkan %{buildroot}/%{_datadir}/%{name}/

%files
%license LICENSE
%dir %{_datadir}/%{name}/
%{_bindir}/deqp-vk
%{_bindir}/glcts
%{_bindir}/testlog-to-csv
%{_bindir}/testlog-to-xml
%{_datadir}/%{name}/*

%changelog
* Tue Jun 25 2019 Karol Herbst <kherbst@redhat.com> - 1.1.4.1-100
- Add testlog conversion executeables
- Fix file permissions

* Tue Jun 11 2019 Karol Herbst <kherbst@redhat.com> - 1.1.4.1-0
- Initial RPM release
