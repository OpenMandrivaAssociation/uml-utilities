Name:		uml-utilities
Version:	20070815
Release:	14
Summary:	Tools to run and configure usermodes linux
License:	GPL
Group:		Emulators
Url:		http://user-mode-linux.sourceforge.net/
Source0:	uml_utilities_%{version}.tar.bz2
Source1:	tun.rules
Source2:	umlswitch.init
Source3:	umlswitch.sysconfig
Patch0:		uml-utilities-fix-install-usage.patch
Patch1:		tools-20070815-no-strip.patch
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	fuse-devel
Requires:	tunctl

%description
This package contains tools that permit to you:
- configure on fly running usermode kernel
- setting up virtual network between usermode host.

%package -n tunctl
Summary:	Tool to create and manage persistent TUN/TAP interfaces
Group:		Networking/Other
Requires(pre): rpm-helper
Requires(postun): rpm-helper

%description -n tunctl
tunctl allows the host sysadmin to preconfigure a TUN/TAP device for
use by a particular user. That user may open and use the device, but
may not change any aspects of the host side of the interface.

%prep
%setup -n tools-%{version} -q
%patch0 -p0
%patch1 -p1

%build
%make

%install
%makeinstall_std
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/45-tun.rules

install -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/umlswitch
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/umlswitch

%pre -n tunctl
%_pre_groupadd tun

%postun -n tunctl
%_postun_groupdel tun

%files
%exclude %{_bindir}/tunctl
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/uml
%{_initrddir}/umlswitch
%config %{_sysconfdir}/sysconfig/umlswitch

%files -n tunctl
%{_bindir}/tunctl
%config(noreplace) %{_sysconfdir}/udev/rules.d/45-tun.rules



%changelog

