%define _disable_ld_no_undefined 1

%define major 1

%define libeloop %mklibname eloop %{major}
%define libeloop_devel %mklibname eloop -d
%define libuterm %mklibname uterm %{major}
%define libuterm_devel %mklibname uterm -d

Summary:	KMS/DRM based System Console
Name:		kmscon
Version:	8
Release:	4
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/kmscon/
Source0:	http://www.freedesktop.org/software/kmscon/releases/%{name}-%{version}.tar.xz
#Patch0:		0001-fix-service-file.patch
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(libsystemd-daemon)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangoft2)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(libtsm)
Requires(post,preun):	spec-helper

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

%package -n %{libuterm}
Summary:	User-space Terminal Helper Library
Group:		System/Libraries

%description -n %{libuterm}
User-space Terminal Video/Input/Hotplug/etc Helper Library.

%package -n %{libuterm_devel}
Summary:	Development libraries for libuterm
Group:		Development/C

%description -n %{libuterm_devel}
Development libraries for libuterm.

%prep
%setup -q
%apply_patches

%build
%serverbuild_hardened

%configure2_5x \
		--disable-wlterm

%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_unitdir}
install -pm0644 docs/*.service %{buildroot}%{_unitdir}/

%post
if [ -e /etc/systemd/system/autovt\@.service ]; then
	# backup the original autovt
	mv -f /etc/systemd/system/autovt\@.service /etc/systemd/system/autovt\@.kmscon
fi

ln -s /lib/systemd/system/kmsconvt\@.service /etc/systemd/system/autovt\@.service

%_post_service kmsconvt\@.service

%preun
%_preun_service kmsconvt\@.service

if [ -e /etc/systemd/system/autovt\@.service ]; then
	rm -rf /etc/systemd/system/autovt\@.service
	mv -f /etc/systemd/system/autovt\@.kmscon autovt\@.service
fi

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

%files -n %{libuterm}
%{_libdir}/libuterm.so.%{major}*

%files -n %{libuterm_devel}
%{_libdir}/libuterm.so
%{_libdir}/pkgconfig/libuterm.pc
%{_includedir}/uterm_*.h

