%define _disable_ld_no_undefined 1

%define major 1

%define libeloop %mklibname eloop %{major}
%define libeloop_devel %mklibname eloop -d
%define libtsm %mklibname tsm %{major}
%define libtsm_devel %mklibname tsm -d
%define libuterm %mklibname uterm %{major}
%define libuterm_devel %mklibname uterm -d

Summary:	KMS/DRM based System Console
Name:		kmscon
Version:	7
Release:	1
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/kmscon/
Source0:	http://www.freedesktop.org/software/kmscon/releases/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(libsystemd-daemon)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(fuse)

%description
Kmscon is a simple terminal emulator based on 
linux kernel mode setting (KMS).
It is an attempt to replace the in-kernel 
VT implementation with a userspace console.

%package -n %{libeloop}
Summary:	Epoll-based Event-Loop Library
Group:		System/Libraries

%description -n %{libeloop}
Epoll-based Event-Loop Library.

%package -n %{libeloop_devel}
Summary:	Development libraries for libeloop
Group:		Development/C

%description -n %{libeloop_devel}
Development libraries for libeloop.

%package -n %{libtsm}
Summary:	Terminal-emulator State Machine
Group:		System/Libraries

%description -n %{libtsm}
Terminal-emulator State Machine.

%package -n %{libtsm_devel}
Summary:	Development libraries for libtsm	
Group:		Development/C

%description -n %{libtsm_devel}
Development libraries for libtsm.

%package -n %{libuterm}
Summary:	User-space Terminal Helper Library
Group:		System/Libraries

%description -n %{libuterm}
User-space Terminal Video/Input/Hotplug/etc Helper Library.

%package -n %{libuterm-devel}
Summary:	Development libraries for libuterm
Group:		Development/C

%description -n %{libuterm-devel}
Development libraries for libuterm.

%prep
%setup -q

%build
%serverbuild_hardened

%configure2_5x \
		--disable-wlterm

%make

%install
%makeinstall_std
install -pm0644 docs/*.service -D %{buildroot}%{_unitdir}

%files
%{_bindir}/%{name}
%{_libdir}/%{name}/*.so
%{_unitdir}/%{name}*.service

%files -n %{libeloop}
%{_libdir}/libeloop.so.%{major}*

%files -n %{libeloop_devel}
%{_libdir}/libeloop.so
%{_libdir}/pkgconfig/libeloop.pc
%{_includedir}/eloop.h

%files -n %{libtsm}
%{_libdir}/libtsm.so.%{major}*

%files -n %{libtsm_devel}
%{_libdir}/libtsm.so
%{_libdir}/pkgconfig/libtsm.pc
%{_includedir}/tsm_*.h

%files -n %{libuterm}
%{_libdir}/libuterm.so.%{major}*

%files -n %{libuterm_devel}
%{_libdir}/libuterm.so
%{_libdir}/pkgconfig/libuterm.pc
%{_includedir}/uterm_*.h

