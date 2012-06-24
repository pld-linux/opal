#
# Don't touch this! strip removes all symbols from library
%define		no_install_post_strip		1
#
Summary:	Open Phone Abstraction Library (aka OpenH323 v2)
Summary(pl):	Biblioteka Open Phone Abstraction Library (aka OpenH323 v2)
Name:		opal
Version:	2.2.1
Release:	2
License:	MPL
Group:		Libraries
Source0:	http://www.ekiga.org/admin/downloads/latest/sources/sources/%{name}-%{version}.tar.gz
# Source0-md5:	bc6079100e831cf117597bb99b266a0c
Patch0:		%{name}-libname.patch
Patch1:		%{name}-mak_files.patch
URL:		http://www.openh323.org/
BuildRequires:	libstdc++-devel
BuildRequires:	pwlib-devel >= 1.10.0
BuildRequires:	sed >= 4.0
BuildRequires:	speex-devel >= 1:1.1.5
%requires_eq	pwlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OPAL project aims to create a full featured, interoperable,
Open Source implementation of the ITU H.323 teleconferencing protocol
that can be used by personal developers and commercial users without
charge.

%description -l pl
Celem projektu OPAL jest stworzenie w pe�ni funkcjonalnej i
wyposa�onej implementacji protoko�u telekonferencyjnego ITU H.323,
kt�ry mo�e by� u�ywany przez u�ytkownik�w prywatnych i komercyjnych
bez op�at.

%package devel
Summary:	Opal development files
Summary(pl):	Pliki dla developer�w Opal
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	pwlib-devel

%description devel
Header files and libraries for developing applications that use
OPAL.

%description devel -l pl
Pliki nag��wkowe i biblioteki konieczne do rozwoju aplikacji
u�ywaj�cych OPAL.

%package static
Summary:	OPAL static libraries
Summary(pl):	Biblioteki statyczne OPAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
OPAL static libraries.

%description static -l pl
Biblioteki statyczne OPAL.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPALDIR=`pwd`; export OPALDIR
OPAL_BUILD="yes"; export OPAL_BUILD
%configure 

%{__make} %{?debug:debug}%{!?debug:opt} \
	CC="%{__cc}" \
	CPLUS="%{__cxx}" \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}"

%{__make} -C samples/simple %{?debug:debug}%{!?debug:opt} \
	CC="%{__cc}" \
	CPLUS=%{__cxx} \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/opal,%{_bindir},%{_datadir}/%{name}}

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

# using cp as install won't preserve links
cp -d lib/lib*.a $RPM_BUILD_ROOT%{_libdir}
install version.h $RPM_BUILD_ROOT%{_includedir}/opal
install samples/simple/obj_*/simpleopal $RPM_BUILD_ROOT%{_bindir}
sed -i -e 's@\$(OPALDIR)/include@&/opal@' \
       -e 's@\$(OPALDIR)/lib@\$(OPALDIR)/%{_lib}@' $RPM_BUILD_ROOT%{_datadir}/opal/opal_inc.mak

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_datadir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
