Summary:	rshproxy is an application level gateway for the remote shell protocol
Summary(pl):	rshproxy jest aplikacyjn± bramk± dla protoko³u remote shell
Name:		rshproxy
Version:	1.0.3
Release:	1
License:	GPL
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Source0:	http://www.quietsche-entchen.de/download/rshproxy-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		%{name}-crypt.patch
Prereq:		rc-inetd >= 0.8.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rsh.proxy is a proxy server for remote shell protocol.

%description -l pl
rsh.proxy jest aplikacyjn± bramk± dla protoko³u zdalnego shella (remote
shell).

%prep
%setup -q
%patch -p1

%build
%{__make} \
	CC=%{__cc} \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,/etc/sysconfig/rc-inetd}

install rsh.proxy $RPM_BUILD_ROOT%{_sbindir}
install rsh.proxy.1 $RPM_BUILD_ROOT%{_mandir}/man1

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/rshproxy

gzip -9nf README

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
    /etc/rc.d/init.d/rc-inetd reload 1>&2
else
    echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
    /etc/rc.d/init.d/rc-inetd reload
fi
    
%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/rsh.proxy
%{_mandir}/man1/*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/rshproxy
