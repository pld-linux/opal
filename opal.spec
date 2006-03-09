Summary:	Open Phone Abstraction Library (aka OpenH323 v2)
Summary(pl):	Biblioteka Open Phone Abstraction Library (aka OpenH323 v2)
Name:		opal
Version:	2.1.3
Release:	0.1
License:	MPL
Group:		Libraries
Source0:	http://www.ekiga.org/downloads/beta2/sources/%{name}-%{version}.tar.gz
# Source0-md5:	10cbc244058b8f4928a9e337a9025fb7
#Patch0:		%{name}-opaldir.patch
URL:		http://www.openh323.org/
BuildRequires:	pwlib-devel >= 1.9.3-1
BuildRequires:	speex-devel >= 1:1.1.5
BuildRequires:	libstdc++-devel
%requires_eq	pwlib
Obsoletes:	openh323
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenH323 project aims to create a full featured, interoperable,
Open Source implementation of the ITU H.323 teleconferencing protocol
that can be used by personal developers and commercial users without
charge.

%description -l pl
Celem projektu OpenH323 jest stworzenie w pe³ni funkcjonalnej i
wyposa¿onej implementacji protoko³u telekonferencyjnego ITU H.323,
który mo¿e byæ u¿ywany przez u¿ytkowników prywatnych i komercyjnych
bez op³at.

%package devel
Summary:	Opal development files
Summary(pl):	Pliki dla developerów Opal
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	libstdc++-devel
Requires:	pwlib-devel
Obsoletes:	openh323-devel

%description devel
Header files and libraries for developing applications that use
Opal.

%description devel -l pl
Pliki nag³ówkowe i biblioteki konieczne do rozwoju aplikacji
u¿ywaj±cych Opal.

#%package static
#Summary:	Opal static libraries
#Summary(pl):	Biblioteki statyczne Opal
#Group:		Development/Libraries
#Requires:	%{name}-devel = %{version}
#Obsoletes:	openh323-static

#%description static
#OpenH323 static libraries.

#%description static -l pl
#Biblioteki statyczne OpenH323.

%prep
%setup -q
#%patch0 -p1

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
#OPALDESTDIR=%{_prefix}; export OPALDIR
#OPENH323_BUILD="yes"; export OPENH323_BUILD
#cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure 
#	--disable-iax
#touch .asnparser.version

%{__make}

#%{__make} %{?debug:debug}%{!?debug:opt} \
#		CC="%{__cc}" CPLUS=%{__cxx} \
#		PWLIB_MAKE=%{_datadir}/pwlib \
#		ASNPARSER=%{_bindir}/asnparser \
#		OPTCCFLAGS="%{rpmcflags}"

#%%{__make} -C samples/simple %{?debug:debugshared}%{!?debug:optshared} \
#		CC="%{__cc}" CPLUS=%{__cxx} \
#		OPTCCFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/openh323,%{_bindir},%{_datadir}/misc}

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

#using cp as install won't preserve links
#cp -d lib/lib* $RPM_BUILD_ROOT%{_libdir}
#install include/*.h $RPM_BUILD_ROOT%{_includedir}/openh323
#install version.h $RPM_BUILD_ROOT%{_includedir}/openh323
#install samples/simple/obj_*/simph323 $RPM_BUILD_ROOT%{_bindir}

#sed -e's@\$(OPALDIR)/include@&/opal@' < opal_inc.mak \
#	> $RPM_BUILD_ROOT%{_datadir}/opal/opal_inc1.mak

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
#%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
#%doc *.txt
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_datadir}/%{name}

#%files static
#%defattr(644,root,root,755)
#%{_libdir}/*.a
