Summary:	KMS/DRM based System Console
Name:		kmscon
Version:	7
Release:	1
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/kmscon/
Source0:	http://www.freedesktop.org/software/kmscon/releases/%{name}-%{version}.tar.bz2

%description
Kmscon is a simple terminal emulator based on linux kernel mode setting (KMS).
It is an attempt to replace the in-kernel VT implementation with a userspace console.

%prep
%setup -q

%build
%serverbuild_hardened
%configure2_5x

%make

%install
%makeinstall_std

%files
