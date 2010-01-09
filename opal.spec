# TODO:
#	fix static libname (libopal_s.a)
#	IPv6 support requires IPv6 support in ptlib
#	x264+ffmpeg detection sucks - it doesn't work with --as-needed
#       SpanDSP FAX support requires t38_indicator symbol
#	MPEG4 rate control correction requires libavcodec sources
#       CAPI support
#
# Don't touch this! strip removes all symbols from library
%define		no_install_post_strip		1
#
Summary:	Open Phone Abstraction Library (aka OpenH323 v2)
Summary(pl.UTF-8):	Biblioteka Open Phone Abstraction Library (aka OpenH323 v2)
Name:		opal
Version:	3.6.6
Release:	2
License:	MPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/opal/3.6/%{name}-%{version}.tar.bz2
# Source0-md5:	43b363c860780e7f1a0361cfee8f9f4a
#Source0:	http://www.ekiga.org/admin/downloads/latest/sources/sources/%{name}-%{version}.tar.gz
Patch0:		%{name}-libname.patch
Patch1:		%{name}-mak_files.patch
Patch2:		%{name}-ac.patch
Patch3:		%{name}-build.patch
URL:		http://www.openh323.org/
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	libgsm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtheora-devel
BuildRequires:	libx264-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	ptlib-devel >= 2.4.2-3
BuildRequires:	sed >= 4.0
BuildRequires:	speex-devel >= 1:1.1.5
BuildRequires:	unixODBC-devel
%requires_eq	ptlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_ld    -Wl,--as-needed

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
#%patch2 -p1
%patch3 -p1

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPALDIR=`pwd`; export OPALDIR
OPAL_BUILD="yes"; export OPAL_BUILD
%{__aclocal}
%{__autoconf}
%configure \
	--enable-ixj

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
%dir %{_libdir}/opal-%{version}
%dir %{_libdir}/opal-%{version}/codecs
%dir %{_libdir}/opal-%{version}/codecs/audio
%dir %{_libdir}/opal-%{version}/codecs/video
%dir %{_libdir}/opal-%{version}/lid
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/g722_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/g726_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/gsm0610_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/gsmamrcodec_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/ilbc_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/ima_adpcm_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/lpc10_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/speex_audio_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h261-vic_video_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h263-1998_video_pwplugin.so
#%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h263-ffmpeg_video_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h264_video_pwplugin_helper
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h264_video_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/mpeg4-ffmpeg_video_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/theora_video_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/lid/ixj_lid_pwplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/lid/vpb_lid_pwplugin.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/opal
%{_pkgconfigdir}/opal.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
