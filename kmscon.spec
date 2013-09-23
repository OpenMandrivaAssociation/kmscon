%define _disable_ld_no_undefined 1

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

%description
Kmscon is a simple terminal emulator based on 
linux kernel mode setting (KMS).
It is an attempt to replace the in-kernel 
VT implementation with a userspace console.

%prep
%setup -q

%build
%serverbuild_hardened

%configure2_5x \
		--disable-wlterm

%make

%install
%makeinstall_std

%files
