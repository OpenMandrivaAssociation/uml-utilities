Summary:	Tools to run and configure usermodes linux
Name:		uml-utilities
Version:	20070815
Release:	25
License:	GPLv2+
Group:		Emulators
Url:		http://user-mode-linux.sourceforge.net/
Source0:	uml_utilities_%{version}.tar.bz2
Source1:	tun.rules
Source2:	umlswitch.service
Source3:	umlswitch.sysconfig
Source4:        umlswitch-wrapper.sh
Patch0:		uml-utilities-fix-install-usage.patch
Patch1:		tools-20070815-no-strip.patch
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(ncurses)
Requires:	tunctl

%description
This package contains tools that permit to you:
- configure on fly running usermode kernel
- setting up virtual network between usermode host.

%files
%exclude %{_bindir}/tunctl
%{_bindir}/uml_switch
%{_bindir}/umlswitch-wrapper.sh
%{_libdir}/uml
%attr(0644,root,root) %{_unitdir}/umlswitch.service
%config %{_sysconfdir}/sysconfig/umlswitch

%post
%systemd_post umlswitch.service

%preun
%systemd_preun umlswitch.service

%postun
%systemd_postun_with_restart umlswitch.service

#----------------------------------------------------------------------------

%package -n tunctl
Summary:	Tool to create and manage persistent TUN/TAP interfaces
Group:		Networking/Other
Requires(pre): rpm-helper
Requires(postun): rpm-helper

%description -n tunctl
tunctl allows the host sysadmin to preconfigure a TUN/TAP device for
use by a particular user. That user may open and use the device, but
may not change any aspects of the host side of the interface.

%files -n tunctl
%{_bindir}/humfsify
%{_bindir}/jailtest
%{_bindir}/uml_mconsole
%{_bindir}/uml_mkcow
%{_bindir}/uml_moo
%{_bindir}/uml_mount
%{_bindir}/uml_net
%{_bindir}/uml_watchdog
%{_bindir}/tunctl

%{_sbindir}/jail_uml

%config(noreplace) %{_sysconfdir}/udev/rules.d/45-tun.rules

%pre -n tunctl
%_pre_groupadd tun

%postun -n tunctl
%_postun_groupdel tun

#----------------------------------------------------------------------------

%prep
%setup -n tools-%{version} -q
%patch0 -p0
%patch1 -p1

%build
%make

%install
%makeinstall_std
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/45-tun.rules

install -m0644 -D %{SOURCE2} %{buildroot}%{_unitdir}/umlswitch.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/umlswitch
install -D -m 755 %{SOURCE4} %{buildroot}%{_bindir}/umlswitch-wrapper.sh

sed "s:sysconfig:%{_sysconfdir}/sysconfig:" -i %{buildroot}%{_unitdir}/umlswitch.service
sed "s:libexecdir:%{_libexecdir}:" -i %{buildroot}%{_unitdir}/umlswitch.service
