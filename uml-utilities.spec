%define name uml-utilities 
%define version 20070815
%define release %mkrel 1

%define	Summary	Tools to run and configure usermodes linux

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
Source0:	uml_utilities_%{version}.tar.bz2
Source1:	tun.rules
Patch0:     uml-utilities-fix-install-usage.patch
License:	GPL
Group:		Emulators
BuildRoot:	%{_tmppath}/%{name}-buildroot
Url:		http://user-mode-linux.sourceforge.net/
BuildRequires:	libreadline-devel
BuildRequires:	libncurses-devel
BuildRequires:  fuse-devel
Requires:	tunctl

%description
This package contains tools that permit to you:
- configure on fly running usermode kernel
- setting up virtual network between usermode host.

%package -n tunctl
Summary: Tool to create and manage persistent TUN/TAP interfaces
Group: Networking/Other
Conflicts: %{name} <= 20060323-2mdv2007.1
Requires(pre): rpm-helper
Requires(postun): rpm-helper

%description -n tunctl
tunctl allows the host sysadmin to preconfigure a TUN/TAP device for
use by a particular user. That user may open and use the device, but
may not change any aspects of the host side of the interface.

%prep
%setup -n tools-%{version} -q
%patch0 -p0

%build
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/90-tun.rules

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n tunctl
%_pre_groupadd tun

%postun -n tunctl
%_postun_groupdel tun

%files
%defattr(-,root,root)
%exclude %{_bindir}/tunctl
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/uml

%files -n tunctl
%defattr(-,root,root)
%{_bindir}/tunctl
%config(noreplace) %{_sysconfdir}/udev/rules.d/90-tun.rules
