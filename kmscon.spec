%define _disable_ld_no_undefined 1

%define major 1

%define libeloop %mklibname eloop %{major}
%define libeloop_devel %mklibname eloop -d
%define libuterm %mklibname uterm %{major}
%define libuterm_devel %mklibname uterm -d

Summary:	KMS/DRM based System Console
Name:		kmscon
Version:	8
Release:	9
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/kmscon/
Source0:	http://www.freedesktop.org/software/kmscon/releases/%{name}-%{version}.tar.xz
Source1:	kmscon.conf
Patch0:		kmscon-8-add-aliast-to-kmsconvt-service.patch
BuildRequires:	pkgconfig(libsystemd)
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
BuildRequires:	pkgconfig(libtsm) = 3
BuildRequires:	pkgconfig(libudev)
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
Requires(post,preun):	rpm-helper

%description
Kmscon is a simple terminal emulator based on 
linux kernel mode setting (KMS).
It is an attempt to replace the in-kernel 
VT implementation with a userspace console.

%prep
%setup -q
%apply_patches

%build
%serverbuild_hardened

%configure2_5x \
	--disable-wlterm \
	--disable-static

%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}

mkdir -p %{buildroot}%{_unitdir}
install -pm0644 docs/*.service %{buildroot}%{_unitdir}/

%post
if [ -e /etc/systemd/system/autovt\@.service ]; then
	# backup the original autovt
	mv -f /etc/systemd/system/autovt\@.service /etc/systemd/system/autovt\@.kmscon
fi

# (tpg) comment out line with pam_securetty.so
if grep -q pam_securetty.so$ /etc/pam.d/login ; then
    sed -i -e '/^auth.*pam_securetty.so$/s/^/#/' /etc/pam.d/login
fi

# (tpg) yes, first this is enabled in systemd(fallback) but now time to die :)
/bin/systemctl --quiet disable getty@tty1.service

%systemd_post kmsconvt\@.service
%systemd_post kmsconvt@tty1.service

%preun
%systemd_postun kmsconvt\@.service
%systemd_post kmsconvt@tty1.service

if [ -e /etc/systemd/system/autovt\@.service ]; then
	rm -rf /etc/systemd/system/autovt\@.service
	mv -f /etc/systemd/system/autovt\@.kmscon autovt\@.service
fi
/bin/systemctl --quiet enable getty@tty1.service

%files
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%{_bindir}/%{name}
%{_libdir}/%{name}/*.so
%{_unitdir}/%{name}*.service
%{_mandir}/man1/%{name}*
