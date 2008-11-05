# TODO:
#	fix static libname (libopal_s.a)
#	check why:
#		checking PTLIB has expat... no
#		checking PTLIB has vxml... no
#		checking PTLIB has ipv6... no
#		checking PTLIB has ldap... no
#	... and check plugin configuration:
#                              GSM :  yes (internal)
#                           H.263+ :  
#                           H.264  :  no
#                          THEORA  :  no
#                    MPEG4 Part 2  :  no
#                     SpanDSP FAX  :  no
#                            CAPI  :  no
#           Quicknet xJACK support :  no
#
# Don't touch this! strip removes all symbols from library
%define		no_install_post_strip		1
#
Summary:	Open Phone Abstraction Library (aka OpenH323 v2)
Summary(pl.UTF-8):	Biblioteka Open Phone Abstraction Library (aka OpenH323 v2)
Name:		opal
Version:	3.4.2
Release:	0.2
License:	MPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/opal/3.4/%{name}-%{version}.tar.bz2
# Source0-md5:	a1d11099fa00d77a79dcfe513872e8dc
#Source0:	http://www.ekiga.org/admin/downloads/latest/sources/sources/%{name}-%{version}.tar.gz
Patch0:		%{name}-libname.patch
Patch1:		%{name}-mak_files.patch
Patch2:		%{name}-ac.patch
Patch3:		%{name}-build.patch
URL:		http://www.openh323.org/
BuildRequires:	SDL-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	ptlib-devel
BuildRequires:	sed >= 4.0
BuildRequires:	speex-devel >= 1:1.1.5
%requires_eq	pwlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OPAL project aims to create a full featured, interoperable,
Open Source implementation of the ITU H.323 teleconferencing protocol
that can be used by personal developers and commercial users without
charge.

%description -l pl.UTF-8
Celem projektu OPAL jest stworzenie w pełni funkcjonalnej i
wyposażonej implementacji protokołu telekonferencyjnego ITU H.323,
który może być używany przez użytkowników prywatnych i komercyjnych
bez opłat.

%package devel
Summary:	Opal development files
Summary(pl.UTF-8):	Pliki dla developerów Opal
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	ptlib-devel

%description devel
Header files and libraries for developing applications that use
OPAL.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteki konieczne do rozwoju aplikacji
używających OPAL.

%package static
Summary:	OPAL static libraries
Summary(pl.UTF-8):	Biblioteki statyczne OPAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
OPAL static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne OPAL.

%prep
%setup -q
#patch0 -p1
#patch1 -p1
%patch2 -p1
%patch3 -p1

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPALDIR=`pwd`; export OPALDIR
OPAL_BUILD="yes"; export OPAL_BUILD
%{__aclocal}
%{__autoconf}
%configure

%{__make} %{?debug:debug}%{!?debug:opt} \
	CC="%{__cc}" \
	CPLUS="%{__cxx}" \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}"

%{__cp} -a */libopal* .
%{__make} -C samples/simple %{?debug:debug}%{!?debug:opt} \
	CC="%{__cc}" \
	CPLUS=%{__cxx} \
	CFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG} -I`pwd`/include" \
	LDFLAGS="%{rpmldflags} -L`pwd` -lpt -lopal"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

install samples/simple/obj/simpleopal $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/opal-3.4.2
%dir %{_libdir}/opal-3.4.2/codecs
%dir %{_libdir}/opal-3.4.2/codecs/audio
%dir %{_libdir}/opal-3.4.2/codecs/video
%dir %{_libdir}/opal-3.4.2/lid
%attr(755,root,root) %{_libdir}/opal-3.4.2/codecs/audio/g726_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-3.4.2/codecs/audio/gsm0610_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-3.4.2/codecs/audio/gsmamrcodec_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-3.4.2/codecs/audio/ilbc_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-3.4.2/codecs/audio/ima_adpcm_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-3.4.2/codecs/audio/lpc10_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-3.4.2/codecs/audio/speex_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-3.4.2/codecs/video/h261-vic_video_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-3.4.2/codecs/video/h263-ffmpeg_video_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-3.4.2/lid/vpb_lid_pwplugin.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/opal
%{_pkgconfigdir}/opal.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
