Summary:	A free Socks v4/v5 client implementation
Summary(pl):	Darmowa implementacja klienta Socks v4/5
Name:		dante
Version:	1.1.14
Release:	1
License:	BSD-like
Group:		Networking/Daemons
Source0:	ftp://ftp.inet.no/pub/socks/%{name}-%{version}.tar.gz
# Source0-md5:	465c2c615c1aa64afd328feee97ba007
Source1:	sockd.init
URL:		http://www.inet.no/dante/
BuildRequires:	autoconf
BuildRequires:	libwrap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dante is a free implementation of the proxy protocols socks version 4,
socks version 5 (rfc1928) and msproxy. It can be used as a firewall
between networks. It is being developed by Inferno Nettverk A/S, a
Norwegian consulting company. Commercial support is available.

This package contains the dynamic libraries required to "socksify"
existing applications to become socks clients.

%description -l pl
Dante jest darmow� implementacj� protoko��w proxy: socks w wersji 4,
socks w wersji 5 (rfc1928) oraz msproxy. Mo�e by� u�ywany jako zapora
pomi�dzy sieciami. Implementacja jest rozwijana przez Inferno Nettverk
A/S - Norwesk� firm� konsultingow�. Komercyjne wsparcie jest dost�pne.

Ten pakiet zawiera dynamiczne biblioteki wymagane do "usocksowiania"
istniej�cych aplikacji tak by dzia�a�y one jako klienci socks.

%package server
Summary:	A free Socks v4/v5 server implementation
Summary(pl):	Darmowa implementacja serwera Socks v4/5
Group:		Networking/Daemons
Requires:	%{name} = %{version}
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig

%description server
This package contains the socks proxy daemon and its documentation.
The sockd is the server part of the Dante socks proxy package and
allows socks clients to connect through it to the network.

%description server -l pl
Ten pakiet zawiera serwer proxy socks oraz jego dokumentacj�. Serwer
sockd jest cz�ci� pakietu proxy Dante. Za po�rednictwem serwera
klienci mog� ��czy� si� z serwerami w sieci.

%package devel
Summary:	Development libraries for socks
Summary(pl):	Biblioteki developerskie dla socks
Group:		Networking/Daemons
Requires:	%{name} = %{version}

%description devel
Additional libraries required to compile programs that use socks.

%description devel -l pl
Dodatkowe biblioteki wymagane do rozwoju program�w korzystaj�cych z
socks.

%package static
Summary:	Static libraries for socks
Summary(pl):	Statyczne biblioteki socks
Group:		Networking/Daemons
Requires:	%{name}-devel = %{version}

%description static
Static libraries for socks.

%description static -l pl
Statyczne biblioteki socks.

%prep
%setup -q

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install example/sock{s,d}.conf ${RPM_BUILD_ROOT}%{_sysconfdir}

install %{SOURCE1} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/sockd

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post server
/sbin/chkconfig --add sockd
if [ -f /var/lock/subsys/sockd ]; then
	/etc/rc.d/init.d/sockd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/sockd start\" to start dante sockd daemon."
fi

%postun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/sockd ]; then
		/etc/rc.d/init.d/sockd stop 1>&2
	fi
	/sbin/chkconfig --del sockd
fi

%files
%defattr(644,root,root,755)
%doc BUGS CREDITS LICENSE NEWS README SUPPORT TODO
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/socks.conf
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_bindir}/socksify
%{_mandir}/man5/socks.conf.5*

%files server
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sockd.conf
%attr(754,root,root) /etc/rc.d/init.d/sockd
%attr(755,root,root) %{_sbindir}/sockd
%{_mandir}/man8/sockd.8*
%{_mandir}/man5/sockd.conf.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
