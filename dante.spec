Summary:	A free Socks v4/v5 client implementation
Name:		dante
Version:	1.1.9
Release:	1
License:	BSD-type
Group:		Networking/Daemons
URL:		http://www.inet.no/dante/
Source0:	ftp://ftp.inet.no/pub/socks/%{name}-%{version}.tar.gz
Source1:	sockd.init
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define prefix %{_prefix}

%description
Dante is a free implementation of the proxy protocols socks version 4,
socks version 5 (rfc1928) and msproxy. It can be used as a firewall
between networks. It is being developed by Inferno Nettverk A/S, a
Norwegian consulting company. Commercial support is available.

This package contains the dynamic libraries required to "socksify"
existing applications to become socks clients.

%package server
Summary:	A free Socks v4/v5 server implementation
Group:		Networking/Daemons
Requires:	dante = %{version}

%description server
This package contains the socks proxy daemon and its documentation.
The sockd is the server part of the Dante socks proxy package and
allows socks clients to connect through it to the network.

%package devel
Summary:	development libraries for socks
Group:		Networking/Daemons
Requires:	dante = %{version}

%description devel
Additional libraries required to compile programs that use socks.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q

%build

CFLAGS="${RPM_OPT_FLAGS}" 
%configure --prefix=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=${RPM_BUILD_ROOT}

#set library as executable - prevent ldd from complaining
chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so.*.*

install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/rc.d/init.d ${RPM_BUILD_ROOT}%{_bindir}

install example/socks.conf ${RPM_BUILD_ROOT}%{_sysconfdir}
install example/sockd.conf ${RPM_BUILD_ROOT}%{_sysconfdir}

install -m 755 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/sockd

ln -sf %{_libdir}/libdsocks.so $RPM_BUILD_ROOT/%{_libdir}/libdsocks.so.0

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post server
/sbin/chkconfig --add sockd

%postun server
if [ $1 = 0 ]; then
   /sbin/chkconfig --del sockd
fi

%files
%defattr(644,root,root,755)
#files beginning with two capital letters are docs: BUGS, README.foo etc.
%doc [A-Z][A-Z]*
%{_libdir}/libsocks.so.0.1.0
%{_libdir}/libsocks.so.0
%{_libdir}/libdsocks.so.0.1.0
%{_libdir}/libdsocks.so.0
%attr(755,root,root) %{_bindir}/socksify
%{_mandir}/man5/socks.conf.5*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/socks.conf

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/sockd
%{_mandir}/man8/sockd.8*
%{_mandir}/man5/sockd.conf.5*


%config(noreplace) %verify(not size mtime md5)  %{_sysconfdir}/sockd.conf
%config /etc/rc.d/init.d/sockd

%files devel
%defattr(644,root,root,755)
%{_libdir}/libsocks.la
%{_libdir}/libsocks.a
%{_libdir}/libdsocks.la
%{_libdir}/libsocks.so
%{_libdir}/libdsocks.so
